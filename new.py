# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///new_database1.db'
app.config['SECRET_KEY']='satyam98'
db=SQLAlchemy(app)
admin=Admin(app)


class Process(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	process_name=db.Column(db.String(50),nullable=False)
	#total_process=db.Column(db.Integer)
	subprocess=db.relationship('Subprocess', cascade = "all,delete",backref='Main process')#replace main process by prime 2)relaced cascade
	employee=db.relationship('Employee',cascade = "all,delete",backref='Task')
	attribute=db.relationship('Attribute',cascade = "all,delete",backref='process name')#replace process name by pro



#	att=db.relationship('Attribute',backref='att')
	def __repr__(self):
		return '<process %r>' % (self.process_name)
class Processview(ModelView):
	form_excluded_columns=('subprocess','employee','attribute')

class Subprocess(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	subprocess_name=db .Column(db.String(50),nullable=False)
	attribute=db.relationship('Attribute',cascade = "all,delete",backref='subprocess name')
	prime_id=db.Column(db.Integer,db.ForeignKey('process.id'))
	#here we are also required to specify the nature of the value atribute expects.
	#is_subprocess = db.relationship( 'Process', uselist=False, remote_side=[id], post_update=True)
	def __repr__(self):
		return '<Subprocess %r>' % (self.subprocess_name)
class Subprocessview(ModelView):
	form_excluded_columns=('attribute')

class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	employee_name=db.Column(db.String(50),nullable=False)
	employee_password=db.Column(db.String(10),nullable=False)
	attribute_filled=db.relationship('Attribute',cascade = "all,delete",backref='Employee name')
	task_id=db.Column(db.Integer,db.ForeignKey('process.id'))
	def __repr__(self):
		return '<Employee %r>' % (self.employee_name)
class Employeeview(ModelView):
	form_excluded_columns=('attribute_filled')

class Attribute(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	value=db.Column(db.String(100),nullable=False)
	sub_id=db.Column(db.Integer,db.ForeignKey('subprocess.id'),nullable=False)
	emp_id=db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=False)
	pro_id=db.Column(db.Integer,db.ForeignKey('process.id'),nullable=False)
#	att_id=db.Column(db.Integer,db.ForeignKey('process.id'),nullable=False)
	def __repr__(self):
		return '<Set %r>' % (self.id) 
db.create_all()
'''
@app.route('/',methods=['GET','POST'])

def process():
	if request.method=='POST':
		conn=sqlite3.connect('new_database.db')
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

'''
admin.add_view(Processview(Process,db.session))
admin.add_view(Subprocessview(Subprocess,db.session))
admin.add_view(Employeeview(Employee,db.session))
admin.add_view(ModelView(Attribute,db.session))

if __name__ == '__main__':
   app.run(debug = True)



