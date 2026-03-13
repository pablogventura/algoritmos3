/*
 Hungarian Algorithm para resolver el problema de minimizar la suma de los pesos
 en un grafo bipartito G=(X union Y,E), con |X|=|Y|. 
 Para Discreta II
 El algoritmo usa varias subrutinas, pero todas variables globales.
 Ud. deberia modificarlo para que no tenga este defecto.
*/
#include <stdio.h>

#define  TAM (9)
/*
el TAM es el ``n": el tama~no de la matriz=numero de filas=numero de columnas, 
recordemos que solo es para matrices cuadradas
como ejemplo lo fijo en 8
ejercicio para mejorar el algoritmo: modificarlo para que lo acepte como linea de entrada.
*/


//declarar las variables:
int             filas_no_matcheadas;	// lo obvio. Cuando sea 0 paramos.
int             Matriz[TAM][TAM];	// guarda la matriz Filas=X, Columnas=Y
int             MatrizOriginal[TAM][TAM];	// mantendra la original
int             x;		// contador de filas
int             y;		// contador de columnas
int             k;		// contador auxiliar de Kolumnas
int             col_que_matchea_la_fila[TAM];	// indica que columna matchea la fila.
						// sera negativo si no esta matcheada
int             fila_que_matchea_la_col[TAM];	// idem pero al reves: indica con que
						// fila estamos matcheando la columna.
int             etiqueta_de_columna[TAM];	/* para etiquetear columnas con nombres
						 * de filas para poder luego extender el
						 * matching Notar que no hace falta algo
						 * similar para filas (i.e.., no hay un
						 * etiqueta_de_fila) porque en realidad
						 * la etiqueta_de_fila sera siempre igual 
						 * a la col_que_matchea_la_fila y en el
						 * caso de que la fila no esta matcheada
						 * (ie.e, en clase la etiqueteabamos con
						 * una *) entonces
						 * col_que_matchea_la_fila sera negativo, 
						 * asi que no necesitamos un registro
						 * etiqueta_de_fila */
int             S[TAM];		/* Este sera el ``S'' de clase, i.e.., donde se guardan
				 * al principio las filas que no matcheamos (ie., las que 
				 * tienen *) y luego iremos guardando todas las filas que 
				 * luego etiqueteemos para escanearlas. Una pequenha
				 * variacion con lo hecho en clase es que entonces al
				 * escanearlas lo haremos en modo realmente EK, es decir, 
				 * en el orden en que van a ser agregadas a la cola (en
				 * cambio en clase, para no complicar la notacion las
				 * escaneabamos en orden alfabetico por layers. La
				 * complejidad es la misma aunque los resultados
				 * individuales pueden variar. De esta forma evitamos
				 * tener que ir recorriendo cada vez las filas, buscando
				 * cuales son las etiqueteadas no escaneadas. */
int             s;		// guardara cuantos elementos tiene S. 
int             i;		// ``puntero" al elemento i-esimo de S.
int             Minimo;		// para calcular el minimo de Sxcomplemento(Gamma(S)), y
				// tambien para calcular min filas o columnas.
int             restar_de_fila[TAM];	/* esto es lo que debemos restarle a las filas de 
					 * S cuando cambiemos la matriz. para ahorrar
					 * tiempo, en vez de ir y restarlo, se lo guarda
					 * en un registro. */
int             sumar_a_col[TAM];	/* aca guardamos lo que le sumariamos a las
					 * columnas de Gamma(S). Al igual que con las
					 * filas, no lo sumamos realmente. */
int             xy_real;	// cuando deba ver la entrada ``real'' xy, la guardare
				// aqui mientras la examino.
int             min_de_col_int_S[TAM];	/* no es el minimo de TODA la columna, sino que
					 * sera el minimo de la columna en su
					 * interseccion con S */
int             fila_donde_esta_min[TAM];	// donde encontramos el minimo anterior
int             costo = 0;	// para guardar el costo total
int             frigidez;	// sera 1 mientras no haya orgasmo.
int             extension;	// cuando extendamos el match, una flag para saber cuando 
				// terminamos.
int             verboso;	// habra tres niveles de verbosidad, segun lo que quiera
				// que me muetre.
//obviamente esto es mas personal que otra cosa.
int             cambios_de_matriz = 0;
int             extensiones_de_matching = 0;
//las dos ultimas son contadores que no tienen nada que ver con el algoritmo en si, sino
//para ver facilmente que tan complicado fue o no encontrar el matching

