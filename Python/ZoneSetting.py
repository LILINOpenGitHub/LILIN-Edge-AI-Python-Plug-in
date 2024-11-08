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

def PrintCurlResponse(response, type="json"):
    try:
        if not response:
            print("Empty response received.")
            return
        if type == "json":
            try:
                # Parse JSON response
                json_data = json.dumps(json.loads(response[0]),  indent=4)
            except json.JSONDecodeError:
                json_data = response[0]
                print("Failed to decode JSON from response.")
            print(json_data)
        else:
            print("Unsupported type.")
    except IndexError as e:
        print(f"Error while accessing content: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def DisableDetectionZone(iPort=8592,iZone = 0): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&trigger_events=0&checked=0
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&trigger_events=0&checked=0"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Disable DetectionZone successed")
    else:
        print("Disable DetectionZone failed")

def EnableDetectionZone(iPort=8592,iZone = 0): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&trigger_events=0&checked=0
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&trigger_events=0&checked=1"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Enable DetectionZone successed")
    else:
        print("Enable DetectionZone failed")
        
def SetDwellTime(iPort=8592, iZone = 0, iTime=10): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&no_parking_time=5
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&no_parking_time={iTime}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Set DwellTime {iTime} min")
    else:
        print("Set DwellTime failed")

def ModifyDetectionZone(iPort=8592, iZone = 0, iXY = None, iValue = None): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&detection_zone=0&x1=19
    global localIp, pluginUserName, pluginPassword
    if iXY:
        iXY = iXY.lower()
    if iXY not in ["x1", "x2", "x3", "y1", "y2", "y3"] or iValue is None:
        print("Invalid input. Please enter 'x1~3', 'y1~3' or give value.")
        return
    else:
        api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&detection_zone={iZone}&{iXY}={iValue}"  
        set_cmd = f"curl --silent {api_set}"
        response = SysCmd(set_cmd)
        if (SaveConfig(iPort)):
            print(f"Modify DetectionZone{iZone} {iXY}={iValue} successed")
        else:
            print("Modify DetectionZone failed")    

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
    
    print("Disabling Detection Zone")
    DisableDetectionZone(iPort=8592, iZone=0)
    
    print("Enabling Detection Zone")
    EnableDetectionZone(iPort=8592, iZone=0)
    
    print("Setting Dwell Time")
    SetDwellTime(iPort=8592, iZone=0, iTime=10)
    
    print("Modifying Detection Zone Coordinates")
    ModifyDetectionZone(iPort=8592, iZone=0, iXY='x1', iValue=19)
    
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    
