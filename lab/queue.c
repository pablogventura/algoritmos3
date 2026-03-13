#include "queue.h"

queue new_queue (void) {
  /* Returns a new queue to be used in BFS */
  queue new_queue = NULL;
  /* Allocates memory for the queue */
  new_queue = (queue) calloc (1, sizeof (struct queue_s));
  /* Check the calloc result to avoid errors */
  assert (new_queue != NULL);
  /* Initialize first, last and size of the queue */
  new_queue -> first = NULL;
  new_queue -> last = NULL;
  new_queue -> size = 0;
  return new_queue;
}

queue enqueue (queue queue, vertex vertex) {
  node new_node = NULL;
  assert (queue != NULL);
  assert (vertex != NULL);
  /* Allocates memory for the new node */
  new_node = (node) calloc (1, sizeof (struct node_s));
  /* Check the calloc result to avoid errors */
  assert (new_node != NULL);
  /* The vertex is stored into the new node, the next_vertex
  pointer is NULL because this is the last one */
  new_node -> vertex = vertex;
  new_node -> next_vertex = NULL;
  /* If the queue is empty the first element of the queue is new_node.
  If it is not empty, the next vertex field of the last node points to
  new_node, it means that the elements are added to the end of the queue */
  if (queue_is_empty (queue)) {
    queue -> first = new_node;
  } else {
    queue -> last -> next_vertex = new_node;
  }
  /* Now, new_node is the last element of the queue and the size of the
  queue is increased */
  queue -> last = new_node;
  queue -> size++;
  return queue;
}

vertex dequeue (queue queue) {
  node node = NULL;
  vertex vertex = NULL;
  /* Check if the queue is not NULL and if it is not empty */
  assert (queue != NULL);
  assert (!queue_is_empty (queue));
  /* We want to extract the vertex of the first node of the queue, so
  we have different references, both for the first node and its vertex
  to be able to destroy the node without loosing reference to its
  vertex */
  /* References the node */
  node = queue -> first;
  /* References its vertex */
  vertex = node -> vertex;
  /* The first element of the queue is now the second one and the size
  of the queue is decremented */
  queue -> first = queue -> first -> next_vertex;
  queue -> size--;
  /* Destroy the node */
  free (node);
  node = NULL;
  /* We use the reference to the vertex to be able to return it */
  return vertex;
}

bool queue_is_empty (queue queue) {
  /* Returns a boolean value indicating either if the queue
  is empty or not */
  assert (queue != NULL);
  /* To be empty is equivalent to have 0 elements */
  return (queue_size (queue) == 0);
}

unsigned int queue_size (queue queue) {
  /* Returns the size of the queue */
  assert (queue != NULL);
  return queue -> size;
}

int destroy_queue (queue queue) {
  /* Destroy the given queue */
  assert (queue != NULL);
  /* Destroy all elements of the queue */
  while (!queue_is_empty (queue)) dequeue (queue);
  /* Free the memory allocated for the queue */
  free (queue);
  queue = NULL;
  return 0;
}

vertex head (queue queue) {
  /* Return the first element of the queue */
  /* Check if the queue is not NULL and if it is not empty */
  assert (queue != NULL);
  assert (!queue_is_empty (queue));
  return queue -> first -> vertex;
}
