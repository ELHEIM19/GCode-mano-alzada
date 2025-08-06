#!/usr/bin/env python3
"""
Generador avanzado de G-code para trazos a mano alzada
Integra configuraciones de máquinas y perfiles de dibujo
"""

import argparse
import os
import sys
from image_to_gcode import HandDrawnGCodeGenerator
from machine_configs import get_machine_config, list_available_machines

class AdvancedGCodeGenerator(HandDrawnGCodeGenerator):
    """Generador avanzado con soporte para múltiples máquinas"""
    
    def __init__(self, machine_type="grbl", **kwargs):
        super().__init__(**kwargs)
        self.machine_config = get_machine_config(machine_type)
        
    def generate_gcode_header(self):
        """Genera header específico para el tipo de máquina"""
        header = [
            f"; G-code generado para {self.machine_config.name}",
            f"; Generador de trazos a mano alzada",
            f"; Dimensiones: {self.canvas_width}x{self.canvas_height}mm",
            ""
        ]
        header.extend(self.machine_config.get_header())
        header.append("")
        return header
    
    def generate_gcode_footer(self):
        """Genera footer específico para el tipo de máquina"""
        footer = [""]
        footer.extend(self.machine_config.get_footer())
        return footer

def setup_drawing_profiles():
    """Define perfiles de dibujo predefinidos"""
    return {
        "artistic": {
            "description": "Trazo artístico con mucha expresión",
            "z_variation": 1.5,
            "feed_rate": 800,
            "tremor_amplitude": 0.15,
            "pressure_variation": 0.4,
            "speed_variation": 0.3
        },
        "technical": {
            "description": "Trazo técnico preciso",
            "z_variation": 0.3,
            "feed_rate": 1200,
            "tremor_amplitude": 0.05,
            "pressure_variation": 0.1,
            "speed_variation": 0.1
        },
        "sketch": {
            "description": "Boceto rápido y suelto",
            "z_variation": 0.8,
            "feed_rate": 1500,
            "tremor_amplitude": 0.2,
            "pressure_variation": 0.35,
            "speed_variation": 0.25
        },
        "calligraphy": {
            "description": "Estilo caligráfico con variaciones suaves",
            "z_variation": 1.0,
            "feed_rate": 600,
            "tremor_amplitude": 0.08,
            "pressure_variation": 0.5,
            "speed_variation": 0.2
        },
        "engraving": {
            "description": "Grabado controlado para materiales duros",
            "z_variation": 0.2,
            "feed_rate": 400,
            "tremor_amplitude": 0.03,
            "pressure_variation": 0.05,
            "speed_variation": 0.05
        }
    }

def apply_profile(generator, profile_name, profiles):
    """Aplica un perfil de dibujo al generador"""
    if profile_name not in profiles:
        print(f"Perfil '{profile_name}' no encontrado. Usando valores por defecto.")
        return
    
    profile = profiles[profile_name]
    
    # Aplicar configuraciones del perfil
    if "z_variation" in profile:
        generator.z_variation = profile["z_variation"]
    if "feed_rate" in profile:
        generator.feed_rate = profile["feed_rate"]
    if "tremor_amplitude" in profile:
        generator.tremor_amplitude = profile["tremor_amplitude"]
    if "pressure_variation" in profile:
        generator.pressure_variation = profile["pressure_variation"]
    if "speed_variation" in profile:
        generator.speed_variation = profile["speed_variation"]

