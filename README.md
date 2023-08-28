# Like a Pro - Video maker tool

### Description

---
The Like a Pro video maker tool is a routine to process the highlights gotten with the cameras, adding the Like a Pro 
mark and then making a recap.

### Current version

---
`v1.0`

### Installation

___
* `git clone https://github.com/hahoyosc/video-maker.git`
* `cd video-maker`
* `python -m pip install --user virtualenv`
* `python -m venv venv`
* `.\venv\Scripts\activate.bat`
* `pip install -r requirements.txt`
* Move your clips to the `source` folder
* `pyhon main.py --source="source/" --output="output/"`
* Your clips must be available in the `output` folder

### Executable

---
You also can download and execute the `like-a-pro-video-maker.bat` file in your highlight directory.

### Full video feature

---
If you want to run the full video feature you must add a `params.txt` parameters file that contains the time marks you
want in the final video with your raw recording and run the `like-a-pro-full-video.bat` executable file.