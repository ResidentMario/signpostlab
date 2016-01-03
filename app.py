from flask import Flask
from flask import render_template
from flask import request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)


def fetch(url):
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
    linefeed = post.split("\n")
    for line_num in range(0, len(linefeed)):
        # Remove blog-hosted images and their captions.
        if "wikimediablog.files.wordpress" in linefeed[line_num]:
            post = post.replace(linefeed[line_num], "")
            if linefeed[line_num + 1][:2] == "''":
                post = post.replace(linefeed[line_num + 1], "")
            elif linefeed[line_num + 2][:2] == "''":
                post = post.replace(linefeed[line_num + 1], "")
        # But convert Commons ones.
        elif "https://upload.wikimedia.org" in linefeed[line_num]:
            img_str = linefeed[line_num][linefeed[line_num].rfind("/"):]
            img_str_copy = img_str[:]
            # This gets us to 682px-Noor_Mehal_-_WIKI.jpg, still need to remove the filesize.
            # Because this operation fails in certain edge cases a src is provided for manual corrections
            img_str = img_str[img_str.find("-") + 1:]
            # Fix a certain common error.
            img_str = img_str.replace("]", "")
            # If a caption exists it'll be punched down onto the next line with ''This formatting.'' Retrieve that.
            caption = ""
            if linefeed[line_num + 1][:2] == "''":
                caption = linefeed[line_num + 1].replace("''", "")
                post = post.replace(linefeed[line_num + 1], "")
            elif linefeed[line_num + 2][:2] == "''":
                caption = linefeed[line_num + 2].replace("''", "")
                post = post.replace(linefeed[line_num + 2], "")
            img_str = "{{Signpost inline image|image=File:%s|caption=%s}}\n<!-- %s -->" % (img_str, caption,
                                                                                           img_str_copy)
            print(img_str)
            post = post.replace(linefeed[line_num], img_str)
    print(post)
    return post


@app.route('/')
def index():
    return render_template('frame.html')


@app.route('/blog-importer.html', methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        return render_template('blog_importer.html')
    else:
        url = request.form['blog_post_url']
        return render_template('blog_importer.html', code_returned=fetch(url))

if __name__ == '__main__':
    app.run(debug=True)