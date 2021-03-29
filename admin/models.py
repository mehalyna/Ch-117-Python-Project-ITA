from mongoengine import Document, StringField, EmailField


class Users(Document):
    firstname = StringField(max_length=50, required=True)
    lastname = StringField(max_length=50, required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True)
    status = StringField(required=True, default='active')
