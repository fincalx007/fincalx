from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log
from typing import Callable


@dataclass(frozen=True)
class FieldSpec:
    name: str
    label: str
    default: float
    min_value: float
    max_value: float
    step: str = "0.01"
    suffix: str = ""


@dataclass(frozen=True)
class EvergreenCalculator:
    slug: str
    key: str
    title: str
    short_title: str
    description: str
    category: str
    formula: str
    formula_explanation: str
    example: str
    fields: tuple[FieldSpec, ...]
    result_labels: dict[str, str]
    calculator: Callable[[dict[str, float]], dict[str, float]]

    @property
    def path(self) -> str:
        return f"/tools/{self.slug}"

    @property
    def api_path(self) -> str:
        return f"/tools/{self.slug}/api"


def _pct(value: float) -> float:
    return value / 100


def _monthly_rate(annual_rate: float) -> float:
    return _pct(annual_rate) / 12


def _emi(principal: float, annual_rate: float, months: int) -> float:
    if months <= 0:
        return 0
    r = _monthly_rate(annual_rate)
    if r == 0:
        return principal / months
    return principal * r * ((1 + r) ** months) / (((1 + r) ** months) - 1)


def _months_to_payoff(balance: float, annual_rate: float, payment: float) -> float:
    r = _monthly_rate(annual_rate)
    if payment <= 0:
        return 0
    if r == 0:
        return balance / payment
    if payment <= balance * r:
        return 0
    return -log(1 - (balance * r / payment)) / log(1 + r)


def _interest_with_payment(balance: float, annual_rate: float, payment: float, max_months: int = 1200) -> tuple[float, int]:
    r = _monthly_rate(annual_rate)
    total_interest = 0.0
    months = 0
    current = balance
    while current > 0.01 and months < max_months:
        interest = current * r
        principal = min(payment - interest, current)
        if principal <= 0:
            return total_interest, max_months
        total_interest += interest
        current -= principal
        months += 1
    return total_interest, months


def _simple_interest(v: dict[str, float]) -> dict[str, float]:
    interest = v["principal"] * _pct(v["annual_rate"]) * v["years"]
    return {"interest": interest, "maturity_value": v["principal"] + interest}


def _future_value(v: dict[str, float]) -> dict[str, float]:
    future = v["present_value"] * ((1 + _pct(v["annual_rate"])) ** v["years"])
    return {"future_value": future, "growth": future - v["present_value"]}


def _present_value(v: dict[str, float]) -> dict[str, float]:
    present = v["future_value"] / ((1 + _pct(v["discount_rate"])) ** v["years"])
    return {"present_value": present, "discount_amount": v["future_value"] - present}


def _rule_72(v: dict[str, float]) -> dict[str, float]:
    years = 72 / v["annual_rate"] if v["annual_rate"] else 0
    return {"estimated_years_to_double": years}


def _loan_amortization(v: dict[str, float]) -> dict[str, float]:
    months = int(v["years"] * 12)
    payment = _emi(v["loan_amount"], v["annual_rate"], months)
    total_payment = payment * months
    return {"monthly_payment": payment, "total_payment": total_payment, "total_interest": total_payment - v["loan_amount"]}


def _loan_comparison(v: dict[str, float]) -> dict[str, float]:
    months_a = int(v["years_a"] * 12)
    months_b = int(v["years_b"] * 12)
    emi_a = _emi(v["loan_amount_a"], v["rate_a"], months_a)
    emi_b = _emi(v["loan_amount_b"], v["rate_b"], months_b)
    total_a = emi_a * months_a
    total_b = emi_b * months_b
    return {"monthly_payment_a": emi_a, "monthly_payment_b": emi_b, "total_cost_a": total_a, "total_cost_b": total_b, "cost_difference": abs(total_a - total_b)}


def _extra_payment(v: dict[str, float]) -> dict[str, float]:
    months = int(v["years"] * 12)
    standard = _emi(v["loan_amount"], v["annual_rate"], months)
    base_interest = (standard * months) - v["loan_amount"]
    extra_interest, extra_months = _interest_with_payment(v["loan_amount"], v["annual_rate"], standard + v["extra_monthly_payment"])
    return {"standard_monthly_payment": standard, "new_months_to_payoff": extra_months, "interest_saved": max(base_interest - extra_interest, 0)}


