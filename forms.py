from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Email

class ExperienceForm(FlaskForm):
    date = StringField("Date", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    details = TextAreaField("Details")

class ResumeForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    objective = TextAreaField("Objective")
    education = TextAreaField("Education")

    # Corrected Work Experience as a list of structured entries
    experience = FieldList(FormField(ExperienceForm), min_entries=1)

    skills = TextAreaField("Skills")
    projects = TextAreaField("Projects")
    references = TextAreaField("References (Optional)")
    template = SelectField(
        "Resume Template",
        choices=[("1", "Simple"), ("2", "Two-Column"), ("3", "Comprehensive")],
        coerce=int
    )
    submit = SubmitField("Generate Resume")
