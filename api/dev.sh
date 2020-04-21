#!/bin/sh


gunicorn --config app/gunicorn/config-test.py run:app
