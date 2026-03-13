# Matemática Discreta II — FaMAF (UNC)

Implementaciones de la mayoría de los algoritmos que se ven en **Matemática Discreta II** en la Facultad de Matemática, Astronomía, Física y Computación (FaMAF) de la Universidad Nacional de Córdoba (UNC).

---

## Requisitos

- **Python 3** — La mayor parte del código está en Python.
- **numpy** — Usado en `codigos/`, `generacodigos/`, `hungarian/`, `ciclicos/`.
- **sympy** — Usado en `ciclicos/` (polinomios y códigos cíclicos).

Opcional (para comparar rendimiento):

- **Rust** — Edmonds-Karp y Dinic en Rust (`edmonds-karp-rust/`, `dinic-rust/`). Con Rust 1.80+ se puede compilar con la feature `parallel` (Rayon).
- **C + make** — Edmonds-Karp en C (`edmonds-karp-c/`).

---

## Estructura del repositorio

```
├── algoritmos/              # Implementaciones
│   ├── edmonds-karp/        # Edmonds-Karp (Python, vértices numéricos)
│   ├── edmonds-karp-letras/ # Edmonds-Karp (Python, vértices con letras)
│   ├── edmonds-karp-c/      # Edmonds-Karp en C
│   ├── edmonds-karp-rust/   # Edmonds-Karp en Rust
│   ├── dinic/               # Dinic (Python)
│   ├── dinic-rust/          # Dinic en Rust
│   ├── corte/               # Corte mínimo en red de flujo
│   ├── wave/                # Red de flujo con niveles (wave), aristas "xy"
│   ├── coloreo/             # Coloreo de grafos (greedy, DSatur, RLF, WP)
│   ├── codigos/             # Códigos lineales sobre Z₂, matriz de chequeo
│   ├── ciclicos/            # Códigos cíclicos (polinomios, generadora, chequeo)
│   ├── hungarian/           # Algoritmo húngaro (asignación de costo mínimo)
│   └── tests/               # Tests automatizados
│       ├── run_tests.py         # Tests de flujo máximo
│       ├── run_tests_otros.py   # Tests de corte, wave, coloreo, codigos, ciclicos, hungarian
│       ├── flujo-maximo/        # Archivos de test para flujo (formato "x y cap")
│       └── test_*.py            # Tests por algoritmo
├── practicos/               # Material de prácticos (ej. practico4 con Dinic)
└── README.md
```

---

## Tests

Desde la **raíz del repo**:

| Comando | Qué prueba |
|--------|------------|
| `python3 algoritmos/tests/run_tests.py` | Solo flujo máximo (Edmonds-Karp en todas sus versiones y Dinic) |
| `python3 algoritmos/tests/run_tests.py --all` | Flujo máximo y además corte, wave, coloreo, codigos, ciclicos, hungarian |
| `python3 algoritmos/tests/run_tests_otros.py` | Solo los otros algoritmos (sin flujo) |

Opciones útiles:

- `run_tests.py --impl edmonds-karp` — Probar solo una implementación (edmonds-karp, edmonds-karp-letras, edmonds-karp-c, edmonds-karp-rust, dinic, dinic-rust).
- `run_tests.py --list` — Listar archivos de test de flujo y valor esperado.
- `run_tests_otros.py --impl corte` — Probar solo un módulo (corte, wave, coloreo, codigos, ciclicos, hungarian).
- `run_tests_otros.py --list` — Listar módulos disponibles.

Para que los tests de flujo incluyan **C** y **Rust**, hay que compilar antes en cada directorio: `make` (C) o `cargo build --release` (Rust). Para Rust con BFS paralelizado: `cargo build --release --features parallel` (requiere Rust 1.80+).

---

## Formato de entrada (flujo máximo)

Las implementaciones de flujo que leen por **stdin** esperan líneas:

```
origen destino capacidad
```

con **vértice fuente = 0** y **sumidero = 1**. Ejemplo:

```
0 2 10
0 3 5
2 1 8
3 1 3
```

Los archivos en `algoritmos/tests/flujo-maximo/` siguen este formato. El valor esperado del flujo máximo puede estar en el nombre del archivo (ej. `debe_dar_5` → flujo 5).

---

## Cómo ejecutar cada algoritmo a mano

- **Edmonds-Karp (Python):**  
  `cd algoritmos/edmonds-karp && python3 main.py -v 0 < ../tests/flujo-maximo/debe_dar_5`
- **Edmonds-Karp (letras):**  
  Mismo esquema en `algoritmos/edmonds-karp-letras/` (formato de grafo puede usar letras según el reader).
- **Edmonds-Karp (C):**  
  `cd algoritmos/edmonds-karp-c && make && ./main < ../tests/flujo-maximo/debe_dar_5`
- **Edmonds-Karp (Rust):**  
  `cd algoritmos/edmonds-karp-rust && cargo build --release && ./target/release/main < ../tests/flujo-maximo/debe_dar_5`
- **Dinic (Python):**  
  Grafo interno: `cd algoritmos/dinic && python3 dinic.py`. Con archivo: `python3 dinic.py --stdin < archivo.txt` (mismo formato "x y cap", fuente 0, sumidero 1).
- **Dinic (Rust):**  
  Misma entrada que EK: `./target/release/main < archivo`.
- **Corte, wave, coloreo, codigos, ciclicos, hungarian:**  
  Son módulos Python; se pueden importar o ejecutar según el `if __name__ == "__main__"` de cada uno. Los tests en `algoritmos/tests/test_*.py` muestran cómo usarlos.

---

## Resumen por tema (FaMAF – Discreta II)

| Tema | Algoritmos / contenido |
|------|-------------------------|
| Flujo máximo | Edmonds-Karp, Dinic |
| Corte mínimo | Conjunto S del corte (BFS en red residual) |
| Redes con niveles | Wave (BFS por niveles, aristas tipo "0A", "F1") |
| Coloreo de grafos | Greedy, DSatur, RLF, WP |
| Códigos lineales | Z₂, matriz generadora, matriz de chequeo, generación |
| Códigos cíclicos | Polinomios generadores, dimensión, codificación, síndromes |
| Asignación | Algoritmo húngaro (matching de costo mínimo en bipartito) |

---

## Prácticos

En `practicos/` hay material de prácticos de la materia (por ejemplo `practico4/` con Dinic). Los archivos de grafos de flujo en `algoritmos/tests/flujo-maximo/` se usan tanto para los algoritmos como para los tests.
