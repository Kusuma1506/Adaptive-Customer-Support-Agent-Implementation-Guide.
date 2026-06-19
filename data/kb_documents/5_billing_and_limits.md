# Billing, Usage Limits, and Pricing

## Subscription Plans

### Starter Plan
- **Monthly Cost**: $29
- **Data Limit**: 100 GB/month
- **API Calls**: 100,000/month
- **Support**: Email (48-hour response)
- **Syncs**: Up to 5 concurrent syncs
- **Features**: Basic sync, manual scheduling

### Professional Plan
- **Monthly Cost**: $99
- **Data Limit**: 1 TB/month
- **API Calls**: 1,000,000/month
- **Support**: Email (24-hour response) + Chat
- **Syncs**: Up to 25 concurrent syncs
- **Features**: All Starter + Advanced scheduling, versioning

### Enterprise Plan
- **Monthly Cost**: Custom (contact sales)
- **Data Limit**: Unlimited
- **API Calls**: Unlimited
- **Support**: Dedicated account manager, phone support
- **Syncs**: Unlimited
- **Features**: All features + SLA guarantee, custom integrations, on-premise option

## Usage Tracking

### How We Calculate Usage
- **Data Transfer**: All data uploaded OR downloaded counts toward limit
- **Storage**: Data stored in CloudSync Pro system (not source/destination)
- **API Calls**: Every API request counts as one call

### Real-time Usage Dashboard
1. Log in to CloudSync Pro
2. Navigate to Account > Usage
3. View current month's usage
4. See breakdown by sync job
5. Compare against limits

### Overage Charges
- Starter Plan: $0.50 per GB over limit
- Professional Plan: $0.30 per GB over limit
- Enterprise: Included in custom pricing

### Alerts and Warnings
- Alert at 75% of monthly limit
- Alert at 90% of monthly limit
- Hard stop at 100% (syncs pause until next billing cycle)
- Email notifications for each milestone

## Billing and Invoicing

### Billing Cycle
- Monthly on your billing date (same day each month)
- Annual subscriptions available (20% discount)

### Payment Methods
- Credit card (Visa, Mastercard, American Express)
- Bank transfer (enterprise only)
- PayPal

### Invoice Details
- Invoices generated automatically on billing date
- Available in Account > Billing > Invoices
- Email copy sent to billing contact
- PDF download available
- Detailed breakdown of charges and usage

### Changes to Subscription
- Upgrade anytime (prorated charge)
- Downgrade effective end of current billing cycle
- Cancel anytime (no long-term contracts)

## Rate Limits

### API Rate Limiting
- **Starter**: 100 requests/minute
- **Professional**: 500 requests/minute
- **Enterprise**: Custom limits

### Rate Limit Headers
Every response includes:
```
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 487
X-RateLimit-Reset: 1642341600
```

### When Rate Limited (429 Response)
```json
{
  "error": "Too many requests",
  "retry_after": 60
}
```

**How to Handle:**
1. Implement exponential backoff
2. Retry after `retry_after` seconds
3. Consider upgrading plan if frequent

## Data Transfer Limits

### Per-Sync Limits
- Maximum file size: 5GB (Starter), Unlimited (Professional/Enterprise)
- Maximum files per sync: 1,000,000
- Maximum concurrent syncs: See plan details

### Bandwidth Throttling
- Peak hours (9AM-5PM UTC): 50 MB/s
- Off-peak hours: Unlimited
- Enterprise: No throttling with SLA

## Concurrent Operations

### Starter Plan
- Max 5 concurrent syncs
- Max 2 concurrent API requests

### Professional Plan
- Max 25 concurrent syncs
- Max 10 concurrent API requests

### Enterprise Plan
- Unlimited concurrent syncs
- Unlimited API requests (with SLA)

## Storage Retention

### Data Retention Policy
- Active sync data: Retained for 90 days after last sync
- Deleted syncs: Data purged after 30 days
- Backups: Retained for 1 year

### How to Request Deletion
1. Account > Data Management > Request Deletion
2. Select specific syncs or all data
3. Deletion completed within 7 days
4. Confirmation email sent

## Free Trial

### Trial Details
- Duration: 14 days
- Features: Full Professional plan features
- Data limit: 100 GB trial
- No credit card required
- Automatic upgrade after trial ends

### After Trial Ends
- Choose a plan to continue
- No automatic charging
- Can downgrade to free tier (limited to 5GB)
