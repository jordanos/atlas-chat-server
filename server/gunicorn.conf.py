import os

workers = os.environ.get("GUNICORN_WORKERS", 1)
bind = "0.0.0.0:8000"  # Bind to all interfaces
preload_app = False

syslog = True

# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn.error.log"
# Whether to send Django output to the error log
capture_output = True
# How verbose the Gunicorn error logs should be
loglevel = "info"
