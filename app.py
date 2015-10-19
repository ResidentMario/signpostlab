from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    # return 'Hello World! Got this server working---and Git too! (2)'
    return render_template('frame.html')

@app.route('/fc_importer', methods=['POST', 'GET'])
def fc_importer():
	return render_template('fc_importer.html')

@app.route('/wm_blog_importer', methods=['GET', 'POST'])
def blog_importer():
	if request.method == 'POST':
		data = request.form['blog_post_url']
		if not data or 'blog.wikimedia.org' not in data:
			return render_template('blog_importer.html', code_returned="Invalid input. Make sure that you inputted the URL of a valid WM Blog post.")
		else:
			return 'Input successfully parsed; just need to plug the application into here now...'
			# return render_template('blog_importer.html', code_returned=Blog_Importer.import_blog(data, ''))
	else:
		return render_template('blog_importer.html')

@app.route('/tn_importer', methods=['POST', 'GET'])
def tn_importer():
	return render_template('tn_importer.html')



if __name__ == '__main__':
    app.run(debug=True)