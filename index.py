import cgi 

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")


html = """<!DOCTYPE html>
<head>
    <title> Bienvenue dans notre moteur de recherche</title>    
</head>
<body>
	<form action="search" method="POST">
  		<input name="q">
  		<input type="submit">
	</form>
</body>
</html>
"""

print(html)
