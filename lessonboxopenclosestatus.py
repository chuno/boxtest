import adbutils
from apscheduler.schedulers.background import BackgroundScheduler
import time
import arrow

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
    # print(test_object)
def updateAndroiddevice(androido,serial):

    androido.set('serial',serial)

    androido.save()
    # print(androido)
    
def androiddevicelist():
    Todo = leancloud.Object.extend('Androiddevice')
    query = Todo.query
    query_result = query.find()
    conv=[]
    for item in query_result:
        # print(item)
        value=encode(item,dump_objects=True)
        print(value)
        conv.append(item)
    return list(conv)
def androiddevicelistbystatus():
    Todo = leancloud.Object.extend('Androiddevice')
    query = Todo.query
    query.equal_to('status', "device");
    query_result = query.find()
    conv=[]
    for item in query_result:
        # print(item)
        value=encode(item,dump_objects=True)
        print(value)
        conv.append(item)
    return list(conv)

def serial2mem(serial,serialdict):
    print("serial=",serial)
    if serial in serialdict:
        return serialdict[serial]
    else:
        return None
def android2member(devicev,serialdict):
    
    memberv = map(lambda device: serial2mem(device.get("serial"),serialdict), devicev)

    memberv1 = filter(lambda item: item is not None, memberv)
    return memberv1
def noattendmember(memberv,dmemberv):
    return memberv-dmemeberv


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
def studentlist():
    Todo = leancloud.Object.extend('Student')
    query = Todo.query
    query_result = query.find()
    conv=[]
    for item in query_result:
        # print(item)
        value=encode(item,dump_objects=True)
#        print(value)
        conv.append(item)
    return list(conv)
def studentlistbyuserlevel(userlevel):
    Todo = leancloud.Object.extend('Student')
    query = Todo.query
    query.equal_to("userLevel",userlevel)

    query_result = query.find()
    conv=[]
    for item in query_result:
        # print(item)
        value=encode(item,dump_objects=True)
#        print(value)
        conv.append(item)
    return list(conv)
def studentlistbygroup(group):
    Todo = leancloud.Object.extend('Student')
    query = Todo.query
    query.equal_to("group",group)

    query_result = query.find()
    conv=[]
    for item in query_result:
        # print(item)
        # value=encode(item,dump_objects=True)
#        print(value)
        conv.append(item)
    return list(conv)

def equalstudent(student,serial):
    if student.get("serial") == serial:
        return True
    else:
        return False
def getStudentbyserial(studentv,serial):
    overv =filter(lambda student:equalstudent(student,serial),studentv)
    overlist  = list(overv)
    if len(overlist) ==0:
        return None
    else:
        return overlist[0]

def writeAlertlog(item):
    pass
def processlesson(newlesson):
    studentv = studentlist()
    serialdict = {}
    for item in studentv:
        serial = item.get("androidid")
        name = item.get("name")
        if serial is not None:
            serialdict[serial]=name
    # print("serialdiict",serialdict)
    memberv = newlesson.get("members")

    devicev = androiddevicelistbystatus()
    joindevicev = android2member(devicev,serialdict)
    print("no join=")
    print(memberv-list(joindevicev))
    nojoin = memberv-list(joindevicev)
    map(lambda item:writeAlertlog(item),nojoin)
    today=today1.to('Asia/Shanghai')
    todaystr=today.format("YYYYMMDD")
    newlesson.set(todaystr+"checked",1)
    newlesson.save()
def getMembervbyuserlevel(userlevel):
        studentv = studentlistbyuserlevel(userlevel)
        memberv = map(lambda item: item.get("name"),studentv)
        return list(memberv)
def getMembervbygroup(group):
        studentv = studentlistbygroup(group)
        memberv = map(lambda item: item.get("name"),studentv)
        return list(memberv)


def processlessonbyuserLevel(newlesson):
    studentv = studentlist()
    serialdict = {}
    for item in studentv:
        serial = item.get("androidid")
        name = item.get("name")
        if serial is not None:
            serialdict[serial]=name
    # print("serialdiict",serialdict)
    userlevel = newlesson.get("userLevel")
    memberv = getMembervbyuserlevel(userlevel)
    # print("memberv=",memberv)

    devicev = androiddevicelistbystatus()
    joindevicev = list(android2member(devicev,serialdict))
    
    # print("joindevicev",joindevicev)
    # print(set(memberv)- set(joindevicev))
    nojoin = set(memberv)- set(joindevicev)
    print("no join=",nojoin)
    for student in nojoin:
        newAlertlog(student,newlesson.get("name"))
    today1 = arrow.utcnow()
    today=today1.to('Asia/Shanghai')
    todaystr=today.format("YYYYMMDD")
    newlesson.set(todaystr+"checked",1)
    newlesson.save()
def processlessonbygroup(newlesson):
    studentv = studentlist()
    serialdict = {}
    for item in studentv:
        serial = item.get("androidid")
        name = item.get("name")
        if serial is not None:
            serialdict[serial]=name
    # print("serialdiict",serialdict)
    userlevel = newlesson.get("group")
    memberv = getMembervbygroup(userlevel)
    # print("memberv=",memberv)

    devicev = androiddevicelistbystatus()
    joindevicev = list(android2member(devicev,serialdict))
    # print("devicev=",devicev)
    # print("joindevicev",joindevicev)
    # print(set(memberv)- set(joindevicev))
    nojoin = set(memberv)- set(joindevicev)
    print("no join=",nojoin)
 
    lessontime=arrow.utcnow()
