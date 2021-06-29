# Openbudget

Цей репозиторій містить **openbudget** - бібліотеку, покликану спростити взаємодію з Openbudget API. 

## Встановлення
Ці інструкції допоможуть відтворити віртуальне середовище на локальному комп'ютері або в середовищі Google colab

### Відтворення робочого середовища

Скопіюйте репозиторій в нову папку, після чого створіть віртуальне середовище:

```bash
$ git clone https://github.com/hp0404/openbudget-api.git
$ cd openbudget-api
$ python3 -m venv env
$ . env/bin/activate
```

Встановіть бібліотеку та необхідні залежності

```bash
(env)$ python -m pip install --upgrade pip setuptools wheel
(env)$ python -m pip install -r requirements.txt
(env)$ python -m pip install -r requirements-dev.txt
(env)$ python -m pip install -e .
```

Або скористайтесь `make`:
```bash
(env)$ make install-dev
```

### Google colab
Щоб встановити бібліотеку в середовищі google colab, виконайте:
```bash
!pip -q --no-cache-dir install git+https://github.com/hp0404/openbudget-api.git
```

## Приклад використання
```python
from openbudget import Openbudget

# один бюджет за один рік
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

# декілька бюджетів, декілька років
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

# один бюджет без попереднього завантаження даних
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