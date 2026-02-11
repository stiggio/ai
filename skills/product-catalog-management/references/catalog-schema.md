# Product Catalog Schema Reference

## Table of Contents

1. [Products](#products)
2. [Plans](#plans)
3. [Features](#features)
4. [Add-ons](#addons)
5. [Prices](#prices)
6. [Package Entitlements](#package-entitlements)
7. [Feature Groups](#feature-groups)
8. [Coupons](#coupons)
9. [Widget Configuration](#widget-configuration)

## Products

Products are the top-level container for plans and serve as the billing entity.

```json
{
  "products": {
    "product-revvenu": {
      "refId": "product-revvenu",
      "displayName": "Revvenu",
      "description": null,
      "additionalMetaData": {
        "recommendedPlan": "plan-revvenu-essentials"
      },
      "isDefaultProduct": false,
      "multipleSubscriptions": false,
      "status": "PUBLISHED",
      "productSettings": {
        "subscriptionStartSetup": "PLAN_SELECTION",
        "subscriptionEndSetup": "CANCEL_SUBSCRIPTION",
        "subscriptionCancellationTime": "END_OF_BILLING_PERIOD",
        "prorateAtEndOfBillingPeriod": null
      },
      "rules": [],
      "rootClonedProductRefId": null
    }
  }
}
```

### Product Fields

| Field | Type | Description |
|-------|------|-------------|
| `refId` | string | Unique identifier |
| `displayName` | string | Human-readable name |
| `description` | string | Optional description |
| `additionalMetaData` | object | Custom metadata |
| `isDefaultProduct` | boolean | Whether this is the default product |
| `multipleSubscriptions` | boolean | Allow multiple subscriptions per customer |
| `status` | enum | `PUBLISHED` or `DRAFT` |
| `productSettings` | object | Subscription behavior settings |

### Product Settings

| Field | Values | Description |
|-------|--------|-------------|
| `subscriptionStartSetup` | `PLAN_SELECTION`, `UPON_CHECKOUT` | When subscription starts |
| `subscriptionEndSetup` | `CANCEL_SUBSCRIPTION`, `DOWNGRADE_TO_FREE` | What happens at subscription end |
| `subscriptionCancellationTime` | `IMMEDIATE`, `END_OF_BILLING_PERIOD` | When cancellation takes effect |

## Plans

Plans define pricing tiers and the features included.

```json
{
  "plans": {
    "plan-revvenu-basic": {
      "refId": "plan-revvenu-basic",
      "displayName": "Basic",
      "description": null,
      "pricingType": "FREE",
      "productRefId": "product-revvenu",
      "parentPlanRefId": null,
      "additionalMetaData": null,
      "compatibleAddonRefIds": [],
      "compatiblePackageGroups": {},
      "hiddenFromWidgets": [],
      "minimumSpend": null,
      "overageBillingPeriod": null,
      "overagePrices": {},
      "packageEntitlements": { /* ... */ },
      "prices": {}
    },
    "plan-revvenu-essentials": {
      "refId": "plan-revvenu-essentials",
      "displayName": "Essentials",
      "pricingType": "PAID",
      "parentPlanRefId": "plan-revvenu-basic",
      "compatibleAddonRefIds": ["addon-10-campaigns"],
      "prices": { /* ... */ },
      "packageEntitlements": { /* ... */ }
    }
  }
}
```

### Plan Fields

| Field | Type | Description |
|-------|------|-------------|
| `refId` | string | Unique identifier |
| `displayName` | string | Human-readable name |
| `pricingType` | enum | `FREE`, `PAID`, or `CUSTOM` |
| `productRefId` | string | Parent product reference |
| `parentPlanRefId` | string | Parent plan for inheritance |
| `compatibleAddonRefIds` | array | Add-ons purchasable with this plan |
| `packageEntitlements` | object | Features and limits included |
| `prices` | object | Price configurations |
| `hiddenFromWidgets` | array | Widgets where plan is hidden |
| `minimumSpend` | number | Minimum spend requirement |

## Features

Features define capabilities that can be entitled to plans.

```json
{
  "features": {
    "feature-01-templates": {
      "refId": "feature-01-templates",
      "displayName": "Templates",
      "description": null,
      "featureType": "NUMBER",
      "featureUnits": "template",
      "featureUnitsPlural": "templates",
      "meterType": "FLUCTUATING",
      "featureStatus": "NEW",
      "additionalMetaData": null,
      "configuration": null,
      "unitTransformation": null
    },
    "feature-03-custom-domain": {
      "refId": "feature-03-custom-domain",
      "displayName": "Custom domain",
      "featureType": "BOOLEAN",
      "meterType": "None"
    },
    "feature-08-cities": {
      "refId": "feature-08-cities",
      "displayName": "Cities",
      "featureType": "ENUM",
      "featureUnits": "city",
      "featureUnitsPlural": "cities",
      "configuration": [
        { "displayName": "New York", "value": "NY" },
        { "displayName": "Los Angeles", "value": "LA" },
        { "displayName": "Tel-Aviv", "value": "TLV" }
      ]
    },
    "feature-07-active-users": {
      "refId": "feature-07-active-users",
      "displayName": "Active users",
      "featureType": "NUMBER",
      "meterType": "INCREMENTAL",
      "meter": {
        "aggregation": {
          "field": "user_id",
          "function": "UNIQUE"
        },
        "filters": [
          {
            "conditions": [
              { "field": "eventName", "operation": "EQUALS", "value": "user_login" }
            ]
          }
        ]
      }
    }
  }
}
```

### Feature Types

| Type | Description | Use Case |
|------|-------------|----------|
| `BOOLEAN` | On/off feature | Feature flags (e.g., "Custom domain enabled") |
| `NUMBER` | Numeric limit | Usage limits (e.g., "5 templates") |
| `ENUM` | Multiple choice | Feature variants (e.g., "Available cities") |

### Meter Types

| Type | Description |
|------|-------------|
| `None` | Not metered |
| `INCREMENTAL` | Usage accumulates over time |
| `FLUCTUATING` | Current value can go up or down |

### Meter Configuration

For metered features, specify aggregation and filters:

```json
{
  "meter": {
    "aggregation": {
      "field": "user_id",
      "function": "UNIQUE"
    },
    "filters": [
      {
        "conditions": [
          { "field": "eventName", "operation": "EQUALS", "value": "user_login" }
        ]
      }
    ]
  }
}
```

Aggregation functions: `SUM`, `COUNT`, `UNIQUE`, `MAX`

## Addons

Add-ons are purchasable extras that extend plan capabilities.

```json
{
  "addons": {
    "addon-10-campaigns": {
      "refId": "addon-10-campaigns",
      "displayName": "10 campaigns",
      "description": "Additional quota of 10 campaigns",
      "pricingType": "PAID",
      "productRefId": "product-revvenu",
      "additionalMetaData": null,
      "hiddenFromWidgets": [],
      "packageEntitlements": {
        "feature:feature-02-campaigns": {
          "featureRefId": "feature-02-campaigns",
          "isGranted": true,
          "usageLimit": 10,
          "behavior": "Increment",
          "resetPeriod": "MONTH"
        }
      },
      "prices": {
        "FLAT_FEE-RECURRING--MONTHLY-default-RECURRING}": {
          "billingModel": "FLAT_FEE",
          "billingPeriod": "MONTHLY",
          "price": { "amount": 5, "currency": "usd" }
        },
        "FLAT_FEE-RECURRING--ANNUALLY-default-RECURRING}": {
          "billingModel": "FLAT_FEE",
          "billingPeriod": "ANNUALLY",
          "price": { "amount": 54, "currency": "usd" }
        }
      }
    }
  }
}
```

Add-ons have the same structure as plans. Link them to plans via `compatibleAddonRefIds`.

## Prices

Prices define how plans and add-ons are billed.

### Flat Fee Pricing

Fixed recurring or one-time charge:

```json
{
  "FLAT_FEE-RECURRING--MONTHLY-default-RECURRING}": {
    "billingModel": "FLAT_FEE",
    "billingPeriod": "MONTHLY",
    "billingCadence": "RECURRING",
    "price": { "amount": 20, "currency": "usd" },
    "billingCountryCode": null,
    "blockSize": null,
    "tiers": null,
    "tiersMode": null
  }
}
```

### Per Unit Pricing

Charge per unit of a feature:

```json
{
  "PER_UNIT-RECURRING-feature-01-templates-MONTHLY-default-RECURRING}": {
    "billingModel": "PER_UNIT",
    "billingPeriod": "MONTHLY",
    "billingCadence": "RECURRING",
    "featureRefId": "feature-01-templates",
    "price": { "amount": 6, "currency": "usd" },
    "minUnitQuantity": 5,
    "maxUnitQuantity": null
  }
}
```

### Usage-Based Pricing

Charge based on metered usage:

```json
{
  "USAGE_BASED-RECURRING-feature-02-campaigns-MONTHLY-default-RECURRING}": {
    "billingModel": "USAGE_BASED",
    "billingPeriod": "MONTHLY",
    "billingCadence": "RECURRING",
    "featureRefId": "feature-02-campaigns",
    "price": { "amount": 6, "currency": "usd" }
  }
}
```

### Tiered Pricing

For volume-based pricing with tiers:

```json
{
  "tiers": [
    { "upTo": 100, "unitPrice": { "amount": 10, "currency": "usd" } },
    { "upTo": 500, "unitPrice": { "amount": 8, "currency": "usd" } },
    { "upTo": null, "unitPrice": { "amount": 5, "currency": "usd" } }
  ],
  "tiersMode": "VOLUME"
}
```

Tier modes: `VOLUME` (all units at tier rate) or `GRADUATED` (each tier charged separately)

### Price Fields

| Field | Description |
|-------|-------------|
| `billingModel` | `FLAT_FEE`, `PER_UNIT`, `USAGE_BASED` |
| `billingPeriod` | `MONTHLY`, `ANNUALLY` |
| `billingCadence` | `RECURRING`, `ONE_TIME` |
| `price` | `{ amount: number, currency: string }` |
| `featureRefId` | Feature for per-unit/usage pricing |
| `minUnitQuantity` | Minimum units to charge |
| `maxUnitQuantity` | Maximum units allowed |

## Package Entitlements

Define what features are included in a plan/addon and how:

```json
{
  "packageEntitlements": {
    "feature:feature-01-templates": {
      "type": "FEATURE",
      "featureRefId": "feature-01-templates",
      "isGranted": true,
      "usageLimit": 5,
      "hasUnlimitedUsage": null,
      "behavior": "Increment",
      "resetPeriod": null,
      "resetPeriodConfig": null,
      "order": 0,
      "displayNameOverride": null,
      "description": null,
      "isCustom": null,
      "featureGroupRefIds": ["feature-group-basic"],
      "hiddenFromWidgets": [],
      "enumValues": null
    },
    "feature:feature-02-campaigns": {
      "featureRefId": "feature-02-campaigns",
      "isGranted": true,
      "usageLimit": 12,
      "resetPeriod": "MONTH",
      "resetPeriodConfig": { "accordingTo": "SubscriptionStart" }
    },
    "feature:feature-03-custom-domain": {
      "featureRefId": "feature-03-custom-domain",
      "isGranted": true,
      "usageLimit": null
    },
    "feature:feature-08-cities": {
      "featureRefId": "feature-08-cities",
      "isGranted": true,
      "enumValues": ["NY", "LA", "TLV"]
    }
  }
}
```

### Entitlement Fields

| Field | Type | Description |
|-------|------|-------------|
| `featureRefId` | string | Feature reference |
| `isGranted` | boolean | Whether feature is granted |
| `usageLimit` | number | Usage limit (for NUMBER features) |
| `hasUnlimitedUsage` | boolean | Unlimited usage flag |
| `behavior` | string | `Increment` for additive entitlements |
| `resetPeriod` | enum | `MONTH`, `YEAR`, etc. |
| `resetPeriodConfig` | object | Reset timing configuration |
| `isCustom` | boolean | Whether value is customizable |
| `enumValues` | array | Allowed values (for ENUM features) |
| `displayNameOverride` | string | Custom display text |
| `order` | number | Display order |

### Reset Period Config

```json
{
  "resetPeriodConfig": {
    "accordingTo": "SubscriptionStart"
  }
}
```

Options: `SubscriptionStart`, `CalendarMonth`, `CalendarYear`

## Feature Groups

Group related features for display:

```json
{
  "featureGroups": {
    "feature-group-basic": {
      "refId": "feature-group-basic",
      "displayName": "Basic Features",
      "description": "",
      "featureRefIds": ["feature-02-campaigns", "feature-01-templates"]
    }
  }
}
```

## Coupons

Discount codes:

```json
{
  "coupons": {
    "coupon-summer-sale": {
      "refId": "coupon-summer-sale",
      "displayName": "Summer Sale",
      "discountType": "PERCENTAGE",
      "discountValue": 20,
      "durationInMonths": 3,
      "maxRedemptions": 100
    }
  }
}
```

## Widget Configuration

Configure Stigg's embeddable widgets:

```json
{
  "widgetConfiguration": {
    "PAYWALL": {
      "widgetType": "PAYWALL",
      "configuration": {
        "layout": {
          "planWidth": 320,
          "planPadding": 32,
          "planMargin": 20
        },
        "palette": {
          "primary": "#2e7d32",
          "textColor": "#000000",
          "currentPlanBackground": "#f5fbf7"
        },
        "typography": {
          "h1": { "fontSize": 28 },
          "h2": { "fontSize": 20 },
          "h3": { "fontSize": 14 }
        }
      }
    },
    "CHECKOUT": {
      "widgetType": "CHECKOUT",
      "configuration": {
        "palette": {
          "primary": "#2e7d32",
          "textColor": "#000000"
        }
      }
    },
    "CUSTOMER_PORTAL": {
      "widgetType": "CUSTOMER_PORTAL",
      "configuration": {
        "palette": {
          "primary": "#2e7d32",
          "textColor": "#000000",
          "currentPlanBackground": "#f5fbf7"
        }
      }
    }
  }
}
```

Widget types: `PAYWALL`, `CHECKOUT`, `CUSTOMER_PORTAL`
