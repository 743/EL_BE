import json

from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loan_request.util import LENDER_DETAILS


class UserRegisterTest(APITestCase):

    def setUp(self):
        open('db/loan_request.json', 'w').close()  # This will clear the file content
        self.url = reverse('loan-request')

    def tearDown(self):
        pass

    def test_view_returns_400(self):
        """
        This test will error out due to invalid input
        :return:
        """
        data = {"user": {"firstName": "", "lastName": "", "email": "", "employmentStatus": "", "employerName": ""},
                "loanDetail": {"vehiclePrice": 0, "deposit": 0, "purpose": "", "term": 0}}
        response: JsonResponse = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], 'Invalid input')
        self.assertEqual(set(json.loads(response.content)['data'].keys()), {"user", "loanDetail"})
        self.assertEqual(set(json.loads(response.content)['data']["user"].keys()),
                         {'firstName', 'lastName', 'email', 'employmentStatus'})
        self.assertEqual(set(json.loads(response.content)['data']["loanDetail"].keys()),
                         {'vehiclePrice', 'deposit', 'purpose', 'term'})

    def test_view_returns_201(self):
        """
        This should append an entry in DB/file system
        """

        data = {"user": {"firstName": "firstName", "lastName": "lastName", "email": "lastName@email.com",
                         "employmentStatus": "Employed", "employerName": "EL Pvt ltd"},
                "loanDetail": {'deposit': 1000, 'purpose': 'Vehicle maintenance', 'term': 2, 'vehiclePrice': 3000}}
        response: JsonResponse = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['message'], 'Loan request was created successfully!')
        with open('db/loan_request.json', "r") as f:
            file_content = [json.loads(line) for line in f][0]
        self.assertEqual(file_content['user'], data['user'])
        self.assertEqual(file_content['loanDetail'], data['loanDetail'])
        self.assertIsNotNone(file_content['lender_details_and_pricing'])
        self.assertEqual(file_content['lender_details_and_pricing'], response_content['data']['lender_details_and_pricing'])
        self.assertEqual(len(response_content['data']['lender_details_and_pricing']), len(LENDER_DETAILS))
