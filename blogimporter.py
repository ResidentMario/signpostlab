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
    # post = post.replace("<p>", "")
    # post = post.replace("</p>", "NEWLINEPLACEHOLDER")
    post = post.replace("	", "")
    post = requests.post('http://rest.wikimedia.org/en.wikipedia.org/v1/transform/html/to/wikitext',
                        data={'html': post}).text
    post = BeautifulSoup(post, "html.parser")
    post = post.get_text()
    # post = post.replace("NEWLINEPLACEHOLDER",  "\n")
    print(post)
    return post


def save(text, filename='output.txt'):
    with open(filename, mode='w') as fn:
        fn.write(text)


# def main(page, target=signpostlib.get_next_signpost_issue() + '/Blog'):
#     # Check to make sure that the --page argument is filled in with valid input, and return an error if it is not.
#     if not page or 'blog.wikimedia.org' not in page:
#         raise IOError(
#                 "This script requires a valid --page parameter. Otherwise the script doesn\'t know what Blog content "
#                 "to intake! For example try: python Blog_Importer.py --page "
#                 "\'https://blog.wikimedia.org/2015/07/16/third-transparency-report-released/\'")
#
#     # Check if a target is provided. If it is, make sure it is valid; if it isn't have the script fetch it.
#     if 'User:Resident Mario/' not in target and 'Wikipedia:Wikipedia Signpost/' not in target:
#         raise IOError(
#                 'A target page was provided but did not conform to legal targets for this script. Please direct your target at a subpage of User:Resident Mario or of Wikipedia:Wikipedia Signpost. To just set it to the next Signpost issue, don\'t provide this argument at all.')
#
#     # Fetch and store the contents of the blog post.
#     post = requests.get(page).text
#
#     # Core the data to the post itself.
#     post = post[post.index('<div class="entry">') + len('<div class="entry">'):]
#     post = post[:post.index('<div class="socials">')]
#     post = post[:post.rfind('</div>')]
#
#     # Use the RESTBase API to convert the blog's HTML to native wikicode.
#     post = signpostlib.htmlToWikitext(post)
#
#     # Package the post for inclusion in the Signpost.
#     post = '''<noinclude>{{Signpost draft}}
# 	{{Wikipedia:Signpost/Template:Signpost-header|||}}</noinclude>
#
# 	<div style="padding-left:50px; padding-right:50px;">
#
# 	{{Wikipedia:Signpost/Template:Signpost-article-start|{{{1|Your title}}}|By ?| {{subst:#time:j F Y|{{subst:Wikipedia:Wikipedia Signpost/Issue|4}}}}}}
#
# 	</div>
#
# 	{{Wikipedia:Wikipedia Signpost/Templates/WM Blog}}
#
# 	<div style="width:46em; line-height:1.6em; font-size:1em; font-family:Helvetica Neue, Helvetica, Arial, sans-serif; padding-left:5em;" class="plainlinks">''' + post + '''</div>
#
# 	<noinclude>{{Wikipedia:Signpost/Template:Signpost-article-comments-end||2015-04-22|2015-05-06}}
# 	</noinclude>'''
#     return post
#
#
# # The following instructions are only executed with this script is called from the command line.
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--page",
#                         help='The webpage from which this script will attempt to intake content. Must be a page in '
#                              'the Wikimedia Blog domain. This is a required argument.')
#     parser.add_argument("-t", "--target",
#                         help='The target page to which the output of this script will be written. Must be a subpage '
#                              'of the Wikipedia Signpost or in the userspace this script\'s writer, Resident Mario.')
#     args = parser.parse_args()
#
#     # Check to make sure that the --page argument is filled in with valid input, and return an error if it is not.
#     if not args.page or 'blog.wikimedia.org' not in args.page:
#         raise IOError(
#                 'This script requires a valid --page parameter. Otherwise the script doesn\'t know what Blog content to intake! For example try: python Blog_Importer.py --page \'https://blog.wikimedia.org/2015/07/16/third-transparency-report-released/\'')
#
#     # Check if a target is provided. If it is, make sure it is valid; if it isn't have the script fetch it.
#     if not args.target:
#         args.target = signpostlib.get_next_signpost_issue() + '/Blog'
#     elif 'User:Resident Mario/' not in args.target and 'Wikipedia:Wikipedia Signpost/' not in args.target:
#         raise IOError(
#                 'A target page was provided but did not conform to legal targets for this script. Please direct your target at a subpage of User:Resident Mario or of Wikipedia:Wikipedia Signpost. To just set it to the next Signpost issue, don\'t provide this argument at all.')
#     post = main(args.page, args.target)
#     signpostlib.saveContentToPage(post, args.target,
#                                   'Importing basic Blog repost via the [https://github.com/ResidentMario/Blog_Importer Blog_Importer] script.')
