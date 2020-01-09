from flask import Flask

app = Flask(__name__)
app.secret_key = 'my-secret-key-not-secret'
app.database_url = 'app.db'

from app import routes
