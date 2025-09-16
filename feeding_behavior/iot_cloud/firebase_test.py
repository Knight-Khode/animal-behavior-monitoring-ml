import pyrebase

firebaseConfig = {
  'apiKey': "",
  'authDomain': "pigfarm-4b6ab.firebaseapp.com",
  'databaseURL': "https://pigfarm-4b6ab-default-rtdb.firebaseio.com",
  'projectId': "pigfarm-4b6ab",
  'storageBucket': "pigfarm-4b6ab.appspot.com",
  'messagingSenderId': "588943384528",
  'appId': "1:588943384528:web:6e0adbdda7632b2071a3d5",
  'measurementId': "G-2C1FHYK8V3"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

#Authentication
#Login
# email = input("Enter your email: ")
# password = input("Enter your password: ")
#
# try:
#   auth.sign_in_with_email_and_password(email, password)
#   print("SUCCESSFULLY SIGNED IN")
# except:
#   print("INVALID USER OR PASSWORD. TRY AGAIN")


#Database

#db = root node
#.child = child node
#CAN CREATE MULTIPLE .childs
data = {'age':40,
        'address':"New York",
        'employed':True,
        'name': "John Smith"}

db.child('PEOPLE').child("WORKERS").push(data)
