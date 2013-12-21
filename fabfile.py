from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import *
import fabtools

env.shell = "/bin/bash -c -l"
env.hosts = ['django@luccalug.it',]

def runserver():
	with prefix("source ~/.bashrc"):
		with prefix("workon venv-get"):
			local("python manage.py runserver")

def deploy(name):
	if exists("~/%s" % name):
		print(red("Error: Directory gia esistente!"))
	else:
		run("mkdir ~/%s" % name)
		with cd("~/%s" % name):
			run("git clone https://github.com/luk156/get2.git")
			with cd("~/%s/get2" % name):
				configure(name)
			fabtools.require.service.restarted('apache2')

def configure(name):
	print name

def create_database(name):
	with settings(mysql_user='root', mysql_password='Franchini03'):
		password = prompt('Inserisci la password del nuovo database: ')
		fabtools.require.mysql.user(name, password)
		fabtools.require.mysql.database(name, owner=name)