---
name: stigg-product-catalog
description: Manage Stigg product catalog via GraphQL API. Use when working with Stigg environments, plans, features, add-ons, coupons, or pricing. Covers viewing environments, dumping/exporting product catalogs, comparing environments, merging changes between environments, and creating environments from JSON templates. Triggers include "stigg", "product catalog", "environments", "merge environment", "pricing", "plans", "features", "entitlements".
allowed-tools: Read, Grep, Bash, Glob
---

# Stigg Product Catalog Management

This skill enables management of Stigg's product catalog through the GraphQL API.

## Prerequisites

- Stigg API key with appropriate permissions
- Access to Stigg's GraphQL endpoint: `https://api.stigg.io/graphql`

## Authentication

All requests require the `X-API-KEY` header:

```bash
curl -X POST https://api.stigg.io/graphql \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $STIGG_API_KEY" \
  -d '{"query": "..."}'
```

## Critical Requirements

### 1. Always Preview Changes Before Applying

**MANDATORY**: Before executing any `mergeEnvironment` mutation that modifies an environment, you MUST:

1. Run `dumpEnvironmentForMergeComparison` to get the pre-merge and post-merge states
2. Present a clear summary of the changes to the user (what will be added, modified, or removed)
3. Wait for explicit user confirmation before proceeding
4. Only execute the merge if the user approves the changes

Never apply changes without showing the preview first and receiving user approval.

### 2. Migration Type Selection

The `migrationType` field determines how existing customer subscriptions are affected:

- `NEW_CUSTOMERS` (default) - Changes only apply to new subscriptions; existing customers keep their current plan versions
- `ALL_CUSTOMERS` - Migrate all existing customers to the new plan versions

**MANDATORY**: If the user has not explicitly specified the migration type:
1. Default to `NEW_CUSTOMERS` in your preview
2. Ask the user which migration type they want before executing the merge
3. Explain the difference between the options
4. Do NOT assume `ALL_CUSTOMERS` without explicit user confirmation

## Core Operations

### 1. List Environments

Fetch all environments in the account:

```graphql
query {
  environments(paging: { first: 25 }) {
    edges {
      node {
        id
        slug
        displayName
        type
        description
        isSandbox
        provisionStatus
        createdAt
      }
    }
  }
}
```

Environment types: `DEVELOPMENT`, `PRODUCTION`, `SANDBOX`

### 2. Dump Product Catalog

Export the complete product catalog of an environment as JSON:

```graphql
query DumpCatalog($input: DumpEnvironmentProductCatalogInput!) {
  dumpEnvironmentProductCatalog(input: $input) {
    dump
  }
}
```

Variables:

```json
{
  "input": {
    "environmentSlug": "development"
  }
}
```

The dump contains: `products`, `plans`, `addons`, `features`, `featureGroups`, `coupons`, `customCurrencies`, `packageGroups`, `widgetConfiguration`, `workflows`

### 3. Preview Merge Changes (Diff)

Compare source and destination environments before merging:

```graphql
query PreviewMerge($input: DumpEnvironmentForForMergeComparisonInput!) {
  dumpEnvironmentForMergeComparison(input: $input) {
    preMergeDump
    postMergeDump
  }
}
```

Variables:

```json
{
  "input": {
    "sourceEnvironmentSlug": "development",
    "destinationEnvironmentSlug": "production",
    "mergeConfiguration": {
      "includeCoupons": true
    }
  }
}
```

Use this to show users what will change before executing the merge.

### 4. Merge Environments

The `mergeEnvironment` mutation supports three use cases:

#### A. Merge from Source Environment to Destination Environment

```graphql
mutation MergeEnvToEnv($input: MergeEnvironmentInput!) {
  mergeEnvironment(input: $input) {
    environmentSlug
    taskIds
  }
}
```

Variables:

```json
{
  "input": {
    "sourceEnvironmentSlug": "development",
    "destinationEnvironmentSlug": "production",
    "mergeConfiguration": {
      "includeCoupons": true
    },
    "migrationType": "NEW_CUSTOMERS"
  }
}
```

#### B. Create New Environment from Source Environment

Omit `destinationEnvironmentSlug` to create a new environment:

```json
{
  "input": {
    "sourceEnvironmentSlug": "development",
    "destinationEnvironmentName": "staging",
    "destinationEnvironmentType": "DEVELOPMENT"
  }
}
```

#### C. Create/Update Environment from JSON Template

