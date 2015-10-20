from flask import Flask
from flask import render_template
from flask import request
import blogimporter
import tnimporter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('frame.html')

@app.route('/fc_importer', methods=['GET', 'POST'])
def fc_importer():
	if request.method == 'POST':
		pass
	else:
		return render_template('fc_importer.html')

@app.route('/wm_blog_importer', methods=['GET', 'POST'])
def blog_importer():
	if request.method == 'POST':
		data = request.form['blog_post_url']
		if not data or 'blog.wikimedia.org' not in data:
			return render_template('blog_importer.html', code_returned="Invalid input. Make sure that you inputted the URL of a valid WM Blog post.")
		else:
			return render_template('blog_importer.html', code_returned=blogimporter.main(data))
			# return blogimporter.main(data)
	else:
			return render_template('blog_importer.html')

@app.route('/tn_importer', methods=['GET', 'POST'])
def tn_importer():
	if request.method == 'POST':
		return render_template('tn_importer.html', code_returned=tnimporter.main())
			# return blogimporter.main(data)
	else:
		return render_template('tn_importer.html')

if __name__ == '__main__':
    app.run(debug = True) # Change this to just app.run() in the production version.
    # app.run()
