# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database3.db'
db=SQLAlchemy(app)



class Process(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	process_name=db.Column(db.String(50),nullable=False)
	subprocess=db.relationship('Subprocess',backref='prime')
	employee=db.relationship('Employee',backref='task')
#	att=db.relationship('Attribute',backref='att')

class Subprocess(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	subprocess_name=db.Column(db.String(50),nullable=False)
	attribute=db.relationship('Attribute',backref='Sub')
	prime_id=db.Column(db.Integer,db.ForeignKey('process.id'))
	#here we are also required to specify the nature of the value atribute expects.

class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	employee_name=db.Column(db.String(50),nullable=False)
	employee_password=db.Column(db.String(10),nullable=False)
	attribute_filled=db.relationship('Attribute',backref='emp')
	task_id=db.Column(db.Integer,db.ForeignKey('process.id'))

class Attribute(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	value=db.Column(db.Integer,nullable=False)
	sub_id=db.Column(db.Integer,db.ForeignKey('subprocess.id'),nullable=False)
	emp_id=db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=False)
#	att_id=db.Column(db.Integer,db.ForeignKey('process.id'),nullable=False)
db.create_all()

@app.route('/process',methods=['GET','POST'])

def process():
	if request.method=='POST':
		conn=sqlite3.connect('database3.db')
		c=conn.cursor()
		userDetails=request.form
		main=userDetails['processname']
		c.execute("INSERT INTO Process(process_name) VALUES(?)",(main))
		conn.commit()
		c.close()
		return 'success'
	return render_template('process.html')


if __name__ == '__main__':
   app.run(debug = True)



