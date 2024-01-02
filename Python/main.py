import sys
import json
import codecs
import base64
import socket
import subprocess

from hello import PrintHelloWorld

# --------------------------------------------------
# Global variables
localIp = "127.0.0.1"
pluginUserName = "admin"
pluginPassword = "Pass1234"
socketBufferSize = 8192 * 10
getMetadata = True
getMetadataConnectionThreshold = 10

# --------------------------------------------------
def SysCmd(cmd):
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exitCode = p.wait()
    print(f">>> command line: '{cmd}'")
    print(f"<<< return code: {p.returncode}")
    print(f"<<< exit code: {exitCode}")
    return p.stdout.readlines()

def PrintCurlResponse(content, type="text"):
    if type == "json":
        print(json.dumps(json.loads(content[0]), indent=4))
    else: #default to text
        for line in content:
            print(line.decode("UTF-8"), end="")
        print("")

def GetServerConfig(port=80):
    global localIp
    api = f"http://{localIp}:{port}/server"
    response = SysCmd(f"curl --silent {api}")
    PrintCurlResponse(response)

def GetLicenseConfig(port=8592):
    global localIp, pluginUserName, pluginPassword
    api = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{port}/getconfig?ch=about_box"
    response = SysCmd(f"curl --silent {api}")
    PrintCurlResponse(response, type="json")

def GetZoneConfig(port=8592, zone=0):
    global localIp, pluginUserName, pluginPassword
    api = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{port}/getconfig?ch=1&detection_zone={zone}"
    response = SysCmd(f"curl --silent {api}")
    PrintCurlResponse(response, type="json")

def GetHttpsResponse(url):
    response = SysCmd(f"curl -k -L --silent {url}")
    PrintCurlResponse(response)

def GetAIMetaData(port=8592):
    global localIp, pluginUserName, pluginPassword, socketBufferSize, getMetadata
    account = f"{pluginUserName}:{pluginPassword}"
    accountBase64 = str((base64.b64encode(account.encode())).decode())

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((localIp, port))

    requestHeader = f"GET /getalarmmotion HTTP/1.1\r\nCookie: ipcam_lang=0\r\nHost: {localIp}:{port}\r\nAuthorization: Basic {accountBase64}\r\n\r\n"
    clientSocket.send(requestHeader.encode())

    errorCounter = 0
    while getMetadata:
        recvData = clientSocket.recv(socketBufferSize)
        try:
            recvData = recvData.decode().split('\n')[5] # object detection data
            jsonData = json.loads(recvData) 
            print(jsonData)
            
        except:
            print('ERROR : recv data incomplete pass\n')
            errorCounter += 1
            continue
        
        errorCounter = 0
        
        if errorCounter > getMetadataConnectionThreshold:
            errorCounter = 0
            getMetadata = False

# --------------------------------------------------

def main():
    PrintHelloWorld()

    # Communicate with LILIN IP camera service at port 80
    GetServerConfig(port=80)

    # Communicate with LILIN Aida plug-in at port 5892
    GetServerConfig(port=8592)
    GetLicenseConfig(port=8592)
    GetZoneConfig(port=8592, zone=0)

    # Communicate with HTTPs via curl
    GetHttpsResponse("https://event.ddnsipcam.com/")

    # Get the objection meta data (JSON) from /getalarmmotion CGI at port 8592
    GetAIMetaData(port=8592)

if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()