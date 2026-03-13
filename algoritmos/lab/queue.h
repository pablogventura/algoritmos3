#ifndef QUEUE_H
#define QUEUE_H

#include "structures.h"

/* We define the abstract data type Queue which
is a very powerful tool to implement the
Edmonds-Karp algorithm, as it is essential
to run BFS over the network. This is a
queue of vertices. */

/* Returns a new queue */
queue new_queue (void);

/* Enqueue a vertex */
queue enqueue (queue queue, vertex vertex);

/* Dequeue a vertex */
vertex dequeue (queue queue);

/* ¿Is the queue empty? */
bool queue_is_empty (queue queue);

/* Return the queue size */
unsigned int queue_size (queue queue);

/* Destroy the queue */
int destroy_queue (queue queue);

/* Return the head of the queue */
vertex head (queue queue);

#endif /* QUEUE_H */
