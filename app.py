from flask import Flask
from flask import render_template
from flask import request

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
			# return render_template('blog_importer.html', code_returned=os.system("Blog_Importer.py " + data))
			# return render_template('blog_importer.html', code_returned=subprocess.check_output(["ls", '-l'], universal_newlines=True))
			# return render_template('blog_importer.html', code_returned=Blog_Importer.import_blog(data, ''))
			pass
	else:
		return render_template('blog_importer.html')

@app.route('/tn_importer', methods=['GET', 'POST'])
def tn_importer():
	if request.method == 'POST':
		pass
	else:
		return render_template('tn_importer.html')

if __name__ == '__main__':
    # app.run(debug = True) # Change this to just app.run() in the production version.
    app.run()
