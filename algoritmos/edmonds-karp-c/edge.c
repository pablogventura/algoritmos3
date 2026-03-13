#include "edge.h"

edge new_edge (vertex x, vertex y, u32 capacity, u32 flow) {
  /* Returns a new edge xy (->) with capacity and flow */
  edge new_edge = NULL;
  /* Allocates memory for the new edge */
  new_edge = (edge) calloc (1, sizeof (struct edge_s));
  /* Check the calloc result to avoid errors */
  assert (new_edge != NULL);
  /* Assigns the vertices */
  new_edge -> x = x;
  new_edge -> y = y;
  /* Assigns flow and capacity */
  new_edge -> flow = flow;
  new_edge -> capacity = capacity;
  /* Returns the new edge */
  return new_edge;
}

int destroy_edge (edge edge){
  /* Destroy the edge */
  assert (edge != NULL);
  free (edge);
  edge = NULL;
  return 0;
}

u32 edge_flow (edge edge) {
  /* Returns the edge flow */
  assert (edge != NULL);
  return edge -> flow;
}

u32 edge_capacity (edge edge) {
  /* Returns the edge capacity */
  assert (edge != NULL);
  return edge -> capacity;
}

vertex first_vertex (edge edge) {
  /* Returns the first vertex of the edge */
  assert (edge != NULL);
  return edge -> x;
}

vertex second_vertex (edge edge) {
  /* Returns the second vertex of the edge */
  assert (edge != NULL);
  return edge -> y;
}

void increase_edge_flow (edge edge, u32 epsilon) {
  /* Increase the edge flow by epsilon */
  assert (edge != NULL);
  edge -> flow += epsilon;
}

void decrease_edge_flow (edge edge, u32 epsilon) {
  /* Decrease the edge flow by epsilon */
  assert (edge != NULL);
  edge -> flow -= epsilon;
}
