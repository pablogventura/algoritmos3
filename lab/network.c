#include "network.h"

DragonP create_network (void) {
  /* nuevo dragon will be the new DragonP structure */
  DragonP nuevo_dragon = NULL;
  /* Allocates memory for the new structure */
  nuevo_dragon = (DragonP) calloc (1, sizeof (DragonSt));
  /* ERROR: if nuevo_dragon is null then there was an error
  allocating memory and null will be returned, so we assigns
  the nuevo_dragon fields only if the result of calloc was
  not null (successful) */
  if (nuevo_dragon != NULL) {
    /* At the beginning, the number of vertices and edges
    in the network is 0 */
    nuevo_dragon -> edges_count = 0;
    nuevo_dragon -> vertices_count = 0;
  }
  return nuevo_dragon;
}

int destroy_network (DragonP N) {
  unsigned int i = 0;
  /* ERROR: destroy a network that is null */
  if (N == NULL) return 0;
  /* Destroy each vertex in the network */
  for (i = 0; i < network_vertices_count (N); i++) destroy_vertex (network_vertices (N)[i]);
  /* Destroy each edge in the network */
  for (i = 0; i < network_edges_count (N); i++) destroy_edge (network_edges (N)[i]);
  /* Destroy the info data structure in the network, see
  the structure info_s in structures.h */
  info_destroy (network_info (N));
  /* Free the memory allocated for the array of vertices */
  free (N -> vertices);
  /* Free the memory allocated for the array of edges */
  free (N -> edges);
  /* Free the memory allocated for the network structure */
  free (N);
  return 1;
}

int add_edge_to_network (DragonP N, u32 x, u32 y, u32 c) {
  /* x_pos will be used to store the position of the vertex x in the network
  if it is already there, the same stands for y_pos. By position we mean
  the index in the array of vertices in the network structure. If a
  vertex can't be found, then a new vertex will be created and stored in the
  array of vertices of the network, that will be x_aux & y_aux. Edge will
  be the new edge */
  int x_pos = 0, y_pos = 0;
  vertex x_aux = NULL, y_aux = NULL;
  edge edge = NULL;
  /* ERROR: can't add an edge to a NULL network */
  if (N == NULL) return 0;
  /* Find the position (index) of the vertex with label x in the array of vertices
  of the network structure, returns -1 if such a vertex was not found */
  x_pos = vertex_position_in_network (N, x);
  /* x was not found */
  if (x_pos == -1) {
    /* if vertex x was not in the network, then we create a new one */
    x_aux = new_vertex (x, N -> vertices_count);
    /* add the new vertex to the array of vertices of the network */
    add_vertex_to_network (N, x_aux);
  } else {
    /* if a vertex with label x was found, then we search this vertex in the vertices
    array of the network structure */
    x_aux = N -> vertices[x_pos];
  }
  /* Find the position (index) of the vertex with label y in the array of vertices
  of the network structure, returns -1 if such a vertex was not found */
  y_pos = vertex_position_in_network (N, y);
  /* y was not found */
  if (y_pos == -1) {
    /* if vertex y was not in the network, the we create a new one */
    y_aux = new_vertex(y, N -> vertices_count);
    /* add the new vertex to the array of vertices of the network */
    add_vertex_to_network (N, y_aux);
  } else {
    /* if a vertex with label y was found, then we search this vertex in the vertices
    array of the network structure */
    y_aux = N -> vertices[y_pos];
  }
  /* ERROR: x or y vertex neither was found nor was created */
  if (x_aux == NULL || y_aux == NULL) return 0;
  /* Once we have found or created the two vertices in the network, we can
  create a new edge, with capacity c and flow 0 */
  edge = new_edge(x_aux, y_aux, c, 0);
  /* ERROR: the new edge could not be created */
  if (edge == NULL) return 0;
  /* Add this new edge to the list of forward edges of the vertex x, see the definition
  of the vertex structure in structures.h */
  add_forward_edge_to_vertex (x_aux, edge);
  /* Add this new edge to the list of backward edges of the vertex y, see the definition
  of the vertex structure in structures.h */
  add_backward_edge_to_vertex (y_aux, edge);
  /* We created and introduced a new edge to the network, so we increment the number
  of edges in the network and stores it */
  N -> edges_count += 1;
  N -> edges = realloc (N -> edges, N -> edges_count * sizeof (edge));
  N -> edges[N -> edges_count - 1] = edge;
  /* If we reached this point, then the execution was successful and returns 1 */
  return 1;
}

