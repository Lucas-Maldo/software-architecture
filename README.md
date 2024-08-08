# Goodreads

I recommend creating a virtual environment for django and postgres

## Virtual environment (Windows)
Create virtual environment (be sure to create outside of the local repository):
```
py -m venv #name-of-environment
```

To activate enviroment:
```
#name-of-environment/Scripts/activate
```
To deactivate enviroment:
```
deactivate
```

## To initialize django aplication (Windows):
```
cd software-architecture/goodreads
py manage.py runserver
```

### if Css Not Working:
```
python manage.py collectstatic
```

## Apply migrations:
```
python manage.py migrate
```

## Run the Seed Script:
```
python manage.py seed_data
```
Sometimes the seed script does not work for all the data, so you can run it again and it will add the missing data.

## Local URL:
```
http://127.0.0.1:8000/
```

## Users:
Superuser:
```
user: admin
mail: admin@gmail.com
password: administrador
```
## DB info:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Review_app_db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',  # Set to 'localhost' or an IP address if the DB is remote
        'PORT': '5432',  # Default is '5432'
    }
}
```

## Progress:
- [X] add postgresql
