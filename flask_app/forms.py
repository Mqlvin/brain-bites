from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    youtube_url = StringField("Youtube URL", validators=[DataRequired()])
