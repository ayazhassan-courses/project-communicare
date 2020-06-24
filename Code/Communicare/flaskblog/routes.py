import os
import secrets
from datetime import datetime
from PIL import Image
from flask import render_template, url_for , flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import sys
from geopy.geocoders import Nominatim






@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


def calcdist(lat1,lon1,lat2,lon2):
    from math import sin, cos, sqrt, atan2, radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    R_earth = 6373.0

    distlat = lat2 - lat1
    distlon = lon2 - lon1


    tval = sin(distlat / 2)**2 + cos(lat1) * cos(lat2) * sin(distlon / 2)**2
    tval2 = 2 * atan2(sqrt(tval), sqrt(1 - tval))

    distance = R_earth * tval2
    return round(distance,2)


def quickSort(lst,col,cond):
    flst = quickSortreal(lst,0,len(lst)-1,col)
    if cond:
        return flst
    else:
        flst.reverse()
        return flst

def quickSortreal(lst,low,high,col):
    if low>=high:
        return 
    else:
        elesort = partition(lst,low,high,col)
        quickSortreal(lst,low,elesort[1],col)
        quickSortreal(lst,elesort[0],high,col)
        return lst
 
def partition(lst,low,high,col):
    mid = (low+high)//2
    pivot = lst[mid] 
    i = low
    j = high

    while(j>=i):
        while(lst[i][col]<pivot[col]):
            i+=1
        while(lst[j][col]>pivot[col]):
            j-=1
        if i<=j:
            lst[i], lst[j] = lst[j] , lst[i]
            i+=1
            j-=1

    return (i,j) 


def sort_locations(database, sortwrt):
    tvalwrt = sortwrt.split(',')
    tlst = []
    flst=[]
    for post in range(len(database)):
        tval = database[post]['location2'].split(',')
        distance = calcdist(tvalwrt[0],tvalwrt[1],tval[0],tval[1])
        tlst.append((post,distance))
    
    column = 1
    ascending = False
    sortedlst = quickSort(tlst, column, ascending)
    for fpost in sortedlst:
        flst.append(database[fpost[0]])
    return flst 

@app.route('/home')
def home():
    #page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc())
    Post_x = []
    for post in posts:
        post_x = {'title': post.title , 'location': post.location, 'phone_no': post.phone_no, 'content':post.content, 'author': post.author , 'username': post.author.username, 'date_posted': post.date_posted , 'location2': post.location2, 'id': post.id}
        Post_x.append(post_x)
    if len(current_user.location)!=0 and len(Post_x)>2: 
        Post_f = sort_locations(Post_x, current_user.location)
        return render_template("home.html", posts = Post_f)
    else: return render_template("home.html", posts = Post_x)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data ,  email = form.email.data, password= hashed_password )
        db.session.add(user)
        db.session.commit()
        flash('Your account is now created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Register', form= form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('Just loggedin', file=sys.stderr)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print(form.location.data, file=sys.stderr)
            print(form.email.data, file=sys.stderr)
            print('location print', file=sys.stderr)
            user.location = form.location.data
            db.session.commit()
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')  # args is dictionary
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log in unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account is updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename= 'pics/' + current_user.image_file)
    return render_template('account.html', title= 'Account',
                            image_file= image_file, form=form)

# Have to edit
@app.route("/post/new", methods= ['GET', 'POST'])
@login_required #Login hoga tab hi post krsakta hai
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, location = form.location.data, phone_no = form.phone_no.data,  content= form.content.data, author= current_user)
        print('Location', file=sys.stderr)
        print(form.location.data, file=sys.stderr)
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(form.location.data)
        print(location.latitude, location.longitude, file=sys.stderr)
        post.location2 = str(location.latitude)+','+str(location.longitude)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title= 'New Post', form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post',
#                            form=form, legend='Update Post')

@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page = page, per_page=5)
    return render_template("user_posts.html", posts = posts, user=user)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Thanks for Caring!', 'success')
    return redirect(url_for('home'))

