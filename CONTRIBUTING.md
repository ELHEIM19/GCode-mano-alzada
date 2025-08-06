# Contributing to Generador de G-code para Trazos a Mano Alzada

¡Gracias por tu interés en contribuir! Este proyecto es de código abierto y las contribuciones son muy bienvenidas.

## 🤝 Cómo Contribuir

### 1. Fork y Clonar
```bash
# Fork el proyecto en GitHub
# Luego clona tu fork
git clone https://github.com/tu-usuario/gcode-handdrawn-generator.git
cd gcode-handdrawn-generator
```

### 2. Crear Rama Feature
```bash
git checkout -b feature/mi-nueva-funcionalidad
```

### 3. Hacer Cambios
- Escribe código limpio y comentado
- Sigue las convenciones de Python (PEP 8)
- Añade tests si es necesario
- Actualiza documentación

### 4. Probar Cambios
```bash
# Ejecutar tests
python test_installation.py

# Probar funcionamiento básico
python advanced_generator.py test.png
```

### 5. Commit y Push
```bash
git add .
git commit -m "feat: añadir nueva funcionalidad X"
git push origin feature/mi-nueva-funcionalidad
```

### 6. Pull Request
- Abre un PR desde tu fork al repositorio principal
- Describe claramente los cambios
- Incluye capturas si hay cambios visuales

## 📝 Convenciones de Código

### Python
- Usar PEP 8 para formato
- Docstrings en español para funciones públicas
- Type hints cuando sea posible
- Nombres de variables en español descriptivos

### Git Commits
Usar formato convencional:
- `feat:` para nuevas funcionalidades
- `fix:` para correcciones de bugs
- `docs:` para cambios en documentación
- `refactor:` para refactorización
- `test:` para añadir tests

## 🔍 Áreas de Contribución

### 🆕 Nuevas Funcionalidades
- Nuevos perfiles de dibujo
- Soporte para más máquinas
- Efectos adicionales (spray, brush, etc.)
- Interfaz gráfica (GUI)
- Simulador 3D

### 🐛 Corrección de Bugs
- Revisar issues existentes
- Mejorar detección de contornos
- Optimizar rendimiento
- Compatibilidad entre plataformas

### 📚 Documentación
- Mejorar README
- Añadir tutoriales
- Traducir a otros idiomas
- Ejemplos de uso

### 🧪 Testing
- Añadir tests unitarios
- Tests de integración
- Validación de G-code
- Tests en diferentes plataformas

## 📋 Checklist para PRs

- [ ] Código sigue PEP 8
- [ ] Funcionalidad probada
- [ ] Documentación actualizada
- [ ] No rompe funcionalidad existente
- [ ] Commit messages siguen convención
- [ ] PR describe claramente los cambios

## 🎯 Ideas para Contribuir

### Fáciles (Principiantes)
- Mejorar mensajes de error
- Añadir validaciones de entrada
- Documentar funciones
- Corregir typos

### Intermedias
- Optimizar algoritmos de procesamiento
- Añadir nuevos perfiles
- Mejorar configuración JSON
- Soporte para más formatos de imagen

### Avanzadas
- Interfaz gráfica (tkinter/PyQt)
- Plugin para software CAD
- Simulador 3D integrado
- Procesamiento en paralelo

## 🚀 Setup de Desarrollo

### Dependencias de Desarrollo
```bash
pip install -r requirements.txt
pip install black flake8 pytest  # Tools de desarrollo
```

### Ejecutar Tests
```bash
python test_installation.py
python -m pytest tests/  # Si añades pytest
```

### Formato de Código
```bash
black *.py
flake8 *.py
```

## 📞 Contacto

- Abrir issue para bugs o sugerencias
- Discussions para preguntas generales
- Email: [tu-email] para temas sensibles

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la misma licencia MIT del proyecto.

¡Gracias por contribuir! 🙌
