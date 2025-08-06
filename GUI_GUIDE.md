# 🎨 Guía de la Interfaz Gráfica

## Cómo usar la interfaz gráfica del generador G-code

### 1. Iniciar la aplicación
- Ejecuta `run_gui.bat` o directamente `python gui_generator.py`
- Se abrirá una ventana con todos los controles

### 2. Seleccionar imagen
- Haz clic en "Buscar..." junto a "Imagen de entrada"
- Navega por tus archivos y selecciona una imagen (PNG, JPG, etc.)
- La imagen aparecerá en el campo de texto

### 3. Configurar archivo de salida
- El nombre del archivo G-code se genera automáticamente
- Puedes cambiarlo haciendo clic en "Guardar como..."
- Se guardará en el mismo directorio que la imagen por defecto

### 4. Ajustar parámetros

#### Dimensiones del Canvas (mm)
- **Ancho/Alto**: Tamaño del área de trabajo de tu máquina
- Ejemplo: 200x200mm para una máquina pequeña

#### Parámetros Z (mm)
- **Altura segura**: Altura para movimientos sin dibujar (ej: 5mm)
- **Altura base**: Altura mínima de dibujo (ej: 0.2mm)
- **Variación Z**: Cuánto puede variar la altura para simular presión (ej: 0.8mm)

#### Velocidades (mm/min)
- **Dibujo**: Velocidad cuando está dibujando (ej: 1000)
- **Desplazamiento**: Velocidad para movimientos rápidos (ej: 3000)

### 5. Generar G-code
- Haz clic en "Generar G-code"
- El botón cambiará a "Procesando..." 
- Verás el progreso en el área de estado
- Al terminar aparecerá un mensaje de confirmación

### 6. Resultado
- El archivo G-code estará listo para cargar en tu máquina
- Revisa el área de estado para detalles del proceso

## Consejos útiles

### Para mejores resultados:
- Usa imágenes con contornos claros
- Imágenes en blanco y negro funcionan mejor
- Tamaños de imagen entre 500x500 y 2000x2000 píxeles

### Parámetros recomendados por tipo de máquina:

#### CNC Router/Fresadora
- Altura segura: 5-10mm
- Altura base: 0.2-0.5mm
- Velocidad dibujo: 800-1200mm/min

#### Impresora 3D (modo pluma)
- Altura segura: 10-20mm
- Altura base: 0mm
- Velocidad dibujo: 1000-1500mm/min

#### Plotter/Máquina de dibujo
- Altura segura: 2-5mm
- Altura base: 0mm
- Velocidad dibujo: 500-1000mm/min

#### Grabado láser (modo trazo)
- Altura segura: 1-2mm
- Altura base: 0mm
- Velocidad dibujo: 300-800mm/min

## Solución de problemas

### Error: "Selecciona una imagen de entrada"
- Asegúrate de haber seleccionado un archivo de imagen válido

### Error: "El archivo de imagen no existe"
- Verifica que la ruta del archivo sea correcta
- La imagen pudo haber sido movida o renombrada

### Error durante el procesamiento
- Verifica que la imagen no esté corrupta
- Prueba con una imagen más simple
- Revisa que tengas permisos para escribir en el directorio de salida

### La aplicación no se abre
- Verifica que Python esté instalado
- Ejecuta `pip install opencv-python numpy tkinter`
- Usa `run_gui.bat` que instala dependencias automáticamente
