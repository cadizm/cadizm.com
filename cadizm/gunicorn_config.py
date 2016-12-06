
# http://docs.gunicorn.org/en/latest/settings.html

chdir = '/opt/cadizm/cadizm'

bind = '127.0.0.1:8002'
proc_name = 'cadizm.wsgi'
pidfile = '/opt/cadizm/var/run/cadizm.pid'

import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1

reload = True
daemon = False  # use systemd
capture_output = True

user = 'www-data'
group = 'www-data'

accesslog = '/opt/cadizm/var/log/access.log'
errorlog = '/opt/cadizm/var/log/error.log'
