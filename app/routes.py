from app import app
from flask import render_template,url_for,request,redirect,flash
from app.forms import LoginForm,RegistrationForm,predlogForm,EditProfileForm,PostForm,vipForm,deleteForm,commentsForm
from flask_login import current_user,login_user,logout_user
from app.models import User,Post,Offer,DeletedPost,DeleteUser,comm,deletedcomm
from flask_login import login_required
from app import db
from app import mail
from flask_mail import Message
from threading import Thread

def async_mail(f):
    def wrapper(*args,**kwargs):
        t = Thread(target=f,args=args,kwargs=kwargs)
        t.start()
    return wrapper 

@async_mail
def send_async_mail(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject,sender,to_who,text_body='',html_body=''):
    msg = Message(subject=subject,sender=sender,recipients=to_who)
    msg.body = text_body
    msg.html = html_body
    send_async_mail(msg)

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
@login_required
def predlog():
    info = Offer.query.order_by(Offer.timestamp.desc()).first()
    form = predlogForm()
    if form.validate_on_submit():
        user = Offer(FirstName = form.FirstName.data, LastName=form.LastName.data,offer=form.Offer.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('AdminPage'))
    return render_template('predlog.html', form=form)
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        AboutMeInfo = AboutMe(UserName = current_user.username,about_me = form.about_me.data , age=form.age.data,city=form.city.data,Music = form.Music.data,Work=form.work.data,FirstName=form.FirstName.data, SecondName=form.SecondName.data,language=form.language.data)
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
    delete = deleteForm()
    form=PostForm()
    vip = '1'
    user=User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    comments = comm.query.all()
    current_user.body = form.post.data
    if delete.validate_on_submit():
        for u in posts:
            if u.author == user.username:
                delpost = DeletedPost(delbody = u.body, delauthor=u.author,deltimestamp=u.timestamp)
                db.session.delete(u)
                db.session.add(delpost)
                db.session.commit()
                break
        for u in comments:
            if u.commentauthor == user.username:
                delcom = deletedcomm(delcombody = u.commentbody, delcomauthor = u.commentauthor,delcommentid=u.commentid)
                db.session.delete(u) 
                db.session.add(delcom) 
                db.session.commit()
        deluser=DeleteUser(delusername = user.username, delpassword_hash= user.email, delemail = user.email, delvip=user.vip, dellast_seen = user.last_seen,)
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
@login_required
def post():
    form = PostForm()
    comment = commentsForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user.username)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("post.html", title='Home Page', form=form,posts=posts,comment=comment,)
@app.route('/AdminPage' ,methods=['GET','POST'])
@login_required
def AdminPage():
    info = Offer.query.order_by(Offer.timestamp.desc()).first()
    form = predlogForm()
    if form.validate_on_submit():
        send_email('New order',app.config['ADMINS'][0],['artem.soglaev@mail.ru'],'SHITTTTTT',render_template('AdminPage.html',info=info))
        return redirect(url_for('index'))
    return render_template('AdminPage.html',info=info,form=form)
@app.route('/vip',methods=['GET','POST'])
@login_required
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
@app.route('/comments/<id>' ,methods=['GET','POST'])
def comments(id):
    comment=Post.query.filter_by(id=id).first_or_404()
    commentari = comm.query.all()
    form = commentsForm()
    if form.validate_on_submit():
        com = comm(commentbody = form.comments.data, commentauthor=current_user.username, commentid=comment.id)
        db.session.add(com)
        db.session.commit()
        return redirect(url_for('post'))
    return render_template('comments.html',comment=comment,form=form,commentari=commentari)