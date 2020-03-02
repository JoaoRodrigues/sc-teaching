"""
Utility function to write routes as KML files.

Requires simplekml module, available on PyPI.
"""

import simplekml
import math
import pathlib


def route2kml(route, fname):
    """Writes a route as a KML file to visualize in Google Maps."""

    kml = simplekml.Kml()

    for city in route:
        kml.newpoint(
            name=city.name,
            coords=[
                math.degrees(city.lat),
                math.degrees(city.lat)
            ]
        )

     kml.save(fname)
