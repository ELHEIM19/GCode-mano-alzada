#!/usr/bin/env python3
"""
Generador de G-code para simular trazos a mano alzada
Procesa una imagen y genera G-code con movimientos Z variables
"""

import cv2
import numpy as np
import argparse
import os
import random
import math
from typing import List, Tuple, Optional

class HandDrawnGCodeGenerator:
    def __init__(self, 
                 canvas_width: float = 200.0,  # mm
                 canvas_height: float = 200.0,  # mm
                 z_safe: float = 5.0,  # mm altura segura
                 z_draw_base: float = 0.2,  # mm altura base de dibujo
                 z_variation: float = 0.8,  # mm variación en Z
                 feed_rate: int = 1000,  # mm/min
                 travel_speed: int = 3000):  # mm/min
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.z_safe = z_safe
        self.z_draw_base = z_draw_base
        self.z_variation = z_variation
        self.feed_rate = feed_rate
        self.travel_speed = travel_speed
        
        # Parámetros para simular trazo manual
        self.tremor_amplitude = 0.1  # mm - temblor en XY
        self.pressure_variation = 0.3  # variación de presión (afecta Z)
        self.speed_variation = 0.2  # variación de velocidad
        
    def load_and_process_image(self, image_path: str, blur_kernel: int = 5) -> np.ndarray:
        """Carga y procesa la imagen para extraer contornos"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")
        
        # Cargar imagen
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar filtro gaussiano para suavizar
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        
        # Detectar bordes con Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Aplicar operación morfológica para conectar líneas cercanas
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        return edges
    
    def find_contours(self, edges: np.ndarray) -> List[np.ndarray]:
        """Encuentra contornos en la imagen procesada"""
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos muy pequeños
        min_area = 50
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        # Ordenar por área (más grandes primero)
        filtered_contours.sort(key=cv2.contourArea, reverse=True)
        
        return filtered_contours
    
    def image_to_machine_coords(self, point: Tuple[int, int], img_shape: Tuple[int, int]) -> Tuple[float, float]:
        """Convierte coordenadas de imagen a coordenadas de máquina"""
        img_height, img_width = img_shape
        x_img, y_img = point
        
        # Escalar y centrar
        x_machine = (x_img / img_width) * self.canvas_width
        y_machine = ((img_height - y_img) / img_height) * self.canvas_height
        
        return x_machine, y_machine
    
    def add_hand_tremor(self, x: float, y: float) -> Tuple[float, float]:
        """Añade temblor natural al punto"""
        tremor_x = random.uniform(-self.tremor_amplitude, self.tremor_amplitude)
        tremor_y = random.uniform(-self.tremor_amplitude, self.tremor_amplitude)
        return x + tremor_x, y + tremor_y
    
    def calculate_pressure_z(self, progress: float, segment_length: float) -> float:
        """Calcula la altura Z basada en presión simulada"""
        # Presión base
        base_pressure = 1.0
        
        # Variación por posición en el trazo (más presión al inicio y final)
        position_factor = 1.0 + 0.3 * math.sin(progress * math.pi)
        
        # Variación aleatoria para simular inconsistencia humana
        random_factor = 1.0 + random.uniform(-self.pressure_variation, self.pressure_variation)
        
        # Presión total
        total_pressure = base_pressure * position_factor * random_factor
        
        # Convertir presión a altura Z (más presión = menor Z)
        z_offset = self.z_variation * (1.0 - min(total_pressure, 1.5) / 1.5)
        
        return self.z_draw_base + z_offset
    
    def calculate_feed_rate(self, base_rate: int) -> int:
        """Calcula velocidad variable para simular trazo manual"""
        variation = random.uniform(-self.speed_variation, self.speed_variation)
        return max(100, int(base_rate * (1.0 + variation)))
    
    def contour_to_gcode(self, contour: np.ndarray, img_shape: Tuple[int, int]) -> List[str]:
        """Convierte un contorno a comandos G-code"""
        gcode_lines = []
        
        # Simplificar contorno para reducir puntos
        epsilon = 0.005 * cv2.arcLength(contour, True)
        simplified = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(simplified) < 2:
            return gcode_lines
        
        points = simplified.reshape(-1, 2)
        
        # Primer punto - mover sin dibujar
        x, y = self.image_to_machine_coords((points[0][0], points[0][1]), img_shape)
        gcode_lines.append(f"G0 Z{self.z_safe:.2f}")  # Levantar
        gcode_lines.append(f"G0 X{x:.3f} Y{y:.3f} F{self.travel_speed}")  # Posicionar
        
        # Bajar para empezar a dibujar
        z_start = self.calculate_pressure_z(0.0, len(points))
        gcode_lines.append(f"G1 Z{z_start:.3f} F{self.feed_rate // 4}")
        
        # Dibujar el contorno
        for i in range(1, len(points)):
            progress = i / len(points)
            
            # Coordenadas base
            x, y = self.image_to_machine_coords((points[i][0], points[i][1]), img_shape)
            
            # Añadir temblor
            x, y = self.add_hand_tremor(x, y)
            
            # Calcular Z con variación de presión
            z = self.calculate_pressure_z(progress, len(points))
            
            # Velocidad variable
            feed = self.calculate_feed_rate(self.feed_rate)
            
            gcode_lines.append(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f} F{feed}")
        
        # Levantar al final del trazo
        gcode_lines.append(f"G0 Z{self.z_safe:.2f}")
        
        return gcode_lines
    
    def generate_gcode_header(self) -> List[str]:
        """Genera el header del archivo G-code"""
        return [
            "; G-code generado para simular trazos a mano alzada",
            f"; Dimensiones del canvas: {self.canvas_width}x{self.canvas_height}mm",
            f"; Altura segura: {self.z_safe}mm",
            f"; Altura base de dibujo: {self.z_draw_base}mm",
            f"; Variación Z: {self.z_variation}mm",
            "",
            "G21 ; Unidades en milímetros",
            "G90 ; Posicionamiento absoluto",
            "G28 ; Home todos los ejes",
            f"G0 Z{self.z_safe:.2f} ; Mover a altura segura",
            "M3 S1000 ; Encender herramienta (ajustar según máquina)",
            "G4 P2 ; Pausa 2 segundos",
            ""
        ]
    
    def generate_gcode_footer(self) -> List[str]:
        """Genera el footer del archivo G-code"""
        return [
            "",
            "; Finalización",
            f"G0 Z{self.z_safe:.2f} ; Subir a altura segura",
            "G0 X0 Y0 ; Volver al origen",
            "M5 ; Apagar herramienta",
            "M30 ; Fin del programa"
        ]
    
    def process_image_to_gcode(self, image_path: str, output_path: str) -> None:
        """Procesa una imagen completa y genera el archivo G-code"""
        print(f"Procesando imagen: {image_path}")
        
        # Procesar imagen
        edges = self.load_and_process_image(image_path)
        img_shape = edges.shape
        
        # Encontrar contornos
        contours = self.find_contours(edges)
        print(f"Encontrados {len(contours)} contornos")
        
        # Generar G-code
        gcode_lines = []
        gcode_lines.extend(self.generate_gcode_header())
        
        for i, contour in enumerate(contours):
            gcode_lines.append(f"; Contorno {i+1}")
            contour_gcode = self.contour_to_gcode(contour, img_shape)
            gcode_lines.extend(contour_gcode)
            gcode_lines.append("")
        
        gcode_lines.extend(self.generate_gcode_footer())
        
        # Guardar archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(gcode_lines))
        
        print(f"G-code generado: {output_path}")
        print(f"Total de líneas: {len(gcode_lines)}")

def main():
    parser = argparse.ArgumentParser(description='Genera G-code con trazos a mano alzada desde una imagen')
    parser.add_argument('input_image', help='Ruta de la imagen de entrada')
    parser.add_argument('-o', '--output', help='Archivo G-code de salida (default: output.gcode)')
    parser.add_argument('--width', type=float, default=200.0, help='Ancho del canvas en mm (default: 200)')
    parser.add_argument('--height', type=float, default=200.0, help='Alto del canvas en mm (default: 200)')
    parser.add_argument('--z-safe', type=float, default=5.0, help='Altura segura en mm (default: 5)')
    parser.add_argument('--z-base', type=float, default=0.2, help='Altura base de dibujo en mm (default: 0.2)')
    parser.add_argument('--z-variation', type=float, default=0.8, help='Variación máxima en Z en mm (default: 0.8)')
    parser.add_argument('--feed-rate', type=int, default=1000, help='Velocidad de dibujo en mm/min (default: 1000)')
    parser.add_argument('--travel-speed', type=int, default=3000, help='Velocidad de desplazamiento en mm/min (default: 3000)')
    
    args = parser.parse_args()
    
    # Configurar nombre de salida si no se especifica
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.input_image))[0]
        args.output = f"{base_name}_handdrawn.gcode"
    
    # Crear generador
    generator = HandDrawnGCodeGenerator(
        canvas_width=args.width,
        canvas_height=args.height,
        z_safe=args.z_safe,
        z_draw_base=args.z_base,
        z_variation=args.z_variation,
        feed_rate=args.feed_rate,
        travel_speed=args.travel_speed
    )
    
    try:
        generator.process_image_to_gcode(args.input_image, args.output)
        print("¡Proceso completado exitosamente!")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
