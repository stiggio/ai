---
name: stigg-docs
description: Monetization infrastructure for SaaS - pricing, billing,
  entitlements, usage metering, and customer management
license: proprietary
compatibility: Node.js, Python, Ruby, Go, Java, .NET, JavaScript, React, Vue.js, Next.js
metadata:
  category: monetization
  website: https://stigg.io
  docs: https://docs.stigg.io
  mintlify-proj: stigg
---

# Stigg

Stigg is a monetization infrastructure platform that helps SaaS companies implement and manage pricing, billing, entitlements, and usage-based metering.

## Core Capabilities

### Pricing Model Management

- **Features**: Define boolean, configuration, and metered features that control access
- **Products**: Group plans under products for multi-product offerings
- **Plans**: Create free, paid, and custom plans with flexible pricing models
- **Add-ons**: Offer additional capabilities customers can purchase
- **Coupons**: Apply percentage or fixed discounts to subscriptions
- **Credits**: Implement prepaid credit systems with auto-recharge

### Customer & Subscription Management

- **Customers**: Provision and manage customer accounts with metadata
- **Subscriptions**: Create, update, upgrade, downgrade, and cancel subscriptions
- **Entitlements**: Control feature access based on subscription status
- **Promotional entitlements**: Grant temporary access outside of subscriptions

### Usage & Metering

- **Usage reporting**: Report calculated usage or raw events
- **Metering**: Track consumption for usage-based billing
- **Overage handling**: Configure behavior when limits are exceeded

### Billing Integration

- **Stripe**: Native integration for payments and invoicing
- **Zuora**: Enterprise billing integration
- **Multiple providers**: Support for multiple billing providers simultaneously

### Embeddable Widgets

- **Pricing table**: Display plans and pricing to customers
- **Customer portal**: Self-service subscription management
- **Checkout**: Embedded payment flows
- **Credit widgets**: Display balances, grants, and usage

### Workflow Automation

- **Triggers**: React to subscription events, usage thresholds, and more
- **Conditions**: Apply conditional logic to workflows
- **Actions**: Send webhooks, update subscriptions, grant access

## API & SDKs

### GraphQL API

Primary API for all operations. Endpoint: `https://api.stigg.io/graphql`

### Backend SDKs

- Node.js: `@stigg/node-server-sdk`
- Python: `stigg-api-client`
- Ruby: `stigg-api-client`
- Go: `github.com/stiggio/api-client-go`
- Java: Available via Maven
- .NET: Available via NuGet

### Frontend SDKs

- JavaScript: `@stigg/js-client-sdk`
- React: `@stigg/react-sdk`
- Vue.js: `@stigg/vue-sdk`
- Next.js: `@stigg/nextjs-sdk`

## Common Operations

### Provision a Customer

```graphql theme={null}
mutation {
  provisionCustomer(
    input: {
      customerId: "customer-123"
      name: "Acme Inc"
      email: "admin@acme.com"
    }
  ) {
    customer {
      id
      name
    }
  }
}
```

### Create a Subscription

```graphql theme={null}
mutation {
  provisionSubscription(
    input: {
      customerId: "customer-123"
      planId: "plan-pro"
      billingPeriod: MONTHLY
    }
  ) {
    subscription {
      id
      status
    }
  }
}
```

### Check Entitlement

```graphql theme={null}
query {
  entitlement(
    input: { customerId: "customer-123", featureId: "feature-api-calls" }
  ) {
    isGranted
    usageLimit
    currentUsage
  }
}
```

### Report Usage

```graphql theme={null}
mutation {
  reportUsage(
    input: {
      customerId: "customer-123"
      featureId: "feature-api-calls"
      value: 100
    }
  ) {
    id
  }
}
```

## Integrations

- **CRM**: Salesforce, HubSpot
- **Data Warehouses**: Snowflake, BigQuery
- **Marketplaces**: AWS Marketplace
- **Authentication**: Auth0
- **Webhooks**: Real-time event notifications to any endpoint

## Resources

- Documentation: [https://docs.stigg.io](https://docs.stigg.io)
- API Reference: [https://docs.stigg.io/api-and-sdks/api-reference/overview](https://docs.stigg.io/api-and-sdks/api-reference/overview)
- Status: [https://status.stigg.io](https://status.stigg.io)
- Product Updates: [https://changelog.stigg.io](https://changelog.stigg.io)