def _prepayment_savings(v: dict[str, float]) -> dict[str, float]:
    months = int(v["remaining_years"] * 12)
    payment = _emi(v["outstanding_balance"], v["annual_rate"], months)
    base_interest = (payment * months) - v["outstanding_balance"]
    reduced_balance = max(v["outstanding_balance"] - v["one_time_prepayment"], 0)
    new_interest, new_months = _interest_with_payment(reduced_balance, v["annual_rate"], payment)
    return {"monthly_payment_used": payment, "new_months_to_payoff": new_months, "interest_saved": max(base_interest - new_interest, 0)}


def _savings(v: dict[str, float]) -> dict[str, float]:
    months = int(v["years"] * 12)
    r = _monthly_rate(v["annual_rate"])
    future_current = v["current_savings"] * ((1 + r) ** months)
    if r == 0:
        future_monthly = v["monthly_saving"] * months
    else:
        future_monthly = v["monthly_saving"] * ((((1 + r) ** months) - 1) / r)
    total = future_current + future_monthly
    return {"future_savings": total, "total_contributions": v["current_savings"] + (v["monthly_saving"] * months), "growth": total - v["current_savings"] - (v["monthly_saving"] * months)}


def _budget(v: dict[str, float]) -> dict[str, float]:
    expenses = v["needs"] + v["wants"] + v["debt_payments"] + v["planned_savings"]
    surplus = v["monthly_income"] - expenses
    savings_rate = (v["planned_savings"] / v["monthly_income"]) * 100 if v["monthly_income"] else 0
    return {"monthly_surplus": surplus, "total_allocated": expenses, "savings_rate": savings_rate}


def _debt_payoff(v: dict[str, float]) -> dict[str, float]:
    months = _months_to_payoff(v["debt_balance"], v["annual_rate"], v["monthly_payment"])
    interest, rounded_months = _interest_with_payment(v["debt_balance"], v["annual_rate"], v["monthly_payment"])
    return {"months_to_payoff": rounded_months if months else 0, "years_to_payoff": (rounded_months / 12) if months else 0, "total_interest": interest}


def _dti(v: dict[str, float]) -> dict[str, float]:
    ratio = (v["monthly_debt_payments"] / v["gross_monthly_income"]) * 100 if v["gross_monthly_income"] else 0
    return {"debt_to_income_ratio": ratio, "monthly_income_after_debt": v["gross_monthly_income"] - v["monthly_debt_payments"]}


def _financial_freedom(v: dict[str, float]) -> dict[str, float]:
    target = v["annual_expenses"] / _pct(v["withdrawal_rate"])
    monthly_needed = max(target - v["current_savings"], 0)
    months = 0
    current = v["current_savings"]
    r = _monthly_rate(v["annual_return"])
    while current < target and months < 1200:
        current = current * (1 + r) + v["monthly_savings"]
        months += 1
    return {"target_corpus": target, "months_to_target": months, "years_to_target": months / 12, "remaining_gap": monthly_needed}


def _purchasing_power(v: dict[str, float]) -> dict[str, float]:
    power = v["current_amount"] / ((1 + _pct(v["inflation_rate"])) ** v["years"])
    return {"future_purchasing_power": power, "purchasing_power_loss": v["current_amount"] - power}


def _real_rate(v: dict[str, float]) -> dict[str, float]:
    real = (((1 + _pct(v["nominal_return"])) / (1 + _pct(v["inflation_rate"]))) - 1) * 100
    return {"real_rate_of_return": real}


def _investment_growth(v: dict[str, float]) -> dict[str, float]:
    return _savings({"current_savings": v["initial_investment"], "monthly_saving": v["monthly_contribution"], "annual_rate": v["annual_return"], "years": v["years"]})


def _wealth_accumulation(v: dict[str, float]) -> dict[str, float]:
    result = _investment_growth(v)
    return {"estimated_wealth": result["future_savings"], "total_contributions": result["total_contributions"], "growth": result["growth"]}


def _portfolio_return(v: dict[str, float]) -> dict[str, float]:
    total = v["asset_a_value"] + v["asset_b_value"] + v["asset_c_value"]
    weighted = 0 if total == 0 else ((v["asset_a_value"] * v["asset_a_return"]) + (v["asset_b_value"] * v["asset_b_return"]) + (v["asset_c_value"] * v["asset_c_return"])) / total
    return {"portfolio_return": weighted, "portfolio_value": total}


