# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-06

### ✨ Añadido
- **Generador básico de G-code** (`image_to_gcode.py`)
  - Procesamiento de imágenes con OpenCV
  - Detección automática de contornos
  - Generación de trazos con variaciones Z naturales
  - Efectos de temblor, presión y velocidad variable

- **Generador avanzado** (`advanced_generator.py`)
  - Soporte para múltiples tipos de máquinas (Grbl, Marlin, LinuxCNC, Plotter, Láser)
  - 5 perfiles de dibujo predefinidos (artistic, technical, sketch, calligraphy, engraving)
  - Configuración completa por línea de comandos
  - Validación de parámetros de seguridad

- **Configuraciones de máquinas** (`machine_configs.py`)
  - Headers y footers específicos para cada tipo de máquina
  - Comandos de herramientas apropiados
  - Configuraciones optimizadas por tipo

- **Interfaz Windows** (`run_generator.bat`)
  - Menú interactivo fácil de usar
  - Instalación automática de dependencias
  - Opciones para usuarios novatos y avanzados

- **Sistema de configuración**
  - Archivo JSON configurable (`config.json`)
  - Presets para materiales
  - Parámetros de procesamiento de imagen ajustables

- **Utilidades**
  - Script de prueba e instalación (`test_installation.py`)
  - Ejemplos de uso (`example_usage.py`)
  - Documentación completa

### 🎨 Efectos Implementados
- **Temblor natural**: Variaciones aleatorias en coordenadas X,Y
- **Presión variable**: Cambios de altura Z simulando presión de mano
- **Velocidad natural**: Aceleración y desaceleración variable
- **Inicio/final suaves**: Efectos especiales al empezar y terminar trazos

### 🏭 Máquinas Soportadas
- **Grbl CNC**: Fresadoras y grabadoras CNC
- **Marlin**: Impresoras 3D en modo dibujo/pluma
- **LinuxCNC**: Control CNC avanzado
- **Plotter**: Máquinas de dibujo con pluma
- **Láser**: Grabadoras láser con precauciones de seguridad

### 📐 Perfiles de Dibujo
- **Artistic**: Máxima expresión artística (Z±1.5mm, 800mm/min)
- **Technical**: Precisión técnica (Z±0.3mm, 1200mm/min)
- **Sketch**: Boceto rápido (Z±0.8mm, 1500mm/min)
- **Calligraphy**: Estilo caligráfico (Z±1.0mm, 600mm/min)
- **Engraving**: Grabado controlado (Z±0.2mm, 400mm/min)

### 🛡️ Seguridad
- Validación de parámetros Z seguros
- Comandos de altura segura en todos los movimientos
- Advertencias específicas para láser
- Documentación de seguridad completa

### 📚 Documentación
- README completo con ejemplos
- Instrucciones de instalación paso a paso
- Guía de contribución
- Licencia MIT con disclaimers de seguridad

### 🧪 Testing
- Script de verificación de instalación
- Pruebas automáticas de todas las funcionalidades
- Generación de imágenes de prueba
- Validación de G-code generado

---

## Template para Futuras Versiones

### [X.Y.Z] - YYYY-MM-DD

### ✨ Añadido
- Nueva funcionalidad

### 🔧 Cambiado
- Cambios en funcionalidad existente

### 🐛 Corregido
- Bugs corregidos

### 🗑️ Eliminado
- Funcionalidades eliminadas

### 🛡️ Seguridad
- Mejoras de seguridad
