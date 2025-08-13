#!/usr/bin/env python3
"""
Generador de G-code simple: solo alza el lápiz, sin variaciones aleatorias
"""
import cv2
import numpy as np
import argparse
import os
from typing import List, Tuple

class SimpleGCodeGenerator:
    def __init__(self, canvas_width=200.0, canvas_height=200.0, z_safe=5.0, z_draw=0.2, feed_rate=1000, travel_speed=3000):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.z_safe = z_safe
        self.z_draw = z_draw
        self.feed_rate = feed_rate
        self.travel_speed = travel_speed

    def load_and_process_image(self, image_path: str, blur_kernel: int = 5) -> np.ndarray:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        edges = cv2.Canny(blurred, 50, 150)
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        return edges

    def find_contours(self, edges: np.ndarray) -> List[np.ndarray]:
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_area = 50
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        filtered_contours.sort(key=cv2.contourArea, reverse=True)
        return filtered_contours

    def image_to_machine_coords(self, point: Tuple[int, int], img_shape: Tuple[int, int]) -> Tuple[float, float]:
        img_height, img_width = img_shape
        x_img, y_img = point
        x_machine = (x_img / img_width) * self.canvas_width
        y_machine = ((img_height - y_img) / img_height) * self.canvas_height
        return x_machine, y_machine

    def contour_to_gcode(self, contour: np.ndarray, img_shape: Tuple[int, int]) -> List[str]:
        gcode_lines = []
        epsilon = 0.005 * cv2.arcLength(contour, True)
        simplified = cv2.approxPolyDP(contour, epsilon, True)
        if len(simplified) < 2:
            return gcode_lines
        points = simplified.reshape(-1, 2)
        x, y = self.image_to_machine_coords((points[0][0], points[0][1]), img_shape)
        gcode_lines.append(f"G0 Z{self.z_safe:.2f}")
        gcode_lines.append(f"G0 X{x:.3f} Y{y:.3f} F{self.travel_speed}")
        gcode_lines.append(f"G1 Z{self.z_draw:.3f} F{self.feed_rate}")
        for i in range(1, len(points)):
            x, y = self.image_to_machine_coords((points[i][0], points[i][1]), img_shape)
            gcode_lines.append(f"G1 X{x:.3f} Y{y:.3f} Z{self.z_draw:.3f} F{self.feed_rate}")
        gcode_lines.append(f"G0 Z{self.z_safe:.2f}")
        return gcode_lines

    def generate_gcode_header(self) -> List[str]:
        return [
            "; G-code generado sin variaciones aleatorias",
            f"; Dimensiones del canvas: {self.canvas_width}x{self.canvas_height}mm",
            f"; Altura segura: {self.z_safe}mm",
            f"; Altura de dibujo: {self.z_draw}mm",
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
        return [
            "",
            "; Finalización",
            f"G0 Z{self.z_safe:.2f} ; Subir a altura segura",
            "G0 X0 Y0 ; Volver al origen",
            "M5 ; Apagar herramienta",
            "M30 ; Fin del programa"
        ]

    def process_image_to_gcode(self, image_path: str, output_path: str) -> None:
        print(f"Procesando imagen: {image_path}")
        edges = self.load_and_process_image(image_path)
        img_shape = edges.shape
        contours = self.find_contours(edges)
        print(f"Encontrados {len(contours)} contornos")
        gcode_lines = []
        gcode_lines.extend(self.generate_gcode_header())
        for i, contour in enumerate(contours):
            gcode_lines.append(f"; Contorno {i+1}")
            contour_gcode = self.contour_to_gcode(contour, img_shape)
            gcode_lines.extend(contour_gcode)
            gcode_lines.append("")
        gcode_lines.extend(self.generate_gcode_footer())
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(gcode_lines))
        print(f"G-code generado: {output_path}")
        print(f"Total de líneas: {len(gcode_lines)}")

def main():
    parser = argparse.ArgumentParser(description='Genera G-code simple desde una imagen (sin variaciones aleatorias)')
    parser.add_argument('input_image', help='Ruta de la imagen de entrada')
    parser.add_argument('-o', '--output', help='Archivo G-code de salida (default: output.gcode)')
    parser.add_argument('--width', type=float, default=200.0, help='Ancho del canvas en mm (default: 200)')
    parser.add_argument('--height', type=float, default=200.0, help='Alto del canvas en mm (default: 200)')
    parser.add_argument('--z-safe', type=float, default=5.0, help='Altura segura en mm (default: 5)')
    parser.add_argument('--z-draw', type=float, default=0.2, help='Altura de dibujo en mm (default: 0.2)')
    parser.add_argument('--feed-rate', type=int, default=1000, help='Velocidad de dibujo en mm/min (default: 1000)')
    parser.add_argument('--travel-speed', type=int, default=3000, help='Velocidad de desplazamiento en mm/min (default: 3000)')
    args = parser.parse_args()
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.input_image))[0]
        args.output = f"{base_name}_simple.gcode"
    generator = SimpleGCodeGenerator(
        canvas_width=args.width,
        canvas_height=args.height,
        z_safe=args.z_safe,
        z_draw=args.z_draw,
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