Use `sourceTemplate` instead of `sourceEnvironmentSlug` to apply a JSON catalog:

```json
{
  "input": {
    "sourceTemplate": {
      /* product catalog JSON */
    },
    "destinationEnvironmentSlug": "development"
  }
}
```

Or create a new environment from JSON:

```json
{
  "input": {
    "sourceTemplate": {
      /* product catalog JSON */
    },
    "destinationEnvironmentName": "new-environment",
    "destinationEnvironmentType": "DEVELOPMENT"
  }
}
```

### Migration Types

When merging, `migrationType` controls how existing customers are handled:

- `NEW_CUSTOMERS` (default) - Changes only apply to new subscriptions; existing customers keep their current plan versions
- `ALL_CUSTOMERS` - Migrate all existing customers to the new plan versions

**Important**: Always ask the user which migration type they want if not explicitly specified. Do not assume.

## Product Catalog JSON Structure

The catalog JSON has these top-level keys:

```json
{
  "products": {},
  "plans": {},
  "addons": {},
  "features": {},
  "featureGroups": {},
  "coupons": {},
  "customCurrencies": {},
  "packageGroups": {},
  "widgetConfiguration": {},
  "workflows": {}
}
```

### Key Concepts

**Products** - Container for plans, the billing entity

- `refId`: Unique identifier (e.g., "product-revvenu")
- `displayName`: Human-readable name
- `status`: `PUBLISHED` or `DRAFT`
- `productSettings`: Subscription behavior settings

**Plans** - Pricing tiers within a product

- `refId`: Unique identifier (e.g., "plan-basic")
- `pricingType`: `FREE`, `PAID`, or `CUSTOM`
- `prices`: Pricing configuration by billing model
- `packageEntitlements`: Features included in the plan
- `parentPlanRefId`: For plan inheritance
- `compatibleAddonRefIds`: Add-ons that can be purchased with this plan

**Features** - Capabilities that can be entitled

- `featureType`: `BOOLEAN`, `NUMBER`, or `ENUM`
- `meterType`: `INCREMENTAL`, `FLUCTUATING`, or `None`
- `featureUnits`/`featureUnitsPlural`: Display units

**Add-ons** - Purchasable extras for plans

- Same structure as plans
- Linked via `compatibleAddonRefIds` on plans

**Prices** - Billing configuration

- `billingModel`: `FLAT_FEE`, `PER_UNIT`, or `USAGE_BASED`
- `billingPeriod`: `MONTHLY` or `ANNUALLY`
- `billingCadence`: `RECURRING` or `ONE_TIME`

See `references/catalog-schema.md` for complete schema details.

## Common Workflows

### Export Catalog to File

1. Query `dumpEnvironmentProductCatalog`
2. Save the `dump` JSON to a file
3. The file can be version-controlled or used as a template

### Promote Changes to Production

1. Query `dumpEnvironmentForMergeComparison` to preview changes
2. Present a clear summary of what will be added, modified, or removed
3. Ask the user which `migrationType` they want (`NEW_CUSTOMERS` or `ALL_CUSTOMERS`) if not already specified
4. Wait for explicit user approval before proceeding
5. Only if approved, run `mergeEnvironment` mutation with the confirmed settings

### Create Environment from Template

1. Load the JSON template file
2. Run `mergeEnvironment` with `sourceTemplate` and target environment

### Compare Two Environments

1. Dump both environments using `dumpEnvironmentProductCatalog`
2. Compare the JSON structures
3. Highlight differences in products, plans, features, and prices

## Helper Script

The `scripts/stigg_api.py` script provides a CLI for common operations:

```bash
# Set API key
export STIGG_API_KEY="your-api-key"

# List environments
python scripts/stigg_api.py list-environments

# Dump catalog to file
python scripts/stigg_api.py dump-catalog --env development --output catalog.json

# Preview merge
python scripts/stigg_api.py preview-merge --source development --dest production

# Merge environments
python scripts/stigg_api.py merge --source development --dest production

# Create environment from template
python scripts/stigg_api.py merge --template catalog.json --new-env staging --type DEVELOPMENT

# Apply template to existing environment
python scripts/stigg_api.py merge --template catalog.json --dest development
```

## Best Practices

1. **Always preview changes** with `dumpEnvironmentForMergeComparison` before merging and get user confirmation
2. **Always ask about migration type** if the user hasn't specified - default to `NEW_CUSTOMERS` but confirm with the user
3. Keep product catalog JSON files in version control
4. Test changes in development/staging before production
