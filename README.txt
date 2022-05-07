Team members: Nate Chism, Marina Nava, Alex Prieger
Video demo: https://drive.google.com/file/d/1jkTqcien1_N0mABaQ-TiKID5G1WfUjxH/view?usp=sharing
Instructions on how to compile/execute:
	For code in RPi folder:
		Python libraries: Requests, Json, Sys, Pyaudio (requires portaudio installed on system), Time, Gpiozero, libraries installed for grovepi
		To run: execute PiRecordScript.py with a command line argument representing the digital port on the Grovepi to which the button is plugged in.
	For code in AzureVM folder:
		Python libraries: Matplotlib, Numpy, Pydub, Os, Sys, Flask, Wave, Threading
		To run: execute doorbellServer.py in superuser mode.
	For code in LockApp folder:
		External libraries: standard Android libraries (media, os, util, widget) and standard Java libraries (io, net)
		To run: Open the LockApp project in Android Studio, and build app to a phone.