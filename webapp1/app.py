from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

import sqlite3



app=Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
db = SQLAlchemy(app)



class Mainprocess(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	subprocess = db.relationship('Subprocess', backref='owner', lazy='dynamic')

class Subprocess(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))

	owner_id = db.Column(db.Integer, db.ForeignKey('mainprocess.id'))



db.create_all()
@app.route('/',methods=['GET','POST'])


def index():
	if request.method=='POST':
		conn=sqlite3.connect('database.db')
		c=conn.cursor()
		userDetails=request.form
		main=userDetails['mainprocess']
		sub=userDetails['subprocess']
		
		c.execute("INSERT INTO Mainprocess(name) VALUES(?)",(main))
		
		c.execute("INSERT INTO Subprocess(name,owner_id) VALUES(?,?)",(sub,main))
		conn.commit()
		c.close()
		return 'success'
	return render_template('index.html')

if __name__=='__main__':
	app.run(debug=True)
