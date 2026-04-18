import random
from entorno import Agente


class MiAgente(Agente):

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        self.visitados = set()
        self.ultima_accion = None
        self.mapa_obstaculos = set()

    def al_iniciar(self):
        self.visitados = set()
        self.ultima_accion = None
        self.mapa_obstaculos = set()

    # ── Helpers ──────────────────────────────────────────────

    def _pos_futura(self, pos, direccion):
        """Calcula la posición resultante de moverse en 'direccion'."""
        dy, dx = self.DELTAS[direccion]
        return (pos[0] + dy, pos[1] + dx)

    def _vecinos_obstaculo(self, pos):
        """
        Cuenta cuántos de los 4 vecinos de 'pos' están en mapa_obstaculos.
        Se usa como penalización: una celda rodeada de paredes es menos
        deseable aunque esté 'libre'.
        """
        count = 0
        for dy, dx in self.DELTAS.values():
            vecino = (pos[0] + dy, pos[1] + dx)
            if vecino in self.mapa_obstaculos:
                count += 1
        return count

    def _score(self, pos):
        """
        Puntuación de una celda candidata.
        Menor es mejor: premia no visitadas y penaliza vecindad con obstáculos.
        """
        ya_visitada  = 1 if pos in self.visitados else 0
        peligro      = self._vecinos_obstaculo(pos)   # 0–4
        return ya_visitada * 10 + peligro             # visitada pesa más

    # ── Percepción y registro ────────────────────────────────

    def _registrar_obstaculos(self, pos_actual, percepcion):
        """
        Actualiza mapa_obstaculos con lo que el agente ve a su alrededor.
        También filtra candidatos inválidos antes de que lleguen a decidir().
        """
        for direccion in self.ACCIONES:
            estado = percepcion[direccion]
            coord_vista = self._pos_futura(pos_actual, direccion)
            if estado in ('pared', None):
                self.mapa_obstaculos.add(coord_vista)

    # ── Filtrado ─────────────────────────────────────────────

    def _candidatos_validos(self, pos_actual, percepcion):
        """
        Devuelve solo las direcciones libres cuya posición futura
        NO aparece ya en mapa_obstaculos (doble seguro además de la percepción).
        """
        validos = []
        for a in self.ACCIONES:
            if percepcion[a] == 'libre':
                pos_futura = self._pos_futura(pos_actual, a)
                # USO 1: descartar candidatos que el mapa ya marca como obstáculo
                if pos_futura not in self.mapa_obstaculos:
                    validos.append(a)
        return validos

    # ── Decisión ─────────────────────────────────────────────

    def decidir(self, percepcion):
        pos_actual = percepcion['posicion']
        self.visitados.add(pos_actual)

        # Registrar obstáculos visibles
        self._registrar_obstaculos(pos_actual, percepcion)

        # 1. Prioridad absoluta: meta visible
        for a in self.ACCIONES:
            if percepcion[a] == 'meta':
                self.ultima_accion = a
                return a

        # 2. Obtener candidatos (ya filtrados contra mapa_obstaculos)
        candidatos = self._candidatos_validos(pos_actual, percepcion)

        if not candidatos:
            # Sin salida válida — retroceder por camino conocido
            retroceso = [
                a for a in self.ACCIONES
                if percepcion[a] == 'libre'
            ]
            accion = random.choice(retroceso) if retroceso else random.choice(self.ACCIONES)
            self.ultima_accion = accion
            return accion

        # 3. Separar nuevos vs. visitados
        nuevos  = [a for a in candidatos
                   if self._pos_futura(pos_actual, a) not in self.visitados]
        viejos  = [a for a in candidatos
                   if self._pos_futura(pos_actual, a) in self.visitados]

        pool = nuevos if nuevos else viejos

        # 4. Ordenar por score (USO 2: penalizar celdas rodeadas de obstáculos)
        pool.sort(key=lambda a: self._score(self._pos_futura(pos_actual, a)))

        # 5. Preferir continuar recto si está entre los mejores (mismo score mínimo)
        score_min = self._score(self._pos_futura(pos_actual, pool[0]))
        mejores   = [a for a in pool
                     if self._score(self._pos_futura(pos_actual, a)) == score_min]

        if self.ultima_accion in mejores:
            accion = self.ultima_accion          # inercia: seguir recto
        else:
            accion = mejores[0]                  # el de menor score

        self.ultima_accion = accion
        return accion