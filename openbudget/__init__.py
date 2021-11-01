# -*- coding: utf-8 -*-
"""Docstring."""
import io
from time import sleep
from typing import Dict, Iterator, List, Tuple, Union

import pandas as pd  # type: ignore
import requests

from .constants import BudgetConfig

__version__ = "0.1.1"


class Openbudget(BudgetConfig):
    """
    Budget's structure, income, and expenses data retrived from openbudget API.

    Attributes
    ----------
    codes: List[str]
        budget codes, e.g. ["16100000000", "17100000000"]
    years: List[int]
        years to fetch data for (period)
    month_from: int
        first month of a period, defaults to 1
    month_to: int
        last month of a period, defaults to 12
    fund_type: str
        pass, defaults to TOTAL
    tree_type: str
        pass, defaults to WITHOUT_DETALISATION
    translate: bool
        translate en columns to ua, defaults to True
    init_with_budgets_structure: bool
        fetch budgets' structure while creating an instance of a class,
        defaults to True
    init_with_incomes: bool
        fetch budgets' incomes while creating an instance of a class,
        defaults to True
    init_with_expenses: bool
        fetch budgets' expenses while creating an instance of a class,
        defaults to True
    """

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

    @property
    def incomes(self) -> pd.DataFrame:
        """Prettified incomes table, optionally translates columns to uk."""
        data = self.prettify(self._incomes)
        return data.rename(columns=Openbudget.COLS) if self.translate else data

    @property
    def expenses(self) -> pd.DataFrame:
        """Prettified expenses table, optionally translates columns to uk."""
        data = self.prettify(self._expenses)
        return data.rename(columns=Openbudget.COLS) if self.translate else data

    @staticmethod
    def prepare_call(endpoint: str, params: Dict[str, Union[str, int]]) -> str:
        """Prepare url using `endpoint` and `params`."""
        req = requests.Request("GET", endpoint, params=params)
        prepped = req.prepare()
        return prepped.url

    @staticmethod
    def to_dataframe(path: str, **kwargs) -> pd.DataFrame:
        """Read url into `pandas.DataFrame`."""
        content = requests.get(path).content
        df = pd.read_csv(
            io.StringIO(content.decode("cp1251")),
            sep=";",
            encoding="cp1251",
            skiprows=1,
            dtype={"incomeCode": str, "functionCode": str},
        )
        for key, value in kwargs.items():
            df[key] = value
        return df

    @staticmethod
    def merge(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        """Join budget's metadata to main table."""
        duped_cols = ["year", "monthTo", "monthFrom", "budgetCode", "fundType"]
        return pd.merge(
            left,
            right.drop(duped_cols, axis=1),
            how="left",
            on="codeBudget",
        )

    @staticmethod
    def check_exists(attrb: pd.DataFrame) -> bool:
        """Check if attribute exists (contains data)."""
        return attrb is not None

    @staticmethod
    def convert_tolist(
        attrb: Union[List[int], List[str], int, str]
    ) -> Union[List[int], List[str]]:
        """Covert int/str `attrb` values into a list."""
        return [attrb] if isinstance(attrb, (int, str)) else attrb

    def prettify(self, left: pd.DataFrame) -> pd.DataFrame:
        """Join budgets' structure if available."""
        left_exists = self.check_exists(left)
        meta_exists = self.check_exists(self._about)
        if left_exists and meta_exists:
            return self.merge(left, self._about)
        if left_exists and not meta_exists:
            print("Run fetch_about() to join budget's structure.")
            return left
        raise ValueError("Fetch data first.")

    def _iterate_over_period_budget(self) -> Iterator[Tuple[int, str]]:
        """Iterate over given years and codes"""
        codes = self.convert_tolist(self.codes)
        years = self.convert_tolist(self.years)
        for year in years:
            for code in codes:
                yield year, code

    def _fetch(self, endpoint: str, year: int, code: str) -> Iterator[pd.DataFrame]:
        """Retrieve data from `endpoint` for a specific `year` and `code`."""
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

    def _fetch_all(self, endpoint: str) -> Iterator[pd.DataFrame]:
        """Retrieve all data from `endpoint`; functions as a wrapper around
        `_fetch` function."""
        for year, code in self._iterate_over_period_budget():
            yield from self._fetch(endpoint, year, code)

    def fetch_incomes(self, forced: bool = False) -> pd.DataFrame:
        """Fetch incomes table."""
        if not self.check_exists(self._incomes) or forced:
            self._incomes = pd.concat(
                self._fetch_all(Openbudget.INCOMES_URL), ignore_index=True
            )
        return self._incomes

    def fetch_expenses(self, forced: bool = False) -> pd.DataFrame:
        """Fetch expenses table."""
        if not self.check_exists(self._expenses) or forced:
            self._expenses = pd.concat(
                self._fetch_all(Openbudget.EXPENSES_URL), ignore_index=True
            )
        return self._expenses

    def fetch_about(self, forced: bool = False) -> pd.DataFrame:
        """Fetch budget's metadata/structure."""
        if not self.check_exists(self._about) or forced:
            data = pd.concat(
                self._fetch_all(Openbudget.ABOUT_BUDGET_URL), ignore_index=True
            )
            filtered_data = data.loc[
                data["budgetCode"].isin(self.convert_tolist(self.codes))
            ]
            self._about = filtered_data
        return self._about
