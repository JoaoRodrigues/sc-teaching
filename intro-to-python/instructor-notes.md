# Intro to Python - Notes

## Intro
* Python as a general purpose programming language.
* Scientific computing, scripting, plotting.
* Goal: motivate you to learn more with a simple example.

## Intro to Notebooks
* Where to start writing code?
* Jupyter notebooks as a browser-based development environment.
* Notebooks can be exported to scripts and/or shared with others.
* Open Anaconda/Miniconda prompt (or Terminal on Mac)
* `cd Desktop && jupyter notebook`
* New -> Python 3
* Cells -> shift+enter executes code
* Data persists between cells. Order of EXECUTION matters.

## Intro to Python
### Variable Assignment
* `year = 1891`
* Comments annotate code: `# This is a comment.`
* `name = 'Stanford'`
* Variable names: short, descriptive, use_under, 1notgood
* `print(name, 'was founded in', year)`
### Types
* Types of variables: int, string, float, bool
* Know variable type: `type(year); type(name)`
### Operations on Variables
* Arithmetic: +, -, *, /, //, **
* `3 + 3; 3**3; 1/3; 1//3`
* Assign result of operations to new variables:
* `this_year = 2019; age = this_year - year`
* Different types, different results
* `name + name; name - name`
* Traceback message.
* Types do not usually mix.
* `name + age; name * age`
* Type conversion by explicit casting: `name + str(age)`
* Conversions do not always work: `int(name)`
### Reading files
* Download file to Desktop: https://pastebin.com/Trinnt7X
* `fname = 'gapminder_lifeexp.txt'; handle = open(fname, 'r')`
* `print(handle); type(handle)`
* `line = handle.readline(); print(line); type(line)`
* Explain object methods. Everything is an object in Python.
* Strings are also objects and have very useful methods.
* Strip whitespace at the ends of the string: `line.strip()`
* Split line by commas: `fields = line.split(','); print(fields); type(fields)`
### List Indexing
* Lists as a new variable type: containers of other variables.
* Indexing by position: 0->1st element, 1->2nd element, -1-> last element, -2->2nd to last element
* `print('The first field of the line is', fields[0])`
* `print('The second field of the line is', fields[1])`
* `print('The last field of the line is', fields[-1])`
* Read the next line. Repeat splitting.
* `lifeExp_change = fields[-1] - fields[2]` -> Always read as str.
* `lifeExp_change = float(fields[-1]) - float(fields[2])`
* `country = fields[0]; print('Life expectancy of ', country, 'changed:', lifeExp_change)`
* Read next line. Repeat?
* File iteration exhausts. To re-read, reload.
### For-loops: Repeating Actions
* For-loops: repeat same action (code block) n times until exhaustion.
* `for line in handle: country = ...; lifeExp_change = ...; print( ... )`
* Indendation matters. Use (4) spaces, not tabs.
* `handle.close()` -> good practice.
### Storing values in lists
* Boring to repeat open/read/close cycle.
* Store multiple values in variables using lists.
* `countries = []; continents = []; lifeExp_change = []`
* `for line in handle: countries.append(country) ...`
* Calculate average
* `ave_change = 0.0; counts = 0; for item in lifeExp: ave_change = ave_change + item; counts = counts + 1`
* `ave_change = ave_change / counts`
* Simplify by using built-in functions
* `ave_change2 = sum(lifeExp) / len(lifeExp)`
* `max(lifeExp); min(lifeExp)`
### Filtering Data using Conditionals
* Different operations based on data.
* Is there any country with a negative lifeExp change?
* `for entry in lifeExp: if lifeExp < 0: print(lifeExp)`
* `<`, `>`, `<=`, `>=` comparison operators.
* Comparisons return boolean values: True or False.
* Comparisons can be chained with _and_ / _or_ statements
* `for idx, entry in enumerate(lifeExp): if lifeExp < 0: print(countries[idx], lifeExp)`
### Writing to file
* Write only european values to a file
* Same syntax as opening files
* `handle = open(fname, 'w')` -> erases contents of fname
* `ave_europe = 0.0`
* `n_items = len(countries); for idx in range(n_items): if continents[idx] == 'Europe': ave = ave + lifeExp[idx]` 
* `==` is different than `=`. Comparison vs Assignment.
* `!=` is the _not equal_ to operator.
* `for ....: print(key, ave, file=handle); handle.close()`
## Export notebook to file
* Open new notebook
* Rewrite (or copy) script to read file, filter per continent, write to new file
```
#!/usr/bin/env python

# Empty lists to hold file data
countries = []
continents = []
life_exp_delta_list = []

# Read data from file
infname = 'gapminder_lifexp.txt'
infile = open(fname, 'r')

infile.readline()  # skip header!

for line in infile:
    fields = line.strip().split(',')
    country = fields[1]
    continent = fields[0]
    life_exp_delta = float(fields[-1]) - float(fields[2])
    
    countries.append(country)
    continents.append(continent)
    life_exp_delta_list.append(life_exp_delta)

infile.close()

# Write only european countries to disk
outfname = 'gapminder_lifexp_Europe.txt'
outfile = open(outfname, 'w')
for idx, country in enumerate(countries):
    if continents[idx] == 'Europe':
        print(country, life_exp_delta_list[idx], file=outfile)
outfile.close()
```
* Save as python script
* Close jupyter console. Execute script on command line.
* `cd Desktop; python myscript.py; ls`
