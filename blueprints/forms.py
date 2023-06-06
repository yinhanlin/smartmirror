from flask_wtf import Form

from wtforms import StringField, FileField, SubmitField


class UploadForm(Form):
    name = StringField('Name')
    file = FileField('file')
    submit = SubmitField('submit')

