#SQLALCHEMY_TRACK_MODIFICATIONS = False
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/prakhar/Desktop/Diary/diary.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

@app.route("/all")
def all_posts():
	posts = Note.query.all()
	return render_template("all_entries.html",posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Note.query.filter_by(id=post_id).one()	
	return render_template("post.html",post=post)

@app.route("/post_delete/<int:post_id>",methods=["GET","POST"])
def delete_post(post_id):
	delete_this = Note.query.get(post_id)
	db.session.delete(delete_this)
	db.session.commit()

	return redirect(url_for('all_posts'))

@app.route('/edit/<int:post_id>' , methods=['POST', 'GET'])
def edit_post(post_id):

    post = Note.query.get(post_id)
    if request.method == 'POST':         
        post.title = request.form['title']
        post.body =  request.form['body']
        db.session.commit()
        return redirect(url_for('all_posts'))
    
    return render_template('edit_post.html', post=post)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def create_note():
    if request.method == "GET":
        return render_template("new_entry.html")
    else:
        title = request.form["title"]
        body = request.form["body"]

        note = Note(title = title, body = body)
        
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('all_posts'))    

if __name__ == "__main__":
	app.run(debug=True)