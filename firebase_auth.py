import pyrebase
from pyrebase.pyrebase import Firebase ,Auth,raise_detailed_error
import json
import requests
config = {
  "apiKey": "AIzaSyD0ijz05NWwTJ9Xrpc1T57LnU4NbvB0mas",
  "authDomain": "test-e3512.firebaseapp.com",
  "databaseURL": "https://test-e3512-default-rtdb.firebaseio.com",
  "storageBucket": "test-e3512.appspot.com"
}

class addedAuth(Auth):
  def send_password_reset_email(self, email):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(
      self.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

class addedFirebase(Firebase):
  def auth(self):
    return Auth(self.api_key, self.requests, self.credentials)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()