### AI - Grupo 18
<br>

##### Software Requirements:
- Python3.9
- Xampp
- Arduino IDE

<br>

##### 1-DB Setup:
	1- Open Xampp and Run MySQL and Apache services
	2- Open Browser and go to localhost
	3- Create a DB with the name "dbsensores"
	4- Import the "dbsensores.sql" file into the DB created
<br>

##### 2-Arduino Setup:
	1- Connect Arduino via USB
	2- Navigate into the folder "sketch_mar19b" 
	3- Open the "sketch_mar19b.ino" with Arduino IDE
	4- Click on the "Upload" button to load the code into arduino	

	NOTE: All sensors and actuators must be connected to the same ports specified in the code.
<br>

##### 3-ArduinoServer Setup:
	1- Navigate into the folder "ArduinoServer" using your terminal
	2- Run the following command "python3 main.py"

	NOTE: Make sure the ArduinoServer Serial Communication port (ubsport variable) is the same Arduino is connected to.
<br>

##### 4-WebServer Setup:
	1- Navigate into the folder "WebServer" using your terminal
	2- Run the following command "python3 main.py"
	3- Click on the url link in the terminal
	4- Login credentials: (username: sysadmin, password: superpass)