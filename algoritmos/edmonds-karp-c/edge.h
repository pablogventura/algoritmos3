#ifndef EDGE_H
#define EDGE_H

#include "vertex.h"

/* Creates a new Edge */
edge new_edge (vertex x, vertex y, u32 capacity, u32 flow);

/* Destroy an Edge */
int destroy_edge (edge edge);

/* Returns the flow value of the edge */
u32 edge_flow (edge edge);

/* Returns the capacity value of the edge */
u32 edge_capacity (edge edge);

/* Returns the first vertex of the edge */
vertex first_vertex (edge edge);

/* Returns the second vertex of the edge */
vertex second_vertex (edge edge);

/* Increase the edge flow by epsilon */
void increase_edge_flow (edge edge, u32 epsilon);

/* Decrease the edge flow by epsilon */
void decrease_edge_flow (edge edge, u32 epsilon);

#endif /* EDGE_H */
