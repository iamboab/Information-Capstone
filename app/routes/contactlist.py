from app import app
from app.utils.secrets import getSecrets
import requests
from flask import render_template, flash, redirect, url_for
import requests
from flask_login import current_user
from app.classes.data import contactList
from app.classes.forms import contactList
from flask_login import login_required
import datetime as dt