#!/usr/bin/env python3
"""Generate indexable, localized HTML pages with alternate hreflang links.
Localized editorial landing pages are separate from the English interactive site."""
import json, html
from pathlib import Path
data=json.loads(Path("i18n/locales.json").read_text(encoding="utf-8"))
root=Path("_site"); origin="https://sufrivo.github.io/sufrivo-website/"
codes=list(data["languages"])
for path in data["paths"]:
    for code in codes:
        if code=="en": continue
        name,main,desc,explore,demo=data["languages"][code]
        product=path.split("/")[-1] if path.startswith("products/") else ""
        heading=data["products"][product][code] if product in data["products"] else (data["pageTitles"].get(path,[main]*8)[codes.index(code)] if path else main)
        title=f"{heading} | Sufrivo"
        url=origin+code+"/"+(path+"/" if path else "")
        rel="../" if not path else "../"*(path.count("/")+2)
        alts="".join(f'<link rel="alternate" hreflang="{c}" href="{origin+(c+"/" if c!="en" else "")+(path+"/" if path else "")}">' for c in codes)
        alts+=f'<link rel="alternate" hreflang="x-default" href="{origin+(path+"/" if path else "")}">'
        navigation="".join(f'<a href="{rel}{c}/{path+"/" if path else ""}" lang="{c}">{html.escape(data["languages"][c][0])}</a> ' for c in codes if c!="en")
        navigation+=f'<a href="{rel}{path+"/" if path else ""}" lang="en">English</a>'
        productlinks="".join(f'<li><a href="{rel}{code}/products/{p}/">{html.escape(d[code])}</a></li>' for p,d in data["products"].items())
        body=f'''<!doctype html><html lang="{code}" dir="{"rtl" if code=="ar" else "ltr"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc,quote=True)}"><link rel="canonical" href="{url}">{alts}<meta property="og:title" content="{html.escape(title,quote=True)}"><meta property="og:description" content="{html.escape(desc,quote=True)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="{rel}assets/css/site.css"></head><body><header class="site-header"><div class="wrap nav-wrap"><a class="brand" href="{rel}{code}/">sufrivo</a><nav aria-label="Languages">{navigation}</nav></div></header><main class="wrap" style="padding:3rem 1rem;min-height:65vh"><section class="section"><span class="chip">Sufrivo</span><h1>{html.escape(heading)}</h1><p class="section-lead">{html.escape(desc)}</p><p>{html.escape(explore)}</p><ul>{productlinks}</ul><p><a class="btn btn-primary" href="{rel}{code}/demo/">{html.escape(demo)}</a></p></section></main><footer class="footer"><div class="wrap"><a href="{rel}">Sufrivo</a> · {html.escape(name)}</div></footer></body></html>'''
        target=root/code/path/"index.html"
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(body,encoding="utf-8")
# Update sitemap with alternate localized URLs
sitemap=root/"sitemap.xml"
if sitemap.exists():
    xml=sitemap.read_text(encoding="utf-8")
    extra="".join(f'<url><loc>{origin}{c}/{p+"/" if p else ""}</loc></url>\n' for c in codes if c!="en" for p in data["paths"])
    sitemap.write_text(xml.replace("</urlset>",extra+"</urlset>"),encoding="utf-8")
print(f"Generated {(len(codes)-1)*len(data['paths'])} localized static SEO pages")
