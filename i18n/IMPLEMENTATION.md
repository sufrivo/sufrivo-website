# Internationalization implementation specification

Status: foundation only; full-page translations are **not yet implemented**.

Supported languages: en, ar, bn, hi, ur, ml, ta, fr, es. Locale metadata lives in `i18n/locales.json`.

## Required delivery

- Extract **every visible string** from `assets/js/site.js`, including dynamically assembled page sections, navigation, footers, product stories, forms, validation, image alt text, pricing disclosures and legal pages into stable translation keys.
- Provide complete, human-reviewed locale catalogs for all nine languages. No fallback English content on published non-English pages; CI must fail if a key is missing.
- Generate a static, crawlable HTML entrypoint for each locale and each public route, retaining the original GitHub Pages repository prefix. Preserve a matching route when switching languages.
- Generate localized, meaningful titles, descriptions, H1s, open-graph tags and social previews. Avoid keyword stuffing and avoid promising features not yet released.
- Set `html[lang]` and `html[dir]` in the static HTML. Arabic and Urdu are RTL. Include locale-aware language selection on desktop and mobile.
- Add per-route canonical and reciprocal `hreflang` links including `x-default`, plus localized sitemap URLs. Exclude the internal platform administration page from the sitemap.
- Translate legal copy accurately and require legal review before publishing translations as authoritative. Preserve illustrative pricing and product availability caveats in every language.
- Test all 9 x 18 public routes, broken links, metadata, key parity, form semantics, RTL behavior and Lighthouse SEO.

## Release gate

Do not publish localized URLs or declare localization complete until full translated content and SEO prerendering are implemented and verified. A translated title alone is not a localized page.
