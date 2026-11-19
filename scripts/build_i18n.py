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
            page_title=info['title'] if not route else title
            page_desc=info['description'] if not route else description
            out=src.replace('<html lang="en"','<html lang="'+locale+'" dir="'+info['dir']+'"',1)
            out=re.sub(r'data-base="[^"]+"','data-base="'+('../'*(len(route.split('/')) if route else 0)+'../')+'"',out,count=1)
            out=re.sub(r'<title>.*?</title>','<title>'+html.escape(page_title)+'</title>',out,count=1,flags=re.S)
            out=re.sub(r'<meta name="description" content="[^"]*"','<meta name="description" content="'+html.escape(page_desc,quote=True)+'"',out,count=1)
            out=re.sub(r'<link rel="canonical" href="[^"]*">','<link rel="canonical" href="'+url(locale,route)+'">',out,count=1)
            out=re.sub(r'<meta property="og:url" content="[^"]*">','<meta property="og:url" content="'+url(locale,route)+'">',out,count=1)
            out=re.sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="'+html.escape(page_title,quote=True)+'">',out,count=1)
            out=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="'+html.escape(page_desc,quote=True)+'">',out,count=1)
            out=re.sub(r'(<script defer src=")[^"]+(/assets/js/site.js")',lambda m:m.group(1)+('../'*(len(route.split('/')) if route else 0)+'../').replace('//','/')+'assets/js/site.js"',out)
            out=re.sub(r'(<link rel="stylesheet" href=")[^"]+(/assets/css/site.css")',lambda m:m.group(1)+('../'*(len(route.split('/')) if route else 0)+'../')+'assets/css/site.css"',out)
            # Keep all relative assets pointing to the repository root.
            depth=len(route.split('/')) if route else 0
            prefix='../'*(depth+1)
            out=re.sub(r'(href|src)="((?:\.\./)+|\./)(assets/)',lambda m:m.group(1)+'="'+prefix+m.group(3),out)
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
