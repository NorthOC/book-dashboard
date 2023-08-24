# Book dashboard with DRF + jwt-auth using python microservices as a back-end.
## Install

### Linux

``` sh
git clone git@github.com:NorthOC/book-dashboard.git
cd book-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

### windows

``` sh
git clone git@github.com:NorthOC/book-dashboard.git
cd book-dashboard\
python3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

## Explanation

The front-end is built with Django templates and the API with DRF. Calls to the database, from the front-end, are done via microservices to the API.

## DIRECTORIES

* `core/` - project files.
* `api/` - contains `BookViewSet`, serializers and JWT token endpoints. Files to look at: `views.py`, `urls.py` and `serializers.py`
* `backend/` - models. Files to look at: `models.py`.
* `frontend/` - routing, views, forms and templates. Look at: `urls.py`, `views.py` and `templates/`.
* `frontend/services.py` - functions to handle api calls.

## Database

There's a dummy database to save you some time. Feel free to make your own items and users.

admin username: `admin`
admin password: `123`

user username: `denis`
user username: `123qwe123`
