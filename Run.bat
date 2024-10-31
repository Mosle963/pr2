@echo off

:: Check if virtual environment exists
if exist "%USERPROFILE%\Envs\ITE_BPR602_C32_F23" (
    workon ITE_BPR602_C32_F23 && py manage.py runserver
) else (
	
    	pip3 install virtualenvwrapper-win 
	mkvirtualenv ITE_BPR602_C32_F23 && pip3 install -r requirements.txt && py manage.py runserver
)