# Openbudget

This repository contains **openbudget** python API wrapper. 


## Installation

### Local
To use or contribute to this repository, first checkout the code. Then create a new virtual environment:

```bash
$ git clone https://github.com/hp0404/openbudget-api.git
$ cd openbudget-api
$ python3 -m venv env
$ . env/bin/activate
```

Install the package and its dependencies
```bash
(env)$ python -m pip install --upgrade pip setuptools wheel
(env)$ python -m pip install -r requirements.txt
(env)$ python -m pip install -r requirements-dev.txt
(env)$ python -m pip install -e .
```

Alternatively, use `make`:
```bash
(env)$ make install-dev
```


### Google colab
To use this package from google colab, run:
```bash
!pip -q --no-cache-dir install git+https://github.com/hp0404/openbudget-api.git
```

## Usage

```python
from openbudget import Openbudget

# one code, one year
poltava_2020 = Openbudget(
    codes="16100000000",
    years=2020,
    month_from=1,
    month_to=12,
    fund_type="TOTAL",
    tree_type="WITHOUT_DETALISATION",
    translate=True,
    init_with_budgets_structure=True,
    init_with_expenses=False,
    init_with_incomes=True
)
print(poltava_2020.incomes)

# multiple codes, multiple years
regions_2018_2020 = Openbudget(
    codes=["02100000000", "03100000000"],
    years=[2018, 2020],
    month_from=1,
    month_to=12,
    fund_type="TOTAL",
    tree_type="WITHOUT_DETALISATION",
    translate=True,
    init_with_budgets_structure=True,
    init_with_expenses=True,
    init_with_incomes=False
)
print(regions_2018_2020.expenses)

# create an instance of a class without fetching data
kyiv_2021 = Openbudget(
    codes="26000000000",
    years=2021,
    month_from=1,
    month_to=3,
)
print(kyiv_2021.fetch_incomes())
print(kyiv_2021.fetch_expenses())
print(kyiv_2021.incomes)
```