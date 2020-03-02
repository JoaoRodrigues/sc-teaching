"""
Road Trip Planner written in Python!

Uses a database of geographical locations to plan a trip between two cities,
perhaps not very efficiently, but surely more interestingly than Google Maps!

Authors:
	Joao Rodrigues (joaor@stanford.edu)
"""

import argparse
import csv
from dataclasses import dataclass
import logging
import math
import pathlib


@dataclass(unsafe_hash=True)
class City:
    name: str
    state: str
    lat: float
    lon: float
    
    def distance_to(self, other):
        """Returns the distance in km between city and other.
        
        Uses the Haversine formulate to calculate distances between
        points on a sphere.
        
        Args:
           other (City): a city dataclass to calculate the distance to.
        """
        
        lat_i, lon_i = self.lat, self.lon
        lat_j, lon_j = other.lat, other.lon

        # Haversine formula for distances between points on a sphere
        # https://en.wikipedia.org/wiki/Haversine_formula
        dlat = lat_j - lat_i
        dlon = lon_j - lon_i

        a = (
            (math.sin(dlat/2) * math.sin(dlat/2)) + \
            math.cos(lat_i) * math.cos(lat_j) * \
            (math.sin(dlon/2) * math.sin(dlon/2))
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = 6373  * c  # R is 'a' radius of earth

        return d

    def find_neighbors(self, candidates, radius):
        """Returns all cities in candidates within radius of self.
        
        Args:
            candidates (list): list of City objects.
            radius (float): distance cutoff to consider a City a neighbor
        """
        
        for city in candidates:
            if self.distance_to(city) <= radius:
                yield city


def read_input():
    """Parses and validates the command-line options provided by the user.
    """
    
    ap = argparse.ArgumentParser(
    	description=__doc__,
    	formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Mandatory Arguments
    ap.add_argument(
        'database',
        help='Path to file containing the database of possible cities'
    )
    ap.add_argument(
        'start',
        help='Starting point of the route (e.g. "San Francisco, CA")'
    )
    ap.add_argument(
        'finish',
        help='End point of the route (e.g. "Boston, MA")'
    )
    
    # Optional Arguments
    ap.add_argument(
        '--stop',
        type=str,
        action='append',
        help='Additional stops along the route. One per invocation.'
    )
    ap.add_argument(
        '-r',
        '--km-per-day',
        type=float,
        default=200.0,
        help='Rate of travel, in maximum km travelled per day (def: 200.0)'
    )

    ap.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enables debugging messages when running the program.'
    )
    
    return ap.parse_args()
    

def create_database(db_fpath):
    """Reads and creates a database of cities.
    
    Args:
        db_fpath (str): path to the database file on disk.
    """
    
    city_db = {}
    
    path = pathlib.Path(db_fpath)

    with path.open('r') as db_file:
        for line_idx, line in enumerate(csv.reader(db_file), start=1):
            try:
                name, *_, state_code, lat, lon = line
                lat, lon = math.radians(float(lat)), math.radians(float(lon))
            except Exception as err:
                logging.warning(f'Error parsing line {line_idx}: {err}')
                continue
            else:
                city = City(
                    name,
                    state_code,
                    lat,
                    lon
                )
                logging.debug(f'Added city: {city.name}, {city.state}')

                city_db[(name, state_code)] = city

    logging.info(f'Read {len(city_db)} cities into a database')
    return city_db


def find_city_in_db(database, query):
    """Returns a City matching the query from the database.
    
    Args:
        database (dict): dictionary of City objects.
        query (str): city information as "Name, State".
    """
    
    try:
        name, state = map(str.strip, query.split(','))
        city = database[(name, state)]
    except KeyError:
        emsg = f'Query city "{name}, {state}" not found in database'
        raise KeyError(emsg) from None

    logging.info(f'Matched {city.name}, {city.state} to database')
    return city


def validate_cities(database, args):
    """Validates input cities against a database.
    
    Args:
        database (dict): dictionary of City objects.
        args (namespace): parsed arguments, as an argparse.NameSpace object.
    """
    
    args.start = find_city_in_db(database, args.start)
    args.finish = find_city_in_db(database, args.finish)


def find_route(database, start, finish, km_per_day):
    """Finds the shortest path between two cities.
    
    Args:
        database (dict): collection of possible stops encoded as 
            City objects.
        start (City): first city on the route, as a City object.
        finish (City): last city on the route, as a City object.
        km_per_day (float): maximum distance travelled per day.
    """
    
    route = [start]
    visited = set(route)
    list_of_cities = list(database.values())
    distance_to_end = lambda city: city.distance_to(finish)
    
    current = start
    while current != finish:
        neighbors = current.find_neighbors(list_of_cities, km_per_day)
        sorted_neighbors = sorted(neighbors, key=distance_to_end)
        for city in sorted_neighbors:
            if city not in visited:
                current = city
                break
        else:
            emsg = (
                f'Could not find viable route after stop #{len(route)}: '
                f' {current.name}, {current.state}'
            )
            raise Exception(emsg)

        route.append(current)
        visited.add(current)

        logging.debug(
            f'Added {current.name}, {current.state} to route'
        )
        logging.debug(
            f'Distance to end: {current.distance_to(finish):5.2f} km'
        )
        
    return route


def write_route(route):
    """Outputs a route to the screen.
    
    Args:
        route (list): list of City objects.
    """
    
    for stop_idx, city in enumerate(route):
        print(f'[Day {stop_idx}] {city.name}, {city.state}')



def setup_logging(verbose):
    """Creates a logger object to relay messages to users.
    
    Args:
        verbose (bool): if True, sets the default logging level
            to DEBUG. Otherwise, it's set to INFO.
    """
    
    # Setup the logger
    
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=log_level
    )


if __name__ == '__main__':
    args = read_input()
    setup_logging(args.verbose)
    db = create_database(args.database)
    validate_cities(db, args)
    route = find_route(
        db,
        args.start,
        args.finish,
        args.km_per_day
    )
    write_route(route)