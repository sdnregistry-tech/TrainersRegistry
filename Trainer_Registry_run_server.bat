@echo off
echo Starting TESDA Trainer Registry System...

REM Activate the virtual environment
call C:\TrainersRegistry\env_TRainerRegistry\Scripts\activate.bat

REM Change to your Django project directory
cd /d C:\TrainersRegistry\TrainerRegistry_root

REM Start the Django development server
python manage.py runserver

pause
