@echo off
REM Script de instalación y uso del generador de G-code para trazos a mano alzada
REM Para Windows

echo ========================================
echo  Generador G-code Trazos Mano Alzada
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si pip está disponible
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no está disponible
    pause
    exit /b 1
)

echo Python detectado correctamente
echo.

REM Instalar dependencias si no existen
echo Verificando dependencias...
pip show opencv-python >nul 2>&1
if errorlevel 1 (
    echo Instalando OpenCV...
    pip install opencv-python
)

pip show numpy >nul 2>&1
if errorlevel 1 (
    echo Instalando NumPy...
    pip install numpy
)

echo Dependencias instaladas correctamente
echo.

REM Mostrar opciones de uso
:menu
echo Opciones disponibles:
echo.
echo 1. Uso básico (arrastrar imagen)
echo 2. Configuración avanzada
echo 3. Ver máquinas disponibles
echo 4. Ver perfiles disponibles
echo 5. Ejemplo con imagen de prueba
echo 6. Salir
echo.
set /p choice="Selecciona una opción (1-6): "

if "%choice%"=="1" goto basic_usage
if "%choice%"=="2" goto advanced_usage
if "%choice%"=="3" goto list_machines
if "%choice%"=="4" goto list_profiles
if "%choice%"=="5" goto example_usage
if "%choice%"=="6" goto end

echo Opción inválida
goto menu

:basic_usage
echo.
echo === USO BÁSICO ===
echo Arrastra tu imagen aquí y presiona Enter:
set /p image_path=""
if "%image_path%"=="" (
    echo No se especificó imagen
    goto menu
)
REM Remover comillas si las hay
set image_path=%image_path:"=%
echo Procesando imagen con configuración por defecto...
python advanced_generator.py "%image_path%"
echo.
pause
goto menu

:advanced_usage
echo.
echo === CONFIGURACIÓN AVANZADA ===
echo Arrastra tu imagen aquí:
set /p image_path=""
if "%image_path%"=="" (
    echo No se especificó imagen
    goto menu
)
set image_path=%image_path:"=%

echo.
echo Máquinas disponibles: grbl, marlin, linuxcnc, plotter, laser
set /p machine="Tipo de máquina (default: grbl): "
if "%machine%"=="" set machine=grbl

echo.
echo Perfiles disponibles: artistic, technical, sketch, calligraphy, engraving
set /p profile="Perfil de dibujo (default: artistic): "
if "%profile%"=="" set profile=artistic

echo.
set /p width="Ancho del canvas en mm (default: 200): "
if "%width%"=="" set width=200

set /p height="Alto del canvas en mm (default: 200): "
if "%height%"=="" set height=200

echo.
echo Procesando con configuración personalizada...
python advanced_generator.py "%image_path%" --machine %machine% --profile %profile% --width %width% --height %height%
echo.
pause
goto menu

:list_machines
echo.
echo === MÁQUINAS DISPONIBLES ===
python advanced_generator.py --list-machines
echo.
pause
goto menu

:list_profiles
echo.
echo === PERFILES DISPONIBLES ===
python advanced_generator.py --list-profiles
echo.
pause
goto menu

:example_usage
echo.
echo === EJEMPLO CON IMAGEN DE PRUEBA ===
echo Creando imagen de prueba...

python -c "
import cv2
import numpy as np

# Crear imagen de prueba simple
img = np.ones((400, 400, 3), dtype=np.uint8) * 255

# Dibujar algunas formas
cv2.circle(img, (200, 150), 80, (0, 0, 0), 3)
cv2.rectangle(img, (100, 220), (300, 320), (0, 0, 0), 3)
cv2.line(img, (50, 50), (350, 350), (0, 0, 0), 3)

# Texto
cv2.putText(img, 'TEST', (150, 280), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

cv2.imwrite('test_image.png', img)
print('Imagen de prueba creada: test_image.png')
"

if exist test_image.png (
    echo Procesando imagen de prueba...
    python advanced_generator.py test_image.png --machine grbl --profile artistic
    echo.
    echo Archivos generados:
    if exist test_image_grbl_artistic.gcode (
        echo - test_image_grbl_artistic.gcode
    )
) else (
    echo Error creando imagen de prueba
)
echo.
pause
goto menu

:end
echo.
echo Gracias por usar el generador de G-code!
echo.
pause
