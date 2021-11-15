from os import name
import re
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Classes import User, Employee, Department, City, District, Problem, Area, Class, Operation, Activity, Output
import bcrypt
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
salt = b'$2b$12$yikfuoh7WR/uE2iw/aWD2.'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/city', methods=['POST', 'GET'])
@app.route('/city/<city_code>', methods=['POST', 'GET'])
def city(city_code=None):
    city = db.session.query(City).filter(
        City.city_code == city_code).first()
    if request.method == 'GET':
        return render_template('city.html', city_code=city.city_code, city_name=city.city_name)
    elif request.method == 'POST':
        name = request.form['city_name']
        city.city_name = name
        db.session.commit()
        return redirect(url_for('all_cities'))


@app.route('/delete_city')
@app.route('/delete_city/<city_code>')
def delete_city(city_code=None):
    if city_code != None:
        try:
            db.session.query(City).filter(City.city_code == city_code).delete()
            db.session.commit()
        except:
            return render_template('all_cities.html', message='Could not delete, please check references.')
    return redirect(url_for('all_cities'))


@app.route('/create_city', methods=['POST', 'GET'])
def create_city():
    if request.method == 'GET':
        return render_template('create_city.html')
    elif request.method == 'POST':
        city_name = request.form['city_name']
        city_code = request.form['city_code']
        if city_name == '' or city_code == '':
            return render_template('create_city.html', error_message='Please fill all required fields.')
        if db.session.query(City).filter(City.city_code == city_code).count() != 0:
            return render_template('create_city.html', error_message='This city code has already exists, please select another code.')
        data = City(city_code, city_name)
        db.session.add(data)
        db.session.commit()
        return render_template('create_city.html', success_message='City created succesfully.')


@app.route('/all_cities', methods=['GET'])
def all_cities():
    return render_template('all_cities.html', rows=db.session.query(City).all())


@app.route('/create_district', methods=['POST', 'GET'])
def create_district():
    if request.method == 'GET':
        return render_template('create_district.html')
    elif request.method == 'POST':
        district_name = request.form['district_name']
        district_code = request.form['district_code']
        city_code = request.form['city_code']
        if district_name == '' or district_code == '' or city_code == '':
            return render_template('create_district.html', error_message='Please fill all required fields.')

        if db.session.query(District).filter(District.district_code == district_code).count() != 0:
            return render_template('create_district.html', error_message='This district code has already exists, please select another code.')
        if db.session.query(City).filter(City.city_code == city_code).count() == 0:
            return render_template('create_district.html', error_message="This city code doesn't exists, please select another code.")
        data = District(district_code, district_name, city_code)
        db.session.add(data)
        db.session.commit()
        return render_template('create_district.html', success_message='District created succesfully.')


@app.route('/all_districts', methods=['GET'])
def all_districts():
    return render_template('all_districts.html', rows=db.session.query(District).all())


@app.route('/delete_district')
@app.route('/delete_district/<district_code>')
def delete_district(district_code=None):
    if district_code != None:
        db.session.query(District).filter(
            District.district_code == district_code).delete()
        db.session.commit()

    return redirect(url_for('all_districts'))


@app.route('/district', methods=['POST', 'GET'])
@app.route('/district/<district_code>', methods=['POST', 'GET'])
def district(district_code=None):
    district = db.session.query(District).filter(
        District.district_code == district_code).first()
    if request.method == 'GET':
        return render_template('district.html', city_code=district.city_code, district_name=district.district_name, district_code=district.district_code)
    elif request.method == 'POST':
        name = request.form['district_name']
        district.district_name = name
        db.session.commit()
        return redirect(url_for('all_districts'))


@app.route('/all_departments', methods=['GET'])
def all_departments():
    return render_template('all_departments.html', rows=db.session.query(Department).all())


