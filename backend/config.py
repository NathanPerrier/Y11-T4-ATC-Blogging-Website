from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask import Flask, Blueprint, abort, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from django.core.paginator import Paginator
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask.json import jsonify
from socket import gethostname
from datetime import datetime
from functools import wraps
import random, string
import pandas as pd
from PIL import Image 
import requests
import unittest 
import random
import bcrypt
import PIL  
import re
import os 

import googlemaps

gmaps = googlemaps.Client(key='your-google-maps-api-key')

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.session_protection = "strong" # "basic" "strong" "None"
