from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    # return 'Hello World! Got this server working---and Git too! (2)'
    return render_template('frame.html')


if __name__ == '__main__':
    app.run(debug=True)