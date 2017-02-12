from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from TuberDB import Student, Base, Tutor, Campus
 
engine = create_engine('sqlite:///Tuber.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert a Student in the person table
new_student = Student(sname='Mark',id='0001',classkey='cse 20',ckey='05',radius ='1')
session.add(new_student)
session.commit()

 




      
# Insert a Campus
new_cname = Campus(cname='UC Merced')
session.add(new_cname)
session.commit()

new_campus = Campus(ckey='05')
session.add(new_campus)
session.commit()
# Insert Tutor info
new_tutor = Tutor(tname='Oscar')
session.add(new_tutor)
session.commit()

new_tid = Student(id='0002')
session.add(new_tid)
session.commit()

new_major = Tutor(major='Computer Science')
session.add(new_major)
session.commit()

new_year = Tutor(year='Year:Sophomore')
session.add(new_major)
session.commit()

new_gpa = Tutor(gpa='3.5')
session.add(new_gpa)
session.commit()

new_language = Tutor(language='Portugese')
session.add(new_language)
session.commit()

new_classkey = Tutor(classkey='cse 20')
session.add(new_major)
session.commit()

new_ckey = Tutor(ckey='05')
session.add(new_ckey)
session.commit()

new_radius = Tutor(radius='1')
session.add(new_radius)
session.commit()

