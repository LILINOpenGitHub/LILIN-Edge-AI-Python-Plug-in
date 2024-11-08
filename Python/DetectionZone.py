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

    
def GetDetectionZone(iPort=8592, iZone=0): # http://admin:Pass1234@127.0.0.1:8592/getconfig?ch=1&detection_zone=0
    global localIp, pluginUserName, pluginPassword
    api = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/getconfig?ch=1&detection_zone={iZone}"
    response = SysCmd(f"curl --silent {api}")
    PrintCurlResponse(response, type="json")

    
def SetAnalytics(iPort=8592, sEnable="No"): # http://admin:Pass1234@127.0.0.1:8592/setconfig?ch=1&enable_traffic=Yes/No
    global localIp, pluginUserName, pluginPassword
    # Convert input to first letter uppercase and remaining lowercase
    sEnable = sEnable.capitalize()
    # Check if the input is a valid value
    if sEnable not in ["Yes", "No"]:
        print("Invalid input. Please enter 'Yes' or 'No'.")
        return  
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&enable_traffic={sEnable}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    # PrintCurlResponse(response, type="json")
    if (SaveConfig(iPort)):
        print(f"Set enable_traffic = {sEnable}")
    else:
        print("Set enable_traffic Failed")


def SaveConfig(iPort=8592, max_retries=3, delay=1): # http://admin:Pass1234@127.0.0.1:8592/getconfig?reload=1
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
    print("Getting Detection Zone Configuration")
    GetDetectionZone(iPort=8592, iZone=0)
    
    print("Setting Object Classification Analytics")
    SetAnalytics(iPort=8592, sEnable="Yes")
    
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    
