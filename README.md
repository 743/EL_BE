### Built With

* Python
* Django
* Django-rest-framework

<!-- GETTING STARTED -->

## Getting Started

* Setup python virtual env
* Install dependencies from requirements.txt

<!-- USAGE EXAMPLES -->

## Usage

* To run the server, run following command in root directory:
    * python manage.py runserver
* To run the test, run following command in root directory:
    * python manage.py test

## Note

* This application will accept request just from localhost:8081. So, make sure to run the FE on port 8081 in local env.
* All requests will be persisted in [loan_request.json](db/loan_request.json)