#include "info.h"

info new_info (unsigned int size, vertex sink) {
  /* Initialize info */
  info info = NULL;
  /* Allocates memory for the info structure */
  info = calloc (1, sizeof (struct info_s));
  assert (info != NULL);
  /* Allocates memory for the cut, ancestors, forward_edge (indicating either
  if we reached the vertex thorugh a forward edge or not),
  accumulated_flow and augmenting path */
  info -> cut = (vertex *) calloc (size, sizeof (vertex));
  info -> ancestors = (vertex *) calloc (size, sizeof (vertex));
  info -> forward_edge = (bool *) calloc (size, sizeof (bool));
  info -> accumulated_flow = (u64 *) calloc (size, sizeof (u64));
  info -> augmenting_path = (char *) calloc (1, sizeof (char));
  /* Initialization of other fields:
  max_flow_value: store the (max in some case) flow value.
  vertices_count: this is the maximum number of vertices that we could
  need to store within the structure, this is, there will be at most
  vertices_count vertices in the cut, ancestors, etc, we use this field
  to have an uppder bound of the amount of elements on each list,
  and iterate over them.
  is_maximal_flow: indicates either if the flow is maximal or not.
  last_ecaml_reached_sink: indicates if the last mininum length
  path reached the sink or not (in such case we have the cut).
  last_ecaml_result_used: indicates if the result of the last
  minimum length path has been used or not.
  augmenting_path_number: stores the number of the current
  augmenting path, increases progressively as a new path is
  calculated. */
  info -> max_flow_value = 0;
  info -> vertices_count = size;
  info -> is_maximal_flow = 0;
  info -> last_ecaml_reached_sink = 0;
  info -> last_ecaml_result_used = 0;
  info -> augmenting_path_number = 0;
  return info;
}

int info_destroy (info info) {
  /* Destroy the info */
  assert (info != NULL);
  /* Free the memory allocated for the cut */
  free (info -> cut);
  info -> cut = NULL;
  /* Free the memory allocated for the ancestors */
  free (info -> ancestors);
  info -> ancestors = NULL;
  /* Free the memory allocated for the forward_edge flags */
  free (info -> forward_edge);
  info -> forward_edge = NULL;
  /* Free the memory allocated for the accumulated_flow */
  free (info -> accumulated_flow);
  info -> accumulated_flow = NULL;
  /* Free the memory allocated for the augmenting_path */
  free (info -> augmenting_path);
  info -> augmenting_path = NULL;
  /* Free the memory allocated for the info structure */
  free (info);
  info = NULL;
  return 0;
}

vertex* cut (info info) {
  /* Returns the cut */
  assert (info != NULL);
  return info -> cut;
}

vertex* ancestors (info info) {
  /* Returns the ancestors */
  assert (info != NULL);
  return info -> ancestors;
}

bool* forward_edge (info info) {
  /* Returns the forward_edge list */
  assert (info != NULL);
  return info -> forward_edge;
}

u64* accumulated_flow (info info) {
  /* Returns the accumulated_flow list */
  assert (info != NULL);
  return info -> accumulated_flow;
}

unsigned int vertices_count (info info) {
  /* Returns the vertices count */
  assert (info != NULL);
  return info -> vertices_count;
}

u64 max_flow_value (info info) {
  /* Returns the max flow value */
  assert (info != NULL);
  return info -> max_flow_value;
}

void add_vertex_to_augmenting_path (info info, vertex vertex, int flag) {
  /* Adds the given vertex to the augmeting path checking the flag
  first, we assume, that all vertices have labels of size at most 42 */
  char buffer[42];
  assert (info != NULL);
  /* The flag is required as an argument to identify
  forward edges (0), backward edges (1), the sink (-1) or
  the source (2). The returned string have that format to comply
  with the statement required by the project. */
  if (flag == -1) {
    sprintf (buffer, "t");
  } else if (flag == 0) {
    sprintf (buffer, "%u:", vertex_label (vertex));
  } else if (flag == 1) {
    sprintf (buffer, "%u|", vertex_label (vertex));
  } else if (flag == 2) {
    sprintf (buffer, "s");
  }
  /* Reallocates memory to concatenate the augmenting path and the buffer */
  info -> augmenting_path = realloc (info -> augmenting_path, (strlen (info -> augmenting_path) + strlen (buffer) + 1) * sizeof (char));
  strncat (info -> augmenting_path, buffer, strlen (buffer));
}

void reset_augmenting_path (info info) {
  /* Destroy the current augmeting path */
  free (info -> augmenting_path);
  /* Allocates memory for the new augmenting path and initalize it */
  info -> augmenting_path = (char *) calloc (1, sizeof (char));
  info -> augmenting_path[0] = '\0';
}

u64 cut_capacity (info info) {
  /* Returns the cut capacity */
  assert (info != NULL);
  return info -> max_flow_value;
}
