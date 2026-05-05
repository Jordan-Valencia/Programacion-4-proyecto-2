# Sistema de Juego de Bingo — Práctica 2

## Instrucciones de ejecución

Requiere Python 3.11 o superior. No se necesitan dependencias externas.

```bash
cd Programacion-4-proyecto-2
python main.py
```

Al iniciar, el programa pedirá:
1. La palabra de 5 letras sin letras repetidas (ej. BINGO, PLENO, LUNES).
2. El número máximo del bombo (entre 50 y 90, múltiplo de 5).
3. El registro de al menos 3 jugadores, indicando si su cartón es simple o doble.

Durante la partida, presiona **Enter** para extraer un número, **a** para agregar un jugador, **b** para dar de baja un jugador, o **q** para terminar.

## Descripción del diseño

El sistema se divide en cinco clases distribuidas en el paquete `bingo/`:

- **Carton**: genera y gestiona una grilla 5×5 de números, permite marcar números y verificar bingo.
- **CartonDoble**: extiende `Carton` con una segunda grilla independiente; gana si completa cualquiera de las dos.
- **Bombo**: mantiene el conjunto de números disponibles y extrae uno aleatorio sin repetición por turno.
- **Jugador**: posee uno o más cartones, notifica a cada cartón cuando se anuncia un número y acumula la cantidad de marcas realizadas.
- **Juego**: coordina la partida completa: registra jugadores, ejecuta turnos usando el bombo y determina al ganador.

## Relaciones entre clases

**Cartón ↔ CartonDoble — Herencia**
`CartonDoble` es un tipo especializado de `Carton`. Hereda toda la lógica de generación, marcado y verificación de bingo, y añade una segunda grilla con sus propios marcadores. La relación es de herencia porque `CartonDoble` *es un* cartón con comportamiento extendido, no una entidad que simplemente *usa* un cartón.

**Juego ↔ Bombo — Composición**
El `Bombo` es una parte constitutiva del `Juego`: se crea dentro del constructor de `Juego` y su ciclo de vida está completamente ligado al de la partida. No tiene sentido que un `Bombo` exista fuera de un `Juego`, por lo que la relación es de composición. En el código, `Juego` instancia `Bombo` en su `__init__` y lo almacena como atributo propio.

**Jugador ↔ Cartón(es) — Agregación**
Los cartones existen con independencia del jugador: son creados externamente y luego asignados mediante `agregar_carton()`. Si un jugador abandona la partida, sus cartones no dejan de existir como objetos; simplemente se desvinculan. Esta independencia de ciclos de vida define la relación como agregación, no composición. El atributo `_cartones: List[Carton]` en `Jugador` almacena referencias a objetos externos.

**Juego ↔ Jugador(es) — Asociación**
El `Juego` conoce a los jugadores registrados pero no los crea ni los destruye. Los jugadores se registran voluntariamente mediante `registrar_jugador()` y pueden retirarse con `dar_de_baja_jugador()` en cualquier momento. El `Juego` solo mantiene referencias en `_jugadores: List[Jugador]`, lo que refleja una asociación simple: colaboración sin control del ciclo de vida.
