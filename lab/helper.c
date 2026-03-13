#define MIN(a, b) (((a) < (b)) ? (a) : (b))

#include "helper.h"

unsigned int network_vertices_count (DragonP N) {
  /* Returns vertices count */
  assert (N != NULL);
  return N -> vertices_count;
}

unsigned int network_edges_count (DragonP N) {
  /* Returns edges count */
  assert (N != NULL);
  return N -> edges_count;
}

vertex *network_vertices (DragonP N) {
  /* Returns vertices */
  assert (N != NULL);
  return N -> vertices;
}

edge *network_edges (DragonP N) {
  /* Returns edges */
  assert (N != NULL);
  return N -> edges;
}

info network_info (DragonP N) {
  /* Returns info */
  assert (N != NULL);
  return N -> info;
}

vertex network_source (DragonP N) {
  /* Returns the source */
  assert (N != NULL);
  return N -> source;
}

vertex network_sink (DragonP N) {
  /* Returns the sink */
  assert (N != NULL);
  return N -> sink;
}

int vertex_position_in_network (DragonP N, u32 v) {
  /* Found indicates if the vertex is in the network, pos indicates the
  position of the vertex in the network and aux is used in the
  comparation */
  bool found = false;
  unsigned int pos = 0;
  vertex vertex_aux = NULL;
  assert (N != NULL);
  /* Initialize the aux vertex */
  vertex_aux = new_vertex (v, 0);
  assert (vertex_aux != NULL);
  /* Search the vertex position in the network */
  while (pos < network_vertices_count (N) && !found) {
    found = vertices_are_equal (vertex_aux, network_vertices (N)[pos]);
    if (!found) pos++;
  }
  /* If the vertex is not in the network then return -1 */
  if (!found) pos = -1;
  /* Destroy the aux vertex */
  destroy_vertex (vertex_aux);
  return pos;
}

void forward_search (vertex vertex, info info, queue queue) {
  u32 position = 0;
  unsigned int i = 0;
  edge pivote = NULL;
  /* Checking precoditions */
  assert (info != NULL);
  assert (queue != NULL);
  assert (vertex != NULL);
  /* Checks each forward neighbour of the vertex */
  for (i = 0; i < forward_edges_count (vertex); i++) {
    /* Picks a forward edge (the origin vertex is vertex) */
    pivote = forward_edges (vertex)[i];
    /* If the flow in the pivot is less than the capacity and the
       vertex is not in the cut */
    if (edge_flow (pivote) < edge_capacity (pivote) && !(second_vertex(pivote) -> in_the_cut)) {
      /* Enqueue the pivot */
      enqueue (queue, second_vertex (pivote));
      position = second_vertex (pivote) -> tag;
      /* Adds the y vertex to the cut */
      cut (info)[position] = second_vertex (pivote);
      /* Adds the given vertex to the ancestors */
      ancestors (info)[position] = vertex;
      /* Set the forward_edge in true because is forward */
      forward_edge (info)[position] = true;
      /* The accumulated flow is set with the minimum between the
      accumulated flow in the vertex and the substracion between
      the capacity and the flow of the pivot */
      accumulated_flow (info)[position] = MIN (accumulated_flow (info)[vertex -> tag], edge_capacity (pivote) - edge_flow (pivote));
      /* This vertex is now in the cut */
      second_vertex (pivote) -> in_the_cut = true;
    }
  }
}

void backward_search (vertex vertex, info info, queue queue) {
  u32 position = 0;
  unsigned int i = 0;
  edge pivote = NULL;
  /* Checking precoditions */
  assert (info != NULL);
  assert (queue != NULL);
  assert (vertex != NULL);
  /* Checks each backward neighbour of the vertex */
  for (i = 0; i < backward_edges_count (vertex); i++) {
    pivote = backward_edges (vertex)[i];
    /* If the flow in the pivot greater than 0 and the vertex is not in the cut */
    if (edge_flow (pivote) > 0 && !(first_vertex (pivote) -> in_the_cut)) {
      /* Enqueue the pivot */
      enqueue (queue, first_vertex (pivote));
      position = first_vertex (pivote) -> tag;
      /* Adds the x vertex to the cut */
      cut (info)[position] = first_vertex (pivote);
      /* Adds the given vertex to the ancestors */
      ancestors (info)[position] = vertex;
      /* Set the forward_edge in false because is backward */
      forward_edge (info)[position] = false;
      /* The accumulated flow is set with the minimum between the
      accumulated flow in the vertex and the flow in the pivot */
      accumulated_flow (info)[position] = MIN (accumulated_flow (info)[vertex -> tag], edge_flow (pivote));
      /* This vertex is now in the cut */
      first_vertex (pivote) -> in_the_cut = true;
    }
  }
}

void add_vertex_to_network (DragonP N, vertex vertex) {
  /* Check preconditions */
  assert (N != NULL);
  assert (vertex != NULL);
  /* Increase vertices count */
  N -> vertices_count += 1;
  /* Reallocates memory to be able to save the vertex in the vertices list */
  N -> vertices = realloc (N -> vertices, N -> vertices_count * sizeof (vertex));
  /* Adds the given vertex into the last position of the vertices list */
  N -> vertices[N -> vertices_count - 1] = vertex;
}

void increase_network_max_flow (DragonP N, u32 epsilon) {
  /* Increase the value of the max flow field */
  assert (N != NULL);
  network_info (N) -> max_flow_value = Sumar64 (network_info (N) -> max_flow_value, epsilon);
}

void print_path (DragonP N, u32 epsilon) {
  network_info (N) -> augmenting_path[0] = 't';
  /* Prints the path */
  printf ("Camino Aumentante %u:\n%s: %u\n", network_info (N) -> augmenting_path_number, network_info (N) -> augmenting_path, epsilon);
}
