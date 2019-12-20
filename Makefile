run:
	python3 src/app.py
test:
	python3 -m unittest discover
tables:
	(cd src/database && sqlite3 SQlite3 < schema.sql)
