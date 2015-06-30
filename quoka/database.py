# -*- coding: utf-8 -*-

from datetime import date
from sqlalchemy import Table, Column, Integer, String

date_prefix = date.today().strftime('%Y%m')

table_name = '%s_maklerempfehlung_anbieter' % date_prefix
anbieter_table = Table(table_name,
                       Column('id', Integer),
                       Column('Boersen_ID', String(45)),
                       Column('OBID', String(45)),
                       Column('Anbieter_ID', String(100), unique=True),
                       Column('Stadt', String(150)),
                       Column('PLZ', String(10)),
                       Column('Uberschrift', String(100)),
                       Column('Beschreibung', String(45)),
                       Column('Telefon', String(100)),
                       Column('Monat', String(45)),
                       Column('url', String(200)),
                       Column('Erstellungsdatum', String(1)),
                       Column('Gewerblich', String(8)),
                       Column('Kleinanzeigen_App', String(8)),
                       Column('erzeught_am', String(100)),
                       Column('Kaufpreis', String(100)),
                       )
