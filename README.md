# Sufrivo Website

Responsive GitHub Pages/Jekyll-compatible marketing site based on the [Sufrivo Figma design](https://www.figma.com/design/K1iNr0zr9HX8TfWKbTYEVZ).

## Pages
Home, product overview, eight product details, pricing, industries, integrations, about, contact, demo, help, privacy, and terms.

## Run and test
```bash
python3 -m http.server 8000
node --test tests/site.test.cjs
```

## Commercial approval required
Starter (AED 299), Growth (AED 699), Scale (AED 1,499) and Enterprise (custom) are **illustrative proposals only**, not approved public offers. Confirm plan entitlements, taxes, hardware, payment fees and contractual terms before production launch.

## Lead form configuration
The form validates required fields and consent. With no backend configured, it downloads a request text file and **does not send personal data anywhere**. For actual lead capture, add a verified HTTPS endpoint via a meta tag in `demo/index.html` and `contact/index.html`:

```html
<meta name="sufrivo-lead-endpoint" content="https://YOUR-APPROVED-ENDPOINT.example/api/leads">
```

The endpoint must explicitly accept JSON and return 2xx only after saving the lead. Implement CORS, rate limiting, spam protection, input validation, privacy retention and secure storage server-side. No endpoint or mailbox has been invented.

## Arabic
The language switch activates RTL and a translation dictionary for key marketing text and UI. Full editorial Arabic translation and legal review are still required; do not claim complete bilingual localization.

## Images
Figma provides two original restaurant photographs; the published site currently uses CSS dashboard illustrations until the original binary assets can be committed and their licensing/placement verified.

## Deployment
The existing GitHub Pages workflow builds Jekyll on `main`. The quality workflow runs on pull requests and pushes. Check Pages environment configuration and the published URL after merging.
