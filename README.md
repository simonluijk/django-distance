# Django Distance

**Django application to allow looking up objects by distance.**

[![build-status]][travis]

# Overview

OVERVIEW

# Requirements

* Python (2.6, 2.7, 3.3)
* Django (1.5, 1.6)

# Installation

On Debian or Ubuntu install the geos and proj libraries with...

    apt-get install libgeos-c1 proj

Install using `pip`...

    pip install django-distance

If you are using django 1.6+ you will need to install django-localflavor with...

    pip install django-localflavor

Add `'distance'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'distance',
    )

Then run `python manage.py syncdb`

# Import zip data

Import zip data with `python manage.py import_zipdata [path to csv data file]`

You will find two files in the data folder CivicSpace US and GeoPostcodes. The first being a free data-set derived from the US Census 1999, 2000 and 2003. The latter is a sample data-set from http://www.geopostcodes.com/ where you can purchase the full data-set.

# Example usage

Import models and accessories:

    from distance.models import Zip
    from django.contrib.gis.measure import D


Query zip codes within 50 miles:

    myzip = Zip.objects.get(code="94129")
    zips = Zip.objects.within(myzip.location, D(mi=50))

or

    zips = myzip.within(D(mi=50))


Query zip codes between 50 and 100 miles:

    myzip = Zip.objects.get(code="94129")
    zips = Zip.objects.within(myzip.location, D(mi=50), D(mi=100))

or

    zips = myzip.within(D(mi=50), D(mi=100))


# Zip object methods and attr

`Zip.state`
The state the zipcode is within.

`Zip.city`
The city the zipcode is within.

`Zip.distance`
A distance attribute is added to each Zip object when queried using the managers
within method. The attribute indicates the distance in meters.

`Zip.distance_obj`
Wraps the distance attribute in a D (Distance) object.

`Zip.location`
Returns the zip's latitude and longitude as a dict.

`Zip.distance_between(other_zip)`
Returns a D (Distance) object representing the distance between this zip and the
other_zip parsed in.

`Zip.within(distance1, distance2)`
Is a short cut to the managers within method. The method expects either a
D (Distance) object or an int. If passed an int its assumed the measurement is
in meters.

That's it, we're done!

[build-status]: https://secure.travis-ci.org/simonluijk/django-distance.png?branch=master
[travis]: http://travis-ci.org/simonluijk/django-distance?branch=master
