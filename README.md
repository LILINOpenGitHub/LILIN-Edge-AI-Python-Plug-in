# LILIN-Edge-AI-Python-Plug-in
LILIN edge AI Python Plug-in programming tuturial

The purpose of the Python is to allow a developer to write Python script running on the Edge AI camera.  There is no PC needed.  The Python code can be uploaded and run on the edge AI camera.<BR>

There are two plug-in needed for running Python (1) LILIN Python environment plug-in, (2) LILIN AI Plugin. 

(1) The Python environment plug-in can be downloaded [here](https://www.dropbox.com/scl/fo/9glq8s9qlf66w0xqueoml/AEEVVi9JuvTXzzYHkZfkRz4?rlkey=m80ja29siz2tkfjwgi36cp8xj&dl=0).
(2) LILIN AI plug-in can be downloaded [here](https://www.dropbox.com/scl/fo/lhh4atrb8jm3ynh512f4z/AArDr7YB3J7yXs98GDf1d8g?rlkey=30f1j99gsrd0a5omrh13hg2y4&dl=0).

![image](https://github.com/LILINOpenGitHub/LILIN-Edge-AI-Python-Plug-in/blob/main/images/diagram.jpg)

(1)	Allow a devloper to use HTTP to communicate with 127.0.0.1:8592 for metadata via AI API <BR>
(2)	Allow a devloper to use JSON for writing JSON configuration file. <BR>
(3)	Allow a devloper to use to communicate a HTTPs cloud. <BR>

### Prerequisites
Please make sure that both LILIN Edge AI Plug-in and the Python Plug-in are installed on the camera.

![image](https://github.com/LILINOpenGitHub/LILIN-Edge-AI-Python-Plug-in/blob/main/images/imgPlugin.jpg)

### Support Python imports
Support import JSON, HTTP, HTTPs, DNS, socket, date &time, base64, file IO read/write

### Installation ###
After installing Python plug-in, you will see AI plug-in and Python plug-in.  Make sure that both plug-ins are checked.

![image](https://github.com/LILINOpenGitHub/LILIN-Edge-AI-Python-Plug-in/blob/main/images/imgupdate.jpg)

### Open Python Editor ###
After enabling both Python and AI plug-ins, please open AI plug-in.  Visit System->Python page and click the Python button for openning Python Editor.

![image](https://github.com/LILINOpenGitHub/LILIN-Edge-AI-Python-Plug-in/blob/main/images/pythoninstart.jpg)

### The Python Editor ###
The Python page is shown below: <BR><BR>
Upload: Upload a Python file. <BR>
Refresh: Refresh the Python file list. <BR>
Add: Add a Python file. <BR>
Delete: Delete a Python file. <BR>
Play: Run the selected Python file. <BR>
Save: Save a Python file. <BR>
Clean: Clean the message box. <BR> <BR>
![image](https://github.com/LILINOpenGitHub/LILIN-Edge-AI-Python-Plug-in/blob/main/images/python1.jpg)

### Hello World ###
The first Python program is Hello World.  Click on hello.py file and click on Play button for the program.

![image](https://github.com/LILINOpenGitHub/LILIN-Edge-AI-Python-Plug-in/blob/main/images/imghello.jpg)

### main.py ###
Get AI metadata of recognition objects. <BR>
Get AI-plug configuration. <BR>
Demo how to communicate to a remote cloud. <BR>

### DetectionZone.py ###
The Python code is to get detection zone information including X and Y.

### ZoneSetting.py ###
The Python code is to set detection zone.

### FilterSetting.py ###
The Python code is to set the confidence filter for AI objects.

### ZoneBehavior.py ###
The Python code is to set behavior of a detection zone.

### ObjectClassification.py ###
The Python code is to enable or to disable the classified objects.

### LPR.py ###
The python code is to set and to get the confidence of license plate recognition.

### GetBase64JPEG.py ###
The python code is to get the JPEG snapshot of the camera in base64.
