from run import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

    @property
    def serialize(self):
    	return{
	    	'id' : self.id,
	    	'title' : self.title,
	    	'body' : self.body,
    	}