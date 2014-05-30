Install on Webfaction 
=======================

**Add Application**

* Name: inithub
* Apache
* mod_wsgi 3.4
* python 2.7
* Django 1.5.4

**Add Application**

* Name: ihub_static
* Static only (no .htacess)

**Add domain if needed**

**Add Website**

**Install certificate**

**Test 1**

::

	It worked!
	Congratulations on your first Django-powered page.

**Create database user named inithub_[env], where [env] is target environment**

**Create MySql database named inithub**

**Create tables**

**Load tables**

**Install prerequisites**

* install pip

::

	easy_install-2.7 pip

* install Mercurial

::

	easy_install-2.7 Mercurial

* Clone source

::

    cd ~/hg/
    hg clone ssh://rtermondt@hg.solutiosoft.com/hg/django_projects
    cd django_projects
    hg pull ssh://rtermondt@hg.solutiosoft.com/hg/django_projects
    cd ~/hg/
    hg clone ssh://rtermondt@hg.solutiosoft.com/hg/ihub_static
    cd ihub_static/
    hg pull ssh://rtermondt@hg.solutiosoft.com/hg/ihub_static

* rsync source

::

	rsync -tvr --exclude-from '/home/rtermondt/hg/django_projects/solutiosoft/exclude-list.txt' /home/rtermondt/hg/django_projects/solutiosoft/ /home/rtermondt/webapps/inithub/solutiosoft/
	rsync -tvr --exclude-from '/home/rtermondt/hg/ihub_static/exclude-list.txt' /home/rtermondt/hg/ihub_static/ /home/rtermondt/webapps/ihub_static/

* install the rest of prerequisites

::

	cd ~/webapps/inithub
	pip-2.7 install -r ~/hg/django_projects/requirements/base.txt --install-option="--install-scripts=$PWD/bin" --install-option="--install-lib=$PWD/lib/python2.7"

* troubleshooting
The following packages were not installed correctly, so manually install:

::

	pip-2.7 install python-dateutil --install-option="--install-lib=$PWD/lib/python2.7"
	pip-2.7 install python-mimeparse --install-option="--install-lib=$PWD/lib/python2.7"

update httd.conf
copy settings.py
	
create custom_logs	dir

**Create db_backups dir**	

**Create mysql defaults-file named inithub.cnf**	
	
**Add cron job to backup data**

::

	0 2 * * * mysqldump --defaults-file=$HOME/db_backups/inithub.cnf -u inithub_prod inithub > $HOME/db_backups/inithub-`date +\%Y\%m\%d`.sql

**Install mailer**

**Add cron job for mailer restart**

::

	@reboot /usr/local/bin/python2.7 $HOME/bin/solutiosoft_utils/inithub/mailer-daemon.py restart > $HOME/bin/solutiosoft_utils/inithub/cron.log 2>&1
	10 * * * * /usr/local/bin/python2.7 $HOME/bin/solutiosoft_utils/inithub/mailer-daemon.py start > $HOME/bin/solutiosoft_utils/inithub/cron.log 2>&1

**Start memcached**

**Add cron job for memcahced restart on reboot**

::

	@reboot memcached -d -m 25 -s $HOME/memcached.sock -P $HOME/memcached.pid

