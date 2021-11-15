from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/372hw1'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department_code = db.Column(db.String(31), unique=True, nullable=False)
    department_name = db.Column(db.String(31), unique=True, nullable=False)
    top_department_code = db.Column(db.String, db.ForeignKey(
        'departments.department_code'))
    city_code = db.Column(db.String, db.ForeignKey(
        'cities.city_code'), nullable=False)
    district_code = db.Column(db.String, db.ForeignKey(
        'districts.district_code'), nullable=False)
    post_code = db.Column(db.String(31), nullable=False)
    manager_username = db.Column(
        db.String, db.ForeignKey('users.username'), nullable=False)

    def __init__(self, department_code, department_name, top_department_code, city_code, district_code, post_code, manager_username):
        self.department_code = department_code
        self.department_name = department_name
        self.top_department_code = top_department_code
        self.city_code = city_code
        self.district_code = district_code
        self.post_code = post_code
        self.manager_username = manager_username


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(31), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    email = db.Column(db.String(31), unique=True, nullable=False)
    first_name = db.Column(db.String(31), nullable=False)
    last_name = db.Column(db.String(31), nullable=False)
    ssn = db.Column(db.String(31), unique=True, nullable=False)
    mobile = db.Column(db.String(31), nullable=False)
    address = db.Column(db.String(31), nullable=False)
    city_code = db.Column(db.String, db.ForeignKey(
        'cities.city_code'), nullable=False)
    district_code = db.Column(db.String, db.ForeignKey(
        'districts.district_code'), nullable=False)
    post_code = db.Column(db.String(31), nullable=False)
    top_username = db.Column(db.String, db.ForeignKey('users.username'))
    department_code = db.Column(
        db.String, db.ForeignKey('departments.department_code'))

    def __init__(self, username, email, first_name, last_name, ssn, mobile, address, city_code, district_code, post_code, top_username, department_code):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn
        self.mobile = mobile
        self.address = address
        self.city_code = city_code
        self.district_code = district_code
        self.post_code = post_code
        self.top_username = top_username
        self.department_code = department_code


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city_code = db.Column(db.String(31), unique=True, nullable=False)
    city_name = db.Column(db.String(127), unique=True, nullable=False)

    def __init__(self, city_code, city_name):
        self.city_code = city_code
        self.city_name = city_name


class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    district_code = db.Column(
        db.String(31), unique=True, nullable=False)
    district_name = db.Column(db.String(127), unique=True, nullable=False)
    city_code = db.Column(db.String, db.ForeignKey(
        'cities.city_code'), nullable=False)

    def __init__(self, district_code, district_name, city_code):
        self.district_code = district_code
        self.district_name = district_name
        self.city_code = city_code


class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    problem_definition = db.Column(db.String(31), nullable=False)
    problem_definer_first_name = db.Column(db.String(31), nullable=False)
    problem_definer_last_name = db.Column(db.String(31), nullable=False)
    problem_definer_ssn = db.Column(db.String(31), nullable=False)
    problem_purpose = db.Column(db.String(31))

    def __init__(self, problem_definiton, problem_definer_first_name, problem_definer_last_name, problem_definer_ssn, problem_purpose):
        self.problem_definition = problem_definiton
        self.problem_definer_first_name = problem_definer_first_name
        self.problem_definer_last_name = problem_definer_last_name
        self.problem_definer_ssn = problem_definer_ssn
        self.problem_purpose = problem_purpose


class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(31), nullable=False)
    area_type = db.Column(db.Boolean, nullable=False)

    def __init__(self, area_name, area_type):
        self.area_name = area_name
        self.area_type = area_type


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(31), nullable=False)
    class_type = db.Column(db.Boolean, nullable=False)

    def __init__(self, class_name, class_type):
        self.class_name = class_name
        self.class_type = class_type


class Operation(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True)
    operation_name = db.Column(db.String(31), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey(
        'areas.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(
        'classes.id'), nullable=False)

    def __init__(self, operation_name, area_id, class_id):
        self.operation_name = operation_name
        self.area_id = area_id
        self.class_id = class_id


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    activity_definition = db.Column(db.String(31), nullable=False)

    def __init__(self, activity_definition):
        self.activity_definition = activity_definition


class Output(db.Model):
    __tablename__ = 'outputs'
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey(
        'areas.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(
        'classes.id'), nullable=False)
    output_name = db.Column(db.String(31), nullable=False)

    def __init__(self, area_id, class_id, output_name):
        self.area_id = area_id
        self.class_id = class_id
        self.output_name = output_name
