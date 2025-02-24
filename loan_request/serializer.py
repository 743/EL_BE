import copy
import json

from rest_framework import serializers

from loan_request.util import repayment_and_lender_details


class UserSerializer(serializers.Serializer):
    EMPLOYMENT_STATUSES = ['Employed', 'Self-Employed', 'Unemployed']

    # TODO max_length to be confirmed
    firstName = serializers.CharField(required=True, max_length=255, allow_blank=False)
    lastName = serializers.CharField(required=True, max_length=255, allow_blank=False)
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    employmentStatus = serializers.CharField(required=True, max_length=64, allow_blank=False)
    employerName = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['employmentStatus'] not in self.EMPLOYMENT_STATUSES:
            raise serializers.ValidationError("Employment status is invalid", "employmentStatus")
        if attrs['employmentStatus'] and attrs['employmentStatus'] != 'Unemployed' and not attrs[
            'employerName'].strip():
            raise serializers.ValidationError("Employer name is required", "employerName")
        return attrs


class LoanDetailSerializer(serializers.Serializer):
    # TODO max_value to be confirmed
    vehiclePrice = serializers.IntegerField(required=True, min_value=2000, max_value=1_000_000)
    deposit = serializers.IntegerField(required=True, min_value=1)
    purpose = serializers.CharField(required=True, max_length=255, allow_blank=False)
    term = serializers.IntegerField(required=True, min_value=1, max_value=7)  # in years

    def validate(self, attrs):
        if attrs['vehiclePrice'] < attrs['deposit']:
            raise serializers.ValidationError("Deposit should be less than vehicle price", "deposit")
        if (attrs['vehiclePrice'] - attrs['deposit']) < 2000:
            raise serializers.ValidationError("Difference between vehicle price and deposit should be at least 2000",
                                              "vehiclePrice")
        return attrs


class LoanRequestSerializer(serializers.Serializer):
    user = UserSerializer(required=True)
    loanDetail = LoanDetailSerializer(required=True)

    def save(self, **kwargs):
        data = copy.deepcopy(self.validated_data)
        with open('db/loan_request.json', 'a') as f:
            data['lender_details_and_pricing'] = repayment_and_lender_details(vehiclePrice=data['loanDetail']['vehiclePrice'], 
                                                                              deposit=data['loanDetail']['deposit'],
                                                                              term=data['loanDetail']['term'])
            json.dump(data, f)
            f.write("\n")

        return data['lender_details_and_pricing']
