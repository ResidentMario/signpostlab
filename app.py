from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! Got this server working---and Git too! (2)'

if __name__ == '__main__':
    app.run()