/*Abajo pongo las subrutinas para mejorar la lectura del algoritmo principal
Tendremos:
0) Cargar Matriz
1) Parte 1), i.e., restar minimo de cada fila
2) Parte 2), i.e, restar minimo de cada columna
3)Parte 3), i.e., hallar un matching inicial usando Greedy
4) Parte 4), pero como es complicada, ella tiene sub-subrutinas, que van antes:
   4.1)una subrutina que escanea filas
   4.2) una subrutina que cambia la matriz si no se puede extender el matching
   4.3) una subrutina que extiende el matching si encontramos una columna libre
   4.4) una subrutina que reinicializa las etiquetas luego de extender el matching
   Las dos primeras son a su vez complicadas, asi que tienen sub-sub-subrutinas, que van antes:
   La 4.1 tiene la siguiente:
        4.1.1)una que chequea el lugar xy de la matriz , mirando si es cero y si puede etiquetear
                   la columna o extender el matching. Esta requiere a su vez de sub-sub-sub-subrutinas:
                4.1.1.1) una subrutina que etiquetea las columnas
                4.1.1.2)  otra que actualiza el minimo de la columna en su interseccion con S
    La 4.2 tiene las siguientes:
        4.2.1) Calcular el minimo de Sxcomplemento(Gamma(S))
        4.2.2) Restarlo de S
        4.2.3) Sumarlo a Gamma(S) y al mismo tiempo chequear los nuevos ceros que aparezcan.
         Esta tiene una subsubsubrutina 4.2.3.1) que hace esta ultima parte.
*/


void
CargarMatriz()			// subrutina 0
{				// esta es una matriz de ejemplo que use en un final
Matriz[0][0] = 9;
Matriz[0][1] = 8;
Matriz[0][2] = 8;
Matriz[0][3] = 5;
Matriz[0][4] = 6;
Matriz[0][5] = 6;
Matriz[0][6] = 8;
Matriz[0][7] = 6;
Matriz[0][8] = 8;
Matriz[1][0] = 5;
Matriz[1][1] = 6;
Matriz[1][2] = 7;
Matriz[1][3] = 4;
Matriz[1][4] = 2;
Matriz[1][5] = 3;
Matriz[1][6] = 6;
Matriz[1][7] = 5;
Matriz[1][8] = 6;
Matriz[2][0] = 5;
Matriz[2][1] = 5;
Matriz[2][2] = 5;
Matriz[2][3] = 2;
Matriz[2][4] = 2;
Matriz[2][5] = 3;
Matriz[2][6] = 4;
Matriz[2][7] = 3;
Matriz[2][8] = 9;
Matriz[3][0] = 8;
Matriz[3][1] = 7;
Matriz[3][2] = 4;
Matriz[3][3] = 5;
Matriz[3][4] = 5;
Matriz[3][5] = 5;
Matriz[3][6] = 4;
Matriz[3][7] = 6;
Matriz[3][8] = 4;
Matriz[4][0] = 8;
Matriz[4][1] = 5;
Matriz[4][2] = 8;
Matriz[4][3] = 6;
Matriz[4][4] = 5;
Matriz[4][5] = 3;
Matriz[4][6] = 7;
Matriz[4][7] = 7;
Matriz[4][8] = 7;
Matriz[5][0] = 8;
Matriz[5][1] = 7;
Matriz[5][2] = 7;
Matriz[5][3] = 4;
Matriz[5][4] = 5;
Matriz[5][5] = 5;
Matriz[5][6] = 7;
Matriz[5][7] = 5;
Matriz[5][8] = 7;
Matriz[6][0] = 10;
Matriz[6][1] = 7;
Matriz[6][2] = 9;
Matriz[6][3] = 7;
Matriz[6][4] = 7;
Matriz[6][5] = 5;
Matriz[6][6] = 8;
Matriz[6][7] = 8;
Matriz[6][8] = 8;
Matriz[7][0] = 7;
Matriz[7][1] = 7;
Matriz[7][2] = 7;
Matriz[7][3] = 4;
Matriz[7][4] = 5;
Matriz[7][5] = 5;
Matriz[7][6] = 7;
Matriz[7][7] = 5;
Matriz[7][8] = 7;
Matriz[8][0] = 8;
Matriz[8][1] = 5;
Matriz[8][2] = 7;
Matriz[8][3] = 5;
Matriz[8][4] = 5;
Matriz[8][5] = 3;
Matriz[8][6] = 7;
Matriz[8][7] = 7;
Matriz[8][8] = 7;




	for (x = 0; x < TAM; x++) {
		if (verboso)	// muestra matriz a medida que la carga
			printf("\n Fila %d:", x);
		for (y = 0; y < TAM; y++) {
			MatrizOriginal[x][y] = Matriz[x][y];
			if (verboso)
				printf("% d", Matriz[x][y]);
		}
	}
	printf("\n\n");
}				// fin Cargar matriz

