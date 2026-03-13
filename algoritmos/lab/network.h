#ifndef NETWORK_H
#define NETWORK_H

#include "helper.h"
#include "info.h"

/* This functions are mapped one to one with the API.h 
functions, so the specifications are exactly the same, we
wrapped this functions with the API's ones to keep 
language consistency */

DragonP create_network (void);

int destroy_network (DragonP N);

int add_edge_to_network (DragonP N, u32 x, u32 y, u32 c);

int populate_network_from_stdin (DragonP N);

int find_shortest_length_augmenting_path (DragonP N);

int where_we_stand (DragonP N);

u32 increase_flow (DragonP N);

u32 increase_flow_and_print_path (DragonP N);

void print_flow (DragonP N);

void print_flow_value (DragonP N);

void print_cut (DragonP N);

u64 sum64 (u64 a, u32 b);

#endif /* NETWORK_H */
