from unittest import TestCase

from loan_request.serializer import UserSerializer, LoanDetailSerializer, LoanRequestSerializer


class UserSerializerTest(TestCase):
    def test_serializer(self):
        data = {"firstName": "", "lastName": "", "email": "", "employmentStatus": "", "employerName": ""}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'firstName', 'lastName', 'email', 'employmentStatus'})

        data['firstName'] = "firstName"
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'lastName', 'email', 'employmentStatus'})

        data['lastName'] = "lastName"
        data['email'] = "firstName@email.com"
        data['employmentStatus'] = "SelfEmployed"
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0].__str__(), 'Employment status is invalid')
        self.assertEqual(serializer.errors['non_field_errors'][0].code, 'employmentStatus')

        data['employmentStatus'] = "Employed"
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0].code, 'employerName')

        data['employerName'] = "EL"
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        data['employmentStatus'] = "Unemployed"
        data['employerName'] = ""
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class LoanDetailSerializerTest(TestCase):
    def test_serializer(self):
        data = {"vehiclePrice": 0, "deposit": 0, "purpose": "", "term": 0}
        serializer = LoanDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'vehiclePrice', 'deposit', 'purpose', 'term'})

        data['vehiclePrice'] = -1
        serializer = LoanDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'vehiclePrice', 'deposit', 'purpose', 'term'})
        self.assertEqual(serializer.errors['vehiclePrice'][0].__str__(),
                         'Ensure this value is greater than or equal to 2000.')

        data['deposit'] = -1
        serializer = LoanDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'vehiclePrice', 'deposit', 'purpose', 'term'})
        self.assertEqual(serializer.errors['deposit'][0].__str__(),
                         'Ensure this value is greater than or equal to 1.')

        data['vehiclePrice'] = 3000
        data['deposit'] = 4000
        data['purpose'] = "Vehicle maintenance"
        data['term'] = 2
        serializer = LoanDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0].__str__(),
                         'Deposit should be less than vehicle price')
        self.assertEqual(serializer.errors['non_field_errors'][0].code, 'deposit')

        data['deposit'] = 2000
        serializer = LoanDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0].__str__(),
                         'Difference between vehicle price and deposit should be at least 2000')
        self.assertEqual(serializer.errors['non_field_errors'][0].code, 'vehiclePrice')

        data['deposit'] = 1000
        serializer = LoanDetailSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class LoanRequestSerializerTest(TestCase):
    def test_serializer(self):
        data = {"user": {'email': 'firstName@email.com', 'employerName': 'EL', 'employmentStatus': 'Employed',
                                 'firstName': 'firstName', 'lastName': 'lastName'},
                "loanDetail": {'deposit': 1000, 'purpose': 'Vehicle maintenance', 'term': 2, 'vehiclePrice': 3000}}
        serializer = LoanRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
