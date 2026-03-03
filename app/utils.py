from typing import Dict, Any

def mortgage_amortization_summary(principal: float, annual_rate: float, term_months: int, extra_payment: float = 0.0) -> Dict[str, Any]:
    if principal <= 0 or term_months <= 0:
        return {"monthly_payment": 0.0, "months_to_payoff": 0, "total_interest": 0.0}

    r = (annual_rate / 100.0) / 12.0
    if r == 0:
        base = principal / term_months
    else:
        base = principal * (r * (1 + r) ** term_months) / (((1 + r) ** term_months) - 1)

    payment = base + max(extra_payment, 0.0)
    balance = principal
    total_interest = 0.0
    months = 0

    while balance > 0 and months < term_months * 2:
        interest = balance * r
        principal_paid = payment - interest
        if principal_paid <= 0:
            return {"monthly_payment": float(payment), "months_to_payoff": None, "total_interest": None}
        balance -= principal_paid
        total_interest += interest
        months += 1

    return {"monthly_payment": float(payment), "months_to_payoff": int(months), "total_interest": float(total_interest)}
