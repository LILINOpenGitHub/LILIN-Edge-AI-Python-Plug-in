import sys
import json
import codecs
import subprocess
import time
# --------------------------------------------------
# Global variables
localIp = "127.0.0.1"
pluginUserName = "admin"
pluginPassword = "Pass1234"
object_list = []
# --------------------------------------------------
def SysCmd(cmd):
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exitCode = p.wait()
    print(f">>> command line: '{cmd}'")
    print(f"<<< return code: {p.returncode}")
    print(f"<<< exit code: {exitCode}")
    return p.stdout.readlines()
    
def DeleteObjectClassificationAll(iPort=8592, iZone=0): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&metadata1=NULL
    global localIp, pluginUserName, pluginPassword, object_list
    object_list = []
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&metadata1=NULL"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Delete All Object Classification Success")
    else:
        print("Delete All Object Classification Failed")

def EnableObject(iPort=8592, iZone=0): 
    global localIp, pluginUserName, pluginPassword, object_list
    if not object_list:
        print("No Object Selected")
        return
    object_list_str = ",".join(object_list)
    print(f"object_list_str: {object_list_str}")
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&metadata1={object_list_str}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Enable {object_list} Success")
    else:
        print(f"Enable {object_list} Failed")

def EnablePerson(): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&metadata1=person
    global object_list
    object_list.append("person")
        
def EnableBicycle():
    global object_list
    object_list.append("bicycle")

def EnableCar():
    global object_list
    object_list.append("car")

def EnableMotorbike():
    global object_list
    object_list.append("motorbike")

def EnableBus(): 
    global object_list
    object_list.append("bus")
        
def EnableTruck(): 
    global object_list
    object_list.append("truck")

def SaveConfig(iPort=8592, max_retries=3, delay=1):
    global localIp, pluginUserName, pluginPassword
    api_check = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/getconfig?reload=1"
    check_cmd = f"curl --silent {api_check}"
    
    for attempt in range(max_retries):
        response = SysCmd(check_cmd)
        if isinstance(response, list):
            response = ''.join([item.decode('utf-8') for item in response]).strip()
        
        if "Reload OK" in response:
            return True
        else:
            if attempt < max_retries - 1:
                time.sleep(delay)
    return False
 
# --------------------------------------------------

def main():
    print("Deleting All Object Classifications")
    DeleteObjectClassificationAll(iPort=8592, iZone=0)
    
    print("Enabling Person Detection")
    EnablePerson()
    
    print("Enabling Bicycle Detection")
    EnableBicycle()
    
    print("Enabling Car Detection")
    EnableCar()

    print("Enabling Motorbike Detection")
    EnableMotorbike()
    
    print("Enabling Bus Detection")
    EnableBus()
    
    print("Enabling Truck Detection")
    EnableTruck()
    
    print("Enabling Selected Objects")
    EnableObject(iPort=8592, iZone=0)
    
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    





