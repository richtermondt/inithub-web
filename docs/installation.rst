Virtual Machine setup
=======================
**Install on host**

* VirtualBox
* Create Ubuntu 14.04 LTS VM

**Install on guest**


**execute:**

#) sudo apt-get install mysql-server
#) sudo apt-get install mysql-client
#) sudo apt-get install python-pip
#) sudo pip install virtualenv
#) sudo pip install virtualenvwrapper
#) sudo pip install sphinx (optional)
#) sudo apt-get install git
#) sudo apt-get install libmysqlclient-dev
#) sudo apt-get install python-dev

**Setup mysql db database scheme**

#) create new mysql schema named `inithub`
#) create new user named `web_user` with permission to inithub schema

**Clone repository**

#) mkdir projects
#) cd ~/projects/
#) git clone https://github.com/richtermondt/inithub-web.git
#) cd inithub_web

**Setup virtualenv and install prerequisites**
#) cd to project root if not already there
#) virtualenv env
#) source env/bin/activate
#) pip install --allow-external --allow-unverified -r requirements/dev.txt
    
**Create settings.py**

#) cd inithub/inithub
#) cp settings.SAMPLE settings.py
#) Edit settings.py directory paths, email configuration and misc.


**Sync database**

#) cd inithub-web/inithub/
#) python manage.py syncdb
#) When prompted to create a django user, choose no

	
**Load base data**

* ./database/base_data/insert_all.sql



