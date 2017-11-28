
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

## 360

1. Find preferred orientation in Theta S app for thumbnail
2. Upload current saved orientation to theta360
3. Screenshot phone and transfer to Dropbox
5. Scale screenshot to 512 width (maintain aspect ratio)
4. Export 512x512 to `cadizm/cadizm/cadizm/static/images/360`
