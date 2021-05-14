# -*- coding: utf-8 -*-
class BudgetConfig:
    """Budget's endpoints & translated field names."""

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
