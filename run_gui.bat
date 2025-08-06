@echo off
echo Iniciando Generador G-code con Interfaz Grafica...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si las dependencias estan instaladas
python -c "import cv2, numpy, tkinter" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias requeridas...
    pip install opencv-python numpy
    echo.
)

REM Ejecutar la interfaz grafica
python gui_generator.py

REM Pausar al final para ver cualquier error
if errorlevel 1 (
    echo.
    echo Hubo un error al ejecutar el programa.
    pause
)
