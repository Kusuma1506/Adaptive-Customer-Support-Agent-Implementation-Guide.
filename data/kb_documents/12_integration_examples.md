# Integration Examples and Use Cases

## Real-World Use Cases

### Use Case 1: Multi-Cloud Backup Strategy

**Company:** TechCorp (SaaS provider)
**Challenge:** Data spread across AWS, GCS, and Azure; need unified backup
**Solution:** CloudSync Pro syncs all three clouds daily to on-premise NAS

**Implementation:**
```
Sync 1: AWS S3 → NAS (Daily 2:00 AM)
Sync 2: GCS → NAS (Daily 2:30 AM)
Sync 3: Azure Blob → NAS (Daily 3:00 AM)
```

**Results:**
- Unified backup strategy
- 24-hour backup protection
- Single pane of glass monitoring
- RTO: 30 minutes
- Cost saved: $50K/year (vs. manual approach)

### Use Case 2: GDPR Data Residency Compliance

**Company:** EuroBank (Financial services)
**Challenge:** Customer data must stay in EU due to GDPR
**Solution:** CloudSync Pro with EU region endpoint, automated compliance monitoring

**Implementation:**
```
Source: Global AWS S3
Destination: EU Frankfurt datacenter (encrypted)
Schedule: Real-time sync
Retention: 7 years (audit compliance)
```

**Results:**
- 100% GDPR compliant
- Automated data residency enforcement
- Compliance reports auto-generated
- Zero data breaches since implementation

### Use Case 3: CI/CD Pipeline Integration

**Company:** DeviceCo (IoT manufacturer)
**Challenge:** Sync test results from build pipeline to data warehouse
**Solution:** GitHub Actions → CloudSync Pro → Data warehouse

**Implementation:**
```yaml
On: push to main
  Step 1: Run tests
  Step 2: Upload results to S3
  Step 3: CloudSync Pro syncs to data warehouse
  Step 4: Analytics dashboard updated
```

**Results:**
- Automated data pipeline
- Real-time test result availability
- 95% reduction in manual data transfers
- Faster insights into quality metrics

### Use Case 4: Disaster Recovery Automation

**Company:** FinanceFlow (Investment platform)
**Challenge:** RPO < 1 hour, RTO < 4 hours for critical data
**Solution:** Hourly syncs to multiple regions with automated failover

**Implementation:**
```
Primary: us-east
Secondary: us-west (hourly backup)
Tertiary: eu (daily backup)
Automated: Failover when primary unavailable
```

**Results:**
- Meets regulatory RTO/RPO requirements
- Zero unplanned downtime (3 years)
- Reduced recovery costs by 70%
- Passed compliance audits consistently

---

## Integration Patterns

### Pattern 1: ETL Pipeline

**Data Flow:**
```
Source System → CloudSync Pro → Data Lake → Analytics
```

**Code Example:**
```python
import requests
import json

API_KEY = os.environ['CLOUDSYNC_API_KEY']
SYNC_ID = 'sync_analytics_pipeline'

# Trigger sync
response = requests.post(
    f'https://api.cloudsync.com/v1/syncs/{SYNC_ID}/resume',
    headers={'Authorization': f'Bearer {API_KEY}'}
)

# Wait for completion
while True:
    status = requests.get(
        f'https://api.cloudsync.com/v1/syncs/{SYNC_ID}',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    
    if status.json()['status'] == 'completed':
        print(f"Transferred {status.json()['files_transferred']} files")
        break
    
    time.sleep(60)
```

### Pattern 2: Webhook-Driven Notifications

**Event Flow:**
```
CloudSync Pro (sync completed) → Webhook → Slack/Email → Alert Team
```

**Webhook Handler Example:**
```python
from flask import Flask, request
import slack_sdk

app = Flask(__name__)
slack_client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/webhook/cloudsync', methods=['POST'])
def handle_sync_webhook():
    event = request.json
    
    if event['event'] == 'sync.completed':
        message = f"""
        Sync Completed: {event['sync_id']}
        Files: {event['files_transferred']}
        Data: {event['bytes_transferred'] / 1e9:.2f} GB
        Duration: {event['duration_seconds']} seconds
        """
        
        slack_client.chat_postMessage(
            channel='#data-engineering',
            text=message
        )
    
    elif event['event'] == 'sync.failed':
        slack_client.chat_postMessage(
            channel='#alerts',
            text=f"⚠️ Sync Failed: {event['sync_id']}",
            blocks=[{
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Review in dashboard"}
            }]
        )
    
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)
```

### Pattern 3: Scheduled Batch Processing

**Architecture:**
```
CloudSync Pro (schedule) → Batch Job → Process → Result Storage
```

**Lambda Handler Example:**
```python
import boto3
import requests

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Trigger CloudSync Pro to sync input data
    api_key = os.environ['CLOUDSYNC_API_KEY']
    sync_id = event['sync_id']
    
    # Start sync
    requests.post(
        f'https://api.cloudsync.com/v1/syncs/{sync_id}/resume',
        headers={'Authorization': f'Bearer {api_key}'}
    )
    
    # Wait for sync (simplified - use SQS in production)
    time.sleep(300)
    
    # Process files
    response = s3.list_objects_v2(Bucket='processed-data')
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Processed {len(response['Contents'])} files")
    }
```

---

## Popular Integrations

### AWS Services
- **S3**: Primary storage backend
- **Lambda**: Serverless trigger and processing
- **EventBridge**: Event routing
- **CloudWatch**: Monitoring and alerting
- **Glue**: ETL pipeline orchestration

### GCP Services
- **GCS**: Primary storage backend
- **Cloud Functions**: Serverless triggers
- **Pub/Sub**: Event streaming
- **Cloud Monitoring**: Observability
- **Dataflow**: Data pipeline orchestration

### Azure Services
- **Blob Storage**: Primary storage backend
- **Functions**: Serverless execution
- **Event Grid**: Event routing
- **Monitor**: Alerts and dashboards
- **Data Factory**: Data pipeline

### Other Platforms
- **Kubernetes**: Operator-based deployment
- **Docker**: Containerized deployment
- **Airflow**: Workflow orchestration
- **dbt**: Data transformation
- **Tableau**: Analytics and BI

---

## Best Practices for Integration

### 1. Error Handling
```python
def sync_with_retry(sync_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f'https://api.cloudsync.com/v1/syncs/{sync_id}/resume',
                headers={'Authorization': f'Bearer {API_KEY}'},
                timeout=30
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt + random.random()
            time.sleep(wait)
```

### 2. Webhook Verification
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

### 3. Rate Limit Handling
```python
def api_call_with_rate_limit(endpoint, headers):
    while True:
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Retrying after {retry_after}s")
            time.sleep(retry_after)
            continue
        
        return response
```

### 4. Logging and Monitoring
```python
import logging

logger = logging.getLogger(__name__)

def log_sync_event(sync_id, event_type, status, metadata):
    logger.info({
        'sync_id': sync_id,
        'event_type': event_type,
        'status': status,
        'timestamp': datetime.utcnow().isoformat(),
        'metadata': metadata
    })
```
