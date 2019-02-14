#!/usr/bin/env python
# -*- coding: utf-8 -*-

# encoding=utf8
import datetime
import sys
import os
import time
import jinja2
import webapp2
import logging
from models import MailMessage
from HTMLParser import HTMLParser
from google.appengine.api import users

reload(sys)
sys.setdefaultencoding('utf8')


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == False).order(-MailMessage.mailDate).fetch()
        today = datetime.datetime.now()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            myMessages = MailMessage.query(MailMessage.mailRecipient == user.email())

            params = {"myMessages": myMessages, "today": today, "mailList": mailList, "logiran": logiran, "user": user,
                      "logout_url": logout_url}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url}

        self.html = "index.html"
        return self.render_template("%s" % self.html, params=params)


class AddMailMessageHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == False).fetch()
        task = ""
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')

            params = {"mailList": mailList, "task": task, "logiran": logiran, "user": user, "logout_url": logout_url}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"mailList": mailList, "task": task, "logiran": logiran, "user": user, "login_url": login_url}

        self.html = "add.html"
        return self.render_template("%s" % self.html, params=params)

    def post(self):
        user = users.get_current_user()
        mailRecipient = self.request.get("mailRecipient")
        mailSubject = self.request.get("mailSubject")
        mailBody = self.request.get("mailBody")
        mailSender = self.request.get("mailSender")
        mailSender_ID = self.request.get("mailSender_ID")
        today = datetime.datetime.now()
        mailBodyExcerpt = strip_tags(mailBody)[0:150]

        newMailMessage = MailMessage(mailRecipient=mailRecipient, mailSender_ID=mailSender_ID, mailSubject=mailSubject,
                                     mailBody=mailBody, mailBodyExcerpt=mailBodyExcerpt, mailSender=mailSender)

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            newMailMessage.put()

            time.sleep(1)

            mailList = MailMessage.query(MailMessage.mailDeleted == False).fetch()

            params = {"mailList": mailList, "logiran": logiran, "user": user, "logout_url": logout_url, "today": today}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            time.sleep(1)

            mailList = MailMessage.query(MailMessage.mailDeleted == False).fetch()

            params = {"mailList": mailList, "logiran": logiran, "user": user, "login_url": login_url, "today": today}

        self.html = "index.html"
        return self.render_template("%s" % self.html, params=params)


class ReplayMailMessageHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()
        mail = MailMessage.get_by_id(int(message_id))
        params = {"mail": mail, "user": user}

        self.html = "replay.html"
        return self.render_template("%s" % self.html, params=params)

    def post(self, message_id):
        user = users.get_current_user()
        mailRecipient = self.request.get("mailRecipient")
        mailSubject = self.request.get("mailSubject")
        mailBody = self.request.get("mailBody")
        mailSender = self.request.get("mailSender")
        mailSender_ID = self.request.get("mailSender_ID")
        today = datetime.datetime.now()
        mailBodyExcerpt = strip_tags(mailBody)[0:150]

        newMailMessage = MailMessage(mailRecipient=mailRecipient, mailSender_ID=mailSender_ID, mailSubject=mailSubject,
                                     mailBody=mailBody, mailBodyExcerpt=mailBodyExcerpt, mailSender=mailSender)

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            newMailMessage.put()

            time.sleep(1)

            mailList = MailMessage.query(MailMessage.mailDeleted == False).fetch()

            params = {"mailList": mailList, "logiran": logiran, "user": user, "logout_url": logout_url, "today": today}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            time.sleep(1)

            mailList = MailMessage.query(MailMessage.mailDeleted == False).fetch()

            params = {"mailList": mailList, "logiran": logiran, "user": user, "login_url": login_url, "today": today}

        self.html = "index.html"
        return self.render_template("%s" % self.html, params=params)


class DeleteMailHandler(BaseHandler):
    def get(self, message_id):
        mail = MailMessage.get_by_id(int(message_id))
        params = {"mail": mail}

        return self.render_template("delete.html", params=params)

    def post(self, message_id):
        mail = MailMessage.get_by_id(int(message_id))
        user = users.get_current_user()
        usermail = user.email()

        logging.info(usermail)
        logging.info(mail.mailSender)

        if usermail == mail.mailSender:
            mail.mailOutDeleted = True
            mail.mailDeleted = True
        else:
            mail.mailDeleted = True

        mail.put()
        time.sleep(1)

        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == False).order(-MailMessage.mailDate).fetch()
        today = datetime.datetime.now()
        notice = "Message successfully deleted! <a class='alert-link' href='/restore/" + str(mail.key.id()) + "'>Undo delete message</a>"
        style = "danger"

        logging.info(notice)

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            myMessages = MailMessage.query(MailMessage.mailRecipient == user.email())

            params = {"myMessages": myMessages, "today": today, "mailList": mailList, "logiran": logiran, "user": user,
                      "logout_url": logout_url, "notice": notice, "style":style}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url}

        self.html = "index.html"
        return self.render_template("%s" % self.html, params=params)


class MessageHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()
        mail = MailMessage.get_by_id(int(message_id))
        logging.info(user)
        today = datetime.datetime.now()
        timeSinceSendMinutes = str(today - mail.mailDate).split(":")[1]
        timeSinceSendHours = str(today - mail.mailDate).split(":")[0]
        timeSinceSendDays = str(today - mail.mailDate).split(",")[0]

        if "days" in timeSinceSendDays:
            timeSinceSend = timeSinceSendDays
        elif int(timeSinceSendHours) == 0:
            if int(timeSinceSendMinutes[0]) == 0:
                timeSinceSend = timeSinceSendMinutes[1] + " minutes"
            else:
                timeSinceSend = timeSinceSendMinutes + " minutes"

        else:
            timeSinceSend = timeSinceSendHours + " hours"

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            mail.mailStatus = "read"
            mail.put()

            params = {"mail": mail, "logiran": logiran, "user": user, "logout_url": logout_url, "today": today,
                      "timeSinceSend": timeSinceSend}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "user": user, "login_url": login_url}

        self.html = "message.html"
        return self.render_template("%s" % self.html, params=params)


class SendMessageHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()
        mail = MailMessage.get_by_id(int(message_id))
        today = datetime.datetime.now()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')

            params = {"mail": mail, "logiran": logiran, "user": user, "logout_url": logout_url, "today": today}

        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "user": user, "login_url": login_url}

        self.html = "message.html"
        return self.render_template("%s" % self.html, params=params)


class DeleteSendMailHandler(BaseHandler):
    def get(self, message_id):
        mail = MailMessage.get_by_id(int(message_id))
        params = {"mail": mail}

        return self.render_template("delete.html", params=params)

    def post(self, message_id):
        mail = MailMessage.get_by_id(int(message_id))

        mail.mailOutDeleted = True
        mail.put()
        time.sleep(1)

        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == False).order(-MailMessage.mailDate).fetch()
        today = datetime.datetime.now()
        notice = "Message successfully deleted!"
        style = "danger"

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            myMessages = MailMessage.query(MailMessage.mailRecipient == user.email())

            params = {"myMessages": myMessages, "today": today, "mailList": mailList, "logiran": logiran, "user": user,
                      "logout_url": logout_url, "notice": notice, "style":style}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url}

        self.html = "index.html"
        return self.render_template("%s" % self.html, params=params)


class RestoreDeletedMailHandler(BaseHandler):
    def get(self, message_id):
        mail = MailMessage.get_by_id(int(message_id))
        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == False).order(-MailMessage.mailDate).fetch()
        today = datetime.datetime.now()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            myMessages = MailMessage.query(MailMessage.mailRecipient == user.email())

            mail.mailDeleted = False
            mail.put()

            notice = "Message has been successfully restored!"
            style = "success"

            params = {"notice": notice, "myMessages": myMessages, "today": today, "mailList": mailList,
                      "logiran": logiran, "user": user,
                      "logout_url": logout_url, "style":style}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url}

        time.sleep(1)

        self.html = "index.html"
        return self.render_template("%s" % self.html, params=params)


class OutboxHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == False and MailMessage.mailOutDeleted == False).order(
            -MailMessage.mailDate).fetch()
        today = datetime.datetime.now()

        # logging.info(user)

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            myMessages = MailMessage.query(MailMessage.mailRecipient == user.email())

            params = {"myMessages": myMessages, "today": today, "mailList": mailList, "logiran": logiran, "user": user,
                      "logout_url": logout_url}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url}

        self.html = "outbox.html"
        return self.render_template("%s" % self.html, params=params)


class DeletedHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        mailList = MailMessage.query(MailMessage.mailDeleted == True).order(-MailMessage.mailDate).fetch()
        today = datetime.datetime.now()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            myMessages = MailMessage.query(MailMessage.mailRecipient == user.email())

            params = {"myMessages": myMessages, "today": today, "mailList": mailList, "logiran": logiran, "user": user,
                      "logout_url": logout_url}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url}

        self.html = "deleted.html"
        return self.render_template("%s" % self.html, params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/add', AddMailMessageHandler),
    webapp2.Route('/replay/<message_id:\d+>', ReplayMailMessageHandler),
    webapp2.Route('/delete/<message_id:\d+>', DeleteMailHandler),
    webapp2.Route('/restore/<message_id:\d+>', RestoreDeletedMailHandler),
    webapp2.Route('/send-delete/<message_id:\d+>', DeleteSendMailHandler),
    webapp2.Route('/message/<message_id:\d+>', MessageHandler),
    webapp2.Route('/send-message/<message_id:\d+>', SendMessageHandler),
    webapp2.Route('/outbox', OutboxHandler),
    webapp2.Route('/deleted', DeletedHandler),
], debug=True)
