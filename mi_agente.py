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

        self.visitados = set()#guarda las posiciones visitadas
        self.ultima_accion = None #guarda la última acción tomada

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulación. Opcional."""
        self.visitados = set() #reiniciar el registro de posiciones visitadas al iniciar
        self.ultima_accion = None #reiniciar la última acción al iniciar
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

        pos_actual = percepcion['posicion'] # Mira que hay en esta direccion
        self.visitados.add(pos_actual) # Registro de rastro

        # 1. META: Prioridad absoluta
        for a in self.ACCIONES: # Revisar cada dirección posible
            if percepcion[a] == 'meta': return a

        # 2. EVALUAR CAMINOS (Nuevos vs Viejos)
        caminos_nuevos = []#guarda las direcciones que el agente no ha visitado antes
        caminos_viejos = []#guarda las direcciones que el agente ya ha visitado antes

        for a in self.ACCIONES:
            if percepcion[a] == 'libre':
                fila, colum = self.DELTAS[a]
                pos_futura = (pos_actual[0] + fila, pos_actual[1] + colum)
                
                if pos_futura not in self.visitados:
                    caminos_nuevos.append(a)
                else:
                    caminos_viejos.append(a)

        # 3. LÓGICA DE DECISIÓN

        # SI HAY CAMINOS NUEVOS:
        if caminos_nuevos:
            # Intentar seguir recto si la dirección anterior es NUEVA
            if self.ultima_accion in caminos_nuevos:
                accion_elegida = self.ultima_accion
            else:
                # Si no, escoger un camino nuevo al azar
                accion_elegida = random.choice(caminos_nuevos)
        
        # SI ES UN CALLEJÓN (No hay caminos nuevos, solo viejos):
        elif caminos_viejos:
            # Regresar por donde vino 
            accion_elegida = random.choice(caminos_viejos)
        
        else:
            accion_elegida = random.choice(self.ACCIONES)

        self.ultima_accion = accion_elegida
        return accion_elegida