def _portfolio_allocation(v: dict[str, float]) -> dict[str, float]:
    total = v["equity_value"] + v["debt_value"] + v["cash_value"] + v["other_value"]
    if total == 0:
        return {"total_portfolio": 0, "equity_allocation": 0, "debt_allocation": 0, "cash_allocation": 0, "other_allocation": 0}
    return {
        "total_portfolio": total,
        "equity_allocation": (v["equity_value"] / total) * 100,
        "debt_allocation": (v["debt_value"] / total) * 100,
        "cash_allocation": (v["cash_value"] / total) * 100,
        "other_allocation": (v["other_value"] / total) * 100,
    }


def _stock_average(v: dict[str, float]) -> dict[str, float]:
    total_qty = v["existing_quantity"] + v["new_quantity"]
    total_cost = (v["existing_quantity"] * v["existing_average_price"]) + (v["new_quantity"] * v["new_purchase_price"])
    average = total_cost / total_qty if total_qty else 0
    return {"total_quantity": total_qty, "total_cost": total_cost, "average_price": average}


def _fields(*items: FieldSpec) -> tuple[FieldSpec, ...]:
    return items


EVERGREEN_CALCULATORS: tuple[EvergreenCalculator, ...] = (
    EvergreenCalculator("simple-interest-calculator", "simple_interest", "Simple Interest Calculator", "Simple Interest", "Calculate simple interest and maturity value from principal, annual rate, and time.", "Interest", "SI = P x r x t", "Principal is multiplied by the annual rate in decimal form and the number of years. Interest is not added back into principal.", "If Rs. 50,000 earns 8% simple interest for 3 years, interest is 50,000 x 0.08 x 3 = Rs. 12,000, so maturity value is Rs. 62,000.", _fields(FieldSpec("principal", "Principal Amount", 50000, 1, 1000000000, "100"), FieldSpec("annual_rate", "Annual Interest Rate", 8, 0, 100, "0.1", "%"), FieldSpec("years", "Time Period", 3, 0.1, 100, "0.1", "years")), {"interest": "Interest Earned", "maturity_value": "Maturity Value"}, _simple_interest),
    EvergreenCalculator("future-value-calculator", "future_value", "Future Value Calculator", "Future Value", "Estimate what a current amount may become after compounding at a fixed annual rate.", "Time Value", "FV = PV x (1 + r)^t", "Present value grows by the selected annual rate for each year in the time horizon.", "If Rs. 1,00,000 grows at 7% for 10 years, future value is 1,00,000 x 1.07^10.", _fields(FieldSpec("present_value", "Present Value", 100000, 1, 1000000000, "100"), FieldSpec("annual_rate", "Annual Rate", 7, 0, 100, "0.1", "%"), FieldSpec("years", "Years", 10, 0.1, 100, "0.1")), {"future_value": "Future Value", "growth": "Estimated Growth"}, _future_value),
    EvergreenCalculator("present-value-calculator", "present_value", "Present Value Calculator", "Present Value", "Convert a future amount into today's equivalent value using a discount rate.", "Time Value", "PV = FV / (1 + r)^t", "Future value is discounted back by the selected rate and number of years.", "If you need Rs. 5,00,000 in 8 years and use a 6% discount rate, present value is 5,00,000 / 1.06^8.", _fields(FieldSpec("future_value", "Future Value Needed", 500000, 1, 1000000000, "100"), FieldSpec("discount_rate", "Discount Rate", 6, 0, 100, "0.1", "%"), FieldSpec("years", "Years", 8, 0.1, 100, "0.1")), {"present_value": "Present Value", "discount_amount": "Discount Amount"}, _present_value),
    EvergreenCalculator("rule-of-72-calculator", "rule_72", "Rule of 72 Calculator", "Rule of 72", "Estimate how many years it may take an amount to double at a fixed annual return.", "Time Value", "Years to double = 72 / annual rate", "The rule divides 72 by the annual rate percentage to provide a quick approximation.", "At an 8% annual return, the doubling estimate is 72 / 8 = 9 years.", _fields(FieldSpec("annual_rate", "Annual Rate", 8, 0.1, 100, "0.1", "%")), {"estimated_years_to_double": "Estimated Years to Double"}, _rule_72),
    EvergreenCalculator("loan-amortization-calculator", "loan_amortization", "Loan Amortization Calculator", "Loan Amortization", "Estimate monthly payment, total repayment, and total interest for a fixed-rate loan.", "Loans", "Payment = P x r(1+r)^n / ((1+r)^n - 1)", "The loan amount is spread over monthly periods using a fixed monthly rate and fixed number of payments.", "For a Rs. 10,00,000 loan at 9% for 5 years, the calculator estimates the fixed monthly payment and total interest.", _fields(FieldSpec("loan_amount", "Loan Amount", 1000000, 1000, 1000000000, "1000"), FieldSpec("annual_rate", "Annual Rate", 9, 0, 100, "0.1", "%"), FieldSpec("years", "Loan Tenure", 5, 0.1, 50, "0.1", "years")), {"monthly_payment": "Monthly Payment", "total_payment": "Total Payment", "total_interest": "Total Interest"}, _loan_amortization),
    EvergreenCalculator("loan-comparison-calculator", "loan_comparison", "Loan Comparison Calculator", "Loan Comparison", "Compare two fixed-rate loan options by monthly payment and total cost.", "Loans", "Compare each loan using the amortization payment formula", "Each option is calculated separately, then monthly payments and total repayment are compared.", "Compare Loan A at 9% for 5 years with Loan B at 10% for 4 years to see the payment and total cost trade-off.", _fields(FieldSpec("loan_amount_a", "Loan A Amount", 1000000, 1000, 1000000000, "1000"), FieldSpec("rate_a", "Loan A Rate", 9, 0, 100, "0.1", "%"), FieldSpec("years_a", "Loan A Years", 5, 0.1, 50, "0.1"), FieldSpec("loan_amount_b", "Loan B Amount", 1000000, 1000, 1000000000, "1000"), FieldSpec("rate_b", "Loan B Rate", 10, 0, 100, "0.1", "%"), FieldSpec("years_b", "Loan B Years", 4, 0.1, 50, "0.1")), {"monthly_payment_a": "Loan A Monthly Payment", "monthly_payment_b": "Loan B Monthly Payment", "total_cost_a": "Loan A Total Cost", "total_cost_b": "Loan B Total Cost", "cost_difference": "Total Cost Difference"}, _loan_comparison),
    EvergreenCalculator("extra-payment-calculator", "extra_payment", "Extra Payment Calculator", "Extra Payment", "Estimate how an additional monthly loan payment may reduce payoff time and interest.", "Loans", "Simulate loan payoff using standard payment plus extra payment", "The calculator compares the original amortization schedule with a higher monthly payment.", "If your normal payment is Rs. 20,000 and you add Rs. 5,000 per month, the principal reduces faster and interest falls.", _fields(FieldSpec("loan_amount", "Loan Amount", 1000000, 1000, 1000000000, "1000"), FieldSpec("annual_rate", "Annual Rate", 9, 0, 100, "0.1", "%"), FieldSpec("years", "Original Years", 5, 0.1, 50, "0.1"), FieldSpec("extra_monthly_payment", "Extra Monthly Payment", 5000, 0, 10000000, "100")), {"standard_monthly_payment": "Standard Monthly Payment", "new_months_to_payoff": "New Months to Payoff", "interest_saved": "Interest Saved"}, _extra_payment),
    EvergreenCalculator("prepayment-savings-calculator", "prepayment_savings", "Prepayment Savings Calculator", "Prepayment Savings", "Estimate interest saved from making a one-time loan prepayment while keeping the same payment.", "Loans", "Compare remaining-loan interest before and after prepayment", "A one-time prepayment lowers outstanding principal; the same payment then retires the loan sooner.", "If Rs. 8,00,000 remains and you prepay Rs. 1,00,000, interest is calculated on the lower balance going forward.", _fields(FieldSpec("outstanding_balance", "Outstanding Balance", 800000, 1000, 1000000000, "1000"), FieldSpec("annual_rate", "Annual Rate", 9, 0, 100, "0.1", "%"), FieldSpec("remaining_years", "Remaining Years", 5, 0.1, 50, "0.1"), FieldSpec("one_time_prepayment", "One-Time Prepayment", 100000, 0, 1000000000, "1000")), {"monthly_payment_used": "Monthly Payment Used", "new_months_to_payoff": "New Months to Payoff", "interest_saved": "Interest Saved"}, _prepayment_savings),
    EvergreenCalculator("savings-calculator", "savings", "Savings Calculator", "Savings", "Project future savings from current balance, monthly saving, rate, and time.", "Savings", "FV = current balance growth + monthly saving future value", "Current savings compound first, and monthly savings are accumulated across the selected period.", "Starting with Rs. 50,000 and saving Rs. 5,000 monthly at 6% for 5 years creates a future savings estimate.", _fields(FieldSpec("current_savings", "Current Savings", 50000, 0, 1000000000, "100"), FieldSpec("monthly_saving", "Monthly Saving", 5000, 0, 10000000, "100"), FieldSpec("annual_rate", "Annual Rate", 6, 0, 100, "0.1", "%"), FieldSpec("years", "Years", 5, 0.1, 100, "0.1")), {"future_savings": "Future Savings", "total_contributions": "Total Contributions", "growth": "Estimated Growth"}, _savings),
    EvergreenCalculator("budget-planner", "budget_planner", "Budget Planner", "Budget Planner", "Review monthly income allocation across needs, wants, debt payments, and planned savings.", "Savings", "Surplus = income - total allocations", "The planner subtracts major monthly buckets from income and estimates savings rate.", "With Rs. 1,00,000 income, Rs. 50,000 needs, Rs. 20,000 wants, Rs. 10,000 debt, and Rs. 15,000 savings, surplus is Rs. 5,000.", _fields(FieldSpec("monthly_income", "Monthly Income", 100000, 1, 1000000000, "100"), FieldSpec("needs", "Needs", 50000, 0, 1000000000, "100"), FieldSpec("wants", "Wants", 20000, 0, 1000000000, "100"), FieldSpec("debt_payments", "Debt Payments", 10000, 0, 1000000000, "100"), FieldSpec("planned_savings", "Planned Savings", 15000, 0, 1000000000, "100")), {"monthly_surplus": "Monthly Surplus", "total_allocated": "Total Allocated", "savings_rate": "Savings Rate"}, _budget),
    EvergreenCalculator("debt-payoff-calculator", "debt_payoff", "Debt Payoff Calculator", "Debt Payoff", "Estimate how long it may take to repay debt with a fixed monthly payment.", "Debt", "Months use amortization payoff math", "The calculator checks whether the payment covers monthly interest, then estimates payoff time and total interest.", "A Rs. 2,00,000 balance at 18% with Rs. 10,000 monthly payment can be converted into approximate payoff months.", _fields(FieldSpec("debt_balance", "Debt Balance", 200000, 1, 1000000000, "100"), FieldSpec("annual_rate", "Annual Rate", 18, 0, 100, "0.1", "%"), FieldSpec("monthly_payment", "Monthly Payment", 10000, 1, 10000000, "100")), {"months_to_payoff": "Months to Payoff", "years_to_payoff": "Years to Payoff", "total_interest": "Total Interest"}, _debt_payoff),
    EvergreenCalculator("debt-to-income-ratio-calculator", "dti", "Debt-to-Income Ratio Calculator", "Debt-to-Income Ratio", "Calculate monthly debt payments as a percentage of gross monthly income.", "Debt", "DTI = monthly debt payments / gross monthly income x 100", "The ratio compares recurring monthly debt commitments with gross monthly income.", "If monthly debt payments are Rs. 25,000 and gross monthly income is Rs. 1,00,000, DTI is 25%.", _fields(FieldSpec("monthly_debt_payments", "Monthly Debt Payments", 25000, 0, 1000000000, "100"), FieldSpec("gross_monthly_income", "Gross Monthly Income", 100000, 1, 1000000000, "100")), {"debt_to_income_ratio": "Debt-to-Income Ratio", "monthly_income_after_debt": "Income After Debt"}, _dti),
    EvergreenCalculator("financial-freedom-calculator", "financial_freedom", "Financial Freedom Calculator", "Financial Freedom", "Estimate a target corpus and timeline based on annual expenses, savings, return, and withdrawal rate.", "Freedom", "Target corpus = annual expenses / withdrawal rate", "The calculator estimates a corpus that could theoretically support expenses, then projects savings toward that target.", "If expenses are Rs. 12,00,000 and withdrawal rate is 4%, the target corpus is Rs. 3 crore before personal adjustments.", _fields(FieldSpec("annual_expenses", "Annual Expenses", 1200000, 1, 1000000000, "1000"), FieldSpec("current_savings", "Current Savings", 1000000, 0, 1000000000, "1000"), FieldSpec("monthly_savings", "Monthly Savings", 50000, 0, 10000000, "1000"), FieldSpec("annual_return", "Annual Return", 8, 0, 100, "0.1", "%"), FieldSpec("withdrawal_rate", "Withdrawal Rate", 4, 0.1, 20, "0.1", "%")), {"target_corpus": "Target Corpus", "months_to_target": "Months to Target", "years_to_target": "Years to Target", "remaining_gap": "Current Gap"}, _financial_freedom),
    EvergreenCalculator("purchasing-power-calculator", "purchasing_power", "Purchasing Power Calculator", "Purchasing Power", "Estimate how inflation can reduce the future buying power of today's money.", "Inflation", "Future purchasing power = amount / (1 + inflation)^years", "The current amount is discounted by inflation across the selected years.", "At 6% inflation, Rs. 1,00,000 after 10 years has purchasing power of about Rs. 55,840 in today's terms.", _fields(FieldSpec("current_amount", "Current Amount", 100000, 1, 1000000000, "100"), FieldSpec("inflation_rate", "Inflation Rate", 6, 0, 100, "0.1", "%"), FieldSpec("years", "Years", 10, 0.1, 100, "0.1")), {"future_purchasing_power": "Future Purchasing Power", "purchasing_power_loss": "Purchasing Power Loss"}, _purchasing_power),
    EvergreenCalculator("real-rate-of-return-calculator", "real_rate", "Real Rate of Return Calculator", "Real Rate of Return", "Convert a nominal return into an inflation-adjusted real return estimate.", "Inflation", "Real return = ((1 + nominal) / (1 + inflation)) - 1", "Nominal return is adjusted by inflation to show approximate purchasing-power growth.", "If nominal return is 10% and inflation is 6%, real return is about 3.77%.", _fields(FieldSpec("nominal_return", "Nominal Return", 10, -99, 100, "0.1", "%"), FieldSpec("inflation_rate", "Inflation Rate", 6, 0, 100, "0.1", "%")), {"real_rate_of_return": "Real Rate of Return"}, _real_rate),
    EvergreenCalculator("investment-growth-calculator", "investment_growth", "Investment Growth Calculator", "Investment Growth", "Estimate investment value using starting amount, monthly contribution, return, and time.", "Investment", "Future value combines lump sum and recurring contribution growth", "The starting amount compounds, while monthly contributions accumulate using monthly return assumptions.", "Investing Rs. 1,00,000 plus Rs. 10,000 per month at 8% for 10 years estimates long-term investment growth.", _fields(FieldSpec("initial_investment", "Initial Investment", 100000, 0, 1000000000, "100"), FieldSpec("monthly_contribution", "Monthly Contribution", 10000, 0, 10000000, "100"), FieldSpec("annual_return", "Annual Return", 8, 0, 100, "0.1", "%"), FieldSpec("years", "Years", 10, 0.1, 100, "0.1")), {"future_savings": "Future Value", "total_contributions": "Total Contributions", "growth": "Estimated Growth"}, _investment_growth),
    EvergreenCalculator("wealth-accumulation-calculator", "wealth_accumulation", "Wealth Accumulation Calculator", "Wealth Accumulation", "Project wealth accumulation from initial savings, ongoing contributions, return, and time.", "Investment", "Estimated wealth = initial growth + contribution growth", "The calculator separates total contributions from estimated growth so the result is easier to interpret.", "A long horizon makes the growth component more visible, especially when monthly contributions continue consistently.", _fields(FieldSpec("initial_investment", "Initial Wealth", 200000, 0, 1000000000, "100"), FieldSpec("monthly_contribution", "Monthly Addition", 15000, 0, 10000000, "100"), FieldSpec("annual_return", "Annual Return", 8, 0, 100, "0.1", "%"), FieldSpec("years", "Years", 15, 0.1, 100, "0.1")), {"estimated_wealth": "Estimated Wealth", "total_contributions": "Total Contributions", "growth": "Estimated Growth"}, _wealth_accumulation),
    EvergreenCalculator("portfolio-return-calculator", "portfolio_return", "Portfolio Return Calculator", "Portfolio Return", "Estimate weighted portfolio return from asset values and expected returns.", "Portfolio", "Portfolio return = sum(weight x asset return)", "Each asset return is weighted by that asset's share of total portfolio value.", "If equity is 60% at 10%, debt is 30% at 6%, and cash is 10% at 3%, weighted return is 8.1%.", _fields(FieldSpec("asset_a_value", "Asset A Value", 600000, 0, 1000000000, "100"), FieldSpec("asset_a_return", "Asset A Return", 10, -99, 100, "0.1", "%"), FieldSpec("asset_b_value", "Asset B Value", 300000, 0, 1000000000, "100"), FieldSpec("asset_b_return", "Asset B Return", 6, -99, 100, "0.1", "%"), FieldSpec("asset_c_value", "Asset C Value", 100000, 0, 1000000000, "100"), FieldSpec("asset_c_return", "Asset C Return", 3, -99, 100, "0.1", "%")), {"portfolio_return": "Portfolio Return", "portfolio_value": "Portfolio Value"}, _portfolio_return),
    EvergreenCalculator("portfolio-allocation-calculator", "portfolio_allocation", "Portfolio Allocation Calculator", "Portfolio Allocation", "Calculate portfolio allocation percentages across equity, debt, cash, and other assets.", "Portfolio", "Allocation = asset value / total portfolio value x 100", "Each asset bucket is divided by total portfolio value to estimate allocation percentage.", "If total portfolio is Rs. 10,00,000 and equity is Rs. 6,00,000, equity allocation is 60%.", _fields(FieldSpec("equity_value", "Equity Value", 600000, 0, 1000000000, "100"), FieldSpec("debt_value", "Debt Value", 300000, 0, 1000000000, "100"), FieldSpec("cash_value", "Cash Value", 100000, 0, 1000000000, "100"), FieldSpec("other_value", "Other Assets", 0, 0, 1000000000, "100")), {"total_portfolio": "Total Portfolio", "equity_allocation": "Equity Allocation", "debt_allocation": "Debt Allocation", "cash_allocation": "Cash Allocation", "other_allocation": "Other Allocation"}, _portfolio_allocation),
    EvergreenCalculator("stock-average-calculator", "stock_average", "Stock Average Calculator", "Stock Average", "Calculate the average purchase price after buying additional shares or units.", "Portfolio", "Average price = total cost / total quantity", "Existing cost and new purchase cost are added, then divided by total quantity.", "If you own 10 shares at Rs. 100 and buy 5 more at Rs. 80, average price becomes Rs. 93.33.", _fields(FieldSpec("existing_quantity", "Existing Quantity", 10, 0, 100000000, "1"), FieldSpec("existing_average_price", "Existing Average Price", 100, 0, 100000000, "0.01"), FieldSpec("new_quantity", "New Quantity", 5, 0, 100000000, "1"), FieldSpec("new_purchase_price", "New Purchase Price", 80, 0, 100000000, "0.01")), {"total_quantity": "Total Quantity", "total_cost": "Total Cost", "average_price": "Average Price"}, _stock_average),
)


