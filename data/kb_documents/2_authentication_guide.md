# Authentication and Security Guide

## API Authentication

### API Key Authentication
API keys are the primary method for programmatic access.

**How to Generate:**
1. Log in to dashboard
2. Go to Account Settings > API Keys
3. Click "Create New Key"
4. Specify scope (read-only, read-write, admin)
5. Set expiration date (optional)
6. Save securely (you won't see it again)

**Usage:**
```
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0 Flow
For third-party applications:

1. Register your app at https://cloudsync.com/oauth/apps
2. Get Client ID and Client Secret
3. Implement redirect URI
4. User grants permission
5. Receive access token (valid for 1 hour)
6. Use refresh token to get new access token (valid for 7 days)

### Service Accounts
For automated integrations:

1. Create service account in Settings > Service Accounts
2. Generate account key
3. Use account email and key for authentication
4. Recommended for CI/CD pipelines

## Security Best Practices

### Protecting Your API Key
- Never commit API keys to version control
- Use environment variables: `export CLOUDSYNC_API_KEY=your_key`
- Rotate keys regularly (every 90 days recommended)
- Delete unused keys immediately
- Monitor API key activity in dashboard

### Password Security
- Minimum 12 characters
- Include uppercase, lowercase, numbers, symbols
- Enable Two-Factor Authentication (2FA)
- Use authenticator apps (Google Authenticator, Authy)
- Keep recovery codes in secure location

### IP Whitelisting
- Available for enterprise accounts
- Restrict API access to specific IP addresses
- Configure in Settings > Security > IP Whitelist

## Troubleshooting Authentication Issues

### "Invalid API Key" Error
- Verify key is correctly copied
- Check key hasn't expired
- Confirm key is for correct environment (staging vs production)
- Try regenerating a new key

### OAuth Token Expiration
- Tokens expire after 1 hour
- Use refresh token to get new token
- Implement token refresh logic in your app
- Set up alerts for token expiration

### 403 Forbidden Error
- Check API key has required permissions
- Verify account is active and not suspended
- Confirm IP address is whitelisted (if enabled)
- Check request headers for Authorization field

## Rate Limiting
- Free tier: 100 requests/minute
- Professional: 500 requests/minute
- Enterprise: Custom limits
- Rate limit headers returned: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
