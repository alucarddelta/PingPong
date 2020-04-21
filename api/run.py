from app import app
import logging

if __name__ == "__main__":
    app.run()
else:
    gunicornlogger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicornlogger.handlers
    app.logger.setLevel(gunicornlogger.level)
