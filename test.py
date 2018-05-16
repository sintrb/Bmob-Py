# -*- coding:utf-8 -*-

from Bmob import BmobSDK, BmobModel


APP_ID = "3a3e06755ae2a0cc58ccc4747d9b7132"
REST_API_KEY = "b39628bf1e527ffb98527d471d314277"


class Page(BmobModel):

    page_id = ''
    article = {}
    tags = []


if __name__ == '__main__':
    # setup SDK
    BmobSDK.setup(APP_ID, REST_API_KEY)

    # Construct a Course instance and save it into bmob data service
    c1 = Page(page_id='123',article={"id":"hello","content":"shabi"}, tags=['cifa'])
    c1.save()
    
    c2 = Page('5269096a66')
    print("{0}:{1}".format(c2.page_id, c2.article['content']))
    c2.content = "updated"
    c2.save()


    print("The number of pages: {0}".format(Page().query().count()))
    for c in Page().query().w_in('tags', ['cifa']).order("-createdAt").limit(20):
        print("%s,%s" % (c.createdAt, c.page_id))
        print(c.tags)
        print(c.article)
    
    # query like a list
    q = Page().query().skip(5).limit(10)
    print("Items of q:")
    for c in q:
        print("\t%s" % c.objectId)
    print("q.count(): %d" % q.count())
    print(q[-1].page_id)

    # deleting operation
    print("The number before deleting: %d" % len(Page().query()))
    c1.delete()
    print("The number after deleting: %d" % len(Page().query()))




    


