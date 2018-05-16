# Bmob-Py
A Simple Bmob SDK With Python.

DEMO
```python
from Bmob import BmobSDK, BmobModel

# define a Model
class Course(BmobModel):
	name = ''	# string
	score = 1.0	# number

# setup BmobSDK
BmobSDK.setup('77b5dad35e17a087d679e62db9936950', 'a9ab631355ce61f19be22f55a0b1b422')

# create a course and save it
c1 = Course(name="Python 2.x Program", score=4)
c1.save()

# get course of id '957638ab1e'
c2 = Course('957638ab1e')
print('%s : %s'%(c2.name, c2.score))
c2.score = c2.score+1
c2.save()

# Query:
# print the course count
print('count of courses : %d'%Course().query().count() # or Query(Course).count())

# create a Course query and query all contain "Program" courses
for c in Course().query().w_regex('name','Program').order("-createdAt").limit(20):
	print('%s  %s : %s'%(c.createdAt, c.name, c.score))

# query like a list
q = Course().query().skip(5).limit(10)
print('Items of q:')
for c in q:
	print('\t',c.objectId)
print("q.count() : %d"%q.count())
print(q[-1].name)
print(q[3:])

# delete
print('count before delete: %d'%len(Course().query()))
c1.delete()
print('count after delete: %d'%len(Course().query()))
```
