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
# --------------------------------------------------
def SysCmd(cmd):
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exitCode = p.wait()
    print(f">>> command line: '{cmd}'")
    print(f"<<< return code: {p.returncode}")
    print(f"<<< exit code: {exitCode}")
    return p.stdout.readlines()
        
def SetGlobalFoVFilter(iPort=8592,iProportion = 9): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&obj_max_proportion=9
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&obj_max_proportion={iProportion}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Set Global FoV : {iProportion}")
    else:
        print("Set Global FoV Failed")
        
def SetZoneFoVFilter(iPort=8592, iZone = 80, iProportion=9): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&obj_max_proportion_in_zone=80
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&obj_max_proportion_in_zone={iProportion}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Set Zone {iZone} FoV Filter : {iProportion}")
    else:
        print("Set Zone {iZone} FoV Filter Failed")
        
def GetZoneFoVFilter(iPort=8592, iZone = 0):
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/getconfig?ch=1&detection_zone={iZone}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if not response:
        print("Empty response received.")
        return
    try:
        json_data = json.loads(response[0])
        obj_max_proportion = json_data.get("obj_max_proportion_in_zone", None)
        print(f"Get Zone {iZone} FoV Filter : {obj_max_proportion}")
    except json.JSONDecodeError:
         print("Get Zone {iZone} FoV Filter Failed")
       

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
    print("Setting Global Field of View (FoV) Filter")
    SetGlobalFoVFilter(iPort=8592, iProportion=9)
    
    print("Setting Zone Field of View (FoV) Filter")
    SetZoneFoVFilter(iPort=8592, iZone=0)
    
    print("Getting Zone Field of View (FoV) Filter")
    GetZoneFoVFilter(iPort=8592, iZone=0)

if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    
