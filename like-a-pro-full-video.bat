@echo
cls
echo Cloning the repository
git clone https://github.com/hahoyosc/video-maker.git
echo Entering to the project folder
cd video-maker
echo Installing the virtual environment
python -m pip install --user virtualenv
echo Creating the virtual environment
python -m venv venv
echo Activating the virtual environment
call .\venv\Scripts\activate.bat
echo Installing the project dependencies
pip install -r requirements.txt
Creating the processed highlights output folder
mkdir ..\output
echo Running the project
start /wait python main.py -f
echo Deleting every project files
cd ..
rmdir /s /q video-maker
