from flask import Flask
from flask import render_template
from flask import request
import blogimporter
import requests
from bs4 import BeautifulSoup
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
            if "blog.wikimedia.org" not in url:
                raise RuntimeError("The URL" + url + "does not reference the Wikimedia Blog.")
            r = requests.get(url)
            if r.status_code != 200:
                raise RuntimeError("The blog post located at URL " + url + "could not be resolved.")
            post = r.text[r.text.index('<div class="entry">') + len('<div class="entry">'):]
            post = post[:post.index('<div class="socials">')]
            post = post[:post.rindex('</div>')]
            post = post.replace("	", "")
            post = requests.post('http://rest.wikimedia.org/en.wikipedia.org/v1/transform/html/to/wikitext',
                                data={'html': post}).text
            post = BeautifulSoup(post, "html.parser")
            post = post.get_text()
            return render_template('blog_importer.html', code_returned=post)

if __name__ == '__main__':
    app.run(debug=True)