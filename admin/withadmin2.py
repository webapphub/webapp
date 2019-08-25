# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlite3
import time
import datetime
from datetime import datetime

now = datetime.now()
ts = time.time()

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


class Entries(db.Model):
	id=db.Column(db.Integer,primary_key=True)

	employee_name=db.Column(db.String(50),nullable=False)
	main_process=db.Column(db.String(50),nullable=False)
        sub_process=db.Column(db.String(50),nullable=False)
        attribute_name=db.Column(db.String(50),nullable=False)
        attribute_value=db.Column(db.String(50),nullable=False)
	start_time = db.Column(db.DateTime(timezone=True),default=datetime.utcnow())

db.create_all()

admin.add_view(Processview(Process,db.session))
admin.add_view(Subprocessview(Subprocess,db.session))
admin.add_view(Employeeview(Employee,db.session))
admin.add_view(ModelView(Attribute,db.session))
admin.add_view(ModelView(Entries,db.session))


@app.route("/add", methods=["POST"])
def add():
    try:
        newvalue = request.form.get("newvalue")
        
	pro_id = request.form.get("pro_id")
 	sub_id = request.form.get("sub_id")
 	emp_id = request.form.get("emp_id")
 	attr_name = request.form.get("attr_name")
	#timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	#timestamp = datetime.datetistrftime(string_datetime[:len(string_datetime) - 3] + string_datetime[len(string_datetime) - 2:],'%Y-%m-%dT%H:%M:%S%z')
	#timestamp=datetime.utcnow()     
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')   
	entries=Entries					(employee_name=emp_id,main_process=pro_id,sub_process=sub_id,attribute_name=attr_name,attribute_value=newvalue)
	db.session.add(entries)        
	db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
 
    return redirect("./employee")





@app.route('/employee',methods=['GET','POST'])
def employee():
	attr=None
	employee=None
	if request.method=='POST':
		
		employee=Employee.query.filter_by(employee_password=request.form['employee_id']).first()
		attr=Attribute.query.filter_by(emp_id=employee.id).all()


	return render_template('employee_entries.html',attribute=attr,emp=employee)
	return redirect('./employee')

if __name__ == '__main__':
   app.run(debug = True)