void
restarMinimoDeFilas()		// subrutina 1
{
	// Comenzar con Parte 1): sustraccion del minimo por filas. Este si lo sustraemos 
	// en serio
	// por otro lado, podria no hacerlo pero me es mas facil para corregir los
	// examenes.
	for (x = 0; x < TAM; x++) {
		Minimo = Matriz[x][0];
		for (y = 1; y < TAM; y++)
			if (Matriz[x][y] < Minimo)
				Minimo = Matriz[x][y];	// en esta linea y las anteriores 
							// calculo el minimo de la fila
		costo += Minimo;	// incremento el costo por lo que restare
		if (Minimo != 0)	// pequenho truco: si el minimo es cero no hace
					// falta restarlo
			for (y = 0; y < TAM; y++)
				Matriz[x][y] -= Minimo;
	}
	if (verboso)		// muestra matriz luego de la resta
	{
		for (x = 0; x < TAM; x++) {
			for (y = 0; y < TAM; y++)
				printf("% d", Matriz[x][y]);
			printf("\n");
		}
		printf("Costo parcial:%d.\n", costo);
	}
}				// Fin restar minimo por filas 

void
restarMinimoDeColumnas()	// subrutina 2
{
// Comenzar con Parte 2): sustraccion del minimo por columnas. Este tambien lo sustraemos en serio.
	for (y = 0; y < TAM; y++) {
		Minimo = Matriz[0][y];
		for (x = 1; x < TAM; x++)
			if (Matriz[x][y] < Minimo)
				Minimo = Matriz[x][y];	// calculamos el minimo de la
							// columna
		costo += Minimo;
		if (Minimo != 0)	// de vuelta, si es cero no lo restamos para
					// ahorrar tiempo
			for (x = 0; x < TAM; x++)
				Matriz[x][y] -= Minimo;
	}
	if (verboso)		// muestra matriz luego de la resta
	{
		for (x = 0; x < TAM; x++) {
			for (y = 0; y < TAM; y++)
				printf("% d", Matriz[x][y]);
			printf("\n");
		}
		printf("Costo parcial:%d.\n", costo);
	}
}				// Fin restar minimo por columnas


void
MatchingInicial()		// subrutina 3
{
// Comenzar Parte 3):  matching inicial (usando Greedy)
	s = 0;
	for (y = 0; y < TAM; y++) {
		fila_que_matchea_la_col[y] = -1;	// un -1 significara que la
							// columna no esta matcheada.
		etiqueta_de_columna[y] = -1;	// un -1 significa que la column no esta
						// etiqueteada. 
		sumar_a_col[y] = 0;	// aprovecho para inicializar todos estos
		min_de_col_int_S[y] = 2147483647;	// y estos
		// lo anterior es 2^{31}-1, lo mas grande de un signed int
		// asumamos entradas en un rango razonable para no usar longs
	}			// endfor y
	for (x = 0; x < TAM; x++) {
		restar_de_fila[x] = 0;	// aprovecho para inicializar todos estos.
		col_que_matchea_la_fila[x] = -1;	// no matcheada al principio, si
							// no pude matchearla, quedara
							// asi.
		for (y = 0; y < TAM; y++)
			if (0 == Matriz[x][y] && fila_que_matchea_la_col[y] < 0
			    && col_que_matchea_la_fila[x] < 0)
				// busca ceros en la fila que no esten en una col. ya
				// matcheada y solo si la fila no fue ya matcheada
			{
				col_que_matchea_la_fila[x] = y;	// a la fila x la matcheo 
								// con la columna y
				fila_que_matchea_la_col[y] = x;	// a la columna y la
								// matcheo con la fila x.
				if (verboso)	// me dira como se construye el match
						// parcial
					printf("Agregando (%d, %d) al matching.\n", x, y);
			}	// endif
		if (col_que_matchea_la_fila[x] < 0)	// si sali sin poder matchear
		{
			S[s++] = x;	// agrego la fila x a las filas etiqueteadas con
					// * e incremento el s=cardinalidad de S.
			if (verboso)
				printf("Fila %d no se puede matchear. |S|=%d. \n", x, s);
		}		// endif col 
	}			// endfor x
}				// Finalizar Parte 3) ( matching inicial (Greedy))


