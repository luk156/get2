from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import *
import fabtools
from fabric.contrib import django

env.shell = "/bin/bash -c -l"
env.hosts = ['django@luccalug.it',]

virtualenv_dir = "/home/django/stable-env/"

def runserver():
	with prefix("source ~/.bashrc"):
		with prefix("workon get2"):
			local("python manage.py runserver")



def deploy(name):
	if exists("~/%s" % name):
		print(red("Error: Directory gia esistente!"))
	else:
		run("mkdir ~/%s" % name)
		with cd("~/%s" % name):
			fabtools.require.git.working_copy("https://github.com/luk156/get2.git")
			password = create_database(name)
			with cd("get2"):
				configure(name,password)
				with fabtools.python.virtualenv(virtualenv_dir):
					run("python manage.py syncdb")
					run("python manage.py migrate")
					run("python manage.py collectstatic --noinput")
				run ("cp get2/get2.wsgi.sample get2/get2.wsgi")
				sed("get2/get2.wsgi", "_envdir_", virtualenv_dir)
				sed("virtualhost.sample", "_name_", name)
				sudo ("cp virtualhost.sample /etc/apache2/sites-available/%s.conf" % name)
				fabtools.require.apache.enable_site(name)
		fabtools.require.service.restarted('apache2')


def configure(name, password):
	run ("cp get2/settings.py.sample get2/settings.py")
	sed("get2/settings.py", "_database_", name)
	sed("get2/settings.py", "_user_", name)
	sed("get2/settings.py", "_titolo_", name)
	sed("get2/settings.py", "_password_", password)

def create_database(name):
	with settings(mysql_user='root', mysql_password='Franchini03'):
		password = prompt("Inserisci la password per l'utente: %s" % name)
		if not fabtools.mysql.user_exists(name):
			fabtools.mysql.create_user(name, password)
		else:
			change_user_password(name, password)
		fabtools.require.mysql.database(name, owner=name)
		return password

def update(name):
	with cd("~/%s" % name):
		fabtools.require.git.working_copy("https://github.com/luk156/get2.git")
		with fabtools.python.virtualenv(virtualenv_dir):
			run("python get2/manage.py migrate")
			run("python get2/manage.py collectstatic --noinput")
	fabtools.require.service.restarted('apache2')

from fabric.api import env, hide, prompt, puts, run, settings

def change_user_password(name, password, host='localhost', **kwargs):
    """
    Change password to MySQL user.

    """
    with settings(hide('running')):
        fabtools.mysql._query(	"SET PASSWORD FOR '%(name)s'@'%(host)s' = PASSWORD('%(password)s');"
      		 % {
            'name': name,
            'password': password,
            'host': host
        }, **kwargs)
    puts("Change password for MySQL user '%s'." % name)