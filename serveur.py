from bottle import route, run, template
from bottle import get, post, request
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
	return template("view/header.html") + template("view/form_result.html", query = req) + getdf.showResult({1:0.5, 2:0.3, 5:0.1}) + template("view/footer.html")


@route('/doc/<num>')	
def getDoc(num):
	return template("view/header.html") + "<p>" + getdf.getDoc("firstdata", int(num)) + "</p>" + template("view/footer.html")
	
run(host='localhost', port=8080)
