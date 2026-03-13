#ifndef INFO_H
#define INFO_H

#include <stdio.h>
#include <string.h>
#include "vertex.h"
#include "structures.h"

/* Returns a new info structure */
info new_info (unsigned int size, vertex sink);

/* Destroy the info structure */
int info_destroy (info info);

/* Returns the cut */
vertex* cut (info info);

/* Returns the ancestors */
vertex* ancestors (info info);

/* Returns the fordward edge flags list */
bool* forward_edge (info info);

/* Returns the accumulated flow list */
u64* accumulated_flow (info info);

/* Returns the vertices count */
unsigned int vertices_count (info info);

/* Returns the max flow value */
u64 max_flow_value (info info);

/* Adds a vertex to the augmenting path */
void add_vertex_to_augmenting_path (info info, vertex vertex, int flag);

/* Reset the augmenting path  */
void reset_augmenting_path (info info);

/* Returns the capacity of the cut  */
u64 cut_capacity (info info);

#endif /* INFO_H */
