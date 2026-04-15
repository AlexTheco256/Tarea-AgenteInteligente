"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""
import random
from entorno import Agente


class MiAgente(Agente):
    """
    Tu agente de navegación.

    Implementa el método decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        # Puedes agregar atributos aquí si los necesitas.
        # Ejemplo:
        #   self.pasos = 0
        #   self.memoria = {}

        self.memoria = {}
        self.ultima_pos = None # Nueva memoria para no retroceder

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulación. Opcional."""
        self.memoria = {}
        self.ultima_pos = None
        pass

    def decidir(self, percepcion):
        
        """
        Decide la siguiente acción del agente.
        
        Parámetros:
            percepcion – diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        # ╔══════════════════════════════════════╗
        # ║   ESCRIBE TU LÓGICA AQUÍ             ║
        # ╚══════════════════════════════════════╝

        # Ejemplo básico (bórralo y escribe tu propia lógica):
        #
        # vert, horiz = percepcion['direccion_meta']
        #
        # if percepcion[vert] == 'libre' or percepcion[vert] == 'meta':
        #     return vert
        # if percepcion[horiz] == 'libre' or percepcion[horiz] == 'meta':
        #     return horiz
        #
        # return 'abajo'
        """"
        print('Hola decidir')
        for direccion in self.ACCIONES:
            celda = percepcion[direccion]
            if celda == 'meta':
                return direccion
            if celda == 'libre':
                return direccion

        return 'abajo'  # ← Reemplazar con tu lógica
        """

        pos_actual = percepcion.get('posicion')
        
        # 1. Registrar visita (Costo de utilidad)
        self.memoria[pos_actual] = self.memoria.get(pos_actual, 0) + 1
        
        # 2. Prioridad Absoluta: ¡La Meta!
        for d in self.ACCIONES:
            if percepcion.get(d) == 'meta':
                return d
        
        # 3. ANALIZAR ALREDEDORES Y CALCULAR UTILIDAD
        opciones_validas = []
        mejor_utilidad = float('inf')

        for d in self.ACCIONES:
            estado = percepcion.get(d)
            
            # Solo consideramos celdas que NO sean paredes ni bordes (None)
            if estado == 'libre':
                dr, dc = self.DELTAS[d]
                pos_futura = (pos_actual[0] + dr, pos_actual[1] + dc)
                
                # --- ALGORITMO DE EFICIENCIA ---
                # Consultamos visitas previas
                visitas = self.memoria.get(pos_futura, 0)
                
                # Penalización por retroceso (evita el "ping-pong" en pasillos)
                costo_retroceso = 10 if pos_futura == self.ultima_pos else 0
                
                # Calculamos el peso total (A menor peso, mayor utilidad)
                peso_total = visitas + costo_retroceso

                if peso_total < mejor_utilidad:
                    mejor_utilidad = peso_total
                    opciones_validas = [d]
                elif peso_total == mejor_utilidad:
                    opciones_validas.append(d)

        # 4. DECISIÓN Y CAMBIO DE DIRECCIÓN
        if opciones_validas:
            # Si hay varias opciones con igual utilidad, el random ayuda a 
            # "cambiar de dirección" para explorar nuevas áreas.
            accion_elegida = random.choice(opciones_validas)
            self.ultima_pos = pos_actual 
            return accion_elegida

        # 5. Si está bloqueado por todos lados (no debería pasar), baja
        return 'abajo'