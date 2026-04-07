# Common Troubleshooting Guide

## API Connection Issues

### "Connection Refused" Error
**Cause**: Your server cannot reach our API endpoints
**Solution**:
1. Check your internet connection
2. Verify you're using the correct region endpoint
3. Ensure your API key is valid (check dashboard)
4. Check firewall/proxy settings if in corporate network
5. Try from a different network to isolate the issue

### Authentication Failed (401 Error)
**Cause**: Invalid or missing API key
**Solution**:
1. Verify your API key in Settings → API Keys
2. Ensure you're using `Authorization: Bearer YOUR_KEY` header
3. Check that your API key hasn't expired
4. Regenerate key if compromised

### Rate Limited (429 Error)
**Cause**: Exceeded your API quota
**Solution**:
1. Implement exponential backoff retry logic
2. Reduce request frequency or batch requests
3. Upgrade to a higher tier at Settings → Billing
4. Contact support for temporary quota increase

## Data Processing Issues

### Uploads Failing
**Cause**: File too large, unsupported format, or timeout
**Solution**:
1. Check file size limits: Starter (10MB), Professional (500MB), Enterprise (5GB)
2. Verify file format is supported (CSV, JSON, Parquet, Avro)
3. Use chunked upload for files > 100MB
4. Check file doesn't contain special unicode characters

### Incomplete/Missing Data in Results
**Cause**: Field mapping issues or schema mismatch
**Solution**:
1. Verify schema definition matches your data
2. Check for null values in required fields
3. Use field mapping UI to map columns explicitly
4. Check data after transformation steps

## Performance Issues

### Slow API Responses
**Solution**:
1. Check current platform status: https://status.company.com
2. Reduce query complexity (limit time range, reduce data volume)
3. Use pagination for large result sets
4. Ensure API key's tier supports your usage

### High Latency from Specific Region
**Solution**:
1. Switch to nearest region endpoint
2. Contact support if persistent
3. Enterprise customers can request regional CDN

## Incident Runbooks

### Production Checkout Failing for All Customers (HTTP 500)
**Severity**: Critical
**Typical customer message**: "Checkout is failing", "HTTP 500 error", "production outage", "no customer can complete payment", "payment processing failed", "checkout broken", "cannot process transactions"

This is a critical business-critical incident where checkout and payment processing are completely broken. The production checkout service is down, and customers cannot complete any payment transactions.

**Common variations of this issue**:
- Checkout returns HTTP 500 error for all customers
- Payment processing error affecting all transactions  
- Checkout service down causing complete payment failure
- All checkout requests are failing with HTTP error 500
- Production payment system broken - no transactions can complete
- Customers receiving service unavailable when trying to pay
- Payment gateway not responding - checkout timeout
- Transaction processing failed for all users
- Urgent: checkout system down, blocking all revenue
- Production failure: order processing failed completely

**Immediate actions (first 15 minutes)**:
1. Confirm incident scope in logs and monitoring dashboards.
2. Check payment gateway health and recent deployment status.
3. Roll back latest checkout service deployment if error rate spiked after release.
4. Enable incident banner and notify support escalation contacts.
5. Start incident bridge with engineering + support lead.

**Technical checks**:
1. Review application errors around checkout and payment authorization paths.
2. Verify DB connectivity and migration state for order/payment tables.
3. Validate third-party payment API credentials and rate-limit status.
4. Confirm queue/backpressure state for order processing workers.
5. Check recent infrastructure changes, CDN/load balancer configuration.
6. Monitor checkout service memory usage and error logs in real-time.

**Root cause examples**:
- Recent deployment introduced null pointer exception in payment handler
- Database connection pool exhausted causing transaction timeouts
- Payment gateway API credentials expired or rate-limited
- Infrastructure scaling event caused transient failures

**Customer communication template (critical outage)**:
- Acknowledge the outage and apologize immediately.
- Confirm the team is actively working on resolution.
- Share next update window (for example, within 30-60 minutes).
- For finance/payment sensitive customers, offer direct phone escalation.

### Payment Processing Error During Plan Upgrade
**Severity**: High
**Typical customer message**: "I tried to upgrade my plan but got error 500", "upgrade failed", "could not process payment", "plan change rejected"

