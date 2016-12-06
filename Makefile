
.PHONY: all local_setup local_deploy remote_setup remote_deploy remote_adduser_cadizm remote_letsencrypt

all:
	@echo "See this Makefile for targets"

local_setup:
	ansible-playbook --limit=local plays/setup.yml

local_deploy:
	ansible-playbook --limit=local plays/deploy.yml

local_migrate:
	ansible-playbook --limit=local plays/migrate.yml

remote_setup:
	ansible-playbook --limit=remote --user=cadizm plays/setup.yml

remote_deploy:
	ansible-playbook --limit=remote --user=cadizm plays/deploy.yml

remote_migrate:
	ansible-playbook --limit=remote --user=cadizm plays/migrate.yml

## One-time targets that should only be used in production

# note: requires python on remote host and will disable root login
remote_adduser_cadizm:
	ansible-playbook --limit=remote --user=root lib/ansible-provision/adduser-cadizm.yml

remote_letsencrypt:
	ansible-playbook --limit=remote --user=cadizm plays/enable-ssl.yml
