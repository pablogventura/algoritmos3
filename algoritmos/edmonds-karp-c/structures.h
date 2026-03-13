#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <stdlib.h>
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint64_t u64;
typedef uint32_t u32;

typedef struct edge_s *edge;
typedef struct vertex_s *vertex;
typedef struct node_s *node;
typedef struct queue_s *queue;
typedef struct info_s *info;
typedef struct NetworkYFlujo DragonSt;
typedef DragonSt *DragonP;

/* This is the abstraction of an edge. It contains a vertex x, vertex y,
the capacity of the edge and the flow of the edge. If the first parameter is
x and the second parameter is y then the direction of the edge is xy (->). */
struct edge_s {
  vertex x;
  vertex y;

  u32 capacity;
  u32 flow;
};

/* This is the vertex abstraction structure,
we are representing a vertex by an unsigned 32-bits integer,
in this structure we have the list of forward_edges (we can think about
this as the forward neighbours), and, in order to improve the computational
complexity of some functions we also have a field for the number of
forward edges, the same stands for backward edges (and backward
vertices). There is also a flag indicating either if the vertex has been added
to the current calculated cut or not */
struct vertex_s {
  u32 label;

  edge *forward_edges;
  unsigned int forward_edges_count;

  edge *backward_edges;
  unsigned int backward_edges_count;

  bool in_the_cut;
  unsigned int tag;
};

/* This is the abstraction of a Network. It contains a set (list or array in
this case) of vertices and a set of edges. It also
contains the number of vertices and the number of edges in the network, a reference
to the source, a reference to the sink and a info structure which stores information
of each step of the Edmonds-Karp algorithm. */
struct NetworkYFlujo {
  vertex *vertices;
  unsigned int vertices_count;

  edge *edges;
  unsigned int edges_count;

  vertex source;
  vertex sink;

  info info;
};

/* As we need to implement a Queue to run the Edmonds-Karp algorithm, we are
doing this as a linked list of nodes. Each node contains a vertex and a reference
to the next node of the queue. */
struct node_s {
  vertex vertex;
  node next_vertex;
};

/* This is the abstraction of Queue, we store a reference to the first element of the
Queue and a reference to the last element of the Queue. This is to enhance the computational
complexity of the functions provided by this abstract data type. It also stores the size of
the queue for the same reason, to run some functions in constant time. */
struct queue_s {
  node first;
  node last;
  unsigned int size;
};

/* This is a very important abstract data type that helps us to store information of how
the Edmonds-Karp algorithm is going on. It stores the cut, the array of vertices (ancestors),
an array of booleans to indicate if we reached the vertex through a forward edge or a
backward edge, the accumulated flow up to this point for each vertex, the number of
vertices inspected and the max flow value calculated. */
struct info_s {
  vertex *cut;
  vertex *ancestors;
  bool *forward_edge;
  u64 *accumulated_flow;
  unsigned int vertices_count;
  u64 max_flow_value;
  char *augmenting_path;
  bool is_maximal_flow;
  bool last_ecaml_reached_sink;
  bool last_ecaml_result_used;
  unsigned int augmenting_path_number;
};

#endif /* STRUCTURES_H */
