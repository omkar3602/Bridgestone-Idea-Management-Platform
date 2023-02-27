# Bridgestone-Idea-Management-Platform

Team Quark's submission for the Bridgestone Hackathon.

## Setup Instructions

* Clone the Repository

```
git clone https://github.com/omkar3602/Bridgestone-Idea-Management-Platform.git
```

* Make sure you have Python 3.x installed. Or install it from [here](https://www.python.org/downloads/).

* Install the virtualenv package.

```
pip install virtualenv
```

* Create a virtual environment.

```
virtualenv env
```

* Activate virtual environment.

```
env\Scripts\activate
```

* Install the requirements for the project.

```
pip install -r requirements.txt
```
* Create a .env file in the root directory. It sholud contain the following variables.
    * SECRET_KEY: Secret Key used by Django in `projectname\settings.py`
    * DEBUG: Describes whether the project is in development or production.
    * ADMIN_EMAIL: Email ID of sytem admin. Used for automatic mailing feature.
    * PASSWORD: Password of admin email. (If password doesn't work, app password is required).
    * WEB_URL: This is the base url of the website.

&emsp;&emsp;Example:
```
SECRET_KEY="abcdefghi"
DEBUG="False"
ADMIN_EMAIL="admin@abcd.com"
PASSWORD="12345678"
WEB_URL="http://127.0.0.1:8000/"
```
* Start the server.
```
python manage.py runserver
```

* Great! The website should be running at http://localhost:8000/
---

### System Admin credentials for testing

Email: `omkarj3602@gmail.com`

Password: `1234`

### Idea Admin credentials for testing

Email: `omkar3602@gmail.com`

Password: `1234`

### Ideator credentials for testing

Email: `landgechaitanya2002@gmail.com`

Password: `1234`

### Innovation Champion credentials for testing

Email: `rautneha372@gmail.com`

Password: `1234`
