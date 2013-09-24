#-*- coding:utf-8 -*-

import sys
import csv

from django.core.management.base import BaseCommand
from ...models import Zip


def get_key(fl, keys):
    try:
        return u"".join([fl[i] for i in keys])
    except:
        return u"InvalidKey"


def get_data_geopostcodes(row):
    return {
        "code": row[8],
        "city": row[9],
        "state": row[3][3:5],
        "longitude": row[13],
        "latitude": row[12],
    }


def get_data_civicspace(row):
    return {
        "code": row[0],
        "city": row[1],
        "state": row[2],
        "longitude": row[4],
        "latitude": row[3],
    }


class Command(BaseCommand):
    help = "Import zip data"

    def handle(self, *args, **options):
        try:
            file_name = args[0]
        except IndexError:
            print("You must provide a path to the file to import")
            sys.exit()

        csvfile = open(file_name, "rb")
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        fl = reader.next()
        if get_key(fl, [0, 1, 2, 3, 4]) == "zipcitystatelatitudelongitude":
            get_data = get_data_civicspace
        elif get_key(fl, [3, 8, 9, 12, 13]) == "ISO2ZIPCityLatLng":
            get_data = get_data_geopostcodes
        else:
            print("File format not recognosed.")
            sys.exit()

        print("Removing old data.")
        Zip.objects.all().delete()

        print("Importing new data.")
        count = 0
        for row in reader:
            Zip.objects.create(**get_data(row))
            count = count + 1

        print("Import complete. %i zipcodes imported!" % count)