int populate_network_from_stdin (DragonP N) {
  /* x, y, c will be the info parsed from the line,
  x & y will be the vertices of the new edge and c
  its capacity */
  u32 x, y, c = 0;
  /* ERROR: populate from stding a null network */
  if (N == NULL) return 0;
  /* While it is possible to read a line with three values then
  parse the line and add and edge to the network. Note: scanf with
  such format string avoids blank spaces, tabs, etc, so it doens't
  matter how the three values are in the line. Scanf return the
  number of input items successfully matched and assigned, so it
  will keep parsing while it reads three items */
  while (scanf ("%u %u %u", &x , &y, &c) == 3) CargarUnLado (N, x, y, c);
  /* Once we've added all the new vertices, then we set the source
  & sink of the network as the vertex with label 0 & 1 respectively,
  and we can create the info structure (see structures.h, info_s)
  because we need to know the number of vertices in the network to
  create this structure */
  N -> source = N -> vertices[vertex_position_in_network (N, 0)];
  N -> sink = N -> vertices[vertex_position_in_network (N, 1)];
  N -> info = new_info (N -> vertices_count, network_sink (N));
  /* If we reached this point is because the execution was
  successful */
  return 1;
}

int find_shortest_length_augmenting_path (DragonP N) {
  /* To run the Edmonds-Karp algorithm we need to calculate BFS(s)
  so we need a queue, a vertex to pivote over the Network (we calculate
  forward and backward neighbours of this pivote and see which of them
  can be in a potential augmenting path) */
  int result = 0;
  unsigned int i = 0;
  queue queue = NULL;
  vertex pivote = NULL;
  /* We create a new queue and enqueue the source, as we need to find
  a shortest length augmenting path from s to t, we calculate BFS(s),
  that's why the first element on the queue is s. */
  queue = new_queue ();
  /* ERROR: if queue is null there was an error creating the queue */
  if (queue == NULL) return -1;
  queue = enqueue (queue, network_source (N));
  /* The first element of the potential cut is the source */
  cut (network_info (N))[0] = network_source (N);
  /* To store the potential cut we use a static allocated array, so we initialize
  all its entries as NULL (we don't know which vertices will be there) */
  for (i = 1; i < vertices_count (network_info (N)); i++) cut (network_info (N))[i] = NULL;
  for (i = 0; i < N -> vertices_count; i++) N -> vertices[i] -> in_the_cut = false;
  /* As before, we initialize the accumulated flow as the maximum value of the type
  (by this we mean infinite, as this is the neutral element of the min function), this
  for each entry of the static allocated array of acummulated flows */
  for (i = 0; i < vertices_count (network_info (N)); i++) accumulated_flow (network_info (N))[i] = UINT64_MAX;
  /* If the queue is empty there are no more vertices to inspect, by the other hand if we
  are going to inspect the sink is because we already have an augmenting path */
  while (!queue_is_empty (queue) && !vertices_are_equal (head (queue), network_sink (N))) {
    /* Pick an element to inspect */
    pivote = head (queue);
    /* Look up its forward neighbours */
    forward_search (pivote, network_info (N), queue);
    /* Look up its backward neighbours */
    backward_search (pivote, network_info (N), queue);
    /* Dequeue the inspected element */
    dequeue (queue);
  }
  /* Free the memory allocated */
  destroy_queue (queue);
  if (network_sink (N) -> in_the_cut) {
    /* Indicates that the last ecaml search reached sink and return 1 */
    result = 1;
    network_info (N) -> last_ecaml_reached_sink = 1;
    network_info (N) -> augmenting_path_number++;
  } else {
    /* Indicates that the last ecaml search didn't reach sink and return 0 */
    result = 0;
    network_info (N) -> last_ecaml_reached_sink = 0;
    /* If the last ecaml search didn't reached the sink is because we actually
    have a cut, it means that the accumulated flow we have in N (max_flow_value field)
    is a maximal_flow_value */
    network_info (N) -> is_maximal_flow = 1;
  }
  /* As the last ecaml result was just calculated, it has not
  been used yet */
  network_info (N) -> last_ecaml_result_used = 0;
  return result;
}

int where_we_stand (DragonP N) {
  int result = 0;
  info info = NULL;
  /* Extract info data structure inside network */
  info = network_info (N);
  /* Calculate result value according requirements */
  result = 100 * (info -> is_maximal_flow) + 10 * (info -> last_ecaml_reached_sink) + (info -> last_ecaml_result_used);
  return result;
}

