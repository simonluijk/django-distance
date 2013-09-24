from django.test import TestCase
from django.contrib.gis.measure import D
from .models import Zip


class ZipTestCase(TestCase):
    fixtures = ["tests"]

    def setUp(self):
        self.zip = Zip.objects.get(code="0")

    def testZip(self):
        zips = self.zip.within(2000)
        self.assertEquals(len(zips), 2)
        self.assertEquals(zips[1].code, "1")

        zips = self.zip.within(D(m=2000))
        self.assertEquals(len(zips), 2)
        self.assertEquals(zips[1].code, "1")

        zips = self.zip.within(D(m=2000), D(m=4000))
        self.assertEquals(len(zips), 1)
        self.assertEquals(zips[0].code, "2")

        other_zip = Zip.objects.get(code="1")
        self.assertEquals(self.zip.distance_between(other_zip).m,
                          11.008811113204)

        other_zip = Zip.objects.get(code="2")
        self.assertEquals(self.zip.distance_between(other_zip).m,
                          2639.01988429394)
