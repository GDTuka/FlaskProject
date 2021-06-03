from app import app
from flask import render_template,url_for,request,redirect,flash
from app.forms import LoginForm,RegistrationForm,predlogForm,EditProfileForm,PostForm,vipForm,deleteForm
from flask_login import current_user,login_user,logout_user
from app.models import User,Post,AboutMe,predlog,DeletedPost,DeleteUser
from flask_login import login_required
from app import db
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form=RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)
    return render_template('registration.html' ,form=form)
@app.route('/predlog', methods=['GET','POST'])
def predlog():
    form=predlogForm()
    if form.validate_on_submit():
        user = predlog(FirstName = form.FisrtName.data, LastName=form.LastName.data,offer=form.Offer.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('predlog.html', form=form)
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        AboutMeInfo = AboutMe(UserName = form.username.data,about_me = form.about_me.data , age=form.age.data,city=form.city.data,Music = form.Music.data,Work=form.work.data,FirstName=form.FirstName.data, SecondName=form.SecondName.data)
        db.session.add(AboutMeInfo)
        db.session.commit()
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
    AboutUser =AboutMe.query.all()
    delete = deleteForm()
    form=PostForm()
    vip = '1'
    user=User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    current_user.body = form.post.data
    if delete.validate_on_submit():
        for u in posts:
            if u.author == user.username:
                delpost = DeletedPost(delbody = u.body, delauthor=u.author,deltimestamp=u.timestamp)
                db.session.delete(u)
                db.session.add(delpost)
                db.session.commit()
                break
        deluser=DeleteUser(delusername = user.username, delpassword= user.email, delemail = user.email,delabout_me = user.about_me, delvip=user.delvip)
        db.session.add(deluser)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user.html',user=user,posts=posts,PostForm=PostForm,form=form,delete=delete)
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))
@app.route('/post',methods=['GET','POST'])
def post():
    form = PostForm()
    delete = deleteForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user.username)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post'))
    if delete.validate_on_submit():
        db.sesson.delete(post)
        db.session.commit()
        return redirect(url_for('post'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("post.html", title='Home Page', form=form,posts=posts,delete=delete)
@app.route('/AdminPage')
def AdminPage():
    return render_template('AdminPage.html')
@app.route('/vip'  , methods=['GET','POST'])
def vip():
    form = vipForm()
    if form.validate_on_submit():
        user = form.username.data
        users = User.query.all()
        for u in users:
            if user == u.username:
                u.vip = '1'
                lvl = User(vip=form.viplvl.data)
                db.session.add(lvl)
                db.session.commit()
                break
    return render_template('vip.html',form=form)