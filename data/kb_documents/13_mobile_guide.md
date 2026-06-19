# Mobile App Guide and Quick Reference

## Mobile App Overview

### Available Platforms
- **iOS**: Version 2.1.0 (iOS 14.0+)
- **Android**: Version 2.1.0 (Android 9.0+)
- Download: App Store, Google Play Store

### Key Features
- Monitor sync status in real-time
- Start/pause syncs remotely
- Receive instant notifications
- View transfer progress
- Quick troubleshooting guide
- Account management

---

## Getting Started with Mobile

### Installation

**iOS:**
1. Open App Store
2. Search "CloudSync Pro"
3. Tap Install
4. Login with your credentials
5. Enable notifications (recommended)

**Android:**
1. Open Google Play Store
2. Search "CloudSync Pro"
3. Tap Install
4. Login with your credentials
5. Grant permissions when prompted

### First Login

1. Enter email address
2. Enter password (or use Face/Touch ID)
3. Verify via two-factor authentication
4. Accept terms of service
5. Dashboard loads with your syncs

---

## Mobile Dashboard

### Sync Status Overview

**Visual Indicators:**
- 🟢 Active: Sync running
- 🟡 Paused: Sync paused
- 🟣 Scheduled: Awaiting next schedule time
- 🔴 Failed: Sync encountered error

**Metrics Displayed:**
- Current transfer speed (MB/s)
- Files transferred / Total files
- Bytes transferred / Total bytes
- Estimated time remaining
- Last sync timestamp

### Detailed Sync View

Tap any sync to view:
- Source and destination
- Current progress (%)
- Network throughput
- Transfer history (last 7 days)
- Error details (if any)
- Configuration options

---

## Remote Control

### Start Sync
1. Tap sync from dashboard
2. Tap "Start" (green button)
3. Confirm action
4. Sync begins (notification sent)
5. Real-time progress visible

### Pause Sync
1. Tap active sync
2. Tap "Pause" (yellow button)
3. Confirm action
4. Sync pauses (can resume later)
5. Progress saved

### Create Quick Sync
1. Tap "+" button on dashboard
2. Select source (S3, GCS, etc.)
3. Select destination
4. Choose schedule (now, hourly, daily)
5. Tap "Create"
6. Sync created and begins

### Schedule Sync
1. Tap sync settings (⚙️)
2. Select "Schedule"
3. Choose frequency (hourly, daily, weekly)
4. Set time of day
5. Enable/disable
6. Tap "Save"

---

## Notifications

### Push Notification Types

**Sync Completed:**
- Sync name and ID
- Files transferred count
- Total data transferred
- Tap to view full details

**Sync Failed:**
- Sync name and ID
- Error message (abbreviated)
- Recommended action
- Tap for troubleshooting tips

**Performance Alert:**
- Current speed below normal
- Potential issues listed
- Optimization tips provided

**Storage Warning:**
- Storage usage at 80%
- Quota limit approaching
- Action required within N days

### Managing Notifications

1. Tap profile icon (top right)
2. Select "Notifications"
3. Toggle notification types on/off
4. Set quiet hours (e.g., 10 PM - 8 AM)
5. Choose notification sound
6. Tap "Save"

---

## Mobile Security

### Password Management

**Change Password:**
1. Tap profile icon
2. Select "Security"
3. Tap "Change Password"
4. Enter current password
5. Enter new password (twice)
6. Tap "Update"
7. Logout and login with new password

### Two-Factor Authentication (2FA)

**Enable 2FA:**
1. Tap profile icon
2. Select "Security"
3. Tap "Enable 2FA"
4. Scan QR code with authenticator app
5. Enter 6-digit code
6. Save recovery codes securely
7. Tap "Enable"

**Disable 2FA:**
1. Same path as above
2. Tap "Disable 2FA"
3. Enter current password
4. Confirm action
5. 2FA disabled

### Session Management

**View Active Sessions:**
1. Tap profile icon
2. Select "Active Sessions"
3. See all logged-in devices
4. Location and login time shown
5. Tap "Sign Out" to logout remote session

**Logout:**
1. Tap profile icon
2. Select "Logout"
3. Confirm action
4. Returns to login screen
5. Session terminated

---

## Mobile Troubleshooting

### App Won't Connect

**Solutions:**
1. Check internet connection (WiFi or cellular)
2. Restart app (swipe up to close, tap to reopen)
3. Verify API key valid (check dashboard on web)
4. Clear app cache: Settings > App > CloudSync > Storage > Clear Cache
5. Reinstall app if issues persist
6. Contact support: In-app chat

### Notifications Not Arriving

**Solutions:**
1. Verify notifications enabled: Profile > Notifications
2. Check OS notification permissions: Phone Settings > Apps > Permissions
3. Verify WiFi doesn't block notifications
4. Disable battery saver (may block notifications)
5. Test notification: Profile > Settings > Send Test Notification
6. Restart phone if issues persist

### Slow Performance

**Solutions:**
1. Close other apps (free up RAM)
2. Restart app
3. Check network speed (use speed test app)
4. Disable background processes
5. Clear app cache
6. Update app to latest version
7. Check phone storage (needs >500MB free)

### Sync Stuck in Progress

**Solutions:**
1. Wait 5 minutes (network may be slow)
2. Tap refresh button (↻) to update status
3. Pause sync and resume
4. Close app completely and reopen
5. Check source/destination connectivity
6. View error details: Tap sync > "Error Log"
7. Contact support if persists

---

## Mobile Best Practices

### Optimize Battery Life
- Disable notifications for non-critical syncs
- Avoid monitoring during transfer (let it run)
- Disable real-time refresh: Profile > Settings > Refresh Rate (set to Manual)
- Pause long-running syncs and check later
- Keep phone on WiFi (uses less power than cellular)

### Conserve Data Usage
- Use WiFi whenever possible
- Disable mobile notifications: Profile > Notifications > Disable Mobile Data
- Don't stream sync videos on cellular
- Use "Low Bandwidth Mode": Profile > Settings > Data Saver
- Monitor data usage: Profile > Usage > Data

### Security Best Practices
- Use strong password (12+ characters)
- Enable two-factor authentication
- Don't share login credentials
- Logout on shared devices
- Review active sessions regularly
- Don't use public WiFi for sensitive syncs
- Keep app updated to latest version

---

## Mobile Tips and Tricks

### Quick Access Shortcuts

**iOS:**
- Add CloudSync Pro to home screen dock
- Use Siri: "Open CloudSync Pro"
- Use Shortcuts app for automation

**Android:**
- Add CloudSync Pro widget to home screen
- Use Google Assistant: "Open CloudSync Pro"
- Use Android automation apps

### Widget (iOS/Android)

**Available Widgets:**
- Sync Status (shows active syncs count)
- Quick Actions (start/pause favorite sync)
- Storage Usage (shows quota remaining)

**Add Widget:**
1. Long-press home screen
2. Tap "+" button (top left)
3. Search "CloudSync Pro"
4. Select widget
5. Tap "Add Widget"
6. Widget now visible on home screen

### Siri/Google Assistant Integration

**Example Commands:**
- "Show me my active syncs"
- "Pause my S3 backup sync"
- "How much storage am I using?"
- "Start my daily backup"

---

## Mobile App Limitations

**Current Limitations:**
- Can't create complex schedules (use web for cron expressions)
- Can't configure advanced filters/exclusions
- Can't modify webhook integrations
- Real-time monitoring limited to last 24 hours
- File browser not available (source/destination visibility)
- Custom alerting requires web dashboard

**Workarounds:**
- Use web dashboard for complex configurations
- Mobile primarily for monitoring and quick actions
- Set important alerts before leaving computer

---

## Feedback and Support

### Report Issues
1. Tap profile icon
2. Select "Help & Support"
3. Tap "Report Bug"
4. Describe issue
5. Attach screenshot (optional)
6. Submit (goes to support team)

### Feature Requests
1. Tap profile icon
2. Select "Help & Support"
3. Tap "Feature Request"
4. Describe feature needed
5. Vote on existing requests
6. Support votes most popular features
