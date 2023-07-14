from flask import Flask,request,render_template,redirect,send_file,send_from_directory
import os
from script import *


app = Flask(__name__)

# app.config["IMAGE_UPLOADS"] = "/Job_hunt/1july23/auxoai/project/uploads"

from werkzeug.utils import secure_filename

paths = []
filenames = []

@app.route('/home',methods = ["GET","POST"])
def upload_image():
	if request.method == "POST":
		image = request.files['file']

		if image.filename == '':
			print("Image must have a file name")
			return redirect(request.url)


		filename = secure_filename(image.filename)

		basedir = os.path.abspath(os.path.dirname(__file__))
		path = os.path.join(basedir,app.config["IMAGE_UPLOADS"],filename)
		image.save(path)
		pdf_files = [path]
		sections = extract_pdf_sections(pdf_files)
		output_sections_to_files(sections)

		return render_template("main.html",filename=filename)

	return render_template('main.html')


@app.route('/download')
def download():
	upload_path = "D:/Job_hunt/1july23/auxoai/project/uploads/"
	for x in os.listdir(upload_path):
		if x.startswith("Chapter"):
			p = upload_path + x
			paths.append(p)
			filenames.append(x)
	
	return render_template('main.html', your_list=filenames, paths = paths)
			

@app.route('/download/<name>')
def func(name):
    upload_path = "D:/Job_hunt/1july23/auxoai/project/uploads/"
    return send_from_directory(upload_path, name, as_attachment=True)


@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static',filename = "/Images" + filename), code=301)


app.run(debug=True,port=2000)