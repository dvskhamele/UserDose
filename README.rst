ProductVentory
========

ProductVentory is a products listing site, A web service application with all browser compatibility.
It provides a registration page, lists registered users and outputs CSVs as per requirements.
The code is divided is 3 segments.
    - Local
    - Production
    - Test

And is developed entirely using:-

- Python, Django (Python Web Framework), Django Rest Framework (For REST APIs), and some other required modules in backed (You may find list of base requirements under BASE/config/settings/base.py,
   - You may find local requirements under BASE/config/settings/local.py,
   - You may find production level requirements under BASE/config/settings/production.py)
- Html, css, jquery, jquery validation library, bootstrap
- Some other modules for frontend, and using Docker as for containerisation of application, database MongoDB, etc.


:License: MIT

Terminology
--------------
BASE :- Reffers project’s root or base path where this document may also found out or local.yml / production.yml may found out as, /product_ventory/


URLs & Structure
--------
- Registration /accounts/register/
    - Username (required, alphanumeric / basic symbols, must be UNIQUE)
    - Password (required,Password  character, minlength: 8, maxlength:20)
    - Confirm Password (required, Password  character, must be equal to Password)
    - Email (required, basic email validations, must be UNIQUE)
- Login /accounts/login/
    - Username (required, alphanumeric / basic symbols, must be UNIQUE)
    - Password (required,Password  character, minlength: 8, maxlength:20)
- ListProducts /
    - Upload Csv ( Requires a csv file in the order: Name,Type,Quantity,Price,Available,stock,total)
    - Export Csv ( User May select one detailed product entry to be exported as well as may select multiples and then export)
    ![image](https://drive.google.com/file/d/1v4xF3_achzHqZHdGPFZNngGBN9FjM-ZG/view)
- ListVendors /accounts/
    - No required parameter ( As authentication / session management was not necessary as per assignment)
    - Export Csv ( User May select one detailed user entry to be exported as well as may select multiples and then export)
    ![image](https://drive.google.com/file/d/1wygaE0Cz8_I6EZN8C8E5SiJuYx5HDFUF/view)
- GetUsersInCSV /api/v1/users/user_list_in_csv
    - usernames (User May select one detail to be exported as well as may select multiples and then export)
- GetProductsInCSV /api/v1/users/product_list_in_csv
    - usernames (User May select one detail to be exported as well as may select multiples and then export)
- IsUserExists /api/v1/users/check_if_exists/
    - username (Checks if required user already have an account or not, or if username is already taken or not.)


Basic Commands
--------------


Setting Up MongoDB Database
^^^^^^^^^^^^^^^^^^^^^

* To setup a **MongoDB Database**, just go to BASE/settings/base.py,
find  DATABASES and fill out / correct out the required details. Once you save it, its done.

Docker
^^^^^^
Go to terminal and run the following command to build the stack of project. ::

    $ docker-compose -f local.yml build

Or::

    $ docker-compose -f production.yml build

If you are using local.yml, Now you may run::

    $ docker-compose -f local.yml up

To Detach containers run::

    $ docker-compose -f local.yml up -d

To Migrate::

    $ docker-compose -f local.yml --rm django python manage.py makemigrations

    $ docker-compose -f local.yml --rm django python manage.py migrate

For logs::

    $ docker-compose -f local.yml logs



Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ docker-compose -f local.yml --rm django python manage.py  createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy product_ventory

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest
