#include "API.h"

int main (int argc, char* argv[]) {
  DragonP N = NULL;
  /* Creates a new network */
  N = NuevoDragon ();
  /* Populates it from STDIN */
  LlenarDragon (N);
  /* While an augmenting path has been found */
  while (ECAML (N)) {
    /* Increase the flow and print the augmenting path */
    AumentarFlujoYtambienImprimirCamino (N);
    /* Prints the flow value */
    ImprimirValorFlujo (N);
    /* This line is commented out because the output is pretty big */
    /* imprimirFlujo (N); */
  }
  /* Prints the max flow value */
  ImprimirValorFlujo (N);
  /* imprimirFlujo (N); */
  /* Prints the cut */
  ImprimirCorte (N);
  /* Destroy the network */
  DestruirDragon (N);
  return 0;
}
