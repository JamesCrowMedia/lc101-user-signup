#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

header = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="stylesheets/style.css" />
        <title>User Signup</title>
    </head>
    <body>
"""

footer = """
    </body>
    </html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):

        loginForm = """
            <div id="login" class="container">
                <h1>User Signup</h1>
                <form action="/signup" method="post">
                    <label id="username"><span>Username: <input type="text" name="userName"/></span></label>
                    <label id="password"><span>Password: <input type="password" name="password"/></span></label>
                    <label id="password-check"><span>Repeat Password: <input type="password" name="password-check"/></span></label>
                    <label id="email"><span>Email: <input type="text" name="email"/></span></label>
                    <input type="submit" class="submit" value="Create Your Account"/>
                </form>
            </div>
        """
        content = header + loginForm + footer
        self.response.write(content)

class Signup(webapp2.RequestHandler):

    def checkUserName(self, userName):
        userName_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
        return userName_RE.match(userName)

    def checkPassword(self, password):
        password_RE = re.compile("^.{3,20}$")
        return password_RE.match(password)

    def checkEmail(self, email):
        email_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
        return email_RE.match(email)


    def post(self):
        isValid = {"userName":None, "password":None, "email":None} # CHANGE TO None AFTER TESTING

        errors = ''

        userName = self.request.get("userName")
        password = self.request.get("password")
        password_check = self.request.get("password-check")
        email = self.request.get("email")


        if self.checkUserName(userName):
            isValid["userName"] = True
        else:
            errors += "&userNameError={0}".format(userName)

        if len(password) <= 8:
            errors += "&passwordError=short"
        elif password != password_check:
            errors += "&passwordError=nomatch"
        elif self.checkPassword(password):
            isValid["password"] = True
        else:
            errors += "&passwordError=invalid"

        if email == None or len(email) < 1:
            isValid["email"] = True
        elif self.checkEmail(email):
            isValid["email"] = True
        else:
            errors += "&emailError=invalid"


        if (isValid['userName'] == True and #-- Check that things are valid
            isValid['password'] == True and
            isValid['email'] == True and
            userName == self.request.get("userName") and #-- Doublecheck inputs
            password == self.request.get("password") and
            email == self.request.get("email")):

            #-- Escape userName
            esc_userName = cgi.escape(userName)

            success = """
                <div class="container">
                    <h1>Success!</h1>
                    <h3>Welcome <strong>{0}</strong>!</h3>
                    <p>You have successfully created and account.</p>
                </div>
            """.format(esc_userName)
            content = header + success + footer
            self.response.write(content)

        elif errors != '':
            self.redirect("/?" + errors)

        else:
            self.redirect("/?unknownError=True")




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup)
], debug=True)
