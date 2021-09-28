"""Base settings used by all types of deployment"""
import os
from dotenv import load_dotenv, find_dotenv

from estore.utils import required_env_var

load_dotenv(find_dotenv())


# DJANGO
SECRET_KEY = required_env_var("SECRET_KEY")

# DB
DB_NAME = required_env_var("DB_NAME")
DB_USERNAME = required_env_var("DB_USERNAME")
DB_PASSWORD = required_env_var("DB_PASSWORD")
DB_HOST = required_env_var("DB_HOST")
DB_PORT = required_env_var("DB_PORT")

# Sentry
SENTRY_DSN = required_env_var("SENTRY_DSN")

# Sendgrid
SENDGRID_API_KEY = required_env_var("SENDGRID_API_KEY")
