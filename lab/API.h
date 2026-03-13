/*
  Alejandro José Naser Pastoriza - alejnaser@gmail.com
  Nicolás Daniel Gómez - nicolasdanielgomez@gmail.com
  Mariano Jesús Mateuci - mjmateuci@gmail.com
  Francisco Bazán - franbazan26@gmail.com
*/

#ifndef API_H
#define API_H

#include "network.h"

/*
  La función aloca memoria e inicializa una estructura DragonSt y
  devuelve un puntero a ésta. En caso de error, la función devolverá un
  puntero a null.
*/
DragonP NuevoDragon (void);

/*
  Destruye N y libera la memoria alocada. Retorna 1 si todo anduvo
  bien y 0 si no.
*/
int DestruirDragon (DragonP N);

/*
  La función carga el lado xy (->) con capacidad c en N. Debe
  inicializar el flujo en el lado cargado como cero. La función
  retorna 1 si no hubo problemas y 0 en caso contrario.
*/
int CargarUnLado (DragonP N, u32 x, u32 y, u32 c);

/*
  La función lee todos los datos del network donde se correrá el
  algoritmo desde la entrada estándard, y los carga en N usando la
  función CargarUnLado (). La función retorna 1 si no hubo problemas y
  0 en caso contrario.
  Cada línea del formato de entrada es de la siguiente forma:
  x y c, lo cual representa un lado xy (->) con capacidad c. Los
  valores x, y, c serán u32. El valor 0 será la fuente, mientras que
  el valor 1 representrará el resumidero. Que se agregue el vértice v
  al network no implica que se agregue el vértice v' tal que v' < v.
  Por ejemplo, los vértices pueden ser 0, 1, 2, 15768, 21234567. Se
  asegura (por nosotros) que si un lado xy (->) forma parte de la
  entrada, entonces el lado (yx) (<-) no será parte de la entrada.
  También se asegura que no habrá lados repetidos ni loops. La carga
  debe terminar cuando se encuentra una línea que no es de la forma
  descripta arriba. (Por ejempo, si se llega a un EOF pero también si
  hay una línea en blanco o una línea cualquiera que no sea de la forma
  indicada arriba).
*/
int LlenarDragon (DragonP N);

/*
  La función hace una búsqueda de un camino aumentante de menor
  longitud. Debe actualizar en N las etiquetas o datos que ustedes
  hayan decidido crear asociadas a la búsqueda. Pueden elegir parar la
  búsqueda al llegar a t (si llegan) o continuarla hasta que la cola
  se vacíe. Devuelve 1 si se llega a t, 0 sino y -1 si hay un error.
*/
int ECAML (DragonP N);

/*
  La funcion devuelve 100a + 10b + c donde:
  - a = 1 si el flujo guardado en N es maximal.
  - a = 0 si el flujo guardado en N no es maximal.
  - b = 1 si la última búsqueda ECAML efectuada llegó a t.
  - b = 0 si la última búsqueda efectuada no llegó a t.
  - c = 1 si los resultados de la última búsqueda ECAML
    han sido usados para actualizar el flujo.
  - c = 0 si los resultados de la última búsqueda ECAML
    no han sido usados para actualizar el flujo.
*/
int DondeEstamosParados (DragonP N);

/*
  Precondición: se debe haber efectuado una búsqueda ECAML
  que llegó a t pero que todavía no se ha usado para actualizar el flujo.
  Esta condición debe ser chequeada por la función.
  La función actualiza el flujo en el network N.
  Lee los datos internos de N que le permitan reconstruir el camino aumentante
  y cambia el flujo a lo largo de ese camino. (si hay un parámetro interno
  que guarde el valor del flujo, también lo actualiza).
  Valor de retorno: el valor por el cual se aumenta el flujo, o 0 si hubo algún
  error, en particular si no se cumple la precondición.
*/
u32 AumentarFlujo (DragonP N);

/*
  La función hace lo mismo que AumentarFlujo y tiene la misma precondición,
  pero además imprime el camino aumentante y el aumento a lo largo de él.
  La impresión es siempre por standard output.
  Se imprime el camino aumentante y su aumento en el siguiente formato:
  camino aumentante #:
  t:x_r:...:x_1:s: <cantDelIncremento>
  donde # es el número del camino aumentante que se está procesando.
  El doble punto (:) entre vértices va cuando el lado es forward. Si el
  lado es backward en vez de ":" deben escribir |.
  Por ejemplo: t:11|100|2:8:7|4:3:s es un camino con lados forward
  (s,3), (3,4), (7,8), (8,2) y (11,t) y lados backward (4,7), (2, 100), (100, 11).
  Presten atención que si bien internamente s es 0 y t es 1, la salida
  debe decir s y t y no 0 y 1. Observen que el camino se escribe acá al
  revés de como lo estamos haciendo en el práctico. Una razón de esto es
  porque si, y otra es porque pueden imprimirlo mas eficientemente de esta
  forma, aunque en la forma usual tampoco es complicado.
  Valor de retorno: el valor del aumento o 0 si hubo algún error, en particular
  si no se cumple la precondición.
*/
u32 AumentarFlujoYtambienImprimirCamino (DragonP N);

/*
   Imprime el flujo que se tiene en este momento. La impresión debe
   ser siempre por standard output.
   Debe imprimir:
   Flujo t:
   Lado x_1, y_1: <FlujoDelLado>
   ...
   Lado x_m, y_m: <FlujoDelLado>
   Donde t es Maximal si el flujo es maximal y (y no maximal) si no lo es.
*/
void imprimirFlujo (DragonP N);

/* 
   Imprime el valor del flujo. La impresión debe ser por standard output. 
   Debe imprimir: valor del flujo t: <valorDelFlujo>
   donde como antes, t es Maximal si el flujo es maximal y (no maximal) si
   no lo es. (recordar que el valor del flujo puede ser mayor a u32).
*/
void ImprimirValorFlujo (DragonP N);

/*
  Debe imprimir por standard output un corte minimal del network y su 
  capacidad en el siguiente formato:
  Corte Minimal: S = {s, x_1, ...}
  Capacidad: <capacidad>
  (el órden en que quieran poner los vértices de S es arbitrario).
  (recordar que la capacidad del corte minimal puede ser mayor a u32).
*/
void ImprimirCorte (DragonP N);

/*
   Toma los valores de a y b y los suma correctamente. (módulo 2^64)
   Necesitaran esta función para cuando calculen el valor del flujo
   maximal y la capacidad del corte minimal. Pueden asumir que "a"
   en realidad tendrá a lo sumo 50 bits, asi que sumarle un numero de
   32 bits (b) nunca tendran probelmas con la cota superior de 64
   bits, i.e, no es necesario preocuparse porque el resultado sea
   mayor que 2^64.
 */
u64 Sumar64 (u64 a, u32 b);

#endif /* API_H */
