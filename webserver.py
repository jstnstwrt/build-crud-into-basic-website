from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## for crud work
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

### web servers

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += " Hello! "
				output += """<form method = 'POST' enctype = 'multipart/form-data' 
					action='/hello'><h2>What would you like me to say?</h2> <input 
					name = 'message' type='text' ><input type='submit' value='Submit'>
					</form>"""
				output += "</html></body>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new' > Create a new restaurant </a>"

				items =  session.query(Restaurant).all()
				for item in items:
					output += "<h3> %s <br> <a href='/restaurants/%s/edit' > edit </a> <br> <a href='/restaurants/%s/delete' > delete </a> </h3>" % (item.name, item.id, item.id)
				output += "</html></body>"				
				self.wfile.write(output)
				print output
				return
			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += """<form method = 'POST' enctype = 'multipart/form-data' 
					action='/restaurants/new'><h2>Add a new restaurant to the DB!</h2>""" 
				output += "<input name = 'restaurant' type='text' >"
				output += "<input type='submit' value='Create'>"
				output += "</form></html></body>"
				self.wfile.write(output)
				print output
				return

			
			#editing
			items =  session.query(Restaurant).all()
			for item in items:
				if self.path.endswith("/restaurants/%s/edit" % item.id ):
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1> %s </h1>" % item.name
					output += """<form method = 'POST' enctype = 'multipart/form-data' 
						action='/restaurants/%s/edit'>""" % item.id
					output += "<input name = 'renamed_rest' type='text' >"
					output += "<input type='submit' value='Rename'>"
						
					output += "</form></html></body>"
					self.wfile.write(output)
					print output
					return
			


			#deleting
			items =  session.query(Restaurant).all()
			for item in items:
				if self.path.endswith("/restaurants/%s/delete" % item.id ):
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1> Are you sure you want to delete %s ?</h1>" % item.name
					output += """<form method = 'POST' enctype = 'multipart/form-data' 
						action='/restaurants/%s/delete'><input type='submit' value='Delete'>
						</form>""" % item.id
					output += "</html></body>"
					self.wfile.write(output)
					print output
					return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					# adding restaurant to db
				restaurant_name = fields.get('restaurant')
				myFirstRestaurant = Restaurant( name = restaurant_name[0] )
				session.add(myFirstRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location','/restaurants')
				self.end_headers

			items =  session.query(Restaurant).all()
			for item in items:
				if self.path.endswith("/restaurants/%s/edit" % item.id ):
					ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict)
						# adding restaurant to db
					restaurant = session.query(Restaurant).filter_by(id = item.id ).one()
					new_restaurant_name = fields.get('renamed_rest')
					restaurant.name = new_restaurant_name[0]
					session.add(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()


			items =  session.query(Restaurant).all()
			for item in items:
				if self.path.endswith("/restaurants/%s/delete" % item.id ):
					ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

					restaurant = session.query(Restaurant).filter_by(id = item.id ).one()
					session.delete(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()
			


		except:
			pass



def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server is running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping the web server..."
		server.socket.close()


if __name__ == '__main__':
	main()