from google.appengine.ext import ndb


class MailMessage(ndb.Model):
    mailSender = ndb.StringProperty()
    mailSender_ID = ndb.StringProperty()
    mailRecipient = ndb.StringProperty()
    mailSubject = ndb.StringProperty()
    mailBody = ndb.TextProperty()
    mailBodyExcerpt = ndb.StringProperty()
    mailStatus = ndb.StringProperty()
    mailDate = ndb.DateTimeProperty(auto_now_add=True)
    mailDeleted = ndb.BooleanProperty(default=False)
    mailOutDeleted = ndb.BooleanProperty(default=False)


class WeatherData(ndb.Model):
    weatherUser = ndb.StringProperty()
    weatherLocation = ndb.StringProperty()