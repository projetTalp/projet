import cgi 

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")


html = """<!DOCTYPE html>
<head>
    <title> Bienvenue dans notre moteur de recherche</title>    
</head>
<body>
	<div class="input-group mb-3">
  		<input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="button-addon2">
  		<div class="input-group-append">
    			<button class="btn btn-outline-secondary" type="button" id="button-addon2">Chercher</button>
  		</div>
	</div>
</body>
</html>
"""

print(html)
