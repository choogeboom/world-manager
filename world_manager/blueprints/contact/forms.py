from flask_wtf.form import Form
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_components import EmailField


class ContactForm(Form):
    email = EmailField("What's your e-mail address?",
                       [DataRequired(), Length(3, 254)])
    message = TextAreaField("What's your question or issue?",
                            [DataRequired(), Length(1, 8192)])
