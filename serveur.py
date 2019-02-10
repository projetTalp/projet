from bottle import route, run, template
from bottle import post, request
import time
import getdf
import trt_doc as td
#import word2Vec as wv
import getdf_neural_network as gnn

@route('/index')
def index():
	return template("view/form_search.html")


@post('/search')
def search():
	req = request.forms.get('request')
	h = time.time()
	rez = getdf.sortResult(getdf.search(req))
	h = time.time() - h
	return template("view/header.html") + template("view/form_result.html", query=req, time=h) + getdf.showResult(rez) + template("view/footer.html")


@route('/doc/<num>')	
def getDoc(num):
	return template("view/header.html") + "<p>" + td.getDoc("./data/database.json", int(num)) + "</p>" + template("view/footer.html")

@post('/searchW2V')
def searchW2V():
	req = request.forms.get('request')
	h = time.time()
	rez = wv.get_results(req)
	h = time.time() - h
	return template("view/header.html") + template("view/form_result.html", query=req, time=h) + wv.showResult(rez) + template("view/footer.html")	
	
	
@post('/searchNN')
def search():
	req = request.forms.get('request')
	h = time.time()
	rez = getdf.sortResult(gnn.search(req))
	h = time.time() - h
	return template("view/header.html") + template("view/form_result.html", query=req, time=h) + getdf.showResult(rez) + template("view/footer.html")

run(host='localhost', port=8080)

