
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text_blog = db.Column(db.String(500))

    def __init__(self, title, text_blog):
        self.title = title
        self.text_blog = text_blog


@app.route('/')
def index():
  blogs = Blog.query.all()
  return render_template('index.html',title="Build-a-Blog", blogs=blogs )

    
@app.route('/newpost', methods=['POST', 'GET'])
def entry():
    
    if request.method == "POST":
        blog_name = request.form['blogtitle']
        text_blog = request.form['blogtext']
        new_blog = Blog(blog_name, text_blog)
        db.session.add(new_blog)
        db.session.commit()
        blogid = Blog.query.filter_by(title=blog_name).first()
        newblogid = blogid.id
        return redirect(url_for('blog', blog_id = newblogid))
    else:
        blogs = Blog.query.all()
        return render_template('entry.html',title="Build-a-Blog", blogs=blogs)    

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    if blog_id == None:
        return render_template('index.html',title="Build-a-Blog", blog=blog )
    else:
        blog = Blog.query.get(blog_id)
        return render_template('blogs.html',title="Build-a-Blog", blog=blog)


@app.route('/delete-blog', methods=['POST'])
def delete_blog():
    blog_id = (request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect('/')
  

if __name__ == '__main__':
app.run()