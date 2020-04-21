#!/bin/sh

gunicorn --config app/gunicorn/config-prod.py run:app