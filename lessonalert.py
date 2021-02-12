import adbutils
from apscheduler.schedulers.background import BackgroundScheduler
import time


#/Users/aadebuger/Library/Android/sdk/platform-tools
def init_leancloud_client():
    import os

    LEANCLOUD_APP_ID = os.environ.get("LEANCLOUD_APP_ID", "rGngnUit9fqERRVjQMfzQhWg-gzGzoHsz")
    LEANCLOUD_APP_KEY = os.environ.get("LEANCLOUD_APP_KEY", "xWQ3c4CoLPXIlRd6UxLRGndX")
    LEANCLOUD_MASTER_KEY = os.environ.get("LEANCLOUD_MASTER_KEY", "x3cl6OYR2mC6dDQsW0dMeceJ")
    LEANCLOUD_REGION = os.environ.get("LEANCLOUD_REGION", "CN")
    leancloud.init(app_id=LEANCLOUD_APP_ID, app_key=LEANCLOUD_APP_KEY, master_key=LEANCLOUD_MASTER_KEY)
    leancloud.use_region(LEANCLOUD_REGION)
    print("leancloud init success with app_id: {}, app_key: {}, region: {}".format(LEANCLOUD_APP_ID, LEANCLOUD_APP_KEY,
                                                                                   LEANCLOUD_REGION))

def newAndroiddevice(serial):
    TestObject = leancloud.Object.extend('Androiddevice')
    test_object = TestObject()
    test_object.set('serial',serial)

    test_object.save()
    print(test_object)
def updateAndroiddevice(androido,serial):

    androido.set('serial',serial)

    androido.save()
    print(androido)
    
def androiddevicelist():
    Todo = leancloud.Object.extend('Androiddevice')
    query = Todo.query
    query_result = query.find()
    conv=[]
    for item in query_result:
        print(item)
        value=encode(item,dump_objects=True)
        print(value)
        conv.append(item)
    return list(conv)
def monitorp(serial):
        Todo = leancloud.Object.extend('Androiddevice')
        query = Todo.query
        query.equal_to('serial', serial);
        adevice = None
        try:
            adevice = query.first()
        except Exception as e:
            print("except ",e)
        if adevice is None:
            newAndroiddevice(serial)
        else:
            updateAndroiddevice(adevice,serial)

def montiorlesson(lesson):
		serialv= checked(lesson)
		if len(serialv)==0:
			return 
		

def lessonlist():
    Student = leancloud.Object.extend('Lesson')
    query = Student.query
    query.descending('createdAt')
    student_list = query.find()
    return student_list

import arrow
def isToday(datadate):
    today1 = arrow.utcnow()
    today=today1.to('Asia/Shanghai')
    if datadate.day==today.day and datadate.month == today.month and datadate.year == today.year:
        return True
    else:
        return False
def isWorktime(todaydate,starttime,endtime):
    todaydate=todaydate.to('Asia/Shanghai')
    nowstr = todaydate.format("HH:mm")

    print("nowstr",nowstr)
    if nowstr <starttime:
        return False
    if nowstr > endtime:
        return False
    return True
def isTodaylesson(lesson1):
    lm = arrow.get(lesson1.get('lm'))
    print("lm=",lm)
    ret= isToday(lm)
    return ret
def isLessonworktime(lesson1):
    starttime= lesson1.get('startTime')
    if starttime is None:
        return False
    endtime = lesson1.get('endTime')
    if endtime is None:
        return False
    ret =isWorktime(array.utcnow(),starttime,endtime)
    return ret

def alert():
        student_list= lessonlist()
        todaylesson=filter(lambda lesson:isTodaylesson(lesson),student_list)
        todaylessonv= list(todaylesson)
        workinglesson = filter(lambda lesson: isLessonworktime(lesson),todaylessonv)

        print(list(workinglesson))

#kangding
import os
import json
import leancloud
from leancloud.utils import encode
#os.environ.setdefault('LEANCLOUD_API_SERVER', "http://localhost:5000")

def startMonitor():
#    scheduler.add_job(event_monitor,'interval', minutes=1) 
    scheduler.add_job(alert,'interval', seconds=60) 
#    scheduler.add_job(appointmentUpdatetask, 'cron', hour=1, minute=10)

    scheduler.daemonic = False 
    scheduler.start()

os.environ['LEANCLOUD_API_SERVER'] = os.environ.get('LEANCLOUD_API_SERVER',"http://192.168.31.82:7000")

init_leancloud_client()
scheduler = BackgroundScheduler()
startMonitor()

time.sleep(50000000) 