@app.route('/create_department', methods=['POST', 'GET'])
def create_department():
    if request.method == 'GET':
        return render_template('create_department.html')
    elif request.method == 'POST':
        department_code = request.form['department_code']
        department_name = request.form['department_name']
        top_department_code = request.form['top_department_code']
        city_code = request.form['city_code']
        district_code = request.form['district_code']
        post_code = request.form['post_code']
        manager_username = request.form['manager_username']
        if department_name == '' or department_code == '' or top_department_code == '' or city_code == '' or district_code == '' or post_code == '' or manager_username == '':
            return render_template('create_department.html', error_message='Please fill all required fields.')

        if db.session.query(Department).filter(Department.department_code == department_code).count() != 0:
            return render_template('create_department.html', error_message='This department code has already exists, please select another code.')

        if db.session.query(City).filter(City.city_code == city_code).count() == 0:
            return render_template('create_department.html', error_message="This city code doesn't exists, please select another code.")
        if db.session.query(District).filter(District.district_code == district_code).count() == 0:
            return render_template('create_department.html', error_message="This district code doesn't exists, please select another code.")
        if db.session.query(User).filter(User.username == manager_username).count() == 0:
            return render_template('create_department.html', error_message="This username code doesn't exists, please select another code.")

        data = Department(department_code, department_name,
                          top_department_code, city_code, district_code, post_code, manager_username)
        db.session.add(data)
        db.session.commit()
        return render_template('create_department.html', success_message='Department created succesfully.')


@app.route('/delete_department')
@app.route('/delete_department/<department_code>')
def delete_department(department_code=None):
    if department_code != None:
        try:
            db.session.query(Department).filter(
                Department.department_code == department_code).delete()
            db.session.commit()
        except:
            return render_template('all_departments.html', message='Could not delete, please check references.')
    return redirect(url_for('all_departments'))


@app.route('/department', methods=['POST', 'GET'])
@app.route('/department/<department_code>', methods=['POST', 'GET'])
def department(department_code=None):
    department = db.session.query(Department).filter(
        Department.department_code == department_code).first()
    if request.method == 'GET':
        return render_template('department.html', department_code=department.department_code,
                               department_name=department.department_name,
                               top_department_code=department.top_department_code,
                               city_code=department.city_code,
                               district_code=department.district_code,
                               post_code=department.post_code,
                               manager_username=department.manager_username)

    elif request.method == 'POST':
        if db.session.query(City).filter(City.city_code == request.form['city_code']).count() == 0:
            return render_template('create_department.html', error_message="This city code doesn't exists, please select another code.")
        if db.session.query(District).filter(District.district_code == request.form['district_code']).count() == 0:
            return render_template('create_department.html', error_message="This district code doesn't exists, please select another code.")
        if db.session.query(User).filter(User.username == request.form['manager_username']).count() == 0:
            return render_template('create_department.html', error_message="This username code doesn't exists, please select another code.")
        department.department_name = request.form['department_name']
        department.top_department_code = request.form['top_department_code']
        department.city_code = request.form['city_code']
        department.district_code = request.form['district_code']
        department.post_code = request.form['post_code']
        department.manager_username = request.form['manager_username']
        db.session.commit()
        return redirect(url_for('all_departments'))


@app.route('/all_employees', methods=['GET'])
def all_employees():
    return render_template('all_employees.html', rows=db.session.query(Employee).all())