def get_calculator(slug: str) -> EvergreenCalculator | None:
    return next((item for item in EVERGREEN_CALCULATORS if item.slug == slug), None)


def calculator_cards() -> list[dict[str, str]]:
    return [{"title": item.short_title, "href": item.path, "description": item.description, "category": item.category} for item in EVERGREEN_CALCULATORS]


def defaults_for(calculator: EvergreenCalculator) -> dict[str, float]:
    return {field.name: field.default for field in calculator.fields}


def validate_inputs(calculator: EvergreenCalculator, raw_values: dict[str, object]) -> tuple[dict[str, float] | None, str | None]:
    cleaned: dict[str, float] = {}
    for field in calculator.fields:
        raw = raw_values.get(field.name)
        if raw is None or raw == "":
            return None, f"{field.label} is required."
        try:
            value = float(raw)
        except (TypeError, ValueError):
            return None, f"Please enter a valid {field.label.lower()}."
        if not isfinite(value) or value < field.min_value or value > field.max_value:
            return None, f"Please enter a valid {field.label.lower()}."
        cleaned[field.name] = value
    return cleaned, None


def calculate(calculator: EvergreenCalculator, values: dict[str, float]) -> dict[str, float]:
    return calculator.calculator(values)


def related_calculators(calculator: EvergreenCalculator) -> list[dict[str, str]]:
    existing = [
        {"title": "SIP Calculator", "href": "/tools/sip-calculator"},
        {"title": "Compound Interest Calculator", "href": "/tools/compound-interest-calculator"},
        {"title": "EMI Calculator", "href": "/tools/emi-calculator"},
        {"title": "Inflation Calculator", "href": "/tools/inflation-calculator"},
        {"title": "Net Worth Calculator", "href": "/tools/net-worth-calculator"},
    ]
    same_category = [
        {"title": item.short_title, "href": item.path}
        for item in EVERGREEN_CALCULATORS
        if item.category == calculator.category and item.slug != calculator.slug
    ]
    return (same_category + existing)[:6]


