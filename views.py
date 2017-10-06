from run import app,db
from models import Note
from flask import render_template,redirect,url_for,request, jsonify

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

@app.route("/all/JSON")
def postsJSON():
    posts = Note.query.all()
    return jsonify(posts=[p.serialize for p in posts])

@app.route("/post/<int:post_id>/JSON")
def entryJSON(post_id):
    entry = Note.query.filter_by(id=post_id).one()   
    return jsonify(entry.serialize)

