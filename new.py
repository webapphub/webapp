# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///abb5.db'
app.config['SECRET_KEY']='satyam98'
db=SQLAlchemy(app)
admin=Admin(app)


class Process(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	process_name=db.Column(db.String(50),nullable=False)
	#total_process=db.Column(db.Integer)
	subprocess=db.relationship('Subprocess',backref='prime')
	employee=db.relationship('Employee',backref='task')
#	att=db.relationship('Attribute',backref='att')
class Processview(ModelView):
	column_excluded_list=('subprocess','employee')

class Subprocess(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	subprocess_name=db .Column(db.String(50),nullable=False)
	attribute=db.relationship('Attribute',backref='Sub')
	prime_id=db.Column(db.Integer,db.ForeignKey('process.id'))
	#here we are also required to specify the nature of the value atribute expects.
	def __repr_(self):
		return '<Set %r>' % (self.id)

class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	employee_name=db.Column(db.String(50),nullable=False)
	employee_password=db.Column(db.String(10),nullable=False)
	attribute_filled=db.relationship('Attribute',backref='emp')
	task_id=db.Column(db.Integer,db.ForeignKey('process.id'))
	def __repr_(self):
		return '<Set %r>' % (self.id)

class Attribute(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	value=db.Column(db.Integer,nullable=False)
	sub_id=db.Column(db.Integer,db.ForeignKey('subprocess.id'),nullable=False)
	emp_id=db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=False)
#	att_id=db.Column(db.Integer,db.ForeignKey('process.id'),nullable=False)
	def __repr_(self):
		return '<Set %r>' % (self.id) 
db.create_all()

@app.route('/',methods=['GET','POST'])

def process():
	if request.method=='POST':
		conn=sqlite3.connect('abb5.db')
		c=conn.cursor()
		userDetails=request.form
		main=userDetails['processname']
		#num=userDetails['totalpro']
		mainp=Process(process_name=main)
		db.session.add(mainp)
		db.session.commit()
		conn.commit()
		c.close()
		return 'success'
	return render_template('process.html')
def subprocess():
	if request.method=='POST':
		conn=sqlite3.connect('abb.db')
		c=conn.cursor()
		userDetails=request.form

admin.add_view(Processview(Process,db.session))
admin.add_view(ModelView(Subprocess,db.session))
admin.add_view(ModelView(Employee,db.session))
admin.add_view(ModelView(Attribute,db.session))

if __name__ == '__main__':
   app.run(debug = True)