**Checks**:
1. Validate billing plan IDs and upgrade API payload schema.
2. Verify payment method token validity and processor response code.
3. Check idempotency key handling for retry attempts.
4. Confirm entitlement sync job completed after successful payment.
5. Verify no duplicate charge on payment processor side.
6. Check if customer hit subscription change cooldown period.

**Support response guidance**:
1. Ask for timestamp and any request ID/error screenshot.
2. Reassure customer no duplicate charge will be applied.
3. Provide a clear follow-up timeline (e.g., issue resolved within 2 hours).
4. Check payment method validity and suggest updating if expired.
5. Offer manual upgrade completion if payment was successfully captured.

### Customer Account Access Issues (Login/MFA Problems)
**Severity**: High
**Typical customer message**: "Can't log in", "forgot password", "2FA not working", "locked out of account"

**Checks**:
1. Verify account exists and is not disabled/suspended.
2. Check if user recently enabled 2FA but lost access device.
3. Review authentication service logs for failures.
4. Confirm email delivery (especially password reset emails).
5. Check if account is under security investigation/lockout.

**Support response**:
1. Verify customer identity through secondary contact method.
2. For MFA lockout, provide account recovery options.
3. Reset password via secure link and guide customer through re-setup.
4. If account disabled, explain reason and provide remediation steps.

### API Integration Failures & SDK Issues
**Severity**: Medium-High
**Typical customer message**: "API keeps returning 401", "authentication header ignored", "SDK not working", "401 unauthorized errors"

**Checks**:
1. Verify API key format and validity in customer's account.
2. Check if API key has expired or been revoked.
3. Validate customer is using correct region endpoint.
4. Confirm request headers are correctly formatted (`Authorization: Bearer KEY_ID`).
5. Check SDK version compatibility with current API version.

**Common issues**:
- API key copied with whitespace (leading/trailing spaces)
- Wrong authorization header format (missing "Bearer", using "Basic")
- Using old/deprecated API key that was rotated
- SDK version mismatch requiring upgrade

**Resolution**:
1. Have customer regenerate new API key.
2. Provide code snippet with correct header format.
3. Suggest SDK upgrade to latest version.
4. Provide curl example for testing endpoint.

### Data Export/Import Failures
**Severity**: Medium
**Typical customer message**: "Export failed", "import hangs", "file too large to upload", "invalid format error"

**Checks**:
1. Verify file size is within tier limits (Starter 10MB, Professional 500MB, Enterprise 5GB).
2. Confirm file format is supported (CSV, JSON, Parquet).
3. Check for special unicode/encoding issues in file.
4. Verify schema matches expected structure.
5. Check for timeout issues on large files.

**Solutions**:
1. For large files, use chunked upload endpoint.
2. Validate CSV/JSON structure before upload.
3. Break into smaller batches if hitting timeout.
4. For special characters, ensure UTF-8 encoding.

### Performance & Slow Response Issues
**Severity**: Medium
**Typical customer message**: "API is slow", "queries timeout", "high latency", "service is sluggish"

**Checks**:
1. Check platform status page for ongoing incidents.
2. Verify customer query complexity (time range, data volume).
3. Check if customer is near rate limit causing throttling.
4. Review query logs to identify inefficient queries.
5. Verify customer is using correct region endpoint for lowest latency.

**Optimization tips**:
1. Use pagination for large result sets.
2. Add date range filters to reduce data scanned.
3. Use field selection to retrieve only needed columns.
4. Implement client-side caching for static data.
5. Consider upgrading to Professional tier for higher limits.

### CSV Export Formatting Issue (Single Optional Column)
**Severity**: Medium
**Typical customer message**: "optional CSV column has incorrect formatting"

**Checks**:
1. Verify locale/formatting rules for that report type.
2. Re-run export with default delimiter and UTF-8 encoding.
3. Compare column serializer behavior across environments.
4. Confirm issue is limited to one report and optional field only.

**Support response guidance**:
1. Mark as non-outage, medium priority.
2. Provide workaround (manual format fix or alternate export).
3. Commit to a fix window (for example, next few days).
