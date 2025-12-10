# Gunicorn configuration hooks for starting background services
# This file defines an `on_starting(server)` callback that Gunicorn will
# call in the master process before spawning workers. We use it to start
# the single `job_timer` background thread so it runs once globally.

import traceback
import os

# Number of gunicorn workers
workers = 4

# Bind address
bind = '0.0.0.0:8000'

# gunicorn log files
LOG_DIR = '/data/syslogs'
os.makedirs(LOG_DIR, exist_ok=True)
accesslog = os.path.join(LOG_DIR, 'access.log')
errorlog = os.path.join(LOG_DIR, 'error.log')


def on_starting(server):
    """Called just before the master process is initialized.

    Start the single job timer thread here so it runs in the master
    process (one thread total) rather than per-worker.
    """
    try:
        # Import lazily to avoid circular import problems during Gunicorn
        from app import start_job_timer, logger
        start_job_timer()
        try:
            logger.info("Started job_timer via Gunicorn on_starting")
        except Exception:
            # If logger is not available for any reason, fall back to server log
            server.log.info("Started job_timer via Gunicorn on_starting")
    except Exception as e:
        # Ensure any start errors are recorded so deployers can diagnose
        try:
            server.log.error("Failed to start job_timer in on_starting: %s", e)
            server.log.debug(traceback.format_exc())
        except Exception:
            pass
