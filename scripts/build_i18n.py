#!/usr/bin/env python3
"""Generate static locale routes and reciprocal SEO metadata for GitHub Pages.
Run before Jekyll build: python3 scripts/build_i18n.py
Non-English body copy still requires reviewed translation catalogs before release.
"""
import json, re, html
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'i18n/locales.json').read_text())
BASE=cfg['baseUrl']
LOCALES=cfg['locales']
ROUTE_TITLES=json.loads((ROOT/'i18n/route-titles.json').read_text())
ROUTES=['','products','pricing','industries','integrations','about','contact','demo','help','privacy','terms']+['products/'+p for p in ['pos','kds','ordering','kiosk','reservations','staff','management']]
def url(locale,route):
    return BASE+locale+'/'+(route+'/' if route else '')
def original(route):
    return ROOT/route/'index.html'
def meta_tag(name,value):
    return '<meta name="'+name+'" content="'+html.escape(value,quote=True)+'">'
def build():
    for route in ROUTES:
        src=original(route).read_text()
        title_match=re.search(r'<title>(.*?)</title>',src,re.S)
        desc_match=re.search(r'<meta name="description" content="([^"]*)"',src)
        title=html.unescape(title_match.group(1)) if title_match else 'Sufrivo'
        description=html.unescape(desc_match.group(1)) if desc_match else ''
        for locale,info in LOCALES.items():
            target=ROOT/locale/route/'index.html'
            target.parent.mkdir(parents=True,exist_ok=True)
            # Do not falsely claim the English body is translated: untranslated pages are noindex.
            localized=locale=='en'
            page_title=(ROUTE_TITLES.get(locale,{}).get(route,{}) or {}).get('title',info['title'] if not route else title)
            page_desc=info['description'] if locale!='en' else (info['description'] if not route else description)
            out=src.replace('<html lang="en"','<html lang="'+locale+'" dir="'+info['dir']+'"',1)
            out=re.sub(r'data-base="[^"]+"','data-base="'+('../'*(len(route.split('/'))+1) if route else '../')+'"',out,count=1)
            out=re.sub(r'<title>.*?</title>','<title>'+html.escape(page_title)+'</title>',out,count=1,flags=re.S)
            out=re.sub(r'<meta name="description" content="[^"]*"','<meta name="description" content="'+html.escape(page_desc,quote=True)+'"',out,count=1)
            out=re.sub(r'<link rel="canonical" href="[^"]*">','<link rel="canonical" href="'+url(locale,route)+'">',out,count=1)
            out=re.sub(r'<meta property="og:url" content="[^"]*">','<meta property="og:url" content="'+url(locale,route)+'">',out,count=1)
            out=re.sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="'+html.escape(page_title,quote=True)+'">',out,count=1)
            out=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="'+html.escape(page_desc,quote=True)+'">',out,count=1)
            # Rewrite root-relative-to-page asset paths exactly once for each locale depth.
            depth=len(route.split('/')) if route else 0
            prefix='../'*(depth+1)
            # Asset paths in source HTML are relative to the source route.
            source_prefix='../'*depth if depth else './'
            for attribute in ('href', 'src'):
                out=out.replace(attribute+'="'+source_prefix+'assets/',attribute+'="../'+source_prefix+'assets/')
            out=out.replace('<head>','<head>'+('' if localized else '<meta name="robots" content="noindex,follow">'),1)
            # Only advertise English translations until full body copy is translated.
            if localized:
                out=out.replace('</head>','<link rel="alternate" hreflang="en" href="'+url('en',route)+'"><link rel="alternate" hreflang="x-default" href="'+BASE+(route+'/' if route else '')+'"></head>',1)
            out=out.replace('<body ', '<body data-locale="'+locale+'" ',1)
            target.write_text(out)
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    root=Element('urlset',{'xmlns':ns})
    for route in ROUTES:
        item=SubElement(root,'url')
        SubElement(item,'loc').text=url('en',route)
    (ROOT/'sitemap-i18n.xml').write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+tostring(root,encoding='utf-8'))
if __name__=='__main__':
    build()            # Update JSON-LD to match the actual localized canonical URL and metadata.
            def rewrite_jsonld(match):
                try:
                    data=json.loads(match.group(1))
                    data.update({'name':page_title,'url':url(locale,route),'description':page_desc,'inLanguage':locale})
                    return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
                except (ValueError,TypeError):
                    return match.group(0)
            out=re.sub(r'<script type="application/ld\\+json">(.*?)</script>',rewrite_jsonld,out,flags=re.S)
            # Rebase asset links by one additional locale directory, without double-rewriting.
            depth=len(route.split('/')) if route else 0
            old_prefix='../'*depth if depth else './'
            for attr in ('href','src'):
                out=out.replace(attr+'="'+old_prefix+'assets/',attr+'="../'+old_prefix+'assets/')
            out=out.replace('<head>','<head>'+('' if localized else '<meta name="robots" content="noindex,follow">'),1)
            # Only advertise English translations until full body copy is translated.
            if localized:
                out=out.replace('</head>','<link rel="alternate" hreflang="en" href="'+url('en',route)+'"><link rel="alternate" hreflang="x-default" href="'+BASE+(route+'/' if route else '')+'"></head>',1)
            out=out.replace('<body ', '<body data-locale="'+locale+'" ',1)
            target.write_text(out)
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    root=Element('urlset',{'xmlns':ns})
    for route in ROUTES:
        item=SubElement(root,'url')
        SubElement(item,'loc').text=url('en',route)
    (ROOT/'sitemap-i18n.xml').write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+tostring(root,encoding='utf-8'))
if __name__=='__main__':
    build()
