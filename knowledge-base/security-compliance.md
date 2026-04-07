# Security & Compliance Policies

## Data Protection

### Encryption Standards
- **In Transit**: All API requests use TLS 1.2+ (HTTPS)
- **At Rest**: AES-256 encryption for sensitive data in database
- **Backups**: Encrypted backups stored in secure locations with redundancy

### Data Retention
- **Active Data**: Retained as long as your account is active
- **Deleted Data**: Permanently deleted within 30 days
- **Audit Logs**: Retained for 90 days (Enterprise: 1 year)
- **Backups**: Deleted after 90 days

### API Key Security
- Never share API keys in code repositories
- Rotate keys regularly (recommended: quarterly)
- Use separate keys for different environments (dev, staging, production)
- Monitor key usage in dashboard audit logs
- Disable unused keys immediately

## Compliance Certifications

### Standards We Meet
- **SOC 2 Type II**: Security, availability, and confidentiality
- **GDPR**: Full GDPR compliance with data processing agreements
- **HIPAA**: Health insurance portability (Enterprise tier)
- **PCI DSS**: If handling payment card data
- **ISO 27001**: Information security management system

### Privacy Policy
See our full privacy policy at: https://company.com/privacy

Key points:
- We do not sell customer data
- We do not use your data for training AI models without explicit consent
- Subprocessors listed at: https://company.com/subprocessors
- GDPR Data Processing Addendum available for Enterprise

## Access Control

### User Roles & Permissions
- **Owner**: Full access, can manage billing and team
- **Admin**: Can manage projects and team members
- **Editor**: Can view and edit projects
- **Viewer**: Read-only access to projects

### IP Whitelisting
Enterprise customers can restrict API access to specific IP addresses via Settings → Security.

### Audit Logging
All actions are logged with: user, timestamp, action, and affected resource.
Accessible in: Settings → Audit Logs

## Vulnerability & Incident Response

### Reporting Security Issues
Found a vulnerability? Report to: security@company.com
We follow responsible disclosure and will:
1. Acknowledge receipt within 24 hours
2. Investigate and reproduce
3. Develop and test fix
4. Release patch update
5. Credit your discovery (unless you prefer anonymity)

### Incident Response Process
If a security incident occurs:
1. We notify affected customers within 24 hours
2. Provide incident details and remediation steps
3. Offer free security audit/consultation
4. Post incident report within 7 days

## OAuth 2.0 / OpenID Connect

### Setting Up OAuth for Third-Party Applications
1. Register application in Settings → OAuth Apps
2. Configure redirect URIs (authorization callback)
3. Obtain Client ID and Client Secret
4. Implement OAuth flow in your application

### OAuth Scopes
Request only necessary scopes:
- `read:projects` - Read project data
- `write:projects` - Modify projects
- `read:data` - Read data files
- `write:data` - Upload/modify data
- `read:team` - View team members
- `write:team` - Manage team (invite, remove)

### Token Management
- Access tokens expire every 1 hour
- Use refresh tokens to obtain new access tokens
- Store tokens securely (not in localStorage if browser-based)
- Implement token rotation for long-lived applications

## AWS/Cloud-Specific Security

### Integration with AWS Secrets Manager
```python
import boto3
from company_sdk import Client

secrets_client = boto3.client('secretsmanager')
api_key_secret = secrets_client.get_secret_value(SecretId='company-api-key')
api_key = api_key_secret['SecretString']

client = Client(api_key=api_key)
```

### Integration with HashiCorp Vault
```python
import hvac
from company_sdk import Client

vault = hvac.Client(url='http://vault:8200')
api_key = vault.secrets.kv.read_secret_version(
    path='company/api-key'
)['data']['data']['key']

client = Client(api_key=api_key)
```

### VPC & Network Security
- Enterprise customers can use PrivateLink for dedicated connections
- IP whitelisting available to restrict access by source IP
- VPC Peering supported for direct network connectivity
- DDoS protection included in all tiers

## Security Checklist for Production Deployment

- [ ] API key stored in secrets manager (not hardcoded)
- [ ] Environment variables used for all configuration
- [ ] TLS 1.2+ enforced for all connections
- [ ] API key rotation scheduled (quarterly minimum)
- [ ] 2FA enabled on dashboard account
- [ ] IP whitelisting enabled if applicable
- [ ] Request signing enabled if available
- [ ] Audit logging enabled and monitored
- [ ] Data encryption at rest verified
- [ ] GDPR DPA signed if handling EU data
- [ ] Regular security scanning of dependencies
- [ ] Incident response plan documented
- [ ] Rate limiting configured to prevent abuse
- [ ] Error messages sanitized (no PII in logs)

## Vulnerability Disclosure

### Responsible Disclosure Timeline
1. **Day 0**: Researcher reports vulnerability
2. **Day 1**: We acknowledge receipt and begin assessment
3. **Day 7**: Provide timeline for fix
4. **Day 30**: Fix developed and deployed
5. **Day 31**: Researcher notified, can publish
6. **Day 32**: We publish security advisory

### After Disclosure
1. Security advisory published on company blog
2. Affected customers contacted with mitigation steps
3. Researcher credited (unless requesting anonymity)
4. Bounty paid if eligible under program
5. Acknowledgment in security report
