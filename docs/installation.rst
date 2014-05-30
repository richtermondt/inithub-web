Virtual Machine setup
=======================
**Install on host**

* VirtualBox
* Create Mint 15 VM

**Install on guest**

* Install emacs (Optional)
* Install MySql servers
 * root pass: TheRealThing
* Install MySql Workstation

**execute:**

#) sudo apt-get install python-pip
#) sudo pip install virtualenv
#) sudo pip install virtualenvwrapper
#) sudo pip install sphinx (optional)
#) sudo apt-get install mercurial
#) sudo apt-get install libmysqlclient-dev
#) sudo apt-get install python-dev

**create project directory**

::

    cd ~/projects/
    hg clone ssh://rtermondt@hg.solutiosoft.com/hg/django_projects
    cd django_projects
    hg pull ssh://rtermondt@hg.solutiosoft.com/hg/django_projects
    cd ~/projects/
    hg clone ssh://rtermondt@hg.solutiosoft.com/hg/ihub_static
    cd ihub_static/
    hg pull ssh://rtermondt@hg.solutiosoft.com/hg/ihub_static


**Create database**

#) create new mysql schema

::

    CREATE SCHEMA `InitHub` ;

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
    pip install -r requirements/dev.txt 

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

