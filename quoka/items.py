# -*- coding: utf-8 -*-


from scrapy.item import Item, Field


class QuokaItem(Item):
    id = Field()
    Boersen_ID = Field()
    OBID = Field()
    erzeught_am = Field()
    Anbienter_ID = Field()
    Stadt = Field()
    PLZ = Field()
    Uberschrift = Field()
    Beschreibung = Field()
    Kaufpreis = Field()
    Monat = Field()
    url = Field()
    Telefon = Field()
    Erstellungsdatum = Field()
    Gewerblich = Field()
    Kleinanzeigen_App = Field()