def faqs_for(calculator: EvergreenCalculator) -> list[dict[str, str]]:
    name = calculator.short_title.lower()
    return [
        {"question": f"What does the {calculator.short_title} calculator do?", "answer": f"It estimates {name} results from the numbers you enter and shows the formula-driven output for planning education."},
        {"question": "Does this calculator depend on tax slabs or government rules?", "answer": "No. This is an evergreen calculator based on stable financial math, not annual policy rules, tax slabs, bank offers, or government limits."},
        {"question": "Are the results guaranteed?", "answer": "No. Results are estimates based on your inputs. Real life can differ because of behavior, fees, market returns, product rules, timing, and data quality."},
        {"question": "What inputs should I use?", "answer": "Use realistic numbers from your own budget, loan statement, portfolio summary, or planning assumptions. Conservative inputs usually produce more useful planning conversations."},
        {"question": "Can I use this for final financial decisions?", "answer": "Use it as a starting point only. Review official documents and speak with a qualified professional before making important financial, borrowing, or investment decisions."},
        {"question": "Why do small rate changes matter?", "answer": "Rates compound or accumulate over time. A small difference may look minor in one year but become meaningful across long horizons or large balances."},
        {"question": "Should I round the output?", "answer": "Yes. Treat the result as an approximate planning estimate. Rounding helps you focus on decisions instead of false precision."},
        {"question": "How often should I revisit the calculation?", "answer": "Revisit it when income, expenses, loan balances, savings rates, time horizon, or expected returns change materially."},
        {"question": "Does the calculator store my inputs?", "answer": "No account is required. The page is designed for privacy-friendly educational calculations rather than storing personal financial records."},
        {"question": "Which calculators should I compare with this one?", "answer": "Use the related calculators on this page to compare adjacent questions such as growth, inflation, loan cost, savings discipline, allocation, or net worth."},
    ]


