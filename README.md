# Goodreads




### To initialize docker containers:
Locate directory:
```
cd .\software-architecture\goodreads\
```
To build docker:
```
docker-compose -f docker-composeX.yml up --build
```
with elasticsearch for some reason it works the third time you run the command, so you can run it again and it will work.
To quit docker:
```
Ctrl+C
```
To deconstruct docker:
```
docker-compose down
```

### Application URL:
```
http://127.0.0.1:8000/
```

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


### To initialize django aplication (Windows):
```
cd software-architecture/goodreads
py manage.py runserver
```
#### Apply migrations:
```
python manage.py migrate
```

#### If css does not work:
```
python manage.py collectstatic
```

#### Run the Seed Script:
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
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

REDIS_URL = 'redis://127.0.0.1:6379/1'
```
