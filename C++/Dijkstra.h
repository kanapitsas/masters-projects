#include "DirectedGraph.h"
#include <vector>

// Runs a Dijkstra search on the graph, starting from node "src".
// See https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm .
// Returns the same "parent" vector as BFS() in 2.2.h.
std::vector<int> Dijkstra(DirectedGraph& graph, int src);

// Used in the priority queue. A pair of a node and a distance,
// with < redefined to have the node with the smallest distance
// at the top of the queue.
struct DistanceNode{
    DistanceNode(int node, double distance);
    bool operator<(const DistanceNode& other) const;

    int node;
    double distance;
};
