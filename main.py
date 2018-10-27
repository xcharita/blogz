
from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(15))
#    blogs = db.relationship('Blog', backref='user') 

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text_blog = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text_blog, username):
        self.title = title
        self.text_blog = text_blog
        self.username = username

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/blogs', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(new_blog).all()
    return render_template('index.html', blogs=blogs)
    
   
@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
#            blog_id = user.blogs
            #session['username'] = username
            # login
            return redirect('/')
        else:
            # login failed
            return '<h1>Error</h1>'
     
    return render_template('login.html',title="Blogz" )


@app.route('/signup', methods=["POST","GET"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        #validate data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
 #           session['username'] = username
            return redirect('/')
        else:
            #user exist in db
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')



@app.route('/logout')
def logout():
    del session['username']
    return "<h1>Thank you for blogging with us!</h1>"

'''
@app.route('/allpost')
def blog():

@app.route('/newpost', methods=["POST","GET"])
def newpost():
    if request.method=="POST":
        blog.name = request.form['blogtitle']
        text_blog = request.form['blogtext']
        new_blog = Blog(blog_name, text_blog)
        db.session.add(new_blog)
        db.session.commit()
        blogid = Blog.query.filter_by(title=blog_name).first()
        newblogid = blogid.id
        return redirect(url_for('blog', blog_id = newblogid))
    else:
        blogs = Blog.query.all()
        return render_template('entry.html', title=Blogz", blogs=blogs)

@app.route('/blog/<int:blog_id>')
def blog(blog_id)
if blog_id == None:
    return render_template('index.html', title="Blogz", blog=blog)
else:
    blog = Blog.query.get(blog_id)
    return render_template('blog.html', title="Blogb", blog=blog)
'''
if __name__ == '__main__':
    app.run()