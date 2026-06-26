from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,TextAreaField,EmailField
from wtforms.validators import DataRequired, URL,Optional,Email
from flask_ckeditor import  CKEditorField

class Project_form(FlaskForm):
    title = StringField('project Title',validators=[DataRequired()])
    tech_stack =StringField('Tech stacks ',validators=[DataRequired()])
    live_link = StringField('Live link ' , validators=[Optional(),URL()])
    git_repo = StringField('Git reop link',validators=[Optional(),URL()])
    img_path = StringField('project screenshot path',validators=[DataRequired()])
    description = CKEditorField('Project description',validators=[DataRequired()])
    submit = SubmitField('submit')

class Certificates_form (FlaskForm):
    issued_aut = StringField('Issued authority',validators=[DataRequired()])
    skill = StringField("skill seperated by ','",validators=[DataRequired()])
    issued_date = StringField('Issued date',validators=[DataRequired()])
    img_path = StringField('certificate path',validators=[DataRequired()])
    submit = SubmitField('submit')

class Admin_form (FlaskForm):
    admin_name =StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('submit')

class Contact (FlaskForm):
    name = StringField('Full Name',validators=[DataRequired()])
    email =EmailField('Email Address',validators=[DataRequired(),Email()])
    msg =TextAreaField('Your Message',validators=[DataRequired()])

class Skill_form(FlaskForm):
    title = StringField('skill',validators=[])
    progress = StringField('progress in the skill',validators=[])
    skill_badges = StringField('skill badges',validators=[])
    submit = SubmitField('submit')

class Learning_journey_form(FlaskForm):
    title = StringField('Role / Title', validators=[DataRequired()])
    time_line = StringField('Timeline (e.g. 2025 - 2026)', validators=[DataRequired()])
    Category = StringField('Category / Company (e.g. BACKEND)', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Education_journey_form(FlaskForm):
    title = StringField('Degree / Title', validators=[DataRequired()])
    time_line = StringField('Timeline (e.g. 2025 - 2029)', validators=[DataRequired()])
    Category = StringField('Institution / Category (e.g. I²IT, PUNE)', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

