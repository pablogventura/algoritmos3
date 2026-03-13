#ifndef VERTEX_H
#define VERTEX_H

#include "structures.h"

/* Create a new vertex */
vertex new_vertex (u32 label, unsigned int tag);

/* Destroy a vertex */
int destroy_vertex (vertex vertex);

/* Returns the label of the vertex */
u32 vertex_label (vertex vertex);

/* ¿Are the two vertices equal? */
bool vertices_are_equal (vertex x, vertex y);

/* Add an edge to the list of forward edges, ie: one vertex of the
edge is vertex and the other is a forward neighbour of vertex */
int add_forward_edge_to_vertex (vertex vertex, edge edge);

/* Add an edge to the list of backward edges, ie: one vertex of the
edge is vertex and the other is a backward neighbour of vertex */
int add_backward_edge_to_vertex (vertex vertex, edge edge);

/* Return the list of forward edges for this vertex */
edge* forward_edges (vertex vertex);

/* Return the list of backward edges for this vertex */
edge* backward_edges (vertex vertex);

/* Return the number of forward edges for this vertex */
unsigned int forward_edges_count (vertex vertex);

/* Return the number of backward edges for this vertex */
unsigned int backward_edges_count (vertex vertex);

#endif /* VERTEX_H */
