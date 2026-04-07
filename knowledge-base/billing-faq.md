# Billing & Subscription FAQ

## Common Billing Questions

### Q: What are your subscription tiers?
A: We offer three subscription tiers:
- **Starter**: $29/month - up to 1,000 API calls/month, 1 project
- **Professional**: $99/month - up to 50,000 API calls/month, 10 projects, priority support
- **Enterprise**: Custom pricing - unlimited API calls, unlimited projects, dedicated support

### Q: How does the billing cycle work?
A: Billing is charged on a monthly basis on the same day each month. If you sign up on the 15th, you'll be billed on the 15th of each month. Pro-rated charges apply for mid-cycle upgrades.

### Q: Can I change my subscription tier?
A: Yes, you can upgrade or downgrade your subscription at any time. Upgrades take effect immediately. Downgrades take effect at the start of your next billing cycle.

### Q: What payment methods do you accept?
A: We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and bank transfers for Enterprise customers.

### Q: Do you offer refunds?
A: We offer a 7-day money-back guarantee for new customers (first month only). After that, we do not offer refunds for partial months.

### Q: Are there any additional fees?
A: There are no hidden fees. Additional charges may apply for:
- Exceeding your API call limit: $0.01 per additional call
- Storage overage: $0.50 per GB over your tier limit
- Premium features: Contact sales for pricing

### Q: How do I see my usage?
A: You can view real-time usage metrics in your dashboard under "Billing & Usage". Detailed invoices are available under "Invoices".

### Q: Can I get an invoice for my subscription?
A: Yes, invoices are emailed automatically each month and are also available for download in your dashboard.

## Billing Error Scenarios

### Plan Upgrade Returns Error 500 or Fails
If a customer reports "upgrade failed" or "error 500 while upgrading plan":
1. Confirm whether payment was captured at the processor.
2. Check upgrade transaction logs for request ID and gateway response.
3. Verify no duplicate charge occurred.
4. Re-run entitlement sync after successful payment confirmation.
5. Check if customer hit upgrade frequency limit (minimum 1 day between changes).

Recommended customer communication:
- Acknowledge the failed upgrade and apologize.
- Confirm charge status clearly (captured/pending/failed).
- Provide ETA for retry or manual completion.
- Offer temporary manual feature access while investigating.

### Payment Processing Error at Checkout or Subscription Creation
If payment fails during checkout or first subscription setup:
1. Validate card token/payment method status.
2. Check fraud/risk rejection code and retry guidance.
3. Confirm billing address and currency compatibility.
4. Escalate to billing operations if repeated failures occur for multiple users.
5. Verify customer hasn't exceeded trial period extensions.

**Common decline reasons**:
- Card expired or reported stolen
- Insufficient funds
- 3D Secure authentication required (request customer enable)
- Address verification (AVS) mismatch
- CVV/CVC validation failed

### Invoice Not Received or Missing
Customer message: "I didn't receive my invoice", "where is my invoice?", "billing email doesn't work"

1. Confirm billing email address in account settings.
2. Check spam/junk folder in email.
3. Verify subscription was charged (check payment processor).
4. Resend invoice from admin panel if found in system.
5. Check if email delivery provider is blocking domain.

### Refund & Cancellation Requests
Customer message: "I want a refund", "charge me", "cancel my subscription"

**Policy reminders**:
- First month: 7-day money-back guarantee (full refund)
- After first month: No refunds for partial months
- Cancellation takes effect at end of current billing cycle
- Can cancel anytime, no penalty

**Process**:
1. Verify customer is within guarantee window (7 days from subscription start).
2. If eligible, process full refund immediately.
3. If outside window, explain policy and offer loyalty discount for retention.
4. Cancel subscription on next billing cycle if requested.
5. Provide confirmation email with effective cancellation date.

### Duplicate Charges or Billing Errors
Customer message: "I was charged twice", "unexpected charge", "wrong amount charged"

1. Pull payment history for customer account.
2. Identify duplicate/erroneous charge.
3. Check if charge failed-then-retried, causing duplication.
4. Determine appropriate action:
   - If duplicate within 24 hours: initiate refund immediately
   - If charge for cancelled subscription: refund with apology
   - If partial refund needed: explain proration and process
5. Document in customer notes for future reference.

### Promotional Codes & Discounts Not Applied
Customer message: "Promo code didn't work", "discount not applied", "coupon expired"

1. Verify promotional code exists and is active.
2. Check code validity period (start/end dates).
3. Verify customer meets code restrictions (new customers only, specific tier, etc.).
4. Check if code already used (usually single-use).
5. If valid, manually apply discount and apologize for friction.

### Trial Period & Grace Period Issues
Customer message: "Trial expired", "extra time granted", "when does trial end?"

1. Check trial start date and standard duration.
2. Verify if extension/grace period was granted.
3. Confirm next charge date to customer.
4. For at-risk churn: offer extended trial or discounted rate.
5. Document any extensions in customer notes.

## Subscription Tier Comparison

| Feature | Starter | Professional | Enterprise |
|---------|---------|--------------|------------|
| **Monthly Cost** | $29 | $99 | Custom |
| **API Calls/Month** | 1,000 | 50,000 | Unlimited |
| **Projects** | 1 | 10 | Unlimited |
| **Team Members** | 1 | 5 | Unlimited |
| **Support** | Community | Email (24-48h) | 24/7 (4h) |
| **SLA** | None | 99.5% | 99.9% |
| **IP Whitelisting** | No | No | Yes |
| **Custom Integrations** | No | No | Yes |
| **Data Retention** | 30 days | 90 days | Configurable |
| **Audit Logs** | No | 90 days | 1 year |
| **Dedicated Support** | No | No | Yes |
