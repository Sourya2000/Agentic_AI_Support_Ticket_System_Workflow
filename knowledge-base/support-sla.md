# Customer Support & SLA Policy

## Support Tiers

### Support Levels by Subscription
- **Starter**: Community forum only (no guaranteed response time)
- **Professional**: Email support (24-48 hour response time)
- **Enterprise**: 24/7 phone/email support (4-hour response time)

## Issue Severity & Response Times

### Critical (Severity 1)
- **Definition**: System completely unavailable, data loss risk, security breach
- **Response Time**: 1 hour (Enterprise), 4 hours (Professional)
- **Escalation**: Automatic escalation to engineering team
- **Example**: API entirely down, unauthorized access detected

### High (Severity 2)
- **Definition**: Major feature broken, significant degradation in performance
- **Response Time**: 4 hours (Enterprise), 8 hours (Professional)
- **Escalation**: Escalated after 2 hours without resolution
- **Example**: Authentication failing, database connection issues

### Medium (Severity 3)
- **Definition**: Minor feature not working, workaround available
- **Response Time**: 24 hours (Enterprise), 48 hours (Professional)
- **Example**: UI element not displaying correctly, occasional timeout errors

### Low (Severity 4)
- **Definition**: Questions, feature requests, documentation issues
- **Response Time**: 5 business days
- **Example**: "How do I...?", "Can you add feature X?"

## Uptime Guarantee

We guarantee 99.9% uptime on our Production environment monthly.
- Uptime is measured excluding scheduled maintenance windows
- Scheduled maintenance performed on Sundays 2:00-4:00 UTC
- If we fall below 99.9%, Enterprise customers receive service credits

## Supported Support Channels
- Email: support@company.com
- Community Forum: https://community.company.com
- Phone: +1-800-COMPANY (Enterprise only)
- Slack: Enterprise customers can request dedicated channel

## Known Issues & Workarounds
Current known issues are tracked at: https://company.com/known-issues

Common issues:
- **Intermittent timeouts on large file uploads**: Use the chunked upload endpoint
- **WebSocket connection drops**: Implement automatic reconnection with exponential backoff
- **Rate limit errors**: Implement request queuing in your client

## Support Ticket Escalation Process

### Severity 1 (Critical) - Escalation Path
1. **Support Agent** (0-15 min): Acknowledge ticket, gather info, identify business impact
2. **Support Manager** (15-30 min): Review context, assign engineering
3. **Engineering On-Call** (30 min+): Begin investigation and remediation
4. **Engineering Manager** (as needed): Coordinate cross-functional response
5. **Executive Escalation** (if needed): CTO/VP informed for major incidents

**Professional/Enterprise**: Direct escalation to engineering without manager approval

### Severity 2 (High) - Escalation Path  
1. **Support Agent** (initial): Gather context and attempt resolution
2. **Support Manager** (after 2 hours): Review if unresolved, escalate to engineering
3. **Engineering** (assigned): Begin investigation

**SLA**: 4-hour response (Enterprise), 8-hour (Professional)

### Severity 3 (Medium) - Support Path
1. **Support Agent**: Attempt resolution first
2. **Back-of-queue escalation**: Assign low-priority to engineering after 24 hours

**SLA**: 24-hour (Enterprise), 48-hour (Professional)

### Severity 4 (Low) - Information Request
1. **Support Agent**: Respond to inquiry

**SLA**: 5 business days

## Escalation Criteria

**When to escalate sooner**:
- Multiple customers affected
- Revenue/billing impact
- Security or compliance issue
- Customer on Enterprise tier
- Customer is high-value/strategic
- Issue involves data loss
- External communication needed (press, blog)

## Meeting Service Level Agreements

### For Starter Tier (Community)
- No guaranteed response time
- Best-effort support via forum
- Public issue tracking

### For Professional Tier
- First response: within stated SLA
- All subsequent: within 24 hours
- Response includes workaround or timeline to fix
- Feature requests: acknowledged, no committed timeline

### For Enterprise Tier
- Dedicated support contact
- Guaranteed response times
- Escalation authority pre-defined
- Quarterly business reviews included
- Custom SLA negotiable

## Support Ticket Best Practices

### Information to Always Collect
1. **Impact Summary**: What can't work due to this issue?
2. **Reproduction Steps**: Exact steps to reproduce
3. **Environment Details**: Region, API key tier, SDK version
4. **Request IDs**: From error messages/API responses
5. **Screenshots/Logs**: Error messages and context
6. **Business Impact**: Revenue loss, customer count affected, urgency

### Ticket Quality Standards
Dispatch ticket to Engineering only when:
- All relevant information collected
- Issue reproduced or root cause identified
- Workaround attempted or customer tested it
- Expected resolution clearly stated
- Acceptance criteria defined

### Follow-up Cadence
- **Critical**: Update customer every 1-2 hours until resolved
- **High**: Update every 4 hours  
- **Medium**: Update every 24 hours
- **Low**: Update when progress made

## Post-Incident Support

### After Resolution
1. Confirm issue resolved with customer
2. Document root cause in internal notes
3. Suggest preventive measures (e.g., upgrade tier, monitoring)
4. Offer free audit or consultation if applicable
5. Follow-up within 7 days to ensure no recurrence

### Pro-Active Outreach
For issues that affect account stability:
1. Proactively reach out within 24 hours of resolution
2. Offer technical review/optimization session
3. Suggest configuration changes to prevent recurrence
4. Provide loyalty discount if incident caused significant disruption
