
## Local setup

```bash
$ vagrant halt && vagrant destroy -f && vagrant up
$ make local_setup && make local_migrate && make local_deploy
```

## Seed bookmarks data

```bash
$ psql cadizm < data/bookmarks.pg_dump
```

## Remote setup

1. First provisio a new box with ssh keys

```bash
local$ ssh root@remote
remote$  sudo apt-get update && sudo apt-get upgrade -y
remote$  sudo apt-get install python
remote$  ^d
local$ make remote_adduser_cadizm
local$ make remote_setup && make remote_migrate
local$ make remote_letsencrypt && make remote_deploy
```