@app.route('/create_employee', methods=['POST', 'GET'])
def create_employee():
    if request.method == 'GET':
        return render_template('create_employee.html')

    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        ssn = request.form['ssn']
        mobile = request.form['mobile']
        address = request.form['address']
        city_code = request.form['city_code']
        district_code = request.form['district_code']
        post_code = request.form['post_code']
        top_username = request.form['top_username']
        department_code = request.form['department_code']

        if username == '' or email == '' or first_name == '' or last_name == '' or ssn == '' or mobile == '' or address == '' or city_code == '' or district_code == '' or post_code == '' or top_username == '' or department_code == '':
            return render_template('create_employee.html', error_message='Please fill all required fields.')

        if db.session.query(Employee).filter(Employee.username == username).count() != 0:
            return render_template('create_employee.html', error_message='This username has already exists, please select.')

        if db.session.query(City).filter(City.city_code == city_code).count() == 0:
            return render_template('create_employee.html', error_message="This city code doesn't exists, please select another code.")
        if db.session.query(District).filter(District.district_code == district_code).count() == 0:
            return render_template('create_employee.html', error_message="This district code doesn't exists, please select another code.")
        if db.session.query(Department).filter(Department.department_code == department_code).count() == 0:
            return render_template('create_employee.html', error_message="This department code doesn't exists, please select another code.")
        if db.session.query(User).filter(User.username == top_username).count() == 0:
            return render_template('create_employee.html', error_message="Top username code doesn't exists, please select another code.")

        data = Employee(username, email, first_name, last_name, ssn, mobile, address, city_code,
                        district_code, post_code, top_username, department_code)
        db.session.add(data)
        db.session.commit()
        return render_template('create_employee.html', success_message='Employee created succesfully.')


@app.route('/employee', methods=['POST', 'GET'])
@app.route('/employee/<username>', methods=['POST', 'GET'])
def employee(username=None):

    employee = db.session.query(Employee).filter(
        Employee.username == username).first()
    if request.method == 'GET':
        return render_template('employee.html', username=employee.username,
                               email=employee.email,
                               first_name=employee.first_name,
                               last_name=employee.last_name,
                               ssn=employee.ssn,
                               mobile=employee.mobile,
                               address=employee.address,
                               city_code=employee.city_code,
                               district_code=employee.district_code,
                               post_code=employee.post_code,
                               top_username=employee.top_username,
                               department_code=employee.department_code)

    elif request.method == 'POST':
        if db.session.query(City).filter(City.city_code == request.form['city_code']).count() == 0:
            return render_template('create_employee.html', error_message="This city code doesn't exists, please select another code.")
        if db.session.query(District).filter(District.district_code == request.form['district_code']).count() == 0:
            return render_template('create_employee.html', error_message="This district code doesn't exists, please select another code.")
        if db.session.query(Department).filter(Department.department_code == request.form['department_code']).count() == 0:
            return render_template('create_employee.html', error_message="This department code doesn't exists, please select another code.")
        if db.session.query(User).filter(User.username == request.form['top_username']).count() == 0:
            return render_template('create_employee.html', error_message="Top username code doesn't exists, please select another code.")
        employee.email = request.form['email']
        employee.first_name = request.form['first_name']
        employee.last_name = request.form['last_name']
        employee.ssn = request.form['ssn']
        employee.mobile = request.form['mobile']
        employee.address = request.form['address']
        employee.post_code = request.form['post_code']
        employee.city_code = request.form['city_code']
        employee.district_code = request.form['district_code']
        employee.top_username = request.form['top_username']
        employee.department_code = request.form['department_code']
        db.session.commit()
        return redirect(url_for('all_employees'))


@app.route('/delete_employee')
@app.route('/delete_employee/<username>')
def delete_employee(username=None):
    if username != None:
        try:
            db.session.query(Employee).filter(
                Employee.username == username).delete()
            db.session.commit()
        except:
            return render_template('all_employees.html', message='Could not delete, please check references.')
    return redirect(url_for('all_employees'))


@app.route('/all_users', methods=['GET'])
def all_users():
    return render_template('all_users.html', rows=db.session.query(User).all())


