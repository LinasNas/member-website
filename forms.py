from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class CourseForm(FlaskForm):
    name = StringField('Name (e.g. Jane Doe)', validators=[InputRequired()])

    affiliation = StringField('Affiliation (e.g. Mainsail Network)', validators=[InputRequired()])

    email = StringField('Institutional email (e.g. jane@mainsail.org)', validators=[InputRequired()])

    location = StringField('Location: City, Country (e.g. New York, United States)', validators=[InputRequired()])

    public_key = StringField('Public key (e.g. 0123456789abcdefABCDEF0123456789abcdefABCDEF)', validators=[InputRequired(), Length(min = 44, max = 44)])


class ConfirmSig(FlaskForm):
   
    signature = StringField('Signature', validators=[InputRequired()])
