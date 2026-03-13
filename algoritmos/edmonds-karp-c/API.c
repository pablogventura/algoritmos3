#include "API.h"

DragonP NuevoDragon (void) {
  return create_network ();
}

int DestruirDragon (DragonP N) {
  return destroy_network (N);
}

int CargarUnLado (DragonP N, u32 x, u32 y, u32 c) {
  return add_edge_to_network (N, x, y, c);
}

int LlenarDragon (DragonP N) {
  return populate_network_from_stdin (N);
}

int ECAML (DragonP N) {
  return find_shortest_length_augmenting_path (N);
}

int DondeEstamosParados (DragonP N) {
  return where_we_stand (N);
}

u32 AumentarFlujo (DragonP N) {
  return increase_flow (N);
}

u32 AumentarFlujoYtambienImprimirCamino (DragonP N) {
  return increase_flow_and_print_path (N);
}

void imprimirFlujo (DragonP N) {
  print_flow (N);
}

void ImprimirValorFlujo (DragonP N) {
  print_flow_value (N);
}

void ImprimirCorte (DragonP N) {
  print_cut (N);
}

u64 Sumar64 (u64 a, u32 b) {
  return sum64 (a, b);
}
