from http.server import BaseHTTPRequestHandler
from urllib import parse
import psycopg2
import json
import os

class handler(BaseHTTPRequestHandler):

	def do_GET(self):
		connection = psycopg2.connect (
			host = os.environ.get('HOST'),
			database = os.environ.get('DATABASE'),
			user = os.environ.get('USER'),
			password = os.environ.get('PASSWORD'),
			port = os.environ.get('PORT'),
		)

		cursor = connection.cursor()

		dic = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
		self.send_response(200)
		self.send_header('Content-type','application/json; charset=utf-8')
		self.end_headers()

		if "student_id" in dic:
			cursor.execute("SELECT * FROM students WHERE id = %(student_id)s",{'student_id': dic["student_id"]})
			values_array = list(cursor.fetchone())
			col_names = [desc[0] for desc in cursor.description]
			message	= dict(zip(col_names, values_array))
		else:
			message = {"error": "Please provide student_id"}

		self.wfile.write(json.dumps(message, default=str).encode())
		return