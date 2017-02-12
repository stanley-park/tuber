import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Student(Base):
    __tablename__ = 'student'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    sname = Column(String(250), nullable=False)
    classkey = Column(String(250), nullable=False)
    ckey = Column(String(250), nullable=False)
    radius = Column(String(250), nullable=False)
    
        


class Campus(Base):
    __tablename__ = 'campus'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    cname = Column(String(250), nullable=False)
    ckey = Column(String(250), nullable=False)
    student_classkey = Column(Integer, ForeignKey('student.classkey'))
    student = relationship(Student)
    
    
 
class Tutor(Base):
    __tablename__ = 'tutor'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    tname = Column(String(250), nullable=False)
    major = Column(String(250), nullable=False)
    year = Column(String(250), nullable=False)
    gpa = Column(String(250), nullable=False)
    language = Column(String(250), nullable=False)
    classkey = Column(String(250), nullable=False)
    
    
    student_classkey = Column(Integer, ForeignKey('student.classkey'))
    student = relationship(Student)
    campus_ckey = Column(Integer, ForeignKey('campus.ckey'))
    campus = relationship(Campus)
    student_radius = Column(Integer, ForeignKey('student.radius'))
    student = relationship(Student)
    
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///Tuber.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
