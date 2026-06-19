# Frequently Asked Questions (FAQ)

## General Questions

### What is CloudSync Pro?
CloudSync Pro is a cloud data synchronization platform that allows you to sync data between multiple cloud providers (AWS S3, Google Cloud Storage, Azure Blob Storage) and on-premise systems in real-time.

### Is CloudSync Pro suitable for my use case?
CloudSync Pro is ideal for:
- Multi-cloud data management
- Backup and disaster recovery
- Data migration
- Hybrid cloud environments
- Compliance and data residency requirements

### How long does onboarding take?
Most customers are set up and running syncs within 30 minutes:
1. Create account (2 minutes)
2. Generate API key (2 minutes)
3. Connect data sources (5 minutes)
4. Create first sync (5 minutes)
5. Start sync (1 minute)

## Technical Questions

### What file types can I sync?
CloudSync Pro supports all file types:
- Documents: PDF, DOCX, XLSX, PPTX
- Images: JPG, PNG, GIF, TIFF
- Media: MP4, MP3, WAV
- Archives: ZIP, RAR, 7Z
- Code: .py, .js, .java, .go
- Databases: SQL dumps, exports
- Any binary format

### What's the maximum file size?
- Starter Plan: 5GB per file
- Professional Plan: Unlimited
- Enterprise Plan: Unlimited

### Is there a minimum file size?
No minimum file size. Even 1-byte files are supported.

### Can I sync directories/folders?
Yes! CloudSync Pro treats folders as regular file paths and syncs entire directory trees. All subdirectories and nested files are included.

### How does versioning affect storage?
Each file version is stored separately. A 100MB file with 10 versions uses approximately 1GB (100MB × 10). You can manage storage by setting retention policies.

## Billing Questions

### How is billing calculated?
You're charged for:
1. **Monthly subscription** (based on plan)
2. **Data transfer** (total GB uploaded + downloaded)
3. **Overage fees** (if exceeding plan limit)

### Can I cancel anytime?
Yes, there are no long-term contracts. Cancel anytime in Account Settings > Billing. Your access ends at the end of the current billing cycle.

### Do you offer discounts for annual billing?
Yes! Annual subscriptions receive 20% discount:
- Starter: $29 × 12 × 0.8 = $279.60/year
- Professional: $99 × 12 × 0.8 = $950.40/year

### What about free trials?
We offer a 14-day free trial with full Professional plan features. No credit card required.

### Can I upgrade or downgrade anytime?
Yes. Upgrades take effect immediately (prorated charge). Downgrades take effect at end of current billing cycle.

## Account Questions

### How do I reset my password?
1. Go to login page
2. Click "Forgot Password?"
3. Enter your email
4. Check email for reset link
5. Click link and enter new password
6. Link expires in 24 hours

### Can I have multiple accounts?
No, one account per email. If you need multiple workspaces, use sub-accounts (Professional+). Contact support for details.

### Can I transfer my account to someone else?
Yes, contact support to transfer account ownership. Require verification from both parties.

### How do I enable Two-Factor Authentication?
1. Account Settings > Security
2. Click "Enable 2FA"
3. Scan QR code with authenticator app
4. Enter 6-digit code to verify
5. Save recovery codes safely

## Security Questions

### Is my data encrypted?
Yes, all data is encrypted:
- **In Transit**: TLS 1.3
- **At Rest**: AES-256
- **Keys**: Managed by AWS KMS (Enterprise: Hardware Security Module)

### Where is my data stored?
Default: Virginia, USA. You can choose:
- US East (Virginia)
- US West (California)
- Europe (Frankfurt) - GDPR compliant
- APAC (Singapore)

### Do you sell my data to third parties?
No. Your data is never sold. It's used only for sync operations. See Privacy Policy for details.

### How long do you retain my data after deletion?
- Deleted syncs: Purged after 30 days
- Backup copies: Retained for 1 year for disaster recovery
- Audit logs: Retained for 1 year

## Performance Questions

### Why is my sync slow?
Common causes:
1. **Network latency**: Switch to regional endpoint
2. **Large files**: Enable compression
3. **Many small files**: Increase batch size
4. **Source/destination limits**: Check throughput constraints

See Troubleshooting section for optimization tips.

### How can I speed up my sync?
1. Enable compression: Settings > Network > Compress
2. Use regional endpoints
3. Increase chunk size: Settings > Advanced > Chunk Size
4. Enable parallel transfers (Professional+)
5. Schedule during off-peak hours

### What's the maximum transfer speed?
- Peak hours: 50 MB/s
- Off-peak hours: Unlimited (Professional)
- Enterprise: No throttling with SLA

## Integration Questions

### Can I use CloudSync Pro with CI/CD?
Yes! We support:
- GitHub Actions
- GitLab CI/CD
- Jenkins
- CircleCI
- AWS CodePipeline

See Integration Guide for examples.

### Is there a webhook support?
Yes, webhooks are supported for all events:
- sync.started, sync.completed, sync.failed
- Automatic retry on failure
- Available for Professional+ plans

### Can I monitor syncs programmatically?
Yes, use the REST API:
- GET /syncs - List all syncs
- GET /syncs/{id} - Get sync details
- POST /syncs/{id}/pause - Pause sync
- POST /syncs/{id}/resume - Resume sync

## Support Questions

### How do I contact support?
- **Starter**: Email (48-hour response)
- **Professional**: Email or Chat (24-hour response)
- **Enterprise**: Dedicated manager, phone support

Email: support@cloudsync.com

### Is there a community forum?
Yes! Visit https://forum.cloudsync.com to:
- Ask questions
- Share best practices
- View solutions from other users
- Report issues

### Do you offer SLA guarantees?
Yes, Enterprise plans include:
- 99.95% uptime SLA
- Guaranteed response time
- Dedicated support team
- Priority bug fixes