def educational_sections(calculator: EvergreenCalculator) -> list[dict[str, str]]:
    return [
        {"heading": "Introduction", "body": f"The {calculator.short_title} calculator is designed for a practical planning question that does not depend on annual rule changes. It turns a rough financial idea into a visible estimate using transparent math and plain inputs. The goal is not perfect prediction; it is to expose assumptions and make the next question clearer."},
        {"heading": "What is this calculator?", "body": f"This calculator estimates {calculator.description.lower()} It belongs to the {calculator.category.lower()} planning area and uses stable formulas that remain useful across years. Because it is not tied to tax slabs, government limits, employer policy, or lender campaigns, it can stay educational while products around it change."},
        {"heading": "Formula", "body": calculator.formula},
        {"heading": "Formula explanation", "body": calculator.formula_explanation + " The calculator applies the same logic consistently each time. If the output looks surprising, change one input at a time and observe which assumption drives the result."},
        {"heading": "Step-by-step example", "body": calculator.example + " Replace the sample numbers with your own figures, then run conservative, moderate, and optimistic cases. Comparing scenarios usually teaches more than relying on one estimate."},
        {"heading": "Benefits", "body": f"The main benefit of the {calculator.short_title} calculator is clarity. It separates the core math from emotion, marketing language, and memory-based guesses. It can show whether a goal is realistic, a payment is comfortable, a return assumption is stretched, or an allocation is concentrated."},
        {"heading": "Limitations", "body": "Every calculator has boundaries. This one assumes the inputs are accurate and that the selected rate or payment pattern remains constant unless a field says otherwise. It does not include every fee, tax, penalty, liquidity limit, behavioral change, or market shock. Official product documents should override simplified estimates."},
        {"heading": "Common mistakes", "body": "Common mistakes include using an attractive return without evidence, ignoring inflation, mixing monthly and annual figures, entering stale balances, and treating the estimate as a promise. Also compare timelines carefully; a better-looking output is not automatically a better decision."},
        {"heading": "Best practices", "body": "Use current numbers, keep assumptions conservative, and note why you selected each rate or time period. Run more than one scenario and focus on direction rather than false precision. For major decisions, use this page as preparation for deeper review."},
        {"heading": "Related calculators", "body": "Compare this result with the related calculators below. Financial decisions rarely live alone: loans affect savings, savings affect future value, allocation affects weighted return, and inflation affects purchasing power."},
        {"heading": "Educational note", "body": "FinCalX calculators are built for education and planning literacy. The best use of this page is to improve your questions before you commit money, sign paperwork, change investments, or restructure debt."},
        {"heading": "Disclaimer", "body": "This page is for informational and educational purposes only. It is not financial, investment, tax, legal, lending, or professional advice. Verify important numbers independently and consult qualified professionals before making financial decisions."},
    ]
