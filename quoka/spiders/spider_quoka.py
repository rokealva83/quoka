# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from datetime import date, timedelta
import string, csv
import urllib2


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

    def parse_start_url(self, response):
        hrefs = response.css('.item').xpath('@href').extract()

        for href in hrefs:
            yield FormRequest(self._url(href), callback=self.parse_object)

    def parse_object(self, response):
        element = {}
        try:
            java = response.css('#dspphone1::attr(onclick)').extract()
            if java:
                java = str(java[0])
                java_sr = java[8:15]
                if java_sr != 'Telefon':
                    java = java[25:-3]
                else:
                    java = java[27:-3]
                url_telefon = self._url(java)
                page = urllib2.urlopen(url_telefon).read()
                page = page.split('>')
                page = page[1]
                page = page.split('<')
                Telefon = page[0]
            else:
                Telefon = ''
        except:
            Telefon = ''

        Boersen_ID = '21'
        OBID = response.css('.date-and-clicks strong').xpath('text()').extract()
        OBID = string.rstrip(OBID[0][1:]).encode('utf-8')
        erzeught_am = date.today().strftime('%d.%m.%Y')
        Anbienter_ID = ""
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
        url = response.url
        try:
            Erstellungsdatum = response.css('.today').xpath('text()').extract_first()
            if Erstellungsdatum is not None:
                Erstellungsdatum = date.today().strftime('%d.%m.%Y')
            else:
                s = 1/0
        except:
            datum = response.css('.date-and-clicks').xpath('text()').extract()
            Erstellungsdatum = datum[len(datum) - 2]
            Erstellungsdatum = string.rstrip(Erstellungsdatum)
            if Erstellungsdatum != u'\nGestern':
                Erstellungsdatum = Erstellungsdatum[1:]
            else:
                Erstellungsdatum = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')

        Gewerblich = ""
        Kleinanzeigen_App = ""

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

        with open("/home/tadej/test.csv", 'a') as f:
            names = ['Boersen_ID', 'OBID', 'erzeught_am', 'Anbienter_ID', 'Stadt', 'PLZ', 'Uberschrift', 'Beschreibung',
                     'Kaufpreis', 'Monat', 'url', 'Telefon', 'Erstellungsdatum', 'Gewerblich', 'Kleinanzeigen_App']
    
            writer = csv.DictWriter(f, fieldnames=names)
            writer.writerow(element)

