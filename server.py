from flask import Flask
from flask import render_template
import json

import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("micro.json", "r")
    data = json.load(f)
    f.close()
    return render_template('index.html')
app.run(debug=True)