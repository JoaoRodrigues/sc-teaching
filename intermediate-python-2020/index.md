# Intermediate Python Workshop

### Description

This Python workshop aims to familiarize participants with conventions and features of the language that are not necessarily covered in introductory courses, but that are nonetheless common in daily Python programming. In 3 hours, we will work together and write a Python script that plans a road trip through the USA, from scratch, using our wits, some help from Wikipedia, and a database of US cities (adapted from [here](https://simplemaps.com/data/us-cities)).

### What to expect from the workshop?

Ideally, you will leave this workshop knowing a little bit more about Python than when you came in! Python has a fairly rich standard library that is often overlooked by beginners, so we will explore some of those modules ([see a complete list here](https://docs.python.org/3/library/)). The goal is to equip you with knowledge to tackle programming problems more efficiently.

We will not make use of any third-party libraries, so _pandas_, _numpy_, and others are out of scope of this course. We will also not delve into more 'advanced' topics such as object-oriented programming (e.g. classes), profiling, or unit testing. While important, we consider those to require a little more experience with the language.

### What should I know already?

Participants should have taken an introductory course in Python before, and should be comfortable with the basic of the language. In short, this means we expect you to know how to declare variables, distinguish a string from an integer, and how to write a for-loop and if-statements. If you know how to declare functions, awesome, but we will cover that in the first few minutes of the course anyway.

### Software Requirements

This workshop is designed to run on _any_ Python installation, versions 3.7 and above. If you haven't updated to 3.7, high-time to do it! We recommend installing the latest [Miniconda](https://docs.conda.io/en/latest/miniconda.html) distribution since it allows you to use environments and easily install additional packages. 

We will make use of the terminal and a text editor, not Jupyter notebooks. For an editor, I recommend downloading [Sublime Text](https://www.sublimetext.com/). Terminal choices depend on your operative system. Mac OS and Linux users are lucky in that they already have one pre-installed. For Windows users, you can simply use the Anaconda Prompt, or for a more fully-featured terminal, I recommend installing the full version of [Cmder](https://cmder.net/). All terminal examples throughout the tutorial will assume a bash (or equivalent) shell as found in Linux/Mac OS.



# Ready? Let's go!



### PART 0: Planning a Road Trip!

Google Maps revolutionized how we plan our car trips. It makes it simple to define a route between points A and B and check what is the fastest (or shortest) option. The program we will write today performs a similar task. Given two points, trace a route between them. However, instead of knowing all the roads in the US, we will work with the knowledge of all towns in the US. Our route planner will therefore trace a route that hops from city to city, until we reach our destination. This will be slightly less efficient than Google Maps, but maybe it'll make for more exciting trips!

To begin, we need a database of US cities and their coordinates, which we made available [here](intermediate-python-workshop.tar.gz). We also included a smaller dataset, covering cities and towns in California only. Download the 
compressed archive to the Downloads folder of your computer and unpack it. It should create a folder called `intermediate-python-workshop` that contains two `.csv` files. In your terminal, move to this folder.

```bash
$ cd ~/Downloads
$ tar -xzvf intermediate-python-workshop.tar.gz
$ cd intermediate-python-workshop
```

Then, create an empty Python file that will be your program - let's call it `route_planner.py` - and open it with your favorite editor (e.g. Sublime Text).

### PART I: Modularity, or Breaking Your Programs into Functions

Much like when starting to write a thesis or a paper, it can be daunting to stare at an open, empty, editor waiting to write the first line of code of what will eventually be your program. In either case, it usually helps to start by making an outline. A simple way to create such an outline in Python is to write the logical steps of a program as functions. Answer the following questions:

1. What input will my program need?
2. What output do I want it to produce?
3. What are the steps that go from reading the input, to writing the output?

For our route planner program, we (1) need the start and end points of the route, as well as a database of cities and (2) we want it to produce a route, if possible. Let's write these and some intermediate steps as function stubs in our `route_planner.py` file, along with some very basic documentation:

```python
"""
Road Trip Planner written in Python!

Uses a database of geographical locations to plan a trip between two cities,
perhaps not very efficiently, but surely more interestingly than Google Maps!

Authors:
	Joao Rodrigues (joaor@stanford.edu)
"""


def read_input():
    pass


def create_database():
    pass


def find_route():
    pass


def write_route():
    pass


if __name__ == '__main__':
    read_input()
    create_database()
    find_route()
    write_route()
```

The first lines of the script are a special string, enclosed in triple quotes, known as a docstring. You should use them to tell your users what the program is about, and what they can expect from it. As we will see later, there is no point in being overly descriptive in here about how to _run_ the program and what all the options are. You can also include information about the authors and how users can contact them.

Then, we define our logical steps as functions. For readability, try giving your code some room to breathe by having two empty lines before and after the function definition. Note also that function names should, as per Python conventions, be written in lowercase characters and have different words separated by underscores. Their purpose should also be explicit from the name (e.g. `find_route` vs `route`).

Separating code in functions serves three purposes. First, it becomes more readable. The bottom of the script reads like English. Second, code defined as a function can be reused. This reuse can be within the same script - you can call a function multiple times - but also between scripts, through the import mechanism. While outside the scope of this workshop, keep in mind that scripts can act as 'containers' for functions to be reused in multiple other scripts. Third, sometimes, depending on how you write your code, keeping code inside functions makes it run a bit faster.

The `if __name__ == '__main__'` statement is a special line that you see often in scripts. The statement will be true, and its contents executed, only if the script is being called directly, e.g. `python route_planner.py`, but not if it is being imported as a module, e.g. `import route_planner`.

### Part II: Reading Input from the Command Line

Now that we have an overall structure defined for our program, let's fill in the blanks, starting with our first function: `read_input`. 

Reading _things_ from the command line in Python can be puzzling at first, but luckily there are a few modules in the standard library that make it a breeze! Unless you have a specific reason not to, I recommend defaulting to [argparse](https://docs.python.org/3/library/argparse.html). So, before anything else, let's import the module. Import statements should always come at the top of the script, after the docstring, an should be in alphabetical order:

```python
import argparse
```

Now let's think about exactly what input do we need from our users. We need to know where the database of cities is, we need to know where to start our trip, and we need to know where to end it. Optionally, can also let them change how much they want to travel per day. Let's see how we code all this using `argparse`.

```python
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
        '-r',
        '--km-per-day',
        type=float,
        default=200.0,
        help='Rate of travel, in maximum km travelled per day (def: 200.0)'
    )
    
    return ap.parse_args()
```

Before diving into the nitty gritty details of the code, run the script.

```bash
$ python route_planner.py
usage: route_planner.py [-h] [-r KM_PER_DAY]
                        database start finish
```

Automatically, importing `argparse` and setting up a couple of options creates a short description that tells users how to run your program, which arguments are mandatory, and which options there are. Also, we did not define a `-h` option, which is the usual _help_ flag in Linux programs, but it seems that our program supports it. Let's see what happens:

```bash
$ python route_planner.py -h
usage: route_planner.py [-h] [-r KM_PER_DAY]
                        database start finish

Road Trip Planner written in Python!

Uses a database of geographical locations to plan a trip between two cities,
perhaps not very efficiently, but surely more interestingly than Google Maps!

Authors:
        Joao Rodrigues (joaor@stanford.edu)

positional arguments:
  database              Path to file containing the database of possible
                        cities
  start                 Starting point of the route (e.g. "San Francisco, CA")
  finish                End point of the route (e.g. "Boston, MA")

optional arguments:
  -h, --help            show this help message and exit
  -r KM_PER_DAY, --km-per-day KM_PER_DAY
                        Rate of travel, in maximum km travelled per day (def:
                        200.0)
```

Fantastic! From the list of arguments we defined, `argparse` compiles a very verbose help text, listing mandatory (or positional) and optional arguments, their flags, along with the description we wrote in our program's docstring.

Now let's dive into the code to understand how we got here. Building arguments requires building an argument parser, which Python provides through`argparse.ArgumentParser`. Of the many optional arguments the class constructor has, we used two: `description` sets the text that shows up at the top when you do `-h`. Then, we defined `formatter_class=argparse.RawDescriptionHelpFormatter` so that the line breaks in our showed up properly in the help text. 

With the parser defined, all we have to do is to add arguments to it. The simplest syntax to specify arguments is:

```python
parser.add_argument(
    'name',
)
```

where `'name'` is the actual name that the argument is going to have in our code. If the name starts with one or more `-`, then the argument is optional. Optional arguments can have a short name and a long name, specified with `-X` and `--xxxxx` respectively. The short name should be only a couple of letters long. See the example in our code, `-r` stands for radius, and its long name is `--km-per-day`. 

When defining arguments, you can also pass a number of options. For instance, a `help` text, for the formatter to use when you call `script.py -h`. Other common options are:

* `type`, which defines the type of the variable we are expecting. If you use `type=float`, then the parser will try to coerce the value you passed to a float. 
* `default`, which lets you assign a value to the option in case the user did not specify it.

Finally, when you are done, you call `parser.parse_args()`, which returns a special namespace object that acts like a dictionary with all your arguments and options. You can access each of the arguments by their (long) name, as attributes of the namespace object (e.g. `args.km_per_day`). Note that dashes get converted to underscores.

In our code, we return this object directly as the result of our `read_input` function and then assign it to a variable. Our main script loop now looks like this:

```python
if __name__ == '__main__':
    args = read_input()
    create_database()
    find_route()
    write_route()
```

### Part III: Reading CSV Files the Lazy Way with Context Managers, Pathlib, and the CSV module.

Perhaps the most important part of our program is the database of cities. We need it to know which cities are close enough to each other in order to trace a route from point A to point B. In the folder you downloaded, there are two such databases, one for California and one for the entire USA, stored as comma-separated value (csv) files. It is obvious that we must read one of these files and store it in a way that we can use the information within to build our route. Let's focus on the first part, reading the file.

Reading (or writing) file in Python is done with the `open` function, which returns a _file object_. These file objects have methods such as `read()` or `readline()` that fetch the contents of the file, in bulk or one line at a time. Alternatively, because file objects act as iterators, you can also simply loop through them as if they were a list, getting one line for each iteration.

The obvious argument to the `open` function is the path to the file we want to read from or write to. Python 3.4 introduced [pathlib](https://docs.python.org/3/library/pathlib.html), a module that simplified handling paths across different operating systems. In addition, Path objects support opening/closing operations. Combined with the [with](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) statement, a manager to handle opening/closing the underlying file object, opening and reading files in a safe and cross-platform way boils down to a couple of lines.

Let's use `pathlib` and `with` to open our database file in our `create_database` function. Start by importing `pathlib` at the top of the file, keeping in mind that imports should be listed alphabetically:

```python
import argparse
import pathlib
```

Now on to our function:

```python
def create_database(db_fpath):
    """Reads and creates a database of cities.
    
    Args:
    	db_fpath (str): path to the database file on disk.
    """
    
    path = pathlib.Path(db_fpath)
        
    with path.open('r') as db_file:
        for line in db_file:
            print(line)
```

And finally, passing the path to the database file as read by our `read_cli` function, to the function:

```python
if __name__ == '__main__':
    args = read_input()
    create_database(args.database)
```

Executing our route planner should now print the contents of the database file we picked as input. We could then extend our function to parse the contents of each line and start building our database. However, since CSV is a pretty common format, the Python standard library includes a module to help us! The [csv](https://docs.python.org/3/library/csv.html) module includes a `reader` function that takes a file object and returns the contents of each line as a list. Why should we bother using it instead of writing our own code to parse the file? Because likely, this code has been battle-tested by thousands of people. It might not be the fastest option, but it's the most robust. Besides, it's super readable and readability counts! 

Our `create_database` function looks like this:

```python
import argparse
import csv
import pathlib

...

def create_database(db_fpath):
    """Reads and creates a database of cities.
    
    Args:
    	db_fpath (str): path to the database file on disk.
    """
    
    path = pathlib.Path(db_fpath)
        
    with path.open('r') as db_file:
        for line in csv.reader(db_file):
            print(line)
```

### Part IV: Picking the Right Data Structure

Our skeleton code is able to read our database file, given input from the user. But to use the information in the database to plan our route, we have to turn it into something else. Let's think about what we need to plan routes. We have starting and end points, given as combinations of city names and states. We will trace our route by jumping from city to city, so we need to be able to search which cities are close to each other. 

As such, we need to have a data structure that, first of all, stores each city's information, such as name, state, and coordinates. We could use lists or tuples, but we'd have to remember the index of each field (what was the state again? 2nd or 3rd?). We could use dictionaries, so that we could query `city['state']`. But dictionaries are 1) mutable, meaning we (or someone) could corrupt our database while the program is running and 2) they are somewhat heavy in terms of memory.

Python has a [collections](https://docs.python.org/3/library/collections.html) module that stores additional _container_ data types, which is what we want. In particular, there is a `namedtuple` class that looks like a tuple, acts like a tuple, but its fields can be accessed by their name: e.g. `namedtuple.field`. Isn't that neat?

Let's write some code to understand them better:

```python
import argparse
import collections
import csv
import pathlib 
```

```python
City = collections.namedtuple(
    'City',
    [
        'name',
        'state',
        'lat',
        'lon'
    ]
)
```

```python
def create_database(db_fpath):
    """Reads and creates a database of cities.
    
    Args:
    	db_fpath (str): path to the database file on disk.
    """
    
    path = pathlib.Path(db_fpath)

    with path.open('r') as db_file:
        for line in csv.reader(db_file):
            name, *_, state_code, lat, lon = line
            lat, lon = float(lat), float(lon)
            city = City(
                name,
                state_code,
                lat,
                lon
            )
            print(city)
```

Now we need to find a way to store cities so that they are searchable. Here, dictionaries are the perfect data structure. Unlike lists, dictionaries are blazingly fast at retrieving their members. We just need to decide what will be the key for each city. Looking at our input function, a combination of name and state seems to suffice: `"San Francisco, CA" is a simple enough input for our users that we can easily translate into a searchable query. Let's implement that:

```python
def create_database(db_fpath):
    """Reads and creates a database of cities.
    
    Args:
    	db_fpath (str): path to the database file on disk.
    """
    
    city_db = {}
    
    path = pathlib.Path(db_fpath)

    with path.open('r') as db_file:
        for line in csv.reader(db_file):
            name, *_, state_code, lat, lon = line
            lat, lon = float(lat), float(lon)
            city = City(
                name,
                state_code,
                lat,
                lon
            )

            city_db[(name, state_code)] = city

    return city_db
```

And our main loop now looks like:

```python
if __name__ == '__main__':
    args = read_input()
    db = create_database(args.database)
    find_route()
    write_route()
```

### Part V: Gracefully Handling Errors

In an ideal world, datasets will not have errors. Someone has gone through them and magically cleaned them up so that our parsers read them perfectly every single time. In the real world, this _never_ happens, or you should assume so anyway. Enter error handling. Sometimes, you don't want your program to come to halt (3 hours after it started running ...) because of some minor error you can bypass or work around. Also, you might want to write your own error messages to make the problem clearer to your users.

Python includes a very powerful [try/except](https://docs.python.org/3/tutorial/errors.html) construct to _catch_ errors (or exceptions) and do something about it. We can define what type of exceptions we want to catch, or use a catch-all `Exception`. Whenever the code inside the `try` block raises an exception, Python checks if there is a matching `except` statement and if so, executes that code. You can think of it like an if-statement, but for errors: _if this code gives this error, do this_. As with if-statements, `try/except` blocks also have an `else` condition, that runs whenever the code did _not_ raise an exception.

Most importantly, you must resist the temptation to wrap your entire program in super generic `try/except` blocks to avoid __any__ errors! Use them only when you can predict with confidence that some lines can be problematic and you can provide a very obvious workaround for it. Let's see some code:

```python
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
                lat, lon = float(lat), float(lon)
            except Exception as err:
                continue
            else:
                city = City(
                    name,
                    state_code,
                    lat,
                    lon
                )

                city_db[(name, state_code)] = city

    return city_db
```

Running this on our input files will not give us any trouble. But try changing any line in the CSV file (maybe make a copy first!), such as adding letters to the lat/lon fields, adding an empty line, etc and then re-run the program. Our program will now notice the glitch, ignore that line, and keep going through the rest of the file. We might lose some data in the dataset, but we accept that!

### Part VI: Logging, f-strings, and keeping our users awake!

Part of writing computer programs is _user interface_ design. A command-line interface, like the one we have for this route planner, _is_ a user interface so we must think carefully about how we interact with our users.  An important aspect of interface design is keeping users informed of what programs are up to - logging. Most people do some sort of logging with `print` statements, and that's OK for small programs. But what if you want to start categorizing messages based on importance? Some stuff is debug information only, while other stuff you really want your users to know!

Python ships with a [logging](https://docs.python.org/3/library/logging.html) module that makes this task simple. In a simple example like this, we start by setting up the general logger, including the message format and the base logging level, and then we make calls to this logger when we need to write something to the screen.

The messages we pass to the logger are simple strings, but we can augment them with some information about the state of the program (variable information) using [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings). F-strings are just one of many way of formatting strings in Python, but we prefer them for their terseness and ability to execute logic. You define an f-string by prefixing any string with an _f_ and then include variables, or expressions, inside curly braces: e.g. `f'Hello {name}'` will print `Hello` followed by whatever the contents of the variable `name`. We can also write small pieces of logic inside the curly braces, for example to print the length of a list: `f'List has {len(my_list)} elements'`.

Let's write a logging facility for our program, starting by integrating it with our `read_cli` function to allow users to define how much verbosity they want.

```python
import argparse
import collections
import csv
import logging
import pathlib
```

```python
def read_input():
    """Parses and validates the command-line options provided by the user.
    """
    
    ap = argparse.ArgumentParser(
    	description=__doc__,
    	formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Mandatory Arguments
    ...
    
    # Optional Arguments
    ...
    
    ap.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enables debugging messages when running the program.'
    )
    
    return ap.parse_args()
```

We add a new function to setup the logger:

```python
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
```

And now we add messages to our database function. 

```python
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
                lat, lon = float(lat), float(lon)
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
```

### Part VII: Querying the database

Before we proceed, we must ensure our beginning and end points of the route are in the database. Since we encoded the database as a dictionary, this is extremely easy to do! Let's write a separate function that takes the cities as we parsed them with `argparse` and tries to return the corresponding City object.

```python
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
```

Now we can write a second function that takes the `argparse` namespace object as input and validates the `start` and `finish` options:

```python
def validate_cities(database, args):
    """Validates input cities against a database.
    
    Args:
        database (dict): dictionary of City objects.
        args (namespace): parsed arguments, as an argparse.NameSpace object.
    """
    
    args.start = find_city_in_db(database, args.start)
    args.finish = find_city_in_db(database, args.finish)
```

And integrating it in our code, the main loop looks like:

```python
if __name__ == '__main__':
    args = read_input()
    setup_logging(args.verbose)
    db = create_database(args.database)
    validate_cities(db, args)
    find_route()
    write_route()
```

### Part VIII: Doing heavy math the simple (and fast) way.

We are almost ready to write the heart of our program: the route finding algorithm! For this, we will take a simple approach. For a city, we find all other cities within a radius (the value of `--km-per-day`) and then pick the neighbor that is closest to the end point. In order to do this, we need to calculate distances between cities. Let's write a function for that!

We need to import a bunch of functions from the [math](https://docs.python.org/3/library/math.html) module to calculate the distance between two cities using the [harversine formula](https://en.wikipedia.org/wiki/Haversine_formula).

```python
import argparse
import collections
import csv
import logging
import math
import pathlib
```

Now we write the `get_distance` function, which takes two cities as arguments and returns the distance between them:

```python
def get_distance(city_a, city_b):
    """Returns the distance in km between city_a and city_b.

    Uses the Haversine formulate to calculate distances between
    points on a sphere.

    Args:
       city_a (City): origin city namedtuple.
       city_a (City): destination city namedtuple.
    """

    lat_i, lon_i = city_a.lat, city_a.lon
    lat_j, lon_j = city_b.lat, city_b.lon

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
```

However, the Haversine formula requires latitude and longitude values in radians, not degrees, which is the unit we have our data in. Let's add the conversion when we read in cities and add them to the database.

```python
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
                lat_rad = math.radians(float(lat))
                lon_rad = math.radians(float(lon))
            except Exception as err:
                logging.warning(f'Error parsing line {line_idx}: {err}')
                continue
            else:
                city = City(
                    name,
                    state_code,
                    lat_rad,
                    lon_rad
                )
                logging.debug(f'Added city: {city.name}, {city.state}')

                city_db[(name, state_code)] = city

    logging.info(f'Read {len(city_db)} cities into a database')
    return city_db
```

### Part IX: Finding neighbors using filter and lambda functions

Now that we can get distances between cities, we can write a small function to get us all the neighbors of a given city. For this, we iterate over a list of candidate cities, which can be the entire database, and return only those within a certain distance cutoff of the query city. In other words, we want a _filter_ function that takes an iterable and a condition and returns only the members of the iterable that meet the condition. We could do this ourselves with a for-loop and an if-statement but Python has built-in functions specifically for this:

```python
def find_city_neighbors(city, candidates, radius):
    """Returns all cities in candidates within radius of self.

    Args:
        city (City): query City.
        candidates (list): list of City objects.
        radius (float): distance cutoff to consider a City a neighbor
    """
    
    return filter(
        lambda c: get_distance(city, c) <= radius,
        candidates
    )
```

The [filter](https://docs.python.org/3/library/functions.html#filter) built-in function in Python takes two arguments: a function and an iterable such as a list. It then loops over all elements in the iterable and applies the function to them, returning only those where the result was equivalent to the boolean value `True`. The advantage over our own for-loop + if-statement is two-fold: first, using `filter` results in more compact code, which is more readable; second, it returns an iterator, so you can apply it to very large iterables (think really large lists) without worrying about memory.

The function argument to `filter` can be any function. You can define one yourself using the `def` construct, but in here (and generally when using `filter`) we use a [lambda](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions) function. Think of `lambda` as a short-hand notation to define very simple functions. The general syntax is `lambda <argument>: <result>`. In the case above, our `lambda` takes a city object (`c`) and returns `True`/`False` depending on the result of the comparison `get_distance(city, c) <= radius`. If we want to re-use the `lambda` function, we can always assign it to a variable, as we will see below and call it like a regular function. Neat!

### Part X: Writing our route planning algorithm!

It seems we have all the pieces necessary to write our `find_route` function. We want to write it generically enough so that if we add other options/arguments in the future, we make the least changes possible. So, here we go!

```python
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
    distance_to_end = lambda city: get_distance(finish, city)
    
    current = start
    while current != finish:
        neighbors = find_city_neighbors(
            current,
            list_of_cities,
            km_per_day
        )
        
        sorted_neighbors = sorted(
            neighbors,
            key=distance_to_end
        )
        
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
            f'Added {current.name}, {current.state} to route: '
            f'{get_distance(current, finish):5.2f} km to end'
        )
        
    return route
```

The code above introduces two features of for-loops: the `break` statement and the `else` clause. A `break` statement does it says it does: it stops the loop. In our case, we use it to avoid iterating over all the cities in the `sorted_neighbors` list after we find one we haven't visited yet. The `else` clause in the for-loop is only valid when there is a `break` statement, and executes only if the for-loop is never stopped. In other words, if we iterate over `sorted_neighbors` and none of the cities triggers the if-statement, the `else` clause runs. It's a neat way of controlling the flow of the program and saving compute cycles.

Now we have to update our main loop:

```python
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
    write_route()
```

### Part XI: Printing our route

Let's give the user the chance now to see the result of our calculation by writing the `write_route` function and updating the main loop code:

```python
def write_route(route):
    """Outputs a route to the screen.
    
    Args:
        route (list): list of City objects.
    """
    
    for stop_idx, city in enumerate(route):
        print(f'[Day {stop_idx}] {city.name}, {city.state}')
```

```python
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
```

## Conclusion

We're done! In ~270 lines of code we have a route planner that we can actually use to plan road trips. Throughout this 'journey', we used 6 standard library modules, learned about context managers, `try/except` blocks, f-strings, `else` statements in for-loops, `filter` and `lambda` functions. These are all constructs that are fairly common in Python scripts.

We understand that this is a lot to take in, and we do not expect you to leave here mastering every topic we just covered. We hope, however, that you are not afraid of diving into the online documentation next time you have to write a script and looking for and trying out new features that are included with your Python installation.

Let us know if you have any questions or feedback, you can reach me at `joaor@stanford.edu`. Thank you for following along and good luck with your Python adventures (and road trips)!

---

Content licensed under CC-BY-4.0. For details, see the LICENSE file on the repository.

Last updated: 18 March 2020