#    lessontime30 = lessontime.shift(minutes=-30)
    todaylv=lessoninfolisttoday()
    prevstarttime = prevStarttime(todaylv,newlesson)
    lessontime30=startTimetoDate(prevstarttime )
    faceboxcachev=faceboxlistlast5(lessontime.timestamp*1000,lessontime30.timestamp*1000)
    print("faceboxcachev1",faceboxcachev)
    get_unique_numbersleancloudext(faceboxcachev,joindevicev)

    today1 = arrow.utcnow()
    today=today1.to('Asia/Shanghai')
    todaystr=today.format("YYYYMMDD")
    newlesson.set(todaystr+"faceboxcachechecked",1)
    newlesson.save()

def lessonlist():
    Student = leancloud.Object.extend('Lesson')
    query = Student.query
    today1 = arrow.utcnow()
    today=today1.to('Asia/Shanghai')
    todaystr=today.format("YYYYMMDD")
    query.not_equal_to(todaystr+"faceboxcachechecked", 1)
    query.descending('createdAt')
    student_list = query.find()
    return student_list
def lessoninfolist():
    Student = leancloud.Object.extend('Lesson')
    query = Student.query
    today1 = arrow.utcnow()
    today=today1.to('Asia/Shanghai')
    todaystr=today.format("YYYYMMDD")
    query.ascending('startTime')
    student_list = query.find()
    return student_list

def lessoninfolisttoday():
        student_list= lessoninfolist()
        todaylesson=filter(lambda lesson:isTodaylesson(lesson),student_list)
        todaylessonv= list(todaylesson)
        print("todaylessoonv",todaylessonv)
        return todaylessonv

def newAlertlog(name,lesson):
    print("name=",name)
    print("lesson=",lesson)
    TestObject = leancloud.Object.extend('Alert')
    test_object = TestObject()
    test_object.set("name",name)
    test_object.set("lesson",lesson)
    test_object.set("error","未识别手机")
    test_object.save()

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
def isTodaylessonlm(lesson1):
    lm = arrow.get(lesson1.get('lm'))
    print("lm=",lm)
    ret= isToday(lm)
    return ret
def isTodaylesson(lesson1):
    dates = lesson1.get('dates')
    print("dates=",dates)
    print("\n")
    if dates is None:
        return False
    for lm in dates:
        ret= isToday(arrow.get(lm))
        if ret :
            return True
    return False

def isLessonworktime(lesson1):
    starttime= lesson1.get('startTime')
    if starttime is None:
        return False
    endtime = lesson1.get('endTime')
    if endtime is None:
        return False
    ret =isWorktime(arrow.utcnow(),starttime,endtime)
    return ret

def alerttest():
        student_list= lessonlist()
        todaylesson=filter(lambda lesson:isTodaylesson(lesson),student_list)
        todaylessonv= list(todaylesson)
        print("todaylessoonv",todaylessonv)

        workinglesson = filter(lambda lesson: isLessonworktime(lesson),todaylessonv)
        for item in list(workinglesson):
            value=encode(item,dump_objects=True)
            print(value)
            processlessonbygroup(item)

def alert():
        student_list= lessonlist()
        todaylesson=filter(lambda lesson:isTodaylesson(lesson),student_list)
        todaylessonv= list(todaylesson)
        print("todaylessoonv",todaylessonv)

        workinglesson = filter(lambda lesson: isLessonworktime(lesson),todaylessonv)
        for item in list(workinglesson):
            value=encode(item,dump_objects=True)
            print(value)
            processlessonbygroup(item)
        print("alert end\n")

def faceboxlistlast5(lessontime,lessontime1):
    Todo = leancloud.Object.extend('Faceboxcache')
    query = Todo.query
    query.less_than("boxtime",lessontime)
    query.greater_than("boxtime",lessontime1)
    query.descending('boxtime')
    print("lessontime1=",lessontime1)
    query_result = query.find()
    conv=[]
    for item in query_result:
        print(item)
        value=encode(item,dump_objects=True)
        print(value)
        conv.append(item)
    return conv
def get_unique_numbers(numbers):
    unique = []
    uniquename=[]
    for number in numbers:
        name=number.get("name")
        print(name)
        if number in uniquename:
            continue
        else:
            unique.append(number)
    return unique
def get_unique_numbersleancloud(numbers):
    unique = []
    uniquename=[]
    for number in numbers:
        name=number.get("name")
        print(name)
        if name in uniquename:
            number.set("boxstatus","kai")
            number.save()
        else:
            number.set("boxstatus","cun")
            number.save()     
            uniquename.append(name)
            unique.append(number)
    return unique
def get_unique_numbersleancloudext(numbers,activedevicev):
    unique = []
    uniquename=[]
    for number in numbers:
        name=number.get("name")
        print(name)
        if name in uniquename:
                number.set("boxstatus","kai")
                number.save()                
        else:
            if name in activedevicev:
                number.set("boxstatus","cun")
            else:
                number.set("boxstatus","kai")
            number.save()     
            uniquename.append(name)
            unique.append(number)
    return unique
def prevlesson(todaylessonv,lesson):
    i=0
    for item in todaylessonv:
        if lesson.id==item.id:
            return i
        i=i+1
    return None
def prevStarttime(todaylessonv,lesson):
    ret = prevlesson(todaylessonv,lesson)
    if ret is None or ret ==0:
        return "00:00"
    else:
        return todaylessonv[ret-1].get("endTime")
def startTimetoDate(starttime):
    hour1=starttime[0:2]
    min1 = starttime[3:5]
    print(hour1)
    print(min1)
    today1=arrow.utcnow()
    today=today1.to('Asia/Shanghai')
    
    newdate=today.replace(hour=int(hour1), minute=int(min1))
    print(newdate)
    return newdate

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

if __name__ == '__main__':
    init_leancloud_client()
    scheduler = BackgroundScheduler()
    startMonitor()
    time.sleep(50000000) 



