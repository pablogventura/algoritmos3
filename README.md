# Discreta II

Material y códigos de la materia Matemática Discreta II (cursado y luego como ayudante). Código unificado, sin duplicados; por cada archivo se conservó la versión más reciente.

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| **practicos/** | Código por práctico: `practico1`, `practico2`, `practico4` … `practico8` (una sola copia por archivo, la más nueva) |
| **algoritmos/** | Implementaciones: `edmonds-karp`, `edmonds-karp-letras`, `dinic`, `np`, `lab` (Edmonds-Karp en C, TP de laboratorio) |
| **docs/referencia** | Apuntes y material de referencia (PDF) |
| **docs/enunciados** | Enunciados de prácticos (PDF) |
| **docs/final** | Material del final (PDFs); el código del final está en `algoritmos/` y en `practicos/` |
| **logs/** | Salidas de consola y mediciones de tiempo |

## Notas

- Las carpetas que venían de Subversion (`.svn`) están ignoradas en `.gitignore`.
- Los tests de flujo máximo están en **algoritmos/tests/flujo-maximo/** (el nombre de cada archivo indica el flujo esperado, p. ej. `debe_dar_4` → 4). `edmonds-karp/ejemplos` y `lab/examples` apuntan ahí.