//las siguientes son las subsubsubrutinas de EscanearFilas: 


void
EtiquetearColumna()		// sub 4.1.1.1
{
	etiqueta_de_columna[y] = x;	// etiqueteo la columna "y" con el nombre de la
					// fila x
	S[s++] = fila_que_matchea_la_col[y];	// agrego la fila nueva descubierta por
						// la columna a las filas para escanear y 
						// aumento el s.
	min_de_col_int_S[y] = 0;	// si la etiqueto es porque hay un cero ahi.
	if (verboso)
		printf
		    ("\n    Agregando la %d_a fila de S: es la %d , matcheada con col %d etiqueteada con fila %d\n    ",
		     s, fila_que_matchea_la_col[y], y, x);
}


 // esta actualiza el min_de_col_int_S 
void
ActualizarMinimoColS()		// sub 4.1.1.2
{
	min_de_col_int_S[y] = xy_real;
	fila_donde_esta_min[y] = x;
}				// se efectuara cuando al chequar x,y se sepa que no es
				// cero, pero x esta en S. En ese caso,
   // ``y" estara en complemento(Gamma(S)) y si es menor que el minimo que se tiene, se
   // llama a esta subrutina.


void
ChequearLugarXY()		// sub 4.1.1
{
	if (verboso > 1)
		printf(" %d, ", y);	// superverboso si quiero ver como se va
					// modificando el matching
	if (min_de_col_int_S[y])	// si el min es 0 alguien mas ya la etiqueteo,
					// con lo que no la reviso.
	{
		xy_real = Matriz[x][y] - restar_de_fila[x] + sumar_a_col[y];
		/* el costo - lo que hay que restar a la fila mas el incremento por
		 * columnas i.e., este es el A[x][y] ``real'' que deberiamos haber
		 * calculado, pero en vez de eso, para no perder tiempo O( n^2)
		 * updateando la matriz, uno pierde tiempo O(n), pero luego debe perder
		 * un poquito mas de tiempo en el calculo este. Igual como este hay que
		 * revisarlo el tiempo que se pierde es la diferencia entre chequear que
		 * fuese cero, o chequear que fuese cero previo calculo de algo.
		 * Asumiendo op. aritmeticas rapidas, es casi lo mismo. */
		if (xy_real < min_de_col_int_S[y])
			/* si no es menor, como estoy en el caso de min_de_col_int_S
			 * mayor a cero, tendremos en particular que no es cero, asi que
			 * no hace falta revisarlo. Ademas, si no es menor es mayor o
			 * igual, por lo que min_de_col_int_S, que guarda el minimo, no
			 * cambiara */
		{
			if (xy_real == 0) {
				if (fila_que_matchea_la_col[y] < 0)
					frigidez = 0;	// i.e., orgasmo: la columna esta 
							// libre.
				else
					EtiquetearColumna();	// si no esta libre, la
								// etiqueteo. El ``s"
								// crece aca.
			} else
				ActualizarMinimoColS();	// endif xy_real==0
		}		// endif xy_real<mincol
	}			// endif mincol>0
	if (frigidez)
		y++;		// solo cambio el "y" si debo seguir buscando.
}				// end ChequearLugarXY


void
EscanearFilas()			// sub 4.1
{
	while (i < s && frigidez)	// solo estoy aca si s no es cero, asi que el
					// loop comienza bien.
	{
		// Begin escanear fila i del S. 
		x = S[i];	// recupero cual es la fila a escanear
		if (verboso)
			printf("\n Escaneando fila %d.\n    Chequeando col", x);
		y = 0;
		while (y < TAM && frigidez)
			ChequearLugarXY();
		// oculto aca esta el hecho de que s puede crecer. "y" tambien crece si
		// no hay orgasmo.
		// End escanear fila i del S
		i++;
	}			// endwhile 
}				// end EscanearFilas 


