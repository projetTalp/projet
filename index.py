import cgi 

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

print(form.getvalue("name"))

html = """<!DOCTYPE html>
<head>
    <title> Bienvenu dans notre moteur de recherche</title>
</head>
<body>
	<form action="search">
  		<input name="q">
  		<input type="submit">
	</form>
</body>
</html>
"""

print(html)
