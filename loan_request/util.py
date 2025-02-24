import copy
import math
import uuid

LENDER_DETAILS = [
    {
        "name": "Lender A",
        "fee": 10,
        "fee_type": "processing",
        "currency": "AUD",
        "interest_rate": 5.5,
        "id": uuid.uuid4().__str__()
    },
    {
        "name": "Lender b",
        "fee": 15,
        "fee_type": "application",
        "currency": "AUD",
        "interest_rate": 5,
        "id": uuid.uuid4().__str__()
    },
    {
        "name": "Lender A",
        "fee": 0,
        "fee_type": None,
        "currency": "AUD",
        "interest_rate": 6,
        "id": uuid.uuid4().__str__()
    }
]


def repayment_and_lender_details(vehiclePrice, deposit, term):
    loan_amount = vehiclePrice - deposit
    term_in_months = term * 12
    results = []
    for lender in LENDER_DETAILS:
        result = copy.deepcopy(lender)
        monthly_interest_rate = result["interest_rate"] / 1200
        monthly_repayment = (
            (loan_amount * monthly_interest_rate*(math.pow(1 + monthly_interest_rate, term_in_months))) /
                (math.pow((1 + monthly_interest_rate), term_in_months) - 1)
        )  # M = P [r(1+r)^n] / [(1+r)^n – 1]
        result["monthly_repayment"] = round(monthly_repayment, 2)
        results.append(result)

    return results