//las siguientes 4 las necesito cuando cambio la matriz. 
void
CalcularMinimo()		// sub 4.2.1
{				// el minimo de Sxcomplemento(Gamma(S))
	Minimo = 2147483647;
	for (y = 0; y < TAM; y++)
		if (min_de_col_int_S[y] && min_de_col_int_S[y] < Minimo)
			Minimo = min_de_col_int_S[y];
}				// end calcular minimo. la primera parte del if anterior
				// es para asegurarme que solo lo calculo en
				// complemento(Gamma(S)).

void
RestarMinimo()			// sub 4.2.2
{
	for (i = 0; i < s; i++)
		restar_de_fila[S[i]] += Minimo;	// resto ese minimo a las filas de S,
						// i.e.., incremento lo que debo
						// restarles
}


/*como para sumar el minimo debemos recorrer las columnas,
tenemos dos cosas para hacer: a las de Gamma(S) les sumaremos el minimo,
pero a las del complemento debemos buscarles los nuevos ceros.
Por comodidad, ponemos las dos cosas en una subrutina
*/

/*esta que viene es la que se usara cuando estamos chequeando complemento(Gamma(S))
las columnas se vienen chequeando con el contador auxiliar k
para que si encontramos una columna libre, la llamamos "y"
pues el k seguira corriendo para otra cosa (sumarle los minimos a Gamma(S))
*/
void
NuevosCeros()			// 4.2.3.1
{
	if (frigidez)		// i.e., todavia no encontramos una columna libre
	{
		min_de_col_int_S[k] -= Minimo;	// esto hara que los que tenian el minimo 
						// sean los nuevos ceros, i.e.., se
						// agreguen a Gamma(S)
		if (min_de_col_int_S[k] == 0)	// solo miro los que son cero
		{
			x = fila_donde_esta_min[k];
			y = k;	// necesito el "y" ahora: lo que pasa es que si hay
				// orgasmo quedara fijo aca, y el k lo necesito para
				// updatear Gamma(S).
			if (verboso > 1)	// superverboso
				printf("Nuevo cero en (%d,%d)\n", x, k);
			if (fila_que_matchea_la_col[k] < 0)	// i.e., es una * por lo
								// que voy a poder
								// extender el match.
				frigidez = 0;	// i.e., orgasmo
			else	// si no estoy en el caso anterior, etiqueteo para seguir 
				// la busqueda
				EtiquetearColumna();	// aca tambien se usa el "y"
		}		// endif mincol==0
	}			// endif frigidez
}				// end NuevosCeros 

void
SumarMinimoYHallarNuevosCeros()	// 4.2.3
{				// sumar minimo (al ``viejo'' Gamma(S)), calcular donde
				// estan las nuevas columnas del nuevo Gamma, y
				// etiquetarlas
	for (k = 0; k < TAM; k++)	// debo trabajar con el contador auxiliar
		if (min_de_col_int_S[k])	// i.e., en complemento(Gamma(S))
			NuevosCeros();
		else		// en Gamma(S) debo sumar el minimo.
			sumar_a_col[k] += Minimo;
}				// end sumar Minimo


void
CambiarMatriz()			// 4.2
{
	cambios_de_matriz++;
	CalcularMinimo();
	if (verboso) {
		printf("\n No se puede extender matching.\n S={%d", S[0]);
		for (i = 1; i < s; i++)
			printf(",%d", S[i]);
		printf("}\n");
		printf("\n Cambiando matriz, Minimo: %d.\n", Minimo);
	}
	RestarMinimo();
	SumarMinimoYHallarNuevosCeros();
}


void
ExtenderMatching()		// 4.3
{
	// Begin extender el matching solo si la columna "y", etiqueteada con x esta
	// libre.
	extensiones_de_matching++;
	if (verboso)
		printf("\n Orgasmo! en  columna %d \n\n", y);
	extension = 0;		// para saber cuando terminar
	while (extension == 0) {
		k = col_que_matchea_la_fila[x];
		col_que_matchea_la_fila[x] = y;	// cambiar el matching en la fila x de la 
						// columna k a la y. La k queda libre.
		fila_que_matchea_la_col[y] = x;	// con lo cual ahora y queda matcheada
						// con x.
		if (verboso > 1)	// superverboso
			printf
			    ("rematcheando fila %d<->col %d. Queda libre: columna: %d.\n",
			     x, y, k);
		if (k < 0)	// si x era una fila no matcheada, k no es columna en
				// serio, pero ahora x esta matcheada, terminamos.
			extension = 1;
		else {
			x = etiqueta_de_columna[k];	// si k era columna en serio,
							// estaba etiqueteada, cambio el
							// x a la etiqueta para seguir el 
							// loop
			y = k;
		}
	}			// endwhile del extension
}				// End extender matching (cuando salimos, extendimos el
				// match, i.e.., termina un paso)

