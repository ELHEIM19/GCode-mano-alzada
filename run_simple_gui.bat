@echo off
echo Iniciando Generador G-code Simple con Interfaz Grafica...
echo.
python gui_simple_generator.py
if errorlevel 1 (
    echo.
    echo Hubo un error al ejecutar el programa.
    pause
)
