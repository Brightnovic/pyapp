from   jrlabel import app , db , bcrypt  # Assuming you have your Flask app and SQLAlchemy instance

 







import os
from jrlabel.models import User, Post , Article
import secrets
from PIL import Image

from flask import  render_template ,abort, flash , redirect , url_for , request , current_app
from jrlabel.forms import RegistrationForm, LoginForm , ArticleForm1 ,ArticleForm2 , UpdateAccountForm , PostForm
from flask_login import login_user, current_user, logout_user, login_required ,UserMixin
from flask import render_template, url_for, flash, redirect, request


 

def save_picture_blog(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn







 

@app.route("/", methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
    form = ArticleForm1()
    return render_template('index.html',title="home page")
    
 

    







@app.route("/about")
def about():
    return render_template('about.html',title="about us")




@app.route("/Careers")
def Careers():
    return render_template('Careers.html',title="jobs")









 






@app.route("/service")
def service():
    return render_template('service.html',title="our services")







@app.route("/contact")
def contact():
    return render_template('contact.html',title="contact us")






 




#editing home page!
@app.route("/edithomepage", methods=['GET', 'POST'])
@login_required
def edithomepage():
    form = ArticleForm1()
     
    if form.validate_on_submit():

        image_home = save_picture_blog(form.image_home.data)
        
        # Create a new Article object and populate its attributes
        post = Article(image_home = image_home, title = form.title.data, description = form.description.data)
        
        db.session.add(post)
        db.session.commit()
        
        flash('Update successful', 'success')
        return redirect(url_for('home',  post = post , image_home = image_home))
    return render_template('index.html', form=form)



 





@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))













@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! you can login in to jrstand label  anytime please contact the developers if you encounter any problem', 'success')
        return redirect( url_for('login') )
    return render_template('register.html', title='Register', form=form)















@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file_user = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file_user)
    return render_template('account.html', title='edit Account info',
                           image_file=image_file, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



#blog
@app.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page = page ,per_page=2)
     
    #image_file_blog = url_for('static', filename='profile_pics/' + current_user.image_file_user)

    return render_template('blog.html', post=post,title="blog page")







     
#blog function
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def blogpost():
    form = PostForm()
    if form.validate_on_submit():
        if form.image_file_blog.data:   
             
            image_file_blog = save_picture_blog(form.image_file_blog.data)  
            post = Post(title=form.title.data,
                         image_file_blog=image_file_blog, 
                        content=form.content.data, 
                        author=current_user,
                        text=form.text.data)
            db.session.add(post)
            db.session.commit()
            flash('Your blog post has been created!', 'success')
            return redirect(url_for('blog'))  # Redirect to the blog page
        else:
            flash('Image is required for a blog post', 'danger')
    return render_template('blogpost.html', title='create  New Post', form=form, legend='New Post' )



 

@app.route('/post/<int:post_id>')
 
def post(post_id):
    post = Post.query.get_or_404(post_id)
    #image_fileblog = url_for('static', filename='profile_pics/' + current_user.image_file_user)
    return render_template('updateblog.html', title=post.title, post=post )




 



@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
     
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog'))




@app.errorhandler(404)
def error404_page(error):
    return render_template('404.html',title='page not found!')




@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title="HTTP Version Not Supported")