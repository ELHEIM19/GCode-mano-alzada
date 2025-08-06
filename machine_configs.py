#!/usr/bin/env python3
"""
Configuraciones específicas para diferentes tipos de máquinas CNC
"""

class MachineConfig:
    """Configuración base para máquinas CNC"""
    
    def __init__(self, name: str):
        self.name = name
        self.gcode_header = []
        self.gcode_footer = []
        self.tool_on_command = "M3 S1000"
        self.tool_off_command = "M5"
        self.units = "G21"  # mm
        self.positioning = "G90"  # absoluto
        
    def get_header(self) -> list:
        return self.gcode_header
    
    def get_footer(self) -> list:
        return self.gcode_footer

class GrblConfig(MachineConfig):
    """Configuración para máquinas con controlador Grbl"""
    
    def __init__(self):
        super().__init__("Grbl CNC")
        self.gcode_header = [
            "; Configuración para Grbl CNC",
            "G21 ; Unidades en milímetros",
            "G90 ; Posicionamiento absoluto",
            "G17 ; Plano XY",
            "$H ; Home automático (opcional)",
            "G0 Z5.0 ; Altura segura",
            "M3 S1000 ; Encender husillo",
            "G4 P2 ; Pausa 2 segundos"
        ]
        self.gcode_footer = [
            "G0 Z5.0 ; Subir a altura segura",
            "G0 X0 Y0 ; Volver al origen",
            "M5 ; Apagar husillo",
            "M30 ; Fin del programa"
        ]

class MarlinConfig(MachineConfig):
    """Configuración para impresoras 3D con firmware Marlin (modo dibujo)"""
    
    def __init__(self):
        super().__init__("Marlin 3D Printer")
        self.gcode_header = [
            "; Configuración para Impresora 3D Marlin (modo dibujo)",
            "G21 ; Unidades en milímetros",
            "G90 ; Posicionamiento absoluto",
            "M82 ; Modo extrusor absoluto",
            "G28 ; Home todos los ejes",
            "M104 S0 ; Apagar hotend",
            "M140 S0 ; Apagar cama",
            "M107 ; Apagar ventilador",
            "G0 Z5.0 F3000 ; Altura segura",
            "; Nota: Reemplazar extrusor por pluma/marcador"
        ]
        self.gcode_footer = [
            "G0 Z10.0 ; Subir pluma",
            "G28 X Y ; Home X e Y",
            "M84 ; Apagar motores",
            "M30 ; Fin del programa"
        ]

class LinuxCNCConfig(MachineConfig):
    """Configuración para LinuxCNC"""
    
    def __init__(self):
        super().__init__("LinuxCNC")
        self.gcode_header = [
            "; Configuración para LinuxCNC",
            "G21 ; Unidades en milímetros",
            "G90 ; Posicionamiento absoluto",
            "G17 ; Plano XY",
            "G64 P0.01 ; Control de trayectoria",
            "G0 Z5.0 ; Altura segura",
            "M3 S1000 ; Encender husillo",
            "G4 P2 ; Pausa 2 segundos"
        ]
        self.gcode_footer = [
            "G0 Z5.0 ; Subir a altura segura",
            "G0 X0 Y0 ; Volver al origen",
            "M5 ; Apagar husillo",
            "M2 ; Fin del programa"
        ]

class PlotterConfig(MachineConfig):
    """Configuración para plotters de pluma"""
    
    def __init__(self):
        super().__init__("Pen Plotter")
        self.tool_on_command = "M3 S100"  # Bajar pluma
        self.tool_off_command = "M5"      # Levantar pluma
        self.gcode_header = [
            "; Configuración para Plotter de Pluma",
            "G21 ; Unidades en milímetros",
            "G90 ; Posicionamiento absoluto",
            "G28 ; Home",
            "G0 Z1.0 ; Levantar pluma",
            "; M3 = Bajar pluma, M5 = Levantar pluma"
        ]
        self.gcode_footer = [
            "M5 ; Levantar pluma",
            "G0 X0 Y0 ; Volver al origen",
            "M30 ; Fin del programa"
        ]

class LaserEngraverConfig(MachineConfig):
    """Configuración para grabadoras láser (modo escala de grises)"""
    
    def __init__(self):
        super().__init__("Laser Engraver")
        self.gcode_header = [
            "; Configuración para Grabadora Láser",
            "; ADVERTENCIA: Usar protección ocular",
            "G21 ; Unidades en milímetros",
            "G90 ; Posicionamiento absoluto",
            "G28 ; Home",
            "G0 Z0 ; Altura de trabajo",
            "M5 ; Láser apagado",
            "; Potencia del láser se controla con S (0-1000)"
        ]
        self.gcode_footer = [
            "M5 ; Apagar láser",
            "G0 X0 Y0 ; Volver al origen",
            "M30 ; Fin del programa"
        ]

def get_machine_config(machine_type: str) -> MachineConfig:
    """Obtiene la configuración para un tipo de máquina específico"""
    
    configs = {
        "grbl": GrblConfig,
        "marlin": MarlinConfig,
        "linuxcnc": LinuxCNCConfig,
        "plotter": PlotterConfig,
        "laser": LaserEngraverConfig
    }
    
    if machine_type.lower() not in configs:
        print(f"Tipo de máquina '{machine_type}' no reconocido. Usando Grbl por defecto.")
        return GrblConfig()
    
    return configs[machine_type.lower()]()

def list_available_machines():
    """Lista todas las configuraciones de máquinas disponibles"""
    
    machines = {
        "grbl": "Máquinas CNC con controlador Grbl",
        "marlin": "Impresoras 3D con firmware Marlin (modo dibujo)",
        "linuxcnc": "Máquinas CNC con LinuxCNC",
        "plotter": "Plotters de pluma",
        "laser": "Grabadoras láser (escala de grises)"
    }
    
    print("Configuraciones de máquinas disponibles:")
    for key, description in machines.items():
        print(f"  {key}: {description}")

if __name__ == "__main__":
    list_available_machines()
