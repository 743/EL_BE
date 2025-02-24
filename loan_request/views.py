import json
import traceback

from django.http import JsonResponse
from django.views import View
from rest_framework import status

from loan_request.serializer import LoanRequestSerializer


class LoanRequestView(View):
    http_method_names = [
        "post",
    ]

    def post(self, request):

        serializer = LoanRequestSerializer(data=json.loads(request.body))

        if not serializer.is_valid():
            response = {}
            for k, v in serializer.errors.items():
                if k != 'non_field_errors' and isinstance(v, list):
                    response[k] = v.__str__()

                if isinstance(v, dict):
                    inner_response = {}
                    for k1, v1 in v.items():
                        inner_response[k1] = v1.__str__()

                    if k == 'non_field_errors':
                        for errorDetail in serializer.errors['non_field_errors']:
                            inner_response[errorDetail.code] = errorDetail.__str__()
                    response[k] = inner_response

                if k == 'non_field_errors':
                    for errorDetail in serializer.errors['non_field_errors']:
                        response[errorDetail.code] = errorDetail.__str__()

            if 'non_field_errors' in serializer.errors:
                for errorDetail in serializer.errors['non_field_errors']:
                    response[errorDetail.code] = errorDetail.__str__()
            return JsonResponse({'message': 'Invalid input', "data": response}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = serializer.save()
        except Exception:
            print(f"Error occurred during loan_request save: {traceback.format_exc()}")
            return JsonResponse({'message': 'Internal error occurred during loan_request save'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'message': 'Loan request was created successfully!',
                             'data': {'lender_details_and_pricing': result}},
                            status=status.HTTP_201_CREATED)
