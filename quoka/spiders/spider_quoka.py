# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest, Request
from datetime import date, timedelta
import string, csv
import urllib, urllib2


class QuokaSpyder(CrawlSpider):
    name = "quoka"
    allowed_domains = ["http://www.quoka.de", "www.quoka.de"]

    start_urls = ["http://www.quoka.de/immobilien/bueros-gewerbeflaechen/"]

    rules = (
        Rule(LinkExtractor(allow=('/bueros-gewerbeflaechen/')), follow=True, callback='parse_start_url'),
        Rule(LinkExtractor(allow=(r'/bueros-gewerbeflaechen/+')), callback='parse_object'),
        Rule(LinkExtractor(allow=('/ajax/')), callback='parse_telefon'),
    )

    def _url(self, url):
        return 'http://www.quoka.de' + url

    def _url_js(self, url):
        return 'http://www.quoka.de/' + url

    def parse_start_url(self, response):
        hrefs = response.css('.item').xpath('@href').extract()

        for href in hrefs:
            yield FormRequest(self._url(href), callback=self.parse_object)

    def parse_object(self, response):
        element = {}
        Inserent = response.css('div.cust-type').xpath('text()').extract()
        Inserent = str(Inserent[0])
        if Inserent == 'Gewerblicher Inserent':
            try:
                telefon_js = response.css('#dspphone1::attr(onclick)').extract()
                if telefon_js:
                    telefon_js = str(telefon_js[0])
                    telefon_js_sr = telefon_js[8:15]
                    if telefon_js_sr != 'Telefon':
                        telefon_js = telefon_js[25:-3]
                    else:
                        telefon_js = telefon_js[27:-3]
                    url_telefon = self._url_js(telefon_js)
                    page = urllib2.urlopen(url_telefon).read()
                    page = page.split('>')
                    page = page[1]
                    page = page.split('<')
                    Telefon = page[0].replace(' ', '')
                else:
                    Telefon = 'None'
            except:
                Telefon = 'None'

            Boersen_ID = '21'
            OBID = response.css('.date-and-clicks strong').xpath('text()').extract()
            OBID = string.rstrip(OBID[0][1:]).encode('utf-8')
            erzeught_am = date.today().strftime('%d.%m.%Y')
            url = response.url

            def extract_element(selector):
                return response.css(selector).xpath('text()').extract_first().encode('utf-8')

            Stadt = extract_element('.locality')
            PLZ = extract_element('.postal-code')
            Uberschrift = extract_element('.headline h2')
            Beschreibung = extract_element('.text')
            try:
                Kaufpreis = extract_element('.price span')
            except:
                Kaufpreis = extract_element('.price strong')
            Monat = date.today().strftime('%m')
            try:
                Erstellungsdatum = response.css('.today').xpath('text()').extract_first()
                if Erstellungsdatum is not None:
                    Erstellungsdatum = date.today().strftime('%d.%m.%Y')
                else:
                    s = 1 / 0
            except:
                datum = response.css('.date-and-clicks').xpath('text()').extract()
                Erstellungsdatum = datum[len(datum) - 2]
                Erstellungsdatum = string.rstrip(Erstellungsdatum)
                if Erstellungsdatum != u'\nGestern':
                    Erstellungsdatum = Erstellungsdatum[1:]
                else:
                    Erstellungsdatum = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')

            Gewerblich = '1'
            Kleinanzeigen_App = response.css('#detailMobileAppHint').extract()
            try:
                Kleinanzeigen_App = Kleinanzeigen_App[0]
                Kleinanzeigen_App = 1
            except:
                Kleinanzeigen_App = 0

            Anbienter_ID = response.css('.btn-mail strong').xpath('text()').extract()
            try:
                Anbienter_ID = Anbienter_ID[0].encode('utf-8')
                Anbienter_ID = ' '
                element.update({'Boersen_ID': Boersen_ID,
                                'OBID': OBID,
                                'erzeught_am': erzeught_am,
                                'Anbienter_ID': Anbienter_ID,
                                'Stadt': Stadt,
                                'PLZ': PLZ,
                                'Uberschrift': Uberschrift,
                                'Beschreibung': Beschreibung,
                                'Kaufpreis': Kaufpreis,
                                'Monat': Monat,
                                'url': url,
                                'Telefon': Telefon,
                                'Erstellungsdatum': Erstellungsdatum,
                                'Kleinanzeigen_App': Kleinanzeigen_App,
                                'Gewerblich': Gewerblich,
                                })

            except:
                Anbienter_ID = 'immobilienscout24.de'
                url1 = response.url
                url = response.css('.btn-mail').xpath('@href').extract()
                url = url[0]
                element.update({'Boersen_ID': '-',
                                'OBID': '-',
                                'erzeught_am': '-',
                                'Anbienter_ID': Anbienter_ID,
                                'Stadt': '-',
                                'PLZ': '-',
                                'Uberschrift': '-',
                                'Beschreibung': url1,
                                'Kaufpreis': '-',
                                'Monat': '-',
                                'url': url,
                                'Telefon': '-',
                                'Erstellungsdatum': '-',
                                'Kleinanzeigen_App': '-',
                                'Gewerblich': '-',
                                })

            with open("/home/tadej/test.csv", 'a') as f:
                names = ['Boersen_ID', 'OBID', 'erzeught_am', 'Anbienter_ID', 'Stadt', 'PLZ', 'Uberschrift',
                         'Beschreibung',
                         'Kaufpreis', 'Monat', 'url', 'Telefon', 'Erstellungsdatum', 'Gewerblich', 'Kleinanzeigen_App']

                writer = csv.DictWriter(f, fieldnames=names)
                writer.writerow(element)
