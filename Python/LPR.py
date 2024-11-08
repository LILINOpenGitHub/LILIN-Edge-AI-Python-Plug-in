import sys
import json
import codecs
import subprocess
import time
import shlex
# --------------------------------------------------
# Global variables
localIp = "127.0.0.1"
pluginUserName = "admin"
pluginPassword = "Pass1234"
confidence = None
# --------------------------------------------------
def SysCmd(cmd):
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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

def GetLPRConfidence(iPort=8592): 
    global localIp, pluginUserName, pluginPassword
    api = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/getconfig?ch=1"
    response = SysCmd(f"curl --silent {api}")
    try:
        if not response:
            print("Empty response received.")
            return
        json_data = json.loads(response[0])
        confidence2 = json_data.get("confidence2", "")
        if confidence2:
            confidence = confidence2.split(",")
            print(f"Get LPR Confidence: {confidence}")
        else:
            print("No value found in confidence2.")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.")
    except IndexError as e:
        print(f"Error while accessing content: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def SetLPRConfidence(iPort=8592,iConfidence = 50):
    global localIp, pluginUserName, pluginPassword
    api_set = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/setconfig?ch=1&confidence2={iConfidence}"
    set_cmd = f"curl --silent {api_set}"
    response = SysCmd(set_cmd)
    if (SaveConfig(iPort)):
        print(f"Set LPR Confidence : {iConfidence}")
    else:
        print("Set LPR Confidence Failed")

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
    
    print("Set LPR Confidence")
    SetLPRConfidence(iPort=8592,iConfidence = 50)
    
    print("Get LPR Confidence")
    GetLPRConfidence(iPort=8592)

 
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    
