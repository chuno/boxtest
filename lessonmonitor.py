import adbutils


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

def newAndroiddevice(serial,status,model):
    TestObject = leancloud.Object.extend('Androiddevice')
    test_object = TestObject()
    test_object.set('serial',serial)
    test_object.set('status',"device")
    test_object.set("model",model)
    test_object.save()
    print(test_object)
def updateAndroiddevice(androido,serial,status,model):

    androido.set('serial',serial)
    androido.set('status',status)
    androido.set('model',model)
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
def monitorp(serial,status,model):
        Todo = leancloud.Object.extend('Androiddevice')
        query = Todo.query
        query.equal_to('serial', serial);
        adevice = None
        try:
            adevice = query.first()
        except Exception as e:
            print("except ",e)
        if adevice is None:
            newAndroiddevice(serial,status,model)
        else:
            updateAndroiddevice(adevice,serial,status,model)

def monitorpnodevice(serial,status,model):
        Todo = leancloud.Object.extend('Androiddevice')
        query = Todo.query
        query.equal_to('serial', serial);
        adevice = None
        try:
            adevice = query.first()
        except Exception as e:
            print("except ",e)
        if adevice is None:
            pass
        else:
            updateAndroiddevice(adevice,serial,status,model)

def montiorlesson(lesson):
		serialv= checked(lesson)
		if len(serialv)==0:
			return 

def getModel(serial):
        Todo = leancloud.Object.extend('Student')
        query = Todo.query
        query.equal_to('androidid', serial);
        adevice = None
        try:
            student = query.first()
            return student.get("model")
        except Exception as e:
            print("except ",e)
        return None



#kangding
import os
import json
import leancloud
import time
from leancloud.utils import encode
#os.environ.setdefault('LEANCLOUD_API_SERVER', "http://localhost:5000")


os.environ['LEANCLOUD_API_SERVER'] = os.environ.get('LEANCLOUD_API_SERVER',"http://192.168.31.82:7000")

init_leancloud_client()
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
print(adb.devices())

devices=adb.track_devices()
while True:
	try:
		for item in devices:
			print(item)
			print(item.serial)
			try:
				if item.status=='device' :
					print("device")
					print("item status",item.status)
					d = adb.device(serial=item.serial)
					serial = d.shell(["getprop", "ro.serial"],timeout=0.5)
					print("serial",serial)
					print("name=",d.prop.name)
					print("model=",d.prop.model)
					print("device=",d.prop.device)
					print("moddel=",d.prop.get("ro.product.model"))
					monitorp(item.serial,item.status,d.prop.model)
				else:
					if item.status=='unauthorized' :
						model=getModel(item.serial)
						if  model is None:
							monitorp(item.serial,"device","undefined")
						else:
							monitorp(item.serial,"device",model)
					else:
						monitorpnodevice(item.serial,item.status,"")
			except Exception as e:
				print(e)
	except Exception as e:
		print("devices except")
		print(e)
		time.sleep(1)
