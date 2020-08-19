Simple URL shorten service
==========================

Features
--------

- Convert an valid URL to a fixed length of URL


- Can save more than 10,000,000 unique URLs


  - 11,881,374 URLs to be exact


- Can preview or redirect to the converted URL


Developemnt guide
-----------------

- Set up Python virtual enviroment


  - Install packages from ``requirements.txt``


- Run test by ``pytest`` at ``assignment``


  - To see coverage, run ``pytest --cov=shorten_url --cov-branch --cov-report=term-missing``


- Run development server by ``python manage.py runserver 0.0.0.0:8000``


Testing scenarios
-----------------

Feature: Create path name from an URL
    A valid URL can convert to a fixed length path name

    Scenario: Create path name with valid URL
        Given an valid URL

        When I input the URL
        And I click 'Create' button

        Then I can see the created path name

    Scenario: Notify users when the URL is invalid
        Given an invalid URL

        When I input the URL
        And I click 'Create' button

        Then I can see a message about correcting the invalid URL


Feature: Preview the URL of the path name
    A registered path name can convert to corresponding URL

    Scenario: See the URL of the path name
        Given a valid path name of a registered URL

        When I input the path name
        And I turn on the preview option
        And I click 'Convert' button

        Then I can see the corresponding URL

    Scenario: Notify the user when the path name is illegal
        Given an invalid path name

        When I input the path name
        And I turn on the preview option
        And I click 'Convert' button

        Then I can see a message about correcting the invalid path name

    Scenario: Notify the user when the path name converts to nothing
        Given a valid path name

        When I input the path name
        And I turn on the preview option
        And I click 'Convert' button

        Then I can see a message about this path name converts to nothing


Feature: Redirect to the URL of the path name
    Take the user to corresponding URL of a registered path name

    Scenario: Redirect to the URL of the path name
        Given a valid path name of a registered URL

        When I input the path name
        And I turn on the redirect option
        And I click 'Convert' button

        Then I am redirected to the corresponding URL

    Scenario: Notify the user when the path name is illegal
        Given an invalid path name

        When I input the path name
        And I turn on the redirect option
        And I click 'Convert' button

        Then I can see a message about correcting the invalid path name

    Scenario: Notify the user when the path name converts to nothing
        Given a valid path name

        When I input the path name
        And I turn on the redirect option
        And I click 'Convert' button

        Then I can see a message about this path name converts to nothing
