# Tests de algoritmos

## flujo-maximo/

Entradas de prueba para algoritmos de **flujo máximo** (Edmonds-Karp, Dinic, lab en C).

El nombre del archivo indica el valor esperado del flujo maximal cuando aplica:

| Patrón | Significado |
|--------|-------------|
| `debe_dar_N` | Flujo maximal esperado: **N** (ej. `debe_dar_4` → 4, `debe_dar_23327233` → 23327233) |
| `debe_dar_512_a`, `_b`, `_c`, `_d` | Flujo esperado: **512** |
| `simple_debe_dar_512`, `mediano_debe_dar_512`, `complejo_debe_dar_512` | Flujo esperado: **512** |

Archivos como `muchas_aristas`, `muchos_vertices`, `ejemploceballos_bien.in`, `split150full.in`, `complex5000`, `finalexpansionconmenosdecincomil` son entradas adicionales sin el valor esperado en el nombre (útiles para rendimiento o pruebas manuales).

Las implementaciones en `algoritmos/edmonds-karp` y `algoritmos/lab` usan esta misma carpeta de tests.
