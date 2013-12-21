from fabric.api import run,local

def host_type():
    run('uname -s')

def commit():
	local("git add -A && git commit")
	local("git push")