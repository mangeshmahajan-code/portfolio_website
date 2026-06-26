from flask import Flask, render_template, redirect, url_for, flash ,request
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,Text
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped
from form import Certificates_form,Project_form,Admin_form,Contact,Skill_form, Learning_journey_form, Education_journey_form
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required 
from werkzeug.security import  check_password_hash 
import html as html_module
import resend
import os

load_dotenv()

app = Flask(__name__)
Bootstrap5(app)
class Base(DeclarativeBase):
    pass

app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DB_URL')
db=SQLAlchemy(model_class=Base)
db.init_app(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_page'
login_manager.login_message = "You need to login to access that page."

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Admin,user_id)

svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg.txt')
with open(svg_path, 'r') as svg:
    data = svg.read().split('\n')
    svg_li = [i for i in data]

class Project(db.Model):
    id : Mapped[int] =mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String)
    tech_stack : Mapped[str] = mapped_column(String)
    description : Mapped[str] = mapped_column(String)
    img : Mapped[str] = mapped_column(String)
    live_link : Mapped[str] = mapped_column(String,nullable=True)
    git_repo : Mapped[str] = mapped_column(String,nullable=True)

class Certificates (db.Model):
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    issued_aut : Mapped[str] = mapped_column(String(50))
    skill : Mapped[str] = mapped_column(String(50))
    issued_date : Mapped[str] = mapped_column(String)
    img : Mapped[str] = mapped_column(String)

class Admin(db.Model,UserMixin):
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    admin_name : Mapped[str] = mapped_column(String)
    password : Mapped[str] = mapped_column(String,nullable=False)

class Learning_journey (db.Model):
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String)
    time_line : Mapped[str] = mapped_column(String)
    Category : Mapped[str] =mapped_column(String)
    description : Mapped[str] = mapped_column(String)     

class Education_journey(db.Model):
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String)
    time_line : Mapped[str] = mapped_column(String)
    Category : Mapped[str] =mapped_column(String)
    description : Mapped[str] = mapped_column(String)  


with app.app_context():
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    pro = db.session.execute(db.select(Project).order_by(Project.id.desc()).limit(4))
    projects = pro.scalars().all()
    
    cer = db.session.execute(db.select(Certificates).order_by(Certificates.id.desc()).limit(4))
    certificates =cer.scalars().all()

    learning_journey = db.session.execute(db.select(Learning_journey).order_by(Learning_journey.id.asc())).scalars().all()
    education_journey = db.session.execute(db.select(Education_journey).order_by(Education_journey.id.asc())).scalars().all()

    form = Contact()
    success = request.args.get('success', 'False') == 'True'
    error = request.args.get('error', 'False') == 'True'
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.msg.data
        if send_email(name, email, message):
            return redirect(url_for('index', success=True, _anchor='contact'))
        else:
            return redirect(url_for('index', error=True, _anchor='contact'))
    return render_template('index.html', projects=projects, all_certificates=certificates, svg_list=svg_li, form=form, success=success, learning_journey=learning_journey, education_journey=education_journey, error=error)

@app.route('/admin',methods=['POST','GET'])
def admin_page ():
    form = Admin_form()
    if form.validate_on_submit():
        admin_name= form.admin_name.data
        password = form.password.data
        admin = db.session.execute(db.select(Admin).where(Admin.admin_name==admin_name)).scalar()
        if admin:
            if check_password_hash(admin.password ,password):
                login_user(admin)
                return redirect(url_for('index'))
            else: 
                flash('enter valid admin name or password')
    return render_template('form.html',form = form)

@app.route('/project-form',methods =['POST','GET'])
@login_required
def project():
    form = Project_form()
    if form.validate_on_submit() :
        new_project = Project(
            title = form.title.data,
            tech_stack =form.tech_stack.data,
            description =form.description.data,
            img =form.img_path.data,
            live_link =form.live_link.data,
            git_repo =form.git_repo.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html',form=form,add= 'Project')

@app.route('/certificate-form',methods =['POST','GET'])
@login_required
def certificate():
    form = Certificates_form()
    if form.validate_on_submit():
        new_certificate = Certificates(
            issued_aut =form.issued_aut.data,
            skill =form.skill.data,
            issued_date = form.issued_date.data,
            img = form.img_path.data
        )
        db.session.add(new_certificate)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html',form=form,add = 'Certificate')

@app.route('/journey-form', methods=['POST','GET'])
@login_required
def journey():
    form = Learning_journey_form()
    if form.validate_on_submit():
        new_journey = Learning_journey(
                title=form.title.data,
                time_line=form.time_line.data,
                Category=form.Category.data,
                description=form.description.data
        )
        db.session.add(new_journey)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, add='Learning Journey')

@app.route('/education-form', methods=['POST','GET'])
@login_required
def education():
    form = Education_journey_form()
    if form.validate_on_submit():
        new_edu = Education_journey(
            title=form.title.data,
            time_line=form.time_line.data,
            Category=form.Category.data,
            description=form.description.data
        )
        db.session.add(new_edu)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, add='Education')

def send_email(name, email, message):
    resend.api_key = os.getenv("RESEND_API_KEY")
    safe_name = html_module.escape(name)
    safe_email = html_module.escape(email)
    safe_message = html_module.escape(message)
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": os.getenv("MY_EMAIL"),
            "subject": "New Contact Form Message",
            "html": f"""
            <h2>New Message</h2>
            <p><strong>Name:</strong> {safe_name}</p>
            <p><strong>Email:</strong> {safe_email}</p>
            <p><strong>Message:</strong><br>{safe_message}</p>
            """
        })
        return True
    except Exception:
        return False

@app.route('/edit/<int:id>',methods=['POST','GET'])
@login_required
def edit_project (id):
    project=db.get_or_404(Project,id) 
    form = Project_form(
        title= project.title,
        tech_stack=project.tech_stack,
        live_link=project.live_link,
        git_repo=project.git_repo,
        img_path=project.img,
        description=project.description
    )
    if form.validate_on_submit() :
        project.title = form.title.data
        project.tech_stack=form.tech_stack.data
        project.live_link = form.live_link.data
        project.git_repo=form.git_repo.data
        project.img =form.img_path.data
        project.description = form.description.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('form.html',form=form)

@app.route('/delete/<int:id>',methods=['POST'])
@login_required
def delete_project (id):
    project=db.get_or_404(Project,id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
