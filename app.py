from flask import Flask
from flask import render_template
from flask import request
import blogimporter
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('frame.html')


@app.route('/blog-importer.html', methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        return render_template('blog_importer.html')
    else:
        url = request.form['blog_post_url']
        # noinspection PyUnresolvedReferences
        if '//blog.wikimedia.org/' not in url:
            return render_template('blog_importer.html', code_returned="Failed: please enter a valid URL.")
        else:
            ret = blogimporter.fetch(url)
            return render_template('blog_importer.html', code_returned=ret)

if __name__ == '__main__':
    app.run(debug=True)