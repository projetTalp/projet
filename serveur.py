
from bottle import route, run, template
from bottle import get, post, request
import time
import getdf


@route('/index')
def index():
    return template("view/form_search.html")

@post('/search')
def search():
	req = request.forms.get('request')
	print (req)
	#res = getdf.search(req)
	#getdf.sortResult(res)
	#data = getdf.getDoc("firstdata", 3)
	#return getdf.test()
	#return "<p>"+data+"</p>"
	h = time.time()
	rez = getdf.sortResult(getdf.search(req))
	h = time.time() - h
	return template("view/header.html") + template("view/form_result.html", query = req, time = h) + getdf.showResult(rez) + template("view/footer.html")


@route('/doc/<num>')	
def getDoc(num):
	return template("view/header.html") + "<p>" + getdf.getDoc("./data/firstdata", int(num)) + "</p>" + template("view/footer.html")
	
run(host='localhost', port=8080)

