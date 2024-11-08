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
categories_len = None
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

def GetClassification(iPort=8592, iZone=0): 
    global localIp, pluginUserName, pluginPassword
    api = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/getconfig?ch=1&detection_zone={iZone}"
    response = SysCmd(f"curl --silent {api}")
    try:
        if not response:
            print("Empty response received.")
            return
        json_data = json.loads(response[0])
        metadata1 = json_data.get("metadata1", "")
        if metadata1:
            categories = metadata1.split(",")
            return len(categories)
        else:
            print("No categories found in metadata1.")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.")
    except IndexError as e:
        print(f"Error while accessing content: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def SetBehavior(iPort=8592, sBehavior = ""):
    global localIp, pluginUserName, pluginPassword
    api_url = f"http://{localIp}:{iPort}/setconfigfile"
    detect_event_id = None
    BehaviorName = ""
    if sBehavior == "ProhibitZone":
        detect_event_id = "0x00000001"
        BehaviorName = "Prohibit Zone"
    elif sBehavior == "ParkingViolation":
        detect_event_id = "0x00000004"
        BehaviorName = "Parking Violation"
    elif sBehavior == "LPRAllowedListDetectionInZone":
        detect_event_id = "0x00200000"
        BehaviorName = "LPR Allowed List Detection in Zone"
    elif sBehavior == "LPRDenialListDetectionInZone":
        detect_event_id = "0x00400000"
        BehaviorName = "LPR Denial List Detection in Zone"
    elif sBehavior == "Tripwire":
        detect_event_id = "0x00000008"
    elif sBehavior == "AIMissingObjectDetection":
        detect_event_id = "0x20000000"
        BehaviorName = "AI Missing Object Detection"
    elif sBehavior == "LPRVisitorListDetectionInZone":
        detect_event_id = "0x00800000"
        BehaviorName = "LPR Visitor List Detection in Zone"
    elif sBehavior == "UnattendedOrMissingObject":
        detect_event_id = "0x01000000"
        BehaviorName = "Unattended or Missing Object"
    elif sBehavior == "TamperingDetection":
        detect_event_id = "0x04000000"
        BehaviorName = "Tampering Detection"
    elif sBehavior == "AllObjectsDetection":
        categories_len = GetClassification(iPort=8592, iZone=0)
        if (categories_len >= 2):
            detect_event_id = "0x40000000"
            BehaviorName = "All Objects Detection"
        else:
            print("Please enable at least 2 classifications for AND and NAND operations.")
            return
    elif sBehavior == "MaximumSpeedDetection":
        detect_event_id = "0x00002000"
        BehaviorName = "Maximum Speed Detection"
    elif sBehavior == "MinimumSpeedDetection":
        detect_event_id = "0x00004000"
        BehaviorName = "Minimum Speed Detection"
    elif sBehavior == "LackOfAnyObjectDetection":
        categories_len = GetClassification(iPort=8592, iZone=0)
        if (categories_len >= 2):
            detect_event_id = "0x80000000"  
            BehaviorName = "Lack of Any Object Detection"
        else:
            print("Please enable at least 2 classifications for AND and NAND operations.")
            return
    else:
        print("Invalid Behavior Name.")
        return
    data = {
        "view_setting": {
            "camera01": {
                "detection_zone": [
                    {
                        "trigger_events": [
                            {"checked": 1, "detect_event_id": detect_event_id},
                        ]
                    }
                ]
            }
        }
    }
    
    curl_cmd = f"""curl -X POST {api_url} \
    -H "Content-Type: application/json" \
    -H "If-Modified-Since: 0" \
    -H "Cache-Control: no-cache" \
    -u "{pluginUserName}:{pluginPassword}" \
    -d '{json.dumps(data)}'"""
    
    response = SysCmd(curl_cmd)
    return BehaviorName

def SetProhibitZone(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="ProhibitZone")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")
    
def SetParkingViolation(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="ParkingViolation")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetLPRAllowedListDetectionInZone(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="LPRAllowedListDetectionInZone")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetLPRDenialListDetectionInZone(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="LPRDenialListDetectionInZone")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetTripwire(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="Tripwire")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetAIMissingObjectDetection(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="AIMissingObjectDetection")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")
    
def SetLPRVisitorListDetectionInZone(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="LPRVisitorListDetectionInZone")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetUnattendedOrMissingObject(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="UnattendedOrMissingObject")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetTamperingDetection(iPort=8592):  
    BehaviorName = SetBehavior(sBehavior="TamperingDetection")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetAllObjectsDetection(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="AllObjectsDetection")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetLackOfAnyObjectDetection(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="LackOfAnyObjectDetection")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetMaxSpeedDetection(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="MaximumSpeedDetection")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def SetMinSpeedDetection(iPort=8592):
    BehaviorName = SetBehavior(sBehavior="MinimumSpeedDetection")
    if (BehaviorName):
        print(f"Set {BehaviorName} Success")

def ResetBehavior(iPort=8592):
    global localIp, pluginUserName, pluginPassword
    api_url = f"http://{localIp}:{iPort}/setconfigfile"
    data = {
        "view_setting": {
            "camera01": {
                "detection_zone": [
                    {
                        "trigger_events": [
                            {"checked": 0, "detect_event_id": "0x00000001"}, # Prohibit zone
                            {"checked": 0, "detect_event_id": "0x00000004"}, # Parking violation
                            {"checked": 0, "detect_event_id": "0x00200000"}, # LPR allowed list detection in zone
                            {"checked": 0, "detect_event_id": "0x00400000"}, # LPR denial list detection in zone
                            {"checked": 0, "detect_event_id": "0x00000008"}, # Tripwire
                            {"checked": 0, "detect_event_id": "0x20000000"}, # AI missing object detection
                            {"checked": 0, "detect_event_id": "0x01000000"}, # Unattended or missing object
                            {"checked": 0, "detect_event_id": "0x04000000"}, # Tampering detection
                            {"checked": 0, "detect_event_id": "0x00002000"}, # Maximum speed detection
                            {"checked": 0, "detect_event_id": "0x00004000"}, # Minimum speed detection
                            {"checked": 0, "detect_event_id": "0x40000000"}, # All objects detection (AND)
                            {"checked": 0, "detect_event_id": "0x00800000"}, # LPR visitor list detection in zone
                            {"checked": 0, "detect_event_id": "0x80000000"} # Lack of any object detection (NAND)
                        ]
                    }
                ]
            }
        }
    }
    
    curl_cmd = f"""curl -X POST {api_url} \
    -H "Content-Type: application/json" \
    -H "If-Modified-Since: 0" \
    -H "Cache-Control: no-cache" \
    -u "{pluginUserName}:{pluginPassword}" \
    -d '{json.dumps(data)}'"""
    
    response = SysCmd(curl_cmd)
    
# --------------------------------------------------

def main():
    
    print("Reset Behavior")
    ResetBehavior(iPort=8592)
    
    print("Enable Prohibit Zone")
    SetProhibitZone(iPort=8592)

    # print("Enable Parking Violation")
    # SetParkingViolation(iPort=8592)

    # print("Enable LPR Allowed List Detection in Zone")
    # SetLPRAllowedListDetectionInZone(iPort=8592)

    # print("Enable LPR Denial List Detection in Zone")
    # SetLPRDenialListDetectionInZone(iPort=8592)

    # print("Enable Tripwire")
    # SetTripwire(iPort=8592)

    # print("Enable AI Missing Object Detection")
    # SetAIMissingObjectDetection(iPort=8592)

    # print("Enable LPR Visitor List Detection in Zone")
    # SetLPRVisitorListDetectionInZone(iPort=8592)

    # print("Enable Unattended or Missing Object")
    # SetUnattendedOrMissingObject(iPort=8592)

    # print("Enable Tampering Detection")
    # SetTamperingDetection(iPort=8592)

    # print("Enable All Objects Detection") 
    # SetAllObjectsDetection(iPort=8592)

    # print("Enable Lack of Any Object Detection")
    # SetLackOfAnyObjectDetection(iPort=8592)

    # print("Enable Maximum Speed Detection")
    # SetMaxSpeedDetection(iPort=8592)

    # print("Enable Minimum Speed Detection")
    # SetMinSpeedDetection(iPort=8592)
 
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    
