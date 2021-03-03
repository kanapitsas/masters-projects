#include "Dijkstra.h"
#include <queue>
#include <limits>

DistanceNode::DistanceNode(int node, double distance): node(node), distance(distance) {};

bool DistanceNode::operator<(const DistanceNode& other) const {
    // The operator is inverted, so that the priority queue picks the *smallest*
    // element, instead of the biggest.
    return distance > other.distance;
}

std::vector<int> Dijkstra(DirectedGraph& graph, int src) {
    // Default value of -1 for parent means not reachable
    std::vector<int> parent(graph.NumNodes(), -1);
    parent[src] = src;

    // Distance of all the nodes from the source, default value of infinity,
    // except for the source.
    std::vector<double> distance(graph.NumNodes(), std::numeric_limits<double>::infinity());
    distance[src] = 0;

    // Will contain nodes which have to be discovered
    // The source is the first node to explore.
    std::priority_queue<DistanceNode> to_discover;
    to_discover.push(DistanceNode(src, 0));

    // To keep track of which nodes have already been discovered
    std::vector<bool> discovered(graph.NumNodes());

    while (!to_discover.empty()) {
        // We pop the next node to be discovered, which will be that with the
        // smallest distance.
        int current = to_discover.top().node;
        to_discover.pop();
        // If it's already been discovered, go to the next one.
        if (discovered[current]) {continue;}

        for (auto& e : graph.Neighbors(current)) {
            // We look at undiscovered neighbours of the current node
            int node = e.first;
            if (discovered[node]) {continue;}
            double length = e.second;
            if (distance[node] > distance[current] + length) {
                // If the new path is shorter, we update `distance`,
                // as well as `parent`.
                distance[node] = distance[current] + length;
                parent[node] = current;
            }

            // We can't check whether `node` is already in the priority queue, but
            // it doesn't matter : if there are duplicates, the version with
            // the smallest distance will be popped first. After that, it will be
            // discovered and not picked again.
            to_discover.push(DistanceNode(node, distance[node]));
        }
        discovered[current] = true;
    }
    return parent;
}
