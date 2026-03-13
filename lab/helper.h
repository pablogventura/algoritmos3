#ifndef HELPER_H
#define HELPER_H

#include <stdio.h>
#include "edge.h"
#include "queue.h"
#include "structures.h"
#include "network.h"
#include "API.h"

/* Returns the vertices count */
unsigned int network_vertices_count (DragonP N);

/* Returns the edges count */
unsigned int network_edges_count (DragonP N);

/* Returns the vertices list */
vertex *network_vertices (DragonP N);

/* Returns the edges list */
edge *network_edges (DragonP N);

/* Returns the info structure */
info network_info (DragonP N);

/* Returns the source */
vertex network_source (DragonP N);

/* Returns the sink  */
vertex network_sink (DragonP N);

/* Returns the position of the vertex in the network */
int vertex_position_in_network (DragonP N, u32 v);

/* Forward search */
void forward_search (vertex vertex, info info, queue queue);

/* Backward search */
void backward_search (vertex vertex, info info, queue queue);

/* Adds vertex to the network */
void add_vertex_to_network (DragonP N, vertex vertex);

/* Increases the max flow */
void increase_network_max_flow (DragonP N, u32 epsilon);

/* Prints the path */
void print_path (DragonP N, u32 epsilon);

#endif /* HELPER_H */
