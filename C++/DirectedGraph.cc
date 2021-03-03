#include "DirectedGraph.h"
#include <algorithm>
#include <iostream>

void DirectedGraph::AddArc(int from, int to, double length) {
    graph[from].push_back(std::pair<int, double>(to, length));

    // Vérification de la plus grande valeur utilisée
    // dans le graphe jusqu'à maintenant
    if (std::max(from, to) > max_node) {
        max_node = std::max(from, to);
    }
}

int DirectedGraph::NumNodes() const {
    // max_node correspond à l'index du summet le plus grand;
    // on doit rajouter 1 pour avoir le nombre de sommets.
    return max_node + 1;
}

int DirectedGraph::OutDegree(int node) const {
    try {return graph.at(node).size();}
    // cas où le sommet n'a pas encore été inséré
    // dans `graph`. Aucun voisin dans ce cas.
    catch (std::out_of_range) {return 0;}

}

const std::vector<std::pair<int, double>>& DirectedGraph::Neighbors(int node) {
    return graph[node];
}
