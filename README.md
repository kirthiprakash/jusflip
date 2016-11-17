# Jusflip
Django powered ecomm website demo. Flip through thousands of products.

## Features
- List Products
- Filter Products by category, brand and price
- Global search (backed by elasticsearch search engine)
- Product pagination
- Responsive design

## Architecture

Uses Django python framework to open API's for product listing, filtering and search.
Product details are stored on Postgres database. Bootstrap and jquery library have been used for styling and easy DOM access.
Mustache, a small templating engine has been used to dynamically render the product layout.

Global search is backed by Elasticsearch with the help of Haystack's Django ORM styled search APIs.
If Elasticsearch is down, the search fallsback to local database (postgres). 
The search results might not be relevant during fallback.

##Installation

Please follow respective manuals to install Postgres DB and Elasticsearch search engine.
Create a Postgres user with password. Create a database and grant all priveleges to the user.

Create a virtual environment and install python packages

    >virtualenv jusflip
    >source jusflip/bin/activate
    >(jusflip) pip install -r requirements.txt

Configure database and search backend in settings.py

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jusflip',
        'USER': '<postgres user',
        'PASSWORD': 'password',
        'HOST': 'localhost'
      }
    }
    
    #Search backend
    HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': <ELASTIC_SEARCH_HOST>,
        'INDEX_NAME': 'haystack',
      },
    'db': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
      }
    }

Run Django migrations to create necassary tables in the database. Load sample products from fixtures. Build Index. Ready to launch.

    >(jusflip)cd jusflip
    >(jusflip)python manage.py makemigrations
    >(jusflip)python manage.py migrate
    >(jusflip)python manage.py loaddata store/fixtures/jusflip.json
    >(jusflip)python manage.py rebuild_index
    >(jusflip)python manage.py runserver
    System check identified no issues (0 silenced).
    November 16, 2016 - 19:25:51
    Django version 1.10.3, using settings 'jusflip.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C
