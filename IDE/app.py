from flask import Flask,render_template
import os
import sys
from flask import request
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Power import Power


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('html/index.html')


@app.route('/run', methods=["GET", "POST"])
def CompileAndRun():
	Code = request.form.get("Code")
	FileAddress = os.path.dirname(os.path.abspath(__file__))+"\\TemoraryFile.pwd"
	with open(FileAddress, "w+") as fh:
		fh.write(Code)
	PowerCompilerInstance = Power.Power(FileAddress)
	print(FileAddress)
	return PowerCompilerInstance.Semanter.ReturnitiveEvaluator()