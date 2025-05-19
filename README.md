# DDoSMitigation
Automation of DDoS detection and response workflows

The objectives were:
a)	Analyze traffic flow characteristics: request count and packet size.
b)	Detect DDoS behaviors and classify them by type (protocol and volumetric).
c)	Identify attacking IP addresses.
d)	Automate notifications and mitigation actions.



## User Guide
Note* In file Options.py are listed:
> Path for real-time log files

> Training log files

> Trained models

> Properties of the e-mail address that sends alerts. 
 
The values should be modified in case of necessity.


Launch the program DDoSMonitor.py with arguments
> /tv for volume based model training,

> /tp for protocol based model training

> /r for real-time.


1.	/tv, /tp
   
To use the application in training mode, training CSV log files should be put in the corresponding folder (Options.training_data_folder) beforehand.

The files should have a column “label” to mark whether there is an attack or not. 

If started with /tv or /tp option, the application will display the following information: 

> read and parsed filenames

> generated model’s metrics: Accuracy, F1 score, Precision, Recall, Train and Test labels distributions.

The generated model will be saved to Options.models_folder.


2.	/r
   
If the application is launched in real-time mode, it waits until “esc” is pressed.

As soon as a log file is added to one of the Options.realtime_data_folders, the application starts processing and outputs result:

>	Filename

If attack detected, it displays 

>	Timestamp 

>	Type(volume-based/protocol-based)

>	Notifies that the suspicious IP is blocked

If attack is not detected, it displays a notification that no attack was detected.

