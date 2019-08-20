from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import config

import sqlite3



app=Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database10.db"
db = SQLAlchemy(app)




class Process(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	process_name=db.Column(db.String(50),nullable=False)
	subprocess=db.relationship('Subprocess',backref='prime')
	
#	att=db.relationship('Attribute',backref='att')

class Subprocess(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	subprocess_name=db.Column(db.String(50),nullable=False)
	employee=db.relationship('Employee',backref='task')
	prime_id=db.Column(db.Integer,db.ForeignKey('process.id'))
        
	#here we are also required to specify the nature of the value atribute expects.

class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	employee_name=db.Column(db.String(50),nullable=False)
	employee_id=db.Column(db.String(10),nullable=False)
	attribute_filled=db.relationship('Attribute',backref='assign')
	task_id=db.Column(db.Integer,db.ForeignKey('subprocess.id'))

class Attribute(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	value=db.Column(db.Integer,nullable=False)
	
	emp_id=db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=False)
#	att_id=db.Column(db.Integer,db.ForeignKey('process.id'),nullable=False)








db.create_all()

@app.route('/',methods=['GET','POST'])


def index():
	if request.method=='POST':
		conn=sqlite3.connect('database10.db')
		c=conn.cursor()
		Details=request.form
		
                mainp=Details['mainprocess']
		subp=Details['subprocess']
		emp_name=Details['employee_name']
		emp_id=Details['employee_id']
		attr_value=Details['attribute']	
		
                main=Process(process_name=mainp)
		db.session.add(main)		
		db.session.commit()
		
		sub=Subprocess(subprocess_name=subp,prime=main)
		db.session.add(sub)		
		db.session.commit()



		emp=Employee(employee_name=emp_name,employee_id=emp_id,task=sub)
		db.session.add(emp)		
		db.session.commit()


		attr=Attribute(value=attr_value,assign=emp)
		db.session.add(attr)		
		db.session.commit()

		
		conn.commit()
		c.close()
		return 'success'
	return render_template('index.html')

if __name__=='__main__':
	app.run(debug=True)
