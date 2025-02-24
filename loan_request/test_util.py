import unittest

from loan_request.util import repayment_and_lender_details


class LoanRequestUtilTest(unittest.TestCase):

    def test_repayment_and_lender_details(self):
        result = repayment_and_lender_details(5000, 1000, 1)
        self.assertEqual([r["monthly_repayment"] for r in result], [343.35, 342.43, 344.27])