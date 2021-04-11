from flask import Flask, render_template, request, json, flash
import requests, json
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '0fb59abbe2bb39814d80f1d1'

from grade import routes