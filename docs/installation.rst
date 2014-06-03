Virtual Machine setup
=======================
**Install on host**

* VirtualBox
* Create Ubuntu 14.04 LTS VM

**Install on guest**

* Install emacs (Optional)
* Install MySql servers
 * root pass: TheRealThing
* Install MySql Workstation

**execute:**

Note that on Ubuntu it is advised to use the distributions repository. If you are using different OS follow OS instructions for installing MySQL-python.

#) sudo apt-get install python-pip
#) sudo pip install virtualenv
#) sudo pip install virtualenvwrapper
#) sudo pip install sphinx (optional)
#) sudo apt-get install git
#) sudo apt-get install python-mysqldb


**create project directory**

::

    mkdir projects
	cd ~/projects/
    git clone https://github.com/richtermondt/inithub-web.git
    cd inithub_web
    
**Create database**

#) create new mysql schema

::

    CREATE SCHEMA `inithub` ;

#) Create data structure
    * use latest prod export: ./database/rtermondt_ihub_nodata-*.sql
    * add use statement to top of script

::

    USE InitHub;

#) create db user TODO: need to define required permissions

**Load base data**

* ./database/base_data/insert_all.sql


**Setup Virtualenv**

1) Change to project directory and execute::

    cd django_projects
    virtualenv env
    source env/bin/activate
    pip install --allow-external --allow-unverified -r requirements/dev.txt

2) Update path variables in ./solutiosoft/solutiosoft/settings.py

**Todo**

* create database structure (done)
* create base data (done)
* create db user (done)
* create virtual env (done)
* finalize requirements (done)
* install requirementsin in virtualenvn (done)
* start django!!
* troubleshoot/document any error

Questions on database:
do I need to create data for:
 
* auth_permission
* django_content_type