u32 increase_flow (DragonP N) {
  unsigned int i = 0, where_we_stand = 0;
  u32 epsilon = 0;
  vertex q = NULL;
  vertex pivote = NULL;
  edge edge_pivote = NULL;
  /* We will create a new augmenting path, so destroy the older one */
  reset_augmenting_path(network_info (N));
  /* At first we check where we stand */
  where_we_stand = DondeEstamosParados (N);
  /* ERROR: to go on with this function, we require that an ecaml
  search have been done but it haven't been used to update the flow yet,
  and that the flow_value stored in N is not maximal */
  if (where_we_stand != 10) return 0;
  /* We start from t (the network sink) */
  pivote = network_sink (N);
  /* How much will be the flow value increased? */
  epsilon = accumulated_flow (network_info (N))[N -> sink -> tag];
  /* Actually increase the flow value */
  increase_network_max_flow (N, epsilon);
  /* We calculate while we don't reach the source, in case
  we reach the source we are done */
  while (!vertices_are_equal (pivote, network_source (N))) {
    /* Pick the ancestor of the pivote p, let this ancestor be q, then
    we can determine if qp is a forward or backward edge */
    q = ancestors (network_info (N))[pivote -> tag];
    /* If the edge is forward (look up this in the info data structure) */
    if (forward_edge (network_info (N))[pivote -> tag]) {
      /* If qp is a forward edge is because q is a backward neighbour of p, hence
      we search into the backward edges of p one such that the other vertex is q */
      for (i = 0; i < backward_edges_count (pivote); i++) {
        /* Pick the current edge to inspect */
        edge_pivote = backward_edges (pivote)[i];
        /* Check if the other vertex is q */
        if (vertices_are_equal (first_vertex (edge_pivote), q)) {
          /* In this case we found the edge qp (->), so increase
          the flow in this edge */
          increase_edge_flow (edge_pivote, epsilon);
        }
      }
      /* Add this new vertex to the augmenting path, 0 means
      we add a forward edge */
      add_vertex_to_augmenting_path (network_info (N), pivote, 0);
    /* If the edge is backward */
    } else {
      /* If qp is a backward edge is because q is a forward neighbour of p, hence
      we search into the forward edges of p one such that the other vertex is q */
      for (i = 0; i < forward_edges_count (pivote); i++) {
        /* Pick the current edge to inspect */
        edge_pivote = forward_edges (pivote)[i];
        /* Check if the other vertex is q */
        if (vertices_are_equal (second_vertex (edge_pivote), q)) {
          /* In this case we found the edge qp (<-), so decrease
          the flow in this edge */
          decrease_edge_flow (edge_pivote, epsilon);
        }
      }
      /* Add this new vertex to the augmenting path, 1 means
      we add a backward edge */
      add_vertex_to_augmenting_path (network_info (N), pivote, 1);
    }
    /* The new pivote is the ancestor of the old one */
    pivote = q;
  }
  /* Add the source to the augmenting path */
  add_vertex_to_augmenting_path (network_info (N), N -> source, 2);
  return epsilon;
}

u32 increase_flow_and_print_path (DragonP N) {
  u32 result = 0;
  result = AumentarFlujo (N);
  if (result != 0) print_path (N, result);
  return result;
}

void print_flow (DragonP N) {
  edge pivote = NULL;
  unsigned int i = 0;
  printf ("Flujo");
  /* We print maximal if and only if the value of
  the flow is maximal, this is indicated by a flag in the
  info data structure */
  if (network_info (N) -> is_maximal_flow) printf (" maximal");
  printf (":\n");
  for (i = 0; i < network_edges_count (N); i++) {
    pivote = network_edges (N)[i];
    printf ("Lado %u, %u: %u\n", vertex_label (first_vertex (pivote)), vertex_label (second_vertex (pivote)), edge_flow (pivote));
  }
  printf ("\n\n");
}

void print_flow_value (DragonP N) {
  assert (N != NULL);
  printf ("Valor del flujo");
  /* We print maximal if and only if the value of
  the flow is maximal, this is indicated by a flag in the
  info data structure */
  if (network_info (N) -> is_maximal_flow) printf (" maximal");
  /* Print the flow value */
  printf (": %lu\n", network_info (N) -> max_flow_value);
  printf ("\n\n");
}


void print_cut (DragonP N) {
  unsigned int i = 0;
  printf ("Corte Minimal: S = {");
  printf ("s");
  for (i = 1; i < network_vertices_count (N); i++) {
    if (network_info (N) -> cut[i] != NULL) {
      printf (", %u", vertex_label (network_info (N) -> cut[i]));
    }
  }
  printf ("}\n");
  printf ("Capacidad: %lu\n\n", cut_capacity (network_info (N)));
}

u64 sum64 (u64 a, u32 b) {
  return (u64) a + (u64) b;
}