@app.route('/delete_user')
@app.route('/delete_user/<username>')
def delete_user(username=None):
    if username != None:
        try:
            db.session.query(User).filter(
                User.username == username).delete()
            db.session.commit()
        except:
            return render_template('all_users.html', message='Could not delete, please check references.')
    return redirect(url_for('all_users'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            return render_template('index.html', message='Please enter username and password.')

        hashed = db.session.query(User).filter(
            User.username == username).first().password
        if bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8") == hashed:
            return render_template('home.html')
        else:
            return render_template('index.html', message='Invalid username or password.')
    elif request.method == 'GET':
        return render_template('index.html')


@app.route('/all_problems', methods=['GET'])
def all_problems():
    return render_template('all_problems.html', rows=db.session.query(Problem).all())


@app.route('/all_areas', methods=['GET'])
def all_areas():
    return render_template('all_areas.html', rows=db.session.query(Area).all())


@app.route('/delete_area/<id>')
def delete_area(id=None):
    if id != None:
        try:
            db.session.query(Area).filter(
                Area.id == id).delete()
            db.session.commit()
        except:
            return render_template('all_areas.html', message='Could not delete, please check references.')
    return redirect(url_for('all_areas'))


@app.route('/all_classes', methods=['GET'])
def all_classes():
    return render_template('all_classes.html', rows=db.session.query(Class).all())


@app.route('/delete_class/<id>')
def delete_class(id=None):
    if id != None:
        try:
            db.session.query(Class).filter(
                Class.id == id).delete()
            db.session.commit()
        except:
            return render_template('all_classes.html', message='Could not delete, please check references.')
    return redirect(url_for('all_classes'))


@app.route('/all_operations', methods=['GET'])
def all_operations():
    return render_template('all_operations.html', rows=db.session.query(Operation).all())


@app.route('/create_operation', methods=['POST', 'GET'])
def create_operation():
    if request.method == 'GET':
        return render_template('create_operation.html')
    elif request.method == 'POST':
        operation_name = request.form['operation_name']
        area_id = request.form['area_id']
        class_id = request.form['class_id']
        if operation_name == '' or area_id == '' or class_id == '':
            return render_template('create_operation.html', error_message='Please fill all required fields.')
        if db.session.query(Area).filter(Area.id == area_id).count() == 0:
            return render_template('create_operation.html', error_message="This area id doesn't exists, please select another id.")
        if db.session.query(Class).filter(Class.id == class_id).count() == 0:
            return render_template('create_operation.html', error_message="This class id doesn't exists, please select another id.")
        data = Operation(operation_name, area_id, class_id)
        db.session.add(data)
        db.session.commit()
        return render_template('create_operation.html', success_message='Operation created succesfully.')


@app.route('/delete_operation/<id>')
def delete_operation(id=None):
    if id != None:
        try:
            db.session.query(Operation).filter(
                Operation.id == id).delete()
            db.session.commit()
        except:
            return render_template('all_operations.html', message='Could not delete, please check references.')
    return redirect(url_for('all_operations'))


@app.route('/all_outputs', methods=['GET'])
def all_outputs():
    return render_template('all_outputs.html', rows=db.session.query(Output).all())


@app.route('/delete_output/<id>')
def delete_output(id=None):
    if id != None:
        try:
            db.session.query(Output).filter(
                Output.id == id).delete()
            db.session.commit()
        except:
            return render_template('all_outputs.html', message='Could not delete, please check references.')
    return redirect(url_for('all_outputs'))


@app.route('/all_activities', methods=['GET'])
def all_activities():
    return render_template('all_activities.html', rows=db.session.query(Activity).all())


@app.route('/delete_activity/<id>')
def delete_activity(id=None):
    if id != None:
        try:
            db.session.query(Activity).filter(
                Activity.id == id).delete()
            db.session.commit()
        except:
            return render_template('all_activities.html', message='Could not delete, please check references.')
    return redirect(url_for('all_activities'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            return render_template('register.html', message='Please enter username and password.')
        if db.session.query(User).filter(User.username == username).count() != 0:
            return render_template('register.html', message='This username has taken, please select another username.')
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        data = User(username, hashed.decode('utf-8'))
        db.session.add(data)
        db.session.commit()
        return render_template('home.html')


if __name__ == '__main__':
    app.run()
