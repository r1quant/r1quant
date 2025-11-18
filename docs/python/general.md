# Python 

## f-String

```python 
name = "Bob"
age = 25

#  Using % operator (old style)
print("My name is %s and I'm %d years old" % (name, age)) 

# Using str.format()
print("My name is {} and I'm {} years old".format(name, age))  

# Using f-string
print(f"My name is {name} and I'm {age} years old") 
```

```python
print(f"{x=}, {y=}")
print(f"{x + y=}")
print(f"Price rounded to 2 decimals: {price:.2f}")
print(f"Percentage with 1 decimal: {percentage:.1%}")
print(f"Using comma as thousand separator: ${revenue:,.2f}")
print(f"Using underscore as thousand separator: ${revenue:_.2f}")
print(f"Left aligned:    |{name:<20}|")
print(f"   Right aligned:|{name:>20}|")
print(f" Center aligned: |{name:^20}|")
print(f"Padding numbers with zeros: {customer_id:04d}")
```


## Loops 

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int


users: list[User] = [
    {"name": "Alice", "age": 28},
    {"name": "Bob", "age": 17},
    {"name": "Carol", "age": 35},
]

# For loop (faster)
adult_names: list[str] = []
for user in users:
    if user["age"] >= 18:
        adult_names.append(user["name"].upper())

# Map/filter
adult_users = filter(lambda u: u["age"] >= 18, users)
adult_names = list(map(lambda u: u["name"].upper(), adult_users))

# List comprehension
adult_names = [user["name"].upper() for user in users if user["age"] >= 18]
```

# Datetime

```python 
import datetime

# Get the current datetime
now = datetime.datetime.now()
print(now)

# Get the current UTC datetime
now_utc = datetime.datetime.now(datetime.UTC)
print(now_utc)

# Convert the datetime object to a Unix timestamp in seconds
seconds_since_epoch_dt = now_utc.timestamp()
print(seconds_since_epoch_dt)

# Convert to milliseconds
milliseconds_since_epoch_dt = int(seconds_since_epoch_dt * 1000)
print(milliseconds_since_epoch_dt)

# Start Time
start_time = now_utc - datetime.timedelta(days=90)
print(start_time)

# Subtract a specific number of days from a specific date
specific_date = datetime.datetime(2025, 1, 1, 0, 0, 0)
print(specific_date)
print(specific_date.timestamp())
print(int(specific_date.timestamp() * 1000))
```


## 10 Standard Library Modules

- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [cache](https://docs.python.org/3/library/functools.html)
- [tomllib](https://docs.python.org/3/library/tomllib.html)
- [graphlib](https://docs.python.org/3/library/graphlib.html)
- [heapq](https://docs.python.org/3/library/heapq.html)
- [secrets](https://docs.python.org/3/library/secrets.html)
- [shutil](https://docs.python.org/3/library/shutil.html)
- [textwrap](https://docs.python.org/3/library/textwrap.html)
- [itertools](https://docs.python.org/3/library/itertools.html) 

```python 
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True


print(Product(name="Widget", price=19.99))
# Product(name='Widget', price=19.99, in_stock=True)

```
```python 
import itertools

list(itertools.combinations(["a", "b", "c"], 2))
# [('a', 'b'), ('a', 'c'), ('b', 'c')]
```

## Conditions

**Is None vs None**

```
class Foo:
    def __eq__(self, other):
        return True
foo = Foo()

print(foo == None)
# True

print(foo is None)
# False

#-- is None is a bit (~50%) faster than == None
```

## Python Libraries You Should Know About

- [Pendulum](https://pendulum.eustace.io): Manipulate your datetimes with ease
- [Icecream](https://github.com/gruns/icecream): Never use print() to debug again
- [Loguru](https://github.com/Delgan/loguru): Logging made (stupidly) simple
- [Rich](https://github.com/Textualize/rich): Rich text and beautiful formatting in the terminal.
- [Argparse](https://docs.python.org/3/library/argparse.html): For implementing basic command line applications
- [Tqdm](https://github.com/tqdm/tqdm): Progress Bar for Python and CLI
- [Xarray](https://github.com/pydata/xarray): N-D labeled arrays and datasets
- [Polar](https://www.pola.rs): Blazingly Fast DataFrame Library
- [Seaborn](https://github.com/mwaskom/seaborn): For making statistical graphic
- [Result](https://pypi.org/project/result): A simple Result type 
- [Pydantic](https://github.com/pydantic/pydantic): used data validation library
- [Sqlmodel](https://github.com/fastapi/sqlmodel): For interacting with SQL databases
- [Httpx](https://github.com/encode/httpx): HTTP client 
- [PythonDotenv](https://github.com/theskumar/python-dotenv): Reads key-value pairs from a .env file


```python
import pendulum

dt_toronto = pendulum.datetime(2012, 1, 1, tz='America/Toronto')
```

```python
from icecream import ic

ic(your_function(123))
```

```python
from loguru import logger

logger.debug("That's it, beautiful and simple logging!")
```

```python
from rich.console import Console

console.print("Hello", "World!", style="bold red")
```

```python
parser = argparse.ArgumentParser(prog='ProgramName', description='lorem..')
parser.add_argument('filename') # positional argument
parser.add_argument('-c', '--count') # option that takes a value
parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag
```

```python
from tqdm import tqdm

pbar = tqdm(total=100)
for i in range(10):
    sleep(0.1)
    pbar.update(10)
pbar.close()
```

```python
from result import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("Cannot divide by zero")
    return Ok(a // b)
```

```python
import httpx

r = httpx.get('https://www.example.org/')
```


--- 

#### Sources

- [10 Standard Library Modules Video](https://www.youtube.com/watch?v=eZ9RqnkJxsk)
- [10 Standard Library Modules Repository](https://github.com/ArjanCodes/examples/tree/main/2025/standard)
- [Let’s Replace All For Loops With Map and Filter Repository](https://github.com/ArjanCodes/examples/blob/main/2025/map/basic_example.py)
- [15 Python Libraries You Should Know About Video](https://www.youtube.com/watch?v=o06MyVhYte4)
- [Is None vs None](https://jaredgrubb.blogspot.com/2009/04/python-is-none-vs-none.html)