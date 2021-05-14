# -*- coding: utf-8 -*-
from time import sleep
from typing import Any, Dict, List

import pandas as pd
from requests import Request

__version__ = "0.1.1"


class Openbudget:
    """
    Desc

    Attributes
    ----------

    Methods
    -------

    """

    INCOMES_URL = "https://openbudget.gov.ua/api/localBudgets/incomesLocal/CSV"
    EXPENSES_URL = "https://openbudget.gov.ua/api/localBudgets/functional/CSV"
    ABOUT_BUDGET_URL = (
        "https://openbudget.gov.ua/api/localBudgets/aboutBudgets/plain/CSV"
    )
    COLS = {
        "incomeCode": "код",
        "incomeCodeName": "найменування коду",
        "yearBudgetPlan": "розпис на рік",
        "yearBudgetEstimate": "кошторис на рік",
        "totalDone": "виконано всього",
        "percentDone": "відсоток виконання",
        "codeBudget": "код бюджету",
        "fundType": "тип фонду",
        "programCode": "КПК",
        "programCodeName": "найменування КПК",
        "functionCode": "КФК",
        "functionCodeName": "найменування КФК",
        "doneSpecialFund": "виконано спец фонд",
        "doneService": "виконано послуги",
        "doneOther": "виконано інші джерела",
        "totalBankAccount": "у банках всього",
        "bankSpecialFund": "у банках спец фонд",
        "bankService": "у банках послуги",
        "bankOther": "у банках інші джерела",
        "budgetCode": "код бюджету",
        "budgetName": "найменування бюджету",
        "koatuu": "код КОАТУУ",
        "terUnit": "адміністративно-територіальна одиниця",
        "year": "рік",
        "monthTo": "кінець періоду",
        "monthFrom": "початок періоду",
        "treeType": "ієрархічне представлення",
    }

    def __init__(
        self,
        codes: List[str],
        years: List[int],
        month_from: int = 1,
        month_to: int = 12,
        fund_type: str = "TOTAL",
        tree_type: str = "WITHOUT_DETALISATION",
        translate: bool = True,
        init_with_budgets_structure: bool = True,
        init_with_incomes: bool = False,
        init_with_expenses: bool = False,
    ):
        self.codes = codes
        self.years = years
        self.month_from = month_from
        self.month_to = month_to
        self.fund_type = fund_type
        self.tree_type = tree_type
        self.translate = translate
        self._about = None 
        self._incomes = None
        self._expenses = None 

        self.fetch_about() if init_with_budgets_structure else None
        self.fetch_incomes() if init_with_incomes else None
        self.fetch_expenses() if init_with_expenses else None

    @staticmethod
    def prepare_call(endpoint: str, params: Dict[str, Any]):
        """Prepare url given `endpoint` and `params`."""
        req = Request("GET", endpoint, params=params)
        prepped = req.prepare()
        return prepped.url

    @staticmethod
    def to_dataframe(path: str, **kwargs):
        """Read url into `pandas.DataFrame`."""
        df = pd.read_csv(
            path,
            sep=";",
            encoding="cp1251",
            skiprows=1,
            dtype={"incomeCode": str, "functionCode": str},
        )
        for key, value in kwargs.items():
            df[key] = value
        return df

    def _check_exists(self, attrb):
        """Check if attribute contains data."""
        return attrb is not None

    def _merge(self, left: pd.DataFrame, right: pd.DataFrame):
        """Join budget's metadata to main table."""
        duplicated_columns = ["year", "monthTo", "monthFrom", "budgetCode", "fundType"]
        return pd.merge(
            left,
            right.drop(duplicated_columns, axis=1),
            how="left",
            on="codeBudget",
        )

    def _pairs(self):
        """Iterate over given years and codes"""
        years = [self.years] if isinstance(self.years, int) else self.years
        for year in years:
            for code in self.codes:
                yield year, code

    def _fetch(self, endpoint: str, year: int, code: str):
        """Private function that fetches data from a given endpoint."""
        params = {
            "year": year,
            "monthTo": self.month_to,
            "monthFrom": self.month_from,
            "codeBudget": code,
            "fundType": self.fund_type,
        }
        if endpoint == Openbudget.EXPENSES_URL:
            params.update({"treeType": self.tree_type})
        url = Openbudget.prepare_call(endpoint, params)
        sleep(1.1)
        yield Openbudget.to_dataframe(url, **params)

    def _fetch_all(self, endpoint: str):
        """Concatenate results returned from `_fetch` function."""
        for year, code in self._pairs():
            yield from self._fetch(endpoint, year, code)

    def fetch_incomes(self, forced: bool = False):
        """Fetch incomes table."""
        if not self._check_exists(self._incomes) or forced:
            self._incomes = pd.concat(
                self._fetch_all(Openbudget.INCOMES_URL), ignore_index=True
            )
        return self._incomes

    def fetch_expenses(self, forced: bool = False):
        """Fetch expenses table."""
        if not self._check_exists(self._expenses) or forced:
            self._expenses = pd.concat(
                self._fetch_all(Openbudget.EXPENSES_URL), ignore_index=True
            )
        return self._expenses

    def fetch_about(self, forced: bool = False):
        """Fetch budget's metadata/structure."""
        if not self._check_exists(self._about) or forced:
            about = pd.concat(
                self._fetch_all(Openbudget.ABOUT_BUDGET_URL), ignore_index=True
            )
            self._about = about.loc[about["budgetCode"].isin(self.codes)]
        return self._about

    @property
    def incomes(self):
        if self._incomes is not None and self._about is not None:
            data = self._merge(self._incomes, self._about)
        elif self._incomes is not None and self._about is None:
            print("To join metadata, run fetch_about() first")
            data = self._incomes
        else:
            raise ValueError("Run fetch_incomes() first.")
        return data.rename(columns=Openbudget.COLS) if self.translate else data

    @property
    def expenses(self):
        if self._expenses is not None and self._about is not None:
            data = self._merge(self._expenses, self._about)
        elif self._expenses is not None and self._about is None:
            print("To join metadata, run fetch_about() first")
            data = self._expenses
        else:
            raise ValueError("Run fetch_expenses() first.")
        return data.rename(columns=Openbudget.COLS) if self.translate else data
