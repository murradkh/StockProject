# MySQL Database Setup

## STEP 1 - Install Updated Project Requirements
This pull request adds `mysqlclient==2.0.1` to the `requirments.txt` file. You will need to rerun the command:
    
        pip install -r requirements.txt

## STEP 2 - Setup Localhost MySQL Server on Development Machine
Follow [these instructions](https://ladvien.com/data-analytics-mysql-localhost-setup/) to set up and run a localhost MySQL server.

Then, use the MySQL console to create a database:

        CREATE DATABASE example_db;

Next, ensure the MySQL server is running, on Unix-based systems:
        
        sudo service mysql status

In Windows, go to Administrative tools > Services and check that the MySQL service is listed and running. 

## STEP 3 - Update Configuration File        
Afterwards, create a file `dev.cfg` (similar to `dev-example.cfg`) in the directory `stockproject/myrails/configuration` to match the MySQL server properties (hostname, user, password, etc...).

## STEP 4 - Add a New Environmental Variable
By default, the `settings.py` file uses the SQLite db.

To use the localhost MySQL server instead, add a new environmental variable `STOCK_PROJECT_MACHINE_TYPE` and set its value to `dev`. The `settings.py` file will now use `dev.cfg` instead.

_On the production server, the value of `STOCK_PROJECT_MACHINE_TYPE` should be set to `prod` so that `settings.py` could use the `prod.cfg` file._ 

_The `dev.cfg` and `prod.cfg` files were added to `.gitignore` so that any changes in these two files would not commited to any of the repository branches_

__You may need to restart your machine after defining a new environmental variable!__

Now, in your IDE terminal, excute the following commands:

        python manage.py migrate

If there are no migration errors, you can go ahead and run:

        python manage.py runserver

If there are errors after this step:
* Make sure the values in `dev.cfg` are correct
* Make sure the MySQL server is running
* Make sure the new environmental variable has been correctly set

Otherwise, the Django server should now be running using a local MySQL db server.