def main():
    parser = argparse.ArgumentParser(
        description='Generador avanzado de G-code para trazos a mano alzada',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s imagen.jpg
  %(prog)s imagen.jpg --machine grbl --profile artistic
  %(prog)s logo.png --machine plotter --profile technical --width 100
  %(prog)s dibujo.jpg --machine laser --profile engraving --z-base 0
        """
    )
    
    # Argumentos principales
    parser.add_argument('input_image', help='Imagen de entrada')
    parser.add_argument('-o', '--output', help='Archivo G-code de salida')
    
    # Configuración de máquina
    parser.add_argument('--machine', default='grbl', 
                       help='Tipo de máquina: grbl, marlin, linuxcnc, plotter, laser (default: grbl)')
    parser.add_argument('--list-machines', action='store_true',
                       help='Lista los tipos de máquinas disponibles')
    
    # Perfiles de dibujo
    parser.add_argument('--profile', default='artistic',
                       help='Perfil de dibujo: artistic, technical, sketch, calligraphy, engraving (default: artistic)')
    parser.add_argument('--list-profiles', action='store_true',
                       help='Lista los perfiles de dibujo disponibles')
    
    # Parámetros de canvas
    parser.add_argument('--width', type=float, default=200.0,
                       help='Ancho del canvas en mm (default: 200)')
    parser.add_argument('--height', type=float, default=200.0,
                       help='Alto del canvas en mm (default: 200)')
    
    # Parámetros Z
    parser.add_argument('--z-safe', type=float, default=5.0,
                       help='Altura segura en mm (default: 5)')
    parser.add_argument('--z-base', type=float, default=0.2,
                       help='Altura base de dibujo en mm (default: 0.2)')
    parser.add_argument('--z-variation', type=float,
                       help='Variación máxima en Z en mm (override del perfil)')
    
    # Parámetros de velocidad
    parser.add_argument('--feed-rate', type=int,
                       help='Velocidad de dibujo en mm/min (override del perfil)')
    parser.add_argument('--travel-speed', type=int, default=3000,
                       help='Velocidad de desplazamiento en mm/min (default: 3000)')
    
    # Procesamiento de imagen
    parser.add_argument('--blur', type=int, default=5,
                       help='Kernel de difuminado para suavizar imagen (default: 5)')
    
    args = parser.parse_args()
    
    # Mostrar listas si se solicita
    if args.list_machines:
        list_available_machines()
        return 0
    
    if args.list_profiles:
        profiles = setup_drawing_profiles()
        print("Perfiles de dibujo disponibles:")
        for name, config in profiles.items():
            print(f"  {name}: {config['description']}")
        return 0
    
    # Validar imagen de entrada
    if not os.path.exists(args.input_image):
        print(f"Error: No se encontró la imagen '{args.input_image}'")
        return 1
    
    # Configurar nombre de salida
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.input_image))[0]
        args.output = f"{base_name}_{args.machine}_{args.profile}.gcode"
    
    # Crear generador
    try:
        generator = AdvancedGCodeGenerator(
            machine_type=args.machine,
            canvas_width=args.width,
            canvas_height=args.height,
            z_safe=args.z_safe,
            z_draw_base=args.z_base,
            travel_speed=args.travel_speed
        )
        
        # Aplicar perfil
        profiles = setup_drawing_profiles()
        apply_profile(generator, args.profile, profiles)
        
        # Aplicar overrides de línea de comandos
        if args.z_variation is not None:
            generator.z_variation = args.z_variation
        if args.feed_rate is not None:
            generator.feed_rate = args.feed_rate
        
        # Procesar imagen
        print(f"Procesando: {args.input_image}")
        print(f"Máquina: {generator.machine_config.name}")
        print(f"Perfil: {args.profile} - {profiles.get(args.profile, {}).get('description', 'Personalizado')}")
        print(f"Canvas: {args.width}x{args.height}mm")
        print(f"Variación Z: {generator.z_variation}mm")
        print(f"Velocidad: {generator.feed_rate}mm/min")
        print()
        
        generator.process_image_to_gcode(args.input_image, args.output)
        
        print(f"✓ G-code generado exitosamente: {args.output}")
        print()
        print("Notas importantes:")
        print("- Verifica los parámetros Z según tu máquina y material")
        print("- Prueba en simulador antes del uso real")
        print("- Ajusta velocidades según las capacidades de tu máquina")
        
        if args.machine == "laser":
            print("- ADVERTENCIA: Usar protección ocular con láser")
        elif args.machine == "marlin":
            print("- Asegúrate de reemplazar el extrusor por una pluma/marcador")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
