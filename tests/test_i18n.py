#!/usr/bin/env python3
"""Regression checks for generated locale entrypoints and indexing safety."""
import json, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'i18n/locales.json').read_text())
ROUTES=['','products','pricing','industries','integrations','about','contact','demo','help','privacy','terms']+['products/'+p for p in ['pos','kds','ordering','kiosk','reservations','staff','management']]
class LocaleRoutes(unittest.TestCase):
    def test_every_route_and_language(self):
        for locale,info in CFG['locales'].items():
            for route in ROUTES:
                with self.subTest(locale=locale,route=route):
                    path=ROOT/locale/route/'index.html'
                    self.assertTrue(path.is_file(),str(path))
                    text=path.read_text()
                    self.assertIn('lang="'+locale+'"',text)
                    self.assertIn('dir="'+info['dir']+'"',text)
                    self.assertIn('data-locale="'+locale+'"',text)
                    self.assertIn('rel="canonical"',text)
                    self.assertIn('href="'+CFG['baseUrl']+locale+'/'+(route+'/' if route else '')+'"',text)
                    self.assertIn('assets/js/site.js',text)
                    self.assertIn('assets/css/site.css',text)
                    self.assertIn('noindex,follow',text) if locale!='en' else self.assertNotIn('noindex,follow',text)
                    prefix='../'*(len(route.split('/'))+1 if route else 1)
                    self.assertIn(prefix+'assets/css/site.css',text)
    def test_untranslated_locales_not_in_sitemap(self):
        sitemap=(ROOT/'sitemap-i18n.xml').read_text()
        for locale in CFG['locales']:
            if locale!='en':
                self.assertNotIn(CFG['baseUrl']+locale+'/',sitemap)
if __name__=='__main__':
    unittest.main()
