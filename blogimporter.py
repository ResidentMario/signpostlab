# coding=utf-8
"""
blogimporter.py
This script converts posts on the Wikimedia Blog into posts suitable for inclusion in the Wikipedia Signpost.

To run this file from the command line use `python blogimporter.py`.

It can be run both as a library, returning the post via blogimporter.main(), and as a command line script.
Note that running this script as a library requires that pywikibot by installed.
Running it in the command line further requires that it be configrued.
"""

import requests
from bs4 import BeautifulSoup


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


def save(text, filename='output.txt'):
    with open(filename, mode='w') as fn:
        fn.write(text)
