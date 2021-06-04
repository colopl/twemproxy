#!/usr/bin/env python
#coding: utf-8

from .common import *

def _geoadd_common(r):
    return r.geoadd('Sicily',
        13.361389, 38.115556, 'Palermo',
        15.087269,  37.502669 , 'Catania'
    )

def test_geoadd():
    r = getconn()

    assert(_geoadd_common(r) == 2)

    assert(r.geoadd('Sicily',
        13.583333, 37.316667, 'Agrigento') == 1)

    # reply is not changed count but added count
    assert(_geoadd_common(r) == 0)

    assert_fail('value is not a valid float', r.geoadd, 'key', 'invalidValue', 'invalidValue', 'invalidValue');

    assert_fail('invalid longitude,latitude pair', r.geoadd, 'key', 0.0, -85.05112879, 'tooLowLat')

    assert_fail('invalid longitude,latitude pair', r.geoadd, 'key', 0.0, 85.05112879, 'tooHighLat')

    assert_fail('invalid longitude,latitude pair', r.geoadd, 'key', -180.00000001, 0.0, 'tooLowLng')

    assert_fail('invalid longitude,latitude pair', r.geoadd, 'key', 180.00000001, 0.0, 'tooHighLng')


def test_geodist():
    r = getconn()

    _geoadd_common(r)

    assert(r.geodist('Sicily', 'Palermo' , 'Catania') == 166274.1516)

    assert(r.geodist('Sicily', 'Palermo' , 'Catania', 'km') == 166.2742)

    assert(r.geodist('Sicily', 'Palermo' , 'Catania', 'mi') == 103.3182)

    assert(r.geodist('keyNotExists', 'memberNotExists1', 'memberNotExists2') == None)

    assert(r.geodist('Sicily', 'memberNotExists1', 'memberNotExists2') == None)


def test_geohash():
    r = getconn()

    _geoadd_common(r)

    assert(r.geohash('Sicily', 'Palermo' , 'Catania') == ['sqc8b49rny0', 'sqdtr74hyu0'])

    assert(r.geohash('keyNotExists', 'memberNotExists') == [None])

    assert(r.geohash('Sicily', 'memberNotExists') == [None])

    assert(r.geohash('Sicily') == [])


def test_geopos():
    r = getconn()

    _geoadd_common(r)

    assert(r.geopos('Sicily', 'Palermo', 'Catania') == [(13.361389338970184, 38.1155563954963),
        (15.087267458438873, 37.50266842333162)])

    assert(r.geopos('keyNotExists') == [])

    assert(r.geopos('keyNotExists', 'memberNotExists') == [None])

    assert(r.geopos('Sicily') == [])


def test_georadius():
    r = getconn()

    _geoadd_common(r)

    assert_fail('value is not a valid float', r.georadius, 'Sicily', 'invalidValue', 'invalidValue', 'invalidValue')

    assert(r.georadius('keyNotExists', 15, 37, 200, 'km') == [])

    assert(r.georadius('Sicily', 15, 37, 1, 'm') == [])

    assert(r.georadius('Sicily', 15, 37, 200, 'km') == ['Palermo', 'Catania'])

    assert(r.georadius('Sicily', 15, 37, 100000, 'm') == ['Catania'])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', withdist=True) == [
        ['Palermo', 190.4424],
        ['Catania', 56.4413]
    ])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', withcoord=True) == [
        ['Palermo', (13.361389338970184, 38.1155563954963)],
        ['Catania', (15.087267458438873, 37.50266842333162)]
    ])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', withhash=True) == [
        ['Palermo', 3479099956230698],
        ['Catania', 3479447370796909]
    ])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', withdist=True, withcoord=True, withhash=True) == [
        ['Palermo', 190.4424, 3479099956230698, (13.361389338970184, 38.1155563954963)],
        ['Catania', 56.4413, 3479447370796909, (15.087267458438873, 37.50266842333162)]
    ])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', count=1) == ['Catania'])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', count=1, sort='ASC') == ['Catania'])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', count=1, sort='DESC') == ['Palermo'])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', count=3, sort='ASC') == ['Catania', 'Palermo'])

    assert(r.georadius('Sicily', 15, 37, 200, 'km', withdist=True, count=1) == [['Catania', 56.4413]])


def test_georadiusbymember():
    r = getconn()

    r.geoadd('Sicily',
        13.583333, 37.316667, 'Agrigento')
    _geoadd_common(r)

    assert(r.georadiusbymember('keyNotExists', 'memberNotExists', 200, 'km') == [])

    assert_fail('could not decode requested zset member', r.georadiusbymember, 'Sicily', 'memberNotExists', 200, 'km')

    assert(r.georadiusbymember('Sicily', 'Agrigento', 1, 'm') == ['Agrigento'])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km') == ['Agrigento', 'Palermo'])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', withdist=True) == [
        ['Agrigento', 0.0],
        ['Palermo', 90.9778]
    ])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', withcoord=True) == [
        ['Agrigento', (13.583331406116486, 37.316668049938166)],
        ['Palermo', (13.361389338970184, 38.1155563954963)]
    ])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', withhash=True) == [
        ['Agrigento', 3479030013248308],
        ['Palermo', 3479099956230698]
    ])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', withdist=True, withcoord=True, withhash=True) == [
        ['Agrigento', 0.0, 3479030013248308, (13.583331406116486, 37.316668049938166)],
        ['Palermo', 90.9778, 3479099956230698, (13.361389338970184, 38.1155563954963)]
    ])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', count=1) == ['Agrigento'])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', count=1, sort='ASC') == ['Agrigento'])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', count=1, sort='DESC') == ['Palermo'])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', count=3, sort='ASC') == ['Agrigento', 'Palermo'])

    assert(r.georadiusbymember('Sicily', 'Agrigento', 100, 'km', withdist=True, count=1) == [
        ['Agrigento', 0.0]
    ])

