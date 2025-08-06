#!/usr/bin/env python3
"""
Script de ejemplo para generar G-code a mano alzada
Incluye diferentes configuraciones predefinidas
"""

import os
import sys
from image_to_gcode import HandDrawnGCodeGenerator

def create_artistic_profile():
    """Configuración para dibujo artístico con mucha expresión"""
    return HandDrawnGCodeGenerator(
        canvas_width=200.0,
        canvas_height=200.0,
        z_safe=5.0,
        z_draw_base=0.3,
        z_variation=1.5,  # Mucha variación para efecto artístico
        feed_rate=800,    # Más lento para mejor control
        travel_speed=2500
    )

def create_technical_profile():
    """Configuración para dibujos técnicos más precisos"""
    return HandDrawnGCodeGenerator(
        canvas_width=200.0,
        canvas_height=200.0,
        z_safe=3.0,
        z_draw_base=0.1,
        z_variation=0.3,  # Poca variación para precisión
        feed_rate=1200,   # Más rápido y preciso
        travel_speed=4000
    )

def create_sketch_profile():
    """Configuración para bocetos rápidos"""
    return HandDrawnGCodeGenerator(
        canvas_width=150.0,
        canvas_height=150.0,
        z_safe=4.0,
        z_draw_base=0.2,
        z_variation=0.8,
        feed_rate=1500,   # Rápido como un boceto
        travel_speed=3500
    )

def process_with_profile(image_path, profile_name="artistic"):
    """Procesa una imagen con un perfil predefinido"""
    
    if not os.path.exists(image_path):
        print(f"Error: No se encontró la imagen {image_path}")
        return False
    
    # Seleccionar perfil
    profiles = {
        "artistic": create_artistic_profile,
        "technical": create_technical_profile,
        "sketch": create_sketch_profile
    }
    
    if profile_name not in profiles:
        print(f"Perfil '{profile_name}' no encontrado. Usando 'artistic'")
        profile_name = "artistic"
    
    # Crear generador con perfil seleccionado
    generator = profiles[profile_name]()
    
    # Ajustar parámetros específicos del perfil
    if profile_name == "artistic":
        generator.tremor_amplitude = 0.15
        generator.pressure_variation = 0.4
        generator.speed_variation = 0.3
    elif profile_name == "technical":
        generator.tremor_amplitude = 0.05
        generator.pressure_variation = 0.1
        generator.speed_variation = 0.1
    elif profile_name == "sketch":
        generator.tremor_amplitude = 0.2
        generator.pressure_variation = 0.35
        generator.speed_variation = 0.25
    
    # Generar nombre de archivo de salida
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f"{base_name}_{profile_name}.gcode"
    
    try:
        generator.process_image_to_gcode(image_path, output_path)
        print(f"✓ G-code generado con perfil '{profile_name}': {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error procesando imagen: {e}")
        return False

def main():
    print("=== Generador de G-code para Trazos a Mano Alzada ===")
    print("Perfiles disponibles:")
    print("  - artistic:  Mucha expresión, variaciones amplias")
    print("  - technical: Preciso, variaciones mínimas")
    print("  - sketch:    Estilo boceto rápido")
    print()
    
    if len(sys.argv) < 2:
        print("Uso: python example_usage.py <imagen> [perfil]")
        print("Ejemplo: python example_usage.py mi_imagen.jpg artistic")
        return 1
    
    image_path = sys.argv[1]
    profile = sys.argv[2] if len(sys.argv) > 2 else "artistic"
    
    success = process_with_profile(image_path, profile)
    
    if success:
        print("\n¡Proceso completado! Revisa el archivo .gcode generado.")
        print("\nConsejos:")
        print("- Verifica los parámetros Z según tu máquina")
        print("- Ajusta las velocidades según tu material")
        print("- Prueba en simulador antes del uso real")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
