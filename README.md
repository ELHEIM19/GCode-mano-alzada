# 🎨 Generador de G-code para Trazos a Mano Alzada

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

Convierte imágenes en G-code que simula trazos naturales dibujados a mano alzada, con variaciones realistas de presión, temblor y velocidad.

## ✨ Características Principales

- 🖼️ **Procesamiento inteligente de imágenes** - Detecta contornos automáticamente usando OpenCV
- 🎨 **Trazos naturales** - Simula temblor humano, variación de presión y velocidad
- 🤖 **Movimientos Z realistas** - Cada trazo tiene variaciones de altura para simular presión manual
- 🏭 **Múltiples máquinas** - Soporte para Grbl, Marlin, LinuxCNC, plotters y láser
- **Perfiles predefinidos**: Artístico, técnico, boceto, caligrafía y grabado
- **Configuración avanzada**: Archivo JSON y scripts de ejemplo incluidos
- **Interfaz amigable**: Script batch para Windows con menú interactivo

## 🚀 Instalación Rápida (Windows)

1. **Clona o descarga** este repositorio
2. **Ejecuta** `run_generator.bat` - instalará automáticamente las dependencias
3. **Arrastra tu imagen** al script y ¡listo!

## 📋 Instalación Manual

### Requisitos
- Python 3.7 o superior
- OpenCV
- NumPy

### Comando de instalación
```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install opencv-python numpy
```

## 💻 Uso

### 🎯 Método 1: Interfaz Gráfica (Recomendado)
```bash
run_gui.bat
```
Interfaz gráfica intuitiva con explorador de archivos integrado:
- Buscar imágenes con el explorador de Windows
- Configurar todos los parámetros visualmente
- Ver el progreso en tiempo real
- Validación automática de archivos

Para ejecutar directamente:
```bash
python gui_generator.py
```

### 🖥️ Método 2: Script Interactivo (Windows)
```bash
run_generator.bat
```
Interfaz con menú que te guía paso a paso.

### 🔧 Método 3: Generador Avanzado
```bash
python advanced_generator.py imagen.jpg
```

### ⚡ Método 4: Script Básico
```bash
python image_to_gcode.py imagen.jpg
```

## 🛠️ Ejemplos de Uso Detallados

### Para CNC Router (Grbl)
```bash
python advanced_generator.py dibujo.jpg --machine grbl --profile artistic --width 200 --height 150
```

### Para Impresora 3D (modo pluma)
```bash
python advanced_generator.py logo.png --machine marlin --profile technical --z-base 0
```

### Para Plotter de Pluma
```bash
python advanced_generator.py boceto.jpg --machine plotter --profile sketch --feed-rate 800
```

### Para Grabadora Láser
```bash
python advanced_generator.py texto.png --machine laser --profile engraving --z-variation 0
```

## Parámetros

| Parámetro | Descripción | Default | Unidad |
|-----------|-------------|---------|--------|
| `input_image` | Imagen de entrada (obligatorio) | - | - |
| `-o, --output` | Archivo G-code de salida | `[nombre]_handdrawn.gcode` | - |
| `--width` | Ancho del canvas | 200.0 | mm |
| `--height` | Alto del canvas | 200.0 | mm |
| `--z-safe` | Altura segura de desplazamiento | 5.0 | mm |
| `--z-base` | Altura base de dibujo | 0.2 | mm |
| `--z-variation` | Variación máxima en Z | 0.8 | mm |
| `--feed-rate` | Velocidad de dibujo | 1000 | mm/min |
| `--travel-speed` | Velocidad de desplazamiento | 3000 | mm/min |

## Efectos de Trazo Manual

### 1. Temblor Natural
- Añade pequeñas variaciones aleatorias en X e Y
- Simula el temblor natural de la mano

### 2. Variación de Presión
- Modifica la altura Z según la "presión" simulada
- Mayor presión = menor altura Z (más cerca del material)
- Incluye variaciones al inicio y final de cada trazo

### 3. Velocidad Variable
- Cambia la velocidad durante el dibujo
- Simula aceleración y desaceleración natural

## Tipos de Imagen Compatibles

- **Formatos**: JPG, PNG, BMP, TIFF
- **Recomendaciones**: 
  - Imágenes con contornos claros
  - Alto contraste
  - Resolución media (500-2000px)

## Ejemplos de Uso

### Para dibujo artístico
```bash
python image_to_gcode.py retrato.jpg --z-variation 1.5 --feed-rate 800
```

### Para grabado preciso
```bash
python image_to_gcode.py logo.png --z-variation 0.3 --feed-rate 1200 --z-base 0.1
```

### Para canvas grande
```bash
python image_to_gcode.py paisaje.jpg --width 300 --height 200 --travel-speed 4000
```

## Configuración de Máquina

### CNC Router / Fresadora
- Usar fresa de grabado o marcado
- Ajustar `z-base` según material
- `M3 S1000` para encender husillo

### Plotter / Máquina de dibujo
- Cambiar `M3` por comandos de pluma
- Ajustar `z-safe` para levantamiento de pluma
- Usar `z-base` cerca de 0

### Impresora 3D (modo dibujo)
- Reemplazar extrusor por pluma
- Configurar temperaturas en 0
- Ajustar `feed-rate` según pluma

## Personalización Avanzada

El script permite modificar varios parámetros internos para efectos específicos:

```python
# En la clase HandDrawnGCodeGenerator
self.tremor_amplitude = 0.1    # Intensidad del temblor
self.pressure_variation = 0.3  # Variación de presión
self.speed_variation = 0.2     # Variación de velocidad
```

## Solución de Problemas

### Imagen no se procesa
- Verificar formato de imagen compatible
- Asegurar que la imagen tiene contornos visibles
- Probar con mayor contraste

### G-code muy complejo
- Reducir resolución de imagen
- Ajustar parámetros de detección de contornos
- Filtrar contornos pequeños

### Trazos muy rápidos/lentos
- Ajustar `feed-rate` y `travel-speed`
- Modificar `speed_variation` para menos variabilidad

## Archivos Generados

El script genera archivos `.gcode` con:
- Header con configuración
- Comandos de movimiento con variaciones Z
- Footer con comandos de finalización
- Comentarios descriptivos

## Compatibilidad

Compatible con la mayoría de controladores CNC que soporten:
- G-code estándar
- Comandos G0/G1
- Control de velocidad (F)
- Control de eje Z

Testado con: Grbl, Marlin, LinuxCNC
