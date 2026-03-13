#include "vertex.h"

vertex new_vertex (u32 label, unsigned int tag) {
  /* Returns a new vertex */
  vertex new_vertex = NULL;
  /* Allocates memory for the new vertex */
  new_vertex = (vertex) calloc (1, sizeof (struct vertex_s));
  /* Check the result of the calloc to avoid errors */
  assert (new_vertex != NULL);
  /* Assigns the label */
  new_vertex -> label = label;
  /* Initialize the list of forward edges and the list of backward edges */
  new_vertex -> forward_edges = NULL;
  new_vertex -> backward_edges = NULL;
  /* Initialize forward edges count and backward edges count */
  new_vertex -> forward_edges_count = 0;
  new_vertex -> backward_edges_count = 0;
  /* Initially, the vertex is not in the cut */
  new_vertex -> in_the_cut = false;
  new_vertex -> tag = tag;
  return new_vertex;
}

int destroy_vertex (vertex vertex) {
  /* Precondition: the vertex is not null */
  assert (vertex != NULL);
  /* Free the memory of the array of forward edges */
  free (vertex -> forward_edges);
  vertex -> forward_edges = NULL;
  /* Free the memory of the array of backward edges */
  free (vertex -> backward_edges);
  vertex -> backward_edges = NULL;
  /* Free the memory allocated for the vertex structure */
  free (vertex);
  vertex = NULL;
  return 0;
}

u32 vertex_label (vertex vertex) {
  /* Returns the vertex label */
  assert (vertex != NULL);
  return vertex -> label;
}

bool vertices_are_equal (vertex x, vertex y) {
  /* Returns a bool indicating if the vertices are equal */
  assert (x != NULL);
  assert (y != NULL);
  return (vertex_label (x) == vertex_label (y));
}

int add_forward_edge_to_vertex (vertex vertex, edge edge) {
  /* Adds a forward edge to the vertex */
  assert (vertex != NULL);
  assert (edge != NULL);
  /* Increase forward edges count */
  vertex -> forward_edges_count++;
  /* Reallocates memory of forward_edges to be able to save the new edge */
  vertex -> forward_edges = realloc (forward_edges (vertex), forward_edges_count (vertex) * sizeof (edge));
  /* Assigns the edge to the last position of forward_edges */
  vertex -> forward_edges[forward_edges_count (vertex) - 1] = edge;
  return 0;
}

int add_backward_edge_to_vertex (vertex vertex, edge edge) {
  /* Add a backward edge to the vertex */
  assert (vertex != NULL);
  assert (edge != NULL);
  /* Increase backward edges count */
  vertex -> backward_edges_count++;
  /* Reallocates memory of backward_edges to be able to save the new edge */
  vertex -> backward_edges = realloc (backward_edges (vertex), backward_edges_count (vertex) * sizeof (edge));
  /* Assigns the edge to the last position of the backward_edges list */
  vertex -> backward_edges[backward_edges_count (vertex) - 1] = edge;
  return 0;
}

edge *forward_edges (vertex vertex) {
  /* Returns the forward edges list */
  assert (vertex != NULL);
  return vertex -> forward_edges;
}

edge *backward_edges (vertex vertex) {
  /* Returns the backward edges list */
  assert (vertex != NULL);
  return vertex -> backward_edges;
}

unsigned int forward_edges_count (vertex vertex) {
  /* Returns the forward edges list size */
  assert (vertex != NULL);
  return vertex -> forward_edges_count;
}

unsigned int backward_edges_count (vertex vertex) {
  /* Returns the backward edges list size */
  assert (vertex != NULL);
  return vertex -> backward_edges_count;
}
