#-*- coding:utf-8 -*-

from django.db import models
from django.db.models.sql.aggregates import Aggregate
from django.contrib.gis.measure import D

try:
    from localflavor.us.models import USStateField
except ImportError:
    from django.contrib.localflavor.us.models import USStateField


class Distance(Aggregate):
    is_computed = True
    sql_function = None
    sql_template = ("6371000 * acos( cos( radians(%(lat)f) ) * "
                    "cos( radians( %(field_lat)s ) ) * "
                    "cos( radians( %(field_long)s ) - radians(%(long)f) ) + "
                    "sin( radians(%(lat)f) ) * "
                    "sin( radians( %(field_lat)s ) ) )")

    def __init__(self, pnt, **extra):
        self.lookup = "id"
        extra.update({"long": pnt["longitude"],
                      "lat": pnt["latitude"]})
        self.extra = extra

    def _default_alias(self):
        return '%s__%s' % (self.lookup, self.__class__.__name__.lower())
    default_alias = property(_default_alias)

    def add_to_query(self, query, alias, col, source, is_summary):
        super(Distance, self).__init__(col, source, is_summary, **self.extra)
        query.aggregate_select[alias] = self

    def as_sql(self, qn, connection):
        table = self.col[0]
        self.extra.update({
            "field_lat": '.'.join([qn(table), qn("latitude")]),
            "field_long": '.'.join([qn(table), qn("longitude")])
        })

        return super(Distance, self).as_sql(qn, connection)


class DistanceQuerySet(models.query.QuerySet):
    def distance(self, pnt):
        return self.annotate(distance=Distance(pnt))

    def within(self, pnt, distance1, distance2=None):
        qs = self.distance(pnt)

        if not isinstance(distance1, D):
            distance1 = D(m=distance1)

        if distance2:
            if not isinstance(distance2, D):
                distance2 = D(m=distance2)
            qs = qs.filter(distance__lte=distance2.m,
                           distance__gte=distance1.m)
        else:
            qs = qs.filter(distance__lte=distance1.m)

        return qs.order_by("distance")


class DistanceManager(models.Manager):
    def get_queryset(self):
        return DistanceQuerySet(self.model)

    def distance(self, *args, **kwargs):
        return self.get_queryset().distance(*args, **kwargs)

    def within(self, *args, **kwargs):
        return self.get_queryset().within(*args, **kwargs)


class DistanceAbstractModel(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    distance = DistanceManager()

    class Meta:
        abstract = True

    @property
    def location(self):
        return {"longitude": self.longitude, "latitude": self.latitude}

    @location.setter
    def location(self, location):
        self.latitude = location['latitude']
        self.longitude = location['longitude']

    def set_location(self, zip_code):
        self.location = Zip.objects.get(code=zip_code).location

    @property
    def distance_obj(self):
        return D(m=self.distance)

    def distance_between(self, other):
        otherzip = Zip.distance.distance(self.location).get(pk=other.pk)
        return D(m=otherzip.distance)

    def within(self, distance1, distance2=None):
        return Zip.distance.within(self.location, distance1, distance2)


class Zip(DistanceAbstractModel):
    code = models.CharField("Zip", max_length=5)
    city = models.CharField("City", max_length=128)
    state = USStateField("State")

    objects = models.Manager()

    class Meta:
        ordering = ["code"]

    def __unicode__(self):
        return "%s: %s" % (self.state, self.code)