void
ReinicializarEtiquetas()	// 4.4
{				// Begin reinicializar para comenzar nuevo paso
//esta sera una subrutina luego del termino de un paso, i.e, luego de incrementar el match en un lado.
	s = 0;
	for (y = 0; y < TAM; y++) {
		etiqueta_de_columna[y] = -1;
		min_de_col_int_S[y] = 2147483647;
	}
	for (x = 0; x < TAM; x++)
		if (col_que_matchea_la_fila[x] < 0) {
			S[s++] = x;	// agrego x a las filas no matcheadas y aumento
					// el s.
			if (verboso)
				printf("Re-etiqueteando fila %d con *. |S|=%d.\n", x, s);
		}
}				// End reinicilizar para comenzar nuevo paso


void
Parte4()			// <--------------------------ACA ESTA LA PARTE
				// 4-------------------------
{
// Comenzar Parte 4) i.e.., parte principal donde extendemos el matching usando EK y modificando matriz si es necesario
	filas_no_matcheadas = s;	// el s cambiara luego, y quiero guardar cuantas
					// son las filas no matcheadas.
	while (filas_no_matcheadas > 0)	// condicion para terminar
	{
		if (verboso)
			printf("\n Filas Matcheadas: %d.\n", TAM - s);
		i = 0;
		// no se puede usar un for porque el limite superior es dinamico y cambia 
		// durante la ejecucion del algoritmo.
		// el i lo necesitamos en EscanearFilas, pero no queremos
		// reinicializarlo, por eso esta fuera del loop.
		frigidez = 1;
		while (frigidez) {
			EscanearFilas();
			/* De EscanearFilas salgo si termine de escanear todo S pero no
			 * pude extender el matching o bien si logre extender el matching */
			if (frigidez)
				CambiarMatriz();	// si sali porque no pude
							// extender el matching, debo
							// cambiar la matriz.
		}		// end while(frigidez). Salimos si hay orgasmo
		ExtenderMatching();
		if (--filas_no_matcheadas > 0)	// como extendimos, disminuimos el
						// contador en uno. Si llegamos a cero,
						// no hace falta reinicilializar
			ReinicializarEtiquetas();
	}			// endwhile(filas_no_matcheadas>0)

}				// Fin Parte 4)


int
main(int argc, char *argv[])	// <------------------------ACA ESTA EL
				// MAIN----------------------------
{
	if (argc != 2) {
		printf
		    ("uso: %s -v (verboso), [o -vv (superverboso)] [o culquier otra cosa (no versboso)]\n",
		     argv[0]);
		return 1;
	} else {
		if (strcmp(argv[1], "-v") == 0)
			verboso = 1;
		else {
			if (strcmp(argv[1], "-vv") == 0)
				verboso = 2;
			else
				verboso = 0;
		}
	}
	CargarMatriz();
	restarMinimoDeFilas();
	restarMinimoDeColumnas();
	MatchingInicial();
	Parte4();
	printf("Cambios de Matriz:%d.\n", cambios_de_matriz);
	printf("Extensiones de Matching:%d.\n", extensiones_de_matching);
	if (verboso)
		printf("Matching:\n");
	else			// aunque no sea verboso, puedo querer ver el match final
//por otro lado, puedo no querer verlo, si la matriz es por ejemplo 1000x1000.
	{
		printf("Listo. Quiere ver el Matching? (0= no, otro entero=si)");
		scanf("%d", &verboso);
	}
	for (x = 0; x < TAM; x++) {
		costo += Matriz[x][col_que_matchea_la_fila[x]];
		if (verboso)
			printf("(%d ,%d ): %d \n", x, col_que_matchea_la_fila[x],
			       MatrizOriginal[x][col_que_matchea_la_fila[x]]);
	}
	printf("Costo Total:%d.\n", costo);
	return 0;
}				// fin main
