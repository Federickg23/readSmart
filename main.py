import webapp2
import jinja2
import os
from books import *
from google.appengine.api import users
from google.appengine.ext import ndb
import logging


TEMPLATE = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
)


class HomePage(webapp2.RequestHandler):

	def get(self):
		books = Books.query().fetch()
		if len(books) == 0:
			BookLoader()
		content = TEMPLATE.get_template('/templates/home.html')

		if self.request.cookies.get("logged_in") == "True":
			self.response.write(content.render(active = True))
		else:
			self.response.write(content.render(login = True))

class CssiUser(ndb.Model):

  	first_name = ndb.StringProperty()
  	last_name = ndb.StringProperty()
	username = ndb.StringProperty()
	email = ndb.StringProperty()
	password = ndb.StringProperty()
	location = ndb.StringProperty()



class MainHandler(webapp2.RequestHandler):
	def get(self):
    # user = users.get_current_user()
		content = TEMPLATE.get_template('/templates/signup.html')

		if self.request.cookies.get("logged_in") == "True":

			self.response.write(content.render(success = True, user = self.request.cookies.get("name")))
		else:
			self.response.write(content.render(failure = True))


 	def post(self):
		# logged_in = True
		content = TEMPLATE.get_template('/templates/signup.html')
	  	cssi_user = CssiUser(
	       	first_name=self.request.get('firstname'),
	       	last_name=self.request.get('lastname'),
			username = self.request.get('Username'),
		    email = self.request.get('Email'),
		    password = self.request.get('Password'),
		    location = self.request.get('location'))
		cssi_user.put()
		self.response.set_cookie("logged_in", "True")
		self.response.set_cookie("name", cssi_user.first_name)
		self.response.write(content.render(success = True, user = cssi_user.first_name))

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		content = TEMPLATE.get_template('/templates/signIn.html')
		self.response.write(content.render(start = True, error=False))

	def post(self):
		username = self.request.get("Username")
		password = self.request.get("Password")
		#content = TEMPLATE.get_template('/templates/signup.html')

		# user_key =  CssiUser.all()
		user_signed_in = False
		q = CssiUser.query().fetch()
		for user in q:
			if (user.username == username and user.password == password) or (user.email == username and user.password == password):
				# logged_in = True
				self.response.set_cookie("logged_in", "True")
				self.response.set_cookie("name", user.first_name)
				self.response.clear()
				user_signed_in = True
				break
				# self.response.write(content.render(success = True, user = user.first_name))
				# return
			if user.username != username or user.password != password or user.email != username:
				user_signed_in = False
				self.response.delete_cookie("logged_in")

		if not user_signed_in:
			content = TEMPLATE.get_template('/templates/signIn.html')
			self.response.write(content.render(start = True, error = True, Username = username, Password = password))
		else:
			self.redirect("/")

		# ndb.Query()
		# q.filter("username = ", self.response.get("Username"))
		# print q

class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		self.response.delete_cookie("logged_in")
		self.redirect('/')




class UserInput(webapp2.RequestHandler):
	def get(self):
		content = TEMPLATE.get_template('/templates/UserInput.html')
		self.response.write(content.render(title = "book variable"))
		# print "Class is functional"



def average(persons_input, title):
	b = Books.query().fetch()
	for book in b:
		if b.title == title:
			book_length = persons_input
			book_length = int(book_length)
			b.bookindex.append(book_length)

app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', MainHandler),
  ('/logout', LogoutHandler),
  ('/signIn', LoginHandler),
  ('/input', UserInput),
  ('/booklist', BookHandler),
  ('/bookview', BookView),
  ('/library', PersonalLibrary)
], debug=True)
