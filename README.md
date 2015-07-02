# Bmob-Py
A Simple Bmob SDK With Python.

DEMO
```
# from Bmob import BmobSDK, BmobModel

# define a Model
class Course(BmobModel):
	name = ''	# string
	score = 1.0	# number

# setuo BmobSDK
BmobSDK.setup('77b5dad35e17a087d679e62db9936950', 'a9ab631355ce61f19be22f55a0b1b422')

# create a course and save it
c = Course(name="Python 2.x Program", score=4)
c.save()

# print the course count
print Course().query().count()

# create a Course query and query all contain "Program" courses
for c in Course().query().w_regex('name','Program').order("-createdAt").limit(20):
	print '%s  %s : %s'%(c.createdAt, c.name, c.score)
	if c.score == 4:
		c.delete()	# test delete, delete the object which created just.
```
