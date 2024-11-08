import sys
import base64
import codecs
import subprocess
# --------------------------------------------------
# Global variables
localIp = "127.0.0.1"
pluginUserName = "admin"
pluginPassword = "Pass1234"
# --------------------------------------------------

def GetBase64JPEG(iPort=8592): # curl -s "http://192.168.50.210:8592/snap"
    global localIp, pluginUserName, pluginPassword
    api = f"http://{pluginUserName}:{pluginPassword}@{localIp}:{iPort}/snap"
    curl_command = f"curl -s {api}"
    image_data = subprocess.check_output(curl_command, shell=True)
    base64_image = base64.b64encode(image_data).decode('utf-8')
    print(base64_image)

# --------------------------------------------------
def main():
    print("Get JPEG And Convert To Base64")
    GetBase64JPEG(iPort=8592)
    print("Use Base64 Convert To JPEG : https://base64.guru/converter/decode/image")
    
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    main()
    
    
