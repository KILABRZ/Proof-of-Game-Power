from flask import Flask, render_template
webService = Flask(__name__)

@webService.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	webService.run(host = '0.0.0.0', port = 8000)