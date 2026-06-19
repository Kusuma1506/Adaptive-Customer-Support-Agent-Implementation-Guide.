# Product Updates and Release Notes

## Version 3.2.0 (Latest) - January 2024

### New Features
- **Parallel Upload Support**: Upload up to 8 files simultaneously. Improves large sync performance by 40-60%.
- **Smart Scheduling**: AI-powered scheduling suggests optimal sync times based on your usage patterns
- **Enhanced Webhook System**: Improved retry logic, webhook event filtering, custom headers support
- **Data Encryption Dashboard**: Visual encryption status for all data in transit and at rest

### Bug Fixes
- Fixed rate limiting issue when uploading >10,000 files
- Resolved memory leak in versioning system
- Fixed broken webhook delivery for sync.failed event
- Corrected calculation for storage quota warnings

### Performance Improvements
- 30% faster file indexing for large syncs
- Reduced memory footprint by 20%
- Improved database query performance by 25%

### Deprecated Features
- XML configuration format (use JSON instead)
- Legacy API v0 endpoints (migrate to v1)

### Migration Guide
See docs: https://docs.cloudsync.com/v3.2-migration

---

## Version 3.1.5 - December 2023

### Bug Fixes
- Fixed authentication timeout issue
- Resolved race condition in concurrent file transfers
- Fixed UI freeze when loading large file lists

### Improvements
- Better error messages for permission denied scenarios
- Improved connection stability on high-latency networks

---

## Version 3.1.0 - November 2023

### New Features
- **Conditional Sync**: Trigger syncs based on file changes, size, or modification time
- **Advanced Filtering**: Regex pattern matching for include/exclude rules
- **Sync Templates**: Save and reuse sync configurations
- **API Key Rotation**: Automated security key rotation for enterprise

### Security Fixes
- Fixed privilege escalation vulnerability (CVSS 7.2)
- Improved XSS protection in dashboard
- Added CSRF token validation

### Performance
- 20% faster metadata synchronization
- Reduced bandwidth usage by 15% with improved compression

---

## Version 3.0.0 - September 2023 (Major Release)

### Breaking Changes
⚠️ **Note**: Upgrade carefully! Some APIs changed.

**What Changed:**
- API endpoint structure reorganized
- OAuth flow updated
- Webhook payload format modified

**Migration Required:**
- Update API client libraries
- Modify webhook handlers
- Re-authenticate OAuth applications

See breaking changes guide: https://docs.cloudsync.com/v3-breaking-changes

### New Features
- **Multi-region Support**: Sync across global regions with automatic failover
- **Advanced Monitoring**: Real-time performance metrics and custom dashboards
- **Compliance Features**: GDPR, HIPAA, SOC 2 compliance dashboard
- **Service Accounts**: Improved service account management

### Platform Changes
- Switched from Python to Go backend (faster, more scalable)
- New database architecture (improved reliability)
- Improved scalability (10x more concurrent syncs)

---

## Version 2.8.5 - August 2023

### Bug Fixes
- Fixed S3 IAM policy validation
- Resolved GCS service account key parsing issues
- Fixed Azure SAS token renewal

### Improvements
- Better documentation for complex auth scenarios
- Improved error messaging

---

## Upgrading Your Installation

### Automatic Updates (Recommended)
1. Settings > General > Check for Updates
2. Click "Update Available" if shown
3. Application restarts automatically
4. Syncs resume after restart

### Manual Updates
**Windows:**
```
Download: https://downloads.cloudsync.com/v3.2.0/win
Run installer and follow prompts
```

**macOS:**
```
Download: https://downloads.cloudsync.com/v3.2.0/mac
Open DMG and drag to Applications
```

**Linux:**
```
sudo apt-get update
sudo apt-get install cloudsync-pro=3.2.0
```

### Rolling Back to Previous Version
If you encounter issues after upgrade:
1. Download previous version
2. Uninstall current version
3. Install previous version
4. Contact support with error details

---

## Known Issues

### Current Issues (v3.2.0)

**Issue #1**: Large File Uploads
- **Description**: Files >2GB may timeout on slow connections
- **Workaround**: Split into smaller chunks, use off-peak hours
- **Status**: Fixed in v3.3.0 (beta)

**Issue #2**: Webhook Delivery Delay
- **Description**: Webhooks may deliver 5-10 minutes late during peak load
- **Workaround**: Implement exponential backoff in webhook consumer
- **Status**: Under investigation

**Issue #3**: Docker Container Memory
- **Description**: Docker deployments use 15-20% more memory
- **Workaround**: Allocate 512MB extra RAM in docker-compose
- **Status**: Fixed in v3.2.1 (hotfix)

### Platform-Specific Issues

**Windows**: Console window appears briefly on startup (cosmetic)
**macOS**: Initial launch may take 30 seconds (one-time only)
**Linux**: Some distributions need libssl-dev package

---

## Feature Request & Voting

Have a feature request? Vote or submit at:
https://cloudsync.com/feature-requests

Popular requests:
1. Local caching system (87 votes)
2. Multi-account management (64 votes)
3. Built-in VPN support (52 votes)
4. AWS S3 Select integration (48 votes)

---

## Support Matrix

### Version Support Status

| Version | Release Date | End of Support | Status |
|---------|-------------|----------------|--------|
| 3.2.0 | Jan 2024 | Jan 2026 | **Active** |
| 3.1.5 | Dec 2023 | Dec 2024 | Maintenance |
| 3.1.0 | Nov 2023 | Nov 2024 | Maintenance |
| 3.0.0 | Sep 2023 | Sep 2024 | Extended |
| 2.8.5 | Aug 2023 | Aug 2023 | Unsupported |

### Support Policy
- Active: Full support, security updates
- Maintenance: Critical fixes only
- Extended: Security fixes only
- Unsupported: No support provided

---

## Roadmap

### Q1 2024 (Upcoming)
- Predictive sync scheduling
- Enhanced dashboard analytics
- Mobile app (beta)

### Q2 2024
- Kubernetes operator
- Advanced rate limiting controls
- Multi-factor webhook authentication

### Q3 2024
- GraphQL API (beta)
- Advanced ML-powered anomaly detection
- Real-time sync replication

See full roadmap: https://cloudsync.com/roadmap
