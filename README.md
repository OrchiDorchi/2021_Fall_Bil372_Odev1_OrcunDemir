## Orcun Demir Project 1

Install packages
```
pip install -r requirements.txt
```
Change database uri's in app.py:13 and Classes.py:9 as your local uri's.

Create tables
```
python
>>>from Classes.py import db
>>>db.create_all()
```
Run app.py on local
```
python app.py
```
