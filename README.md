
## Local setup

```bash
$ vagrant halt && vagrant destroy -f && vagrant up
$ make local_setup && make local_migrate && make local_deploy
```

## Seed bookmarks data

```bash
$ psql cadizm < data/bookmarks.pg_dump
```
