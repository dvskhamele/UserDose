UserDose
========

UserDorse is a user listing site, A web service application with all browser compatibility.
It provides a registration page, lists registered users and outputs CSVs as per requirements. 

The code is developed entirely using

- Python, django (Python Web Framework), django rest framework (For REST APIs), and some other required modules in backed (You may find list of base requirements under BASE/config/settings/base.py, 
   - For local requirements under BASE/config/settings/local.py, 
   - For production level requirements under BASE/config/settings/production.py), 
- Html, css, jquery, jquery validation library, bootstrap 
- Some other modules for frontend, and using Docker as for containerisation of application, database MongoDB, etc.


:License: MIT

Terminology
--------------
BASE :- Reffers project’s root or base path where this document may also found out or local.yml / production.yml may found out as, /userdose/


URLs & Structure
--------
- Registration /api/v1/users/
    - Username (required, alphanumeric / basic symbols, must be UNIQUE)
    - Password (required,Password  character, minlength: 8, maxlength:20)
    - Confirm Password (required, Password  character, must be equal to Password)
    - Email (required, basic email validations, must be UNIQUE)
- List Users
- Get Users in CSV (User May select one detail to be exported as well as may select multiples and then export )


Basic Commands
--------------


Setting Up MongoDB Database
^^^^^^^^^^^^^^^^^^^^^

* To setup a **MongoDB Database**, just go to BASE/settings/base.py, 
find  DATABASES and fill out / correct out the required details. Once you save it, its done. 

Docker 
^^^^^^
* Go to terminal and run the following command to build the stack of project. ::

    $ docker-compose -f production.yml build

Now we may run::

    $ docker-compose -f local.yml up

Or::

    $ docker-compose -f production.yml up

If you are using local.yml, To Detach containers run::

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

  $ mypy userdose

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
