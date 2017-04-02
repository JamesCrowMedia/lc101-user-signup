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
def getLoginForm():
    return """
            <div id="login" class="container">
                <h1>
                    <a href="/">User Signup</a>
                </h1>
                <form action="/signup" method="post">
                    <label id="username" {0}><span>Username: </span><input type="text" name="userName" {1}/></label>
                    <div class="spacer">{2}</div>
                    <label id="password" {3}><span>Password: </span><input type="password" name="password"/></label>
                    <div class="spacer">{4}</div>
                    <label id="password-check"><span>Repeat Password: </span><input type="password" name="password-check"/></label>
                    <div class="spacer"></div>
                    <label id="email" {5}><span>Email: </span><input type="text" name="email" {6}/></label>
                    <div class="spacer">{7}</div>
                    <input type="submit" class="submit" value="Create Your Account"/>
                    {8}
                </form>
            </div>
        """.format( error_html[0],              # 0
                    error_html[1],              # 1
                    errors['userNameError'],    # 2
                    error_html[2],              # 3
                    errors['passwordError'],    # 4
                    error_html[3],              # 5
                    error_html[4],              # 6
                    errors['emailError'],       # 7
                    errors['unknownError'])     # 8

errors = {'userNameError':'', 'passwordError':'', 'emailError':'', 'unknownError':''}
error_html = ['','','','','']

class MainHandler(webapp2.RequestHandler):
    def get(self):
        loginForm = getLoginForm()

        for k in errors.keys():
            errors[k] = ''
        for i in xrange(len(error_html)):
            error_html[i] = ''

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

        userName = self.request.get("userName")
        password = self.request.get("password")
        password_check = self.request.get("password-check")
        email = self.request.get("email")

        if self.checkUserName(userName):
            isValid["userName"] = True
            error_html[1] = 'value="{0}"'.format(cgi.escape(userName))
        else:
            errors["userNameError"] = '<div class="errorBox">Invalid Username</div>'
            error_html[0] = 'class="error"'
            error_html[1] = 'value="{0}"'.format(cgi.escape(userName))

        if len(password) <= 8:
            errors["passwordError"] = '<div class="errorBox">Must be at least 8 characters long</div>'
            error_html[2] = 'class="error"'
        elif password != password_check:
            errors["passwordError"] = '<div class="errorBox">Your passwords do not match</div>'
            error_html[2] = 'class="error"'
        elif self.checkPassword(password):
            isValid["password"] = True
        else:
            errors["passwordError"] = '<div class="errorBox">Your password is invalid</div>'
            error_html[2] = 'class="error"'

        if email == None or len(email) < 1:
            isValid["email"] = True
        elif self.checkEmail(email):
            isValid["email"] = True
            error_html[4] = 'value="{0}"'.format(cgi.escape(email))
        else:
            errors["emailError"] = '<div class="errorBox">Your email is invalid</div>'
            error_html[3] = 'class="error"'
            error_html[4] = 'value="{0}"'.format(cgi.escape(email))


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
                    <h1>
                        <a href="/">Success!</a>
                    </h1>
                    <h3>Welcome, <strong>{0}</strong>!</h3>
                    <p>You have successfully created and account.</p>
                    <p><a class="goHome" href="/">Click here to return</a></p>
                </div>
            """.format(esc_userName)
            content = header + success + footer
            self.response.write(content)
        else:
            self.redirect("/")




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup)
], debug=True)
