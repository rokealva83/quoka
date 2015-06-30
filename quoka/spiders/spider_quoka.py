# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from quoka.items import QuokaItem
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
            url = href
            yield FormRequest(self._url(url), callback=self.parse_object)

    def parse_object(self, response):
        resp = response.body
        hxs = HtmlXPathSelector(response)
        item = QuokaItem()
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
        OBID = OBID[0]
        OBID = OBID[1:]
        OBID = string.rstrip(OBID).encode('utf-8')
        erzeught_am = date.today().strftime('%d.%m.%Y')
        Anbienter_ID = ""
        Stadt = response.css('.locality').xpath('text()').extract_first().encode('utf-8')
        PLZ = response.css('.postal-code').xpath('text()').extract_first().encode('utf-8')
        Uberschrift = response.css('.headline h2').xpath('text()').extract_first().encode('utf-8')
        Beschreibung = response.css('.text').xpath('text()').extract_first().encode('utf-8')
        try:
            Kaufpreis = response.css('.price span').xpath('text()').extract_first().encode('utf-8')
        except:
            Kaufpreis = response.css('.price strong').xpath('text()').extract_first().encode('utf-8')
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

        element.update({'Boersen_ID': Boersen_ID})
        element.update({'OBID': OBID})
        element.update({'erzeught_am': erzeught_am})
        element.update({'Anbienter_ID': Anbienter_ID})
        element.update({'Stadt': Stadt})
        element.update({'PLZ': PLZ})
        element.update({'Uberschrift': Uberschrift})
        element.update({'Beschreibung': Beschreibung})
        element.update({'Kaufpreis': Kaufpreis})
        element.update({'Monat': Monat})
        element.update({'url': url})
        element.update({'Telefon': Telefon})
        element.update({'Erstellungsdatum': Erstellungsdatum})
        element.update({'Kleinanzeigen_App': Kleinanzeigen_App})
        element.update({'Gewerblich': Gewerblich})

        file = open("/home/tadej/test.csv", 'a')
        names = ['Boersen_ID', 'OBID', 'erzeught_am', 'Anbienter_ID', 'Stadt', 'PLZ', 'Uberschrift', 'Beschreibung',
                 'Kaufpreis', 'Monat', 'url', 'Telefon', 'Erstellungsdatum', 'Gewerblich', 'Kleinanzeigen_App']

        writer = csv.DictWriter(file, fieldnames=names)
        writer.writerow(element)

