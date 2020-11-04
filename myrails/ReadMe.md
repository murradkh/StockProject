# MySQL Database Setup

## Project Requirements
This pull request adds `mysqlclient==2.0.1` to the `requirments.txt` file. You will need to rerun the command:
    
        pip install -r requirements.txt

## SQLite Data Migration (Optional)
If you would like to move over the data stored in the SQLite db, you will first need to [dump your existing data into a .json file](https://www.shubhamdipt.com/blog/django-transfer-data-from-sqlite-to-another-database/)

Make sure your inside your `settings.py` file, you are still using the old SQLite 3 configuration:

        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

Then, run the following command in your IDE terminal:

        python manage.py dumpdata > db.json

## Localhost MySQL Server on Development Machine
Follow [these instructions](https://ladvien.com/data-analytics-mysql-localhost-setup/) to set up and run a local MySQL server.

To avoid having multiple versions of the `settings.py`file
amongst us, set up the local server with these parameters:

| Parameter | Value       |
|-----------|:-----------:|
| Host      | localhost   |
| Port      | 3306        |
| User      | root        |
| Password  | project1234 |


<br/>Afterwards, use the MySQL console to create a database:

        CREATE DATABASE project_db;
        

<br/>**_Make sure your `settings.py` has the db configuration below:_**

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'project_db',
                'HOST': 'localhost',
                'PORT': '3306',
                'USER': 'root',
                'PASSWORD': 'project1234',
            },
            'OPTIONS': {
                'connect_timeout': 20,
            }
        }


<br/>Now, in your IDE terminal, excute the following commands:

        python manage.py migrate

_If you exported your SQLite data into a .json file in the optional step above, you can now [load it into the new db](https://www.shubhamdipt.com/blog/django-transfer-data-from-sqlite-to-another-database/)_

<br/>If there are no migration errors, you can go ahead and run:

        python manage.py runserver

The Django server should now be running using the new MySQL db server. <br/><br/>


## Remote MySQL Server on Production Server
The production server uses the `settings_server.py` file instead, which has a different `DATABASES` configuration similar to this:


        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'dbmaster',
                'USER': 'dbmasteruser',
                'PASSWORD': 'T**********',          # Password hidden here
                'HOST': 'ls-....rds.amazonaws.com', # Not full hostname
                'PORT': '3306',
            },
            'OPTIONS': {
                'connect_timeout': 20,
            }
        }

**_Here, we may need to migrate the existing data on the SQLite dbas described above._**<br/><br/>

To run the Django server:

        python manage.py migrate
        python manage.py runserver --settings=myrails.settings_server

Note the additional settings argument in the runsever command.

To avoid manaully specifying this each time, we can tell Django to use `settings_server.py` by default by defining an [environmental varaible](https://docs.djangoproject.com/en/3.1/topics/settings/#envvar-DJANGO_SETTINGS_MODULE)
