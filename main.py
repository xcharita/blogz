
from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '#someSecretString'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text_blog = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text_blog, username):
        self.title = title
        self.text_blog = text_blog
        self.username = username


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(15))
    blogs = db.relationship('Blog', backref='username') 

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

@app.before_request
def require_login():
# users dont need to login to see
    allowed_routes = ['login', 'userspost', 'user_blogs', 'list_blogs','index', 'signup']
# filter all incoming request
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/')
def index():
# maak een functie waarbij alle blogs worden geprint
    users = User.query.all()
    return render_template('index.html', title='Blogz', users=users) 


@app.route('/userspost', methods=["POST", "GET"])
def userspost():
    blogs = Blog.query.all()
    users = User.query.all()
    return render_template('userspost.html', title='Blogz', blogs=blogs, users=users)

@app.route('/login', methods=["POST","GET"])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect(url_for('newpost'))
        else:
            if user and not (user.password == password):
                error = 'User password incorrect, try again'
            if not user:
                error = 'Username incorrect, try again'    
    return render_template('login.html',title="Blogz", error = error )


@app.route('/signup', methods=["POST","GET"])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            if (username == '') or (password == ''):
                error = 'Username AND password must be filled'
            if existing_user:
                error = 'Existing user'
            if not (password == verify):
                error = 'Please check your password again'
            if len(password) < 3:
                error = 'Your password should be longer than 3 characters'
            if len(username) < 3:
                error = 'Your username should be longer than 3 characters'
    return render_template('signup.html', title="Blogz", error=error)


@app.route('/newpost', methods=['POST','GET'])
def newpost():   
    owner = User.query.filter_by(username=session['username']).first()
    owner_id = owner.id
    if request.method=="POST":
        blog_name = request.form['blogtitle']
        text_blog = request.form['blogtext'] 
        new_blog = Blog(blog_name, text_blog, owner )
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('user_blogs', user_id=owner_id))
    else:
        blogs = Blog.query.filter_by(owner_id= owner_id)
        return render_template('entry.html', title="Blogz", blogs=blogs)

@app.route('/blog/<int:blog_id>', methods=['POST', 'GET'])
def list_blogs(blog_id):
#printout all the blogs with the usernames clickable
    blog = Blog.query.get(blog_id)
    return render_template('blog.html', title="Blogz", blog=blog)

@app.route('/blog/user/<int:user_id>', methods=['POST', 'GET']) 
def user_blogs(user_id):
#blogs from specific user
    blogs = Blog.query.filter_by(owner_id=user_id).all()
    return render_template('singleUser.html', title="Blogz", blogs=blogs)

# go to userspost for displaying all the posts including authors
@app.route('/logout')
def logout(): 
    session.pop('username', None)
    return redirect('/userspost')


if __name__ == '__main__':
    app.run()