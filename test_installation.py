#!/usr/bin/env python3
"""
Script de prueba para verificar la instalación y funcionamiento
del generador de G-code para trazos a mano alzada
"""

import os
import sys
import tempfile

def test_imports():
    """Prueba que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    try:
        import cv2
        print(f"  ✓ OpenCV {cv2.__version__}")
    except ImportError:
        print("  ✗ OpenCV no encontrado")
        return False
    
    try:
        import numpy as np
        print(f"  ✓ NumPy {np.__version__}")
    except ImportError:
        print("  ✗ NumPy no encontrado")
        return False
    
    return True

def test_image_creation():
    """Crea una imagen de prueba simple"""
    print("\n🎨 Creando imagen de prueba...")
    
    try:
        import cv2
        import numpy as np
        
        # Crear imagen simple de 300x300
        img = np.ones((300, 300, 3), dtype=np.uint8) * 255
        
        # Dibujar algunas formas básicas
        cv2.circle(img, (150, 100), 50, (0, 0, 0), 2)
        cv2.rectangle(img, (75, 150), (225, 200), (0, 0, 0), 2)
        cv2.line(img, (50, 250), (250, 250), (0, 0, 0), 2)
        
        # Guardar imagen temporal
        test_image_path = "test_drawing.png"
        cv2.imwrite(test_image_path, img)
        
        if os.path.exists(test_image_path):
            print(f"  ✓ Imagen creada: {test_image_path}")
            return test_image_path
        else:
            print("  ✗ Error creando imagen")
            return None
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def test_basic_gcode_generation(image_path):
    """Prueba la generación básica de G-code"""
    print("\n⚙️ Probando generación de G-code...")
    
    try:
        from image_to_gcode import HandDrawnGCodeGenerator
        
        # Crear generador con parámetros básicos
        generator = HandDrawnGCodeGenerator(
            canvas_width=100.0,
            canvas_height=100.0,
            z_safe=2.0,
            z_draw_base=0.1,
            z_variation=0.5
        )
        
        # Generar G-code
        output_path = "test_output.gcode"
        generator.process_image_to_gcode(image_path, output_path)
        
        if os.path.exists(output_path):
            # Verificar contenido básico
            with open(output_path, 'r') as f:
                content = f.read()
                
            if "G21" in content and "G90" in content and "G0" in content:
                print(f"  ✓ G-code generado correctamente: {output_path}")
                
                # Mostrar estadísticas básicas
                lines = content.split('\n')
                g_commands = [line for line in lines if line.strip().startswith('G')]
                print(f"  📊 Líneas totales: {len(lines)}")
                print(f"  📊 Comandos G: {len(g_commands)}")
                
                return True
            else:
                print("  ✗ G-code generado pero formato incorrecto")
                return False
        else:
            print("  ✗ No se generó archivo G-code")
            return False
            
    except Exception as e:
        print(f"  ✗ Error generando G-code: {e}")
        return False

def test_advanced_generator(image_path):
    """Prueba el generador avanzado"""
    print("\n🚀 Probando generador avanzado...")
    
    try:
        from advanced_generator import AdvancedGCodeGenerator
        
        # Crear generador avanzado
        generator = AdvancedGCodeGenerator(
            machine_type="grbl",
            canvas_width=100.0,
            canvas_height=100.0
        )
        
        output_path = "test_advanced.gcode"
        generator.process_image_to_gcode(image_path, output_path)
        
        if os.path.exists(output_path):
            print(f"  ✓ Generador avanzado funciona: {output_path}")
            return True
        else:
            print("  ✗ Error con generador avanzado")
            return False
            
    except Exception as e:
        print(f"  ✗ Error con generador avanzado: {e}")
        return False

def test_machine_configs():
    """Prueba las configuraciones de máquinas"""
    print("\n🔧 Probando configuraciones de máquinas...")
    
    try:
        from machine_configs import get_machine_config
        
        machines = ["grbl", "marlin", "linuxcnc", "plotter", "laser"]
        
        for machine in machines:
            config = get_machine_config(machine)
            if config and config.name:
                print(f"  ✓ {machine}: {config.name}")
            else:
                print(f"  ✗ Error con configuración de {machine}")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error con configuraciones: {e}")
        return False

def cleanup_test_files():
    """Limpia archivos de prueba"""
    test_files = [
        "test_drawing.png",
        "test_output.gcode",
        "test_advanced.gcode"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except:
                pass

def main():
    print("🧪 PRUEBA DEL GENERADOR DE G-CODE")
    print("=" * 40)
    
    # Contador de pruebas
    tests_passed = 0
    total_tests = 5
    
    # Prueba 1: Importaciones
    if test_imports():
        tests_passed += 1
    
    # Prueba 2: Creación de imagen
    image_path = test_image_creation()
    if image_path:
        tests_passed += 1
        
        # Prueba 3: Generación básica (solo si tenemos imagen)
        if test_basic_gcode_generation(image_path):
            tests_passed += 1
        
        # Prueba 4: Generador avanzado (solo si tenemos imagen)
        if test_advanced_generator(image_path):
            tests_passed += 1
    
    # Prueba 5: Configuraciones de máquinas
    if test_machine_configs():
        tests_passed += 1
    
    # Resultados finales
    print("\n" + "=" * 40)
    print(f"📈 RESULTADOS: {tests_passed}/{total_tests} pruebas exitosas")
    
    if tests_passed == total_tests:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema está listo para usar")
        print("\n💡 Puedes empezar usando:")
        print("   - run_generator.bat (interfaz fácil)")
        print("   - python advanced_generator.py tu_imagen.jpg")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("🔧 Verifica la instalación de dependencias")
        
        if tests_passed == 0:
            print("\n📦 Para instalar dependencias:")
            print("   pip install opencv-python numpy")
    
    # Limpiar archivos de prueba
    cleanup_test_files()
    
    return 0 if tests_passed == total_tests else 1

if __name__ == "__main__":
    exit(main())
