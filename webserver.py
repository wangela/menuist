from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # READ
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<h1>Menuist Restaurants</h1>"
                output += "<p>"
                for restaurant in restaurants:
                    resto_id = restaurant.id
                    output += restaurant.name
                    output += "<br><a href='/%s/edit'>Edit</a>" % resto_id
                    output += "<br><a href='/%s/delete'>Delete</a>" % resto_id
                    output += "<p>"
                output += "<a href='/restaurants/new'>Add a new restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # CREATE - FORM
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Restaurant to Menuist</h1>"
                output += "<p>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter the restaurant name</h2><input name="message" type="text" ><input type="submit" value="Create"> </form>'''
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<p>"
                output += "<a href='/restaurants'>Back to Menuist Home</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # UPDATE - FORM
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resto_id = self.path.split('/')[1]
                print resto_id
                restaurant = session.query(Restaurant).filter_by(id = resto_id).one()
                resto_name = restaurant.name
                output = ""
                output += "<html><body>"
                output += "<h1>Change the name of %s</h1>" % resto_name
                output += "<p>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/%s/edit'><h2>Enter the new restaurant name</h2><input name="message" type="text" ><input type="submit" value="Update"> </form>''' % resto_id
                output += "<p>"
                output += "<h1>Add an item to the menu</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/%s/add'><h2>Enter the new menu item</h2><input name="message" type="text" ><input type="submit" value="Create"> </form>''' % resto_id
                output += "<a href='/restaurants'>Back to Menuist Home</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # DELETE - FORM
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resto_id = self.path.split('/')[1]
                print resto_id
                restaurant = session.query(Restaurant).filter_by(id = resto_id).one()
                resto_name = restaurant.name
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % resto_name
                output += "<p>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/%s/delete'><h2><input type="submit" value="Yes, Delete"> </form><p>''' % resto_id
                output += "<a href='/restaurants'>Back to Menuist Home</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # CREATE - COMPLETE
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestoName = fields.get('message')
                    newResto = Restaurant(name = newRestoName[0])
                    session.add(newResto)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/add"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    resto_id = self.path.split('/')[1]
                    newMenuItemName = fields.get('message')
                    newMenuItem = MenuItem(name = newMenuItemName[0])
                    newMenuItem.restaurant_id = resto_id
                    newMenuItem.price = '$4.99'
                    session.add(newMenuItem)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            # UPDATE - COMPLETE
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestoName = fields.get('message')
                    resto_id = self.path.split('/')[1]
                    print resto_id
                    restaurant = session.query(Restaurant).filter_by(id = resto_id).one()
                    restaurant.name = newRestoName[0]
                    session.add(restaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            # DELETE - COMPLETE
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    resto_id = self.path.split('/')[1]
                    print resto_id
                    restaurant = session.query(Restaurant).filter_by(id = resto_id).one()
                    session.delete(restaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s"  % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
