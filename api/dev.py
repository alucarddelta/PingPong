#!/usr/bin/python3
from app import app

import threading
from test_ched import do_it
x = threading.Thread(target=do_it, daemon=True)
x.start()

if __name__ == "__main__":
    app.run(debug=app.config.get('FLASK_DEBUG'),
            host=app.config.get('FLASK_HOST'),
            port=app.config.get('FLASK_PORT'))
