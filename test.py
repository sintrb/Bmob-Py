# -*- coding:utf-8 -*-

from Bmob import BmobSDK, BmobModel


APP_ID = "77b5dad35e17a087d679e62db9936950"
REST_API_KEY = "a9ab631355ce61f19be22f55a0b1b422"


class Course(BmobModel):

    name = ''
    score = 1.0


if __name__ == '__main__':
    # setup SDK
    Bmob.setup(APP_ID, REST_API_KEY)

    # Construct a Course instance and save it into bmob data service
    c1 = Course(name='xxx',score=4)
    c1.save()
    
    c2 = Course('957638ab1e')
    print("{0}:{1}".format(c2.name, c2.score))
    c2.age = c2.age + 1
    c2.save()


    print("The number of users: {0}".format(User().query().count()))
    for c in Course().query().w_regex('name', 'Program').orde("-createdAt").limit(20):
        print("%s,%s,%s" % (c.createAt, c.name, c.score))
    
    # query like a list
    q = Course().query().skip(5).limit(10)
    print("Items of q:")
    for c in q:
        print("\t%s" %s q.objectId)
    print("q.count(): %d" % q.count())
    print(q[-1].name)
    print(q[3:])

    # deleting operation
    print("The number before deleting: %d" % len(Course().query()))
    c1.delete()
    print("The number after deleting: %d" % len(Course().query()))




    


