from flask import Flask
from flask import render_template
from flask import request
import requests
from bs4 import BeautifulSoup
# import mwapi

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
        if "blog.wikimedia.org" not in url:
            return render_template('blog_importer.html', code_returned="Blog URL not valid.")
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
                post = post.replace(linefeed[line_num], img_str)
        front_matter = """{{Signpost draft}}{{Wikipedia:Signpost/Template:Signpost-header|||}}

<div style="margin-left:50px; margin-right:50px;">
{{Wikipedia:Signpost/Template:Signpost-article-start|{{{1|(Your article's descriptive subtitle here)}}}|By [[User:{{<includeonly>subst:</includeonly>REVISIONUSER}}|]]| {{<includeonly>subst:</includeonly>#time:j F Y|{{<includeonly>subst:</includeonly>Wikipedia:Wikipedia Signpost/Issue|4}}}}}}
</div>

{{Wikipedia:Wikipedia Signpost/Templates/WM Blog}}

<div style="width:46em; line-height:1.6em; font-size:1em; font-family:Helvetica Neue, Helvetica, Arial, sans-serif; padding-left:5em;" class="plainlinks">"""
        back_matter = """</div>

<noinclude>{{Wikipedia:Signpost/Template:Signpost-article-comments-end||{{
<includeonly>subst:</includeonly>Wikipedia:Wikipedia Signpost/Issue|1}}|{{<includeonly>subst:</includeonly>Wikipedia:Wikipedia Signpost/Issue|5}}<noinclude>|demospace=1</noinclude>}}</noinclude><noinclude>[[Category:Wikipedia Signpost templates|{{SUBPAGENAME}}]]</noinclude>"""
        post = front_matter + post + back_matter
        return render_template('blog_importer.html', code_returned=post)


@app.route('/tech-news-importer.html', methods=['GET', 'POST'])
def tech():
    if request.method == 'GET':
        return render_template('tn_importer.html')
    else:
        redir = requests.get('https://meta.wikimedia' + '.org/w/index.php?&action=raw&title=' + 'Tech/News/Latest').text
        actual_post_name = redir[redir.find("[[") + 2:redir.find("]]")]
        post = requests.get('https://meta.wikimedia' + '.org/w/index.php?&action=raw&title=' + actual_post_name +
                            '/en').text
        post = post[post.find('<section begin="tech-newsletter-content"/>'):post.find('<section end="tech-newsletter-content"/>')]

        front_matter = """{{Signpost draft}}{{Wikipedia:Signpost/Template:Signpost-header|||}}

{{Wikipedia:Signpost/Template:Signpost-article-start|{{{1|Tech news in brief}}}|By [[meta:Tech/Ambassadors|Wikimedia tech ambassadors]]| {{<includeonly>subst:</includeonly>#time:j F Y|{{<includeonly>subst:</includeonly>Wikipedia:Wikipedia Signpost/Issue|4}}}}}}

{{Wikipedia:Wikipedia Signpost/Templates/Tech news}}

"""
        back_matter = """<section end="tech-newsletter-content"/>

<noinclude>{{Wikipedia:Signpost/Template:Signpost-article-comments-end||{{
<includeonly>subst:</includeonly>Wikipedia:Wikipedia Signpost/Issue|1}}|{{<includeonly>subst:</includeonly>Wikipedia:Wikipedia Signpost/Issue|5}}<noinclude>|demospace=1</noinclude>}}</noinclude><noinclude>[[Category:Wikipedia Signpost templates|{{SUBPAGENAME}}]]</noinclude>"""
        post = front_matter + post + back_matter
        return render_template('tn_importer.html', code_returned=post)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()