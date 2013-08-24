# coding: utf-8

"""
Yandex.Maps API wrapper
"""
import json
import urllib
from yandex_maps import http

STATIC_MAPS_URL = 'http://static-maps.yandex.ru/1.x/?'
HOSTED_MAPS_URL = 'http://maps.yandex.ru/?'
GEOCODE_URL = 'http://geocode-maps.yandex.ru/1.x/?'


def _format_point(longitude, latitude):
    return '%0.7f,%0.7f' % (float(longitude), float(latitude),)


def get_map_url(longitude, latitude, zoom, width, height):
    """ returns URL of static yandex map """
    point = _format_point(longitude, latitude)
    params = [
        'll=%s' % point,
        'size=%d,%d' % (width, height,),
        'z=%d' % zoom,
        'l=map',
        'pt=%s' % point
    ]
    return STATIC_MAPS_URL + '&'.join(params)


def get_external_map_url(longitude, latitude, zoom=14):
    """ returns URL of hosted yandex map """
    point = _format_point(longitude, latitude)
    params = dict(
        ll=point,
        pt=point,
        l='map',
    )
    if zoom is not None:
        params['z'] = zoom
    return HOSTED_MAPS_URL + urllib.urlencode(params)


def geocode(address, timeout=2):
    """ returns (longtitude, latitude,) tuple for given address """
    try:
        json_data = _get_geocode_json(address, timeout)
        return _get_coords(json_data)
    except IOError:
        return None, None


def _get_geocode_json(address, timeout=2):
    url = _get_geocode_url(address)
    status_code, response = http.request('GET', url, timeout=timeout)
    return response


def _get_geocode_url(address):
    if isinstance(address, unicode):
        address = address.encode('utf8')
    params = urllib.urlencode({'geocode': address, 'format': 'json', 'results': 1})
    return GEOCODE_URL + params


def _get_coords(response):
    try:
        geocode_data = json.loads(response)
        pos_data = geocode_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return tuple(pos_data.split())
    except (IndexError, KeyError):
        return None, None