from typing import Annotated, Literal

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


def _validate_form(model_class: type[BaseModel], **values):
    try:
        return model_class(**values)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc


def _friendly_error(err: dict) -> str:
    """Convert a Pydantic error dict into a user-friendly message."""
    loc = err.get("loc", [])
    field = loc[-1] if loc else "input"
    msg = err.get("msg", "")
    error_type = err.get("type", "")

    if "greater_than_equal" in error_type or "less_than_equal" in error_type or "too_large" in error_type or "too_small" in error_type:
        return f"Please enter a valid {field.replace('_', ' ')}."
    if "missing" in error_type:
        return f"{field.replace('_', ' ').title()} is required."
    if "invalid_literal" in error_type:
        return "Please select a valid option."
    if "max_length" in error_type:
        return f"{field.replace('_', ' ').title()} is too long."
    if "min_length" in error_type:
        return f"{field.replace('_', ' ').title()} is too short."
    if "invalid" in str(msg).lower():
        return f"Invalid {field.replace('_', ' ')}."
    return msg or f"Invalid {field.replace('_', ' ')}."


def validate_form_data(model_class: type[BaseModel], values: dict):
    """Validate form data and return (instance_or_none, field_errors_dict, general_error_or_none)."""
    try:
        return model_class(**values), {}, None
    except ValidationError as exc:
        field_errors: dict[str, str] = {}
        messages = []
        for err in exc.errors():
            loc = err.get("loc", [])
            field = str(loc[-1]) if loc else "input"
            friendly = _friendly_error(err)
            if field not in field_errors:
                field_errors[field] = friendly
            messages.append(friendly)
        general = messages[0] if messages else "Please check your inputs and try again."
        return None, field_errors, general


class SIPInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    monthly_investment: Annotated[float, Field(ge=100, le=10000000)]
    annual_rate: Annotated[float, Field(ge=0, le=40)]
    years: Annotated[int, Field(ge=1, le=60)]

    @classmethod
    def as_form(
        cls,
        monthly_investment: float = Form(...),
        annual_rate: float = Form(...),
        years: int = Form(...),
    ) -> "SIPInput":
        return _validate_form(
            cls,
            monthly_investment=monthly_investment,
            annual_rate=annual_rate,
            years=years,
        )


class EMIInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    loan_amount: Annotated[float, Field(ge=1000, le=100000000)]
    annual_rate: Annotated[float, Field(ge=0, le=50)]
    years: Annotated[int, Field(ge=1, le=40)]

    @classmethod
    def as_form(
        cls,
        loan_amount: float = Form(...),
        annual_rate: float = Form(...),
        years: int = Form(...),
    ) -> "EMIInput":
        return _validate_form(cls, loan_amount=loan_amount, annual_rate=annual_rate, years=years)


class TaxInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    gross_income: Annotated[float, Field(ge=0, le=100000000)]
    regime: Literal["new", "old"]
    deductions: Annotated[float, Field(ge=0, le=10000000)] = 0

    @field_validator("gross_income", "deductions", mode="before")
    @classmethod
    def reject_negative(cls, value):
        if value is not None and value != "":
            try:
                num = float(value)
            except (TypeError, ValueError):
                return value
            if num < 0:
                raise ValueError("Cannot be negative")
        return value

    @classmethod
    def as_form(
        cls,
        gross_income: float = Form(...),
        regime: Literal["new", "old"] = Form(...),
        deductions: float = Form(0),
    ) -> "TaxInput":
        return _validate_form(cls, gross_income=gross_income, regime=regime, deductions=deductions)


class SalaryInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    ctc: Annotated[float, Field(ge=1000, le=100000000)]
    basic_pct: Annotated[float, Field(ge=0, le=100)]
    hra_pct: Annotated[float, Field(ge=0, le=100)]
    other_allowances: Annotated[float, Field(ge=0, le=10000000)] = 0
    pf_pct: Annotated[float, Field(ge=0, le=100)]
    tax_pct: Annotated[float, Field(ge=0, le=100)]

    @classmethod
    def as_form(
        cls,
        ctc: float = Form(...),
        basic_pct: float = Form(...),
        hra_pct: float = Form(...),
        other_allowances: float = Form(0),
        pf_pct: float = Form(...),
        tax_pct: float = Form(...),
    ) -> "SalaryInput":
        return _validate_form(
            cls,
            ctc=ctc,
            basic_pct=basic_pct,
            hra_pct=hra_pct,
            other_allowances=other_allowances,
            pf_pct=pf_pct,
            tax_pct=tax_pct,
        )


class OverlapInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    first_portfolio: Annotated[str, Field(min_length=1, max_length=5000)]
    second_portfolio: Annotated[str, Field(min_length=1, max_length=5000)]

    @classmethod
    def as_form(
        cls,
        first_portfolio: str = Form(...),
        second_portfolio: str = Form(...),
    ) -> "OverlapInput":
        return _validate_form(cls, first_portfolio=first_portfolio, second_portfolio=second_portfolio)

    @field_validator("first_portfolio", "second_portfolio")
    @classmethod
    def reject_markup(cls, value: str) -> str:
        value = value.strip()
        # Block potential XSS/injection patterns
        dangerous = ["<", ">", "script", "javascript:", "onerror", "onload"]
        lower = value.lower()
        for pattern in dangerous:
            if pattern in lower:
                raise ValueError("Please enter stock names only.")
        return value
