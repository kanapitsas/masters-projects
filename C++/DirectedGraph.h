#pragma once
#include <unordered_set>
#include <unordered_map>
#include <vector>

class DirectedGraph {
 public:
  void AddArc(int from, int to, double length);

  // Returns 1 + the highest node index that was ever given to AddArc(), as
  // 'from' or 'to' argument.
  int NumNodes() const;

  // Returns the number of arcs originating from "node".
  // In the example above, OutDegree(1) = 3, OutDegree(4) = 0.
  int OutDegree(int node) const;

  // Returns all the destination nodes that were added with arcs
  // originating from "node".
  // In the example above, Neighbors(1) is {0, 2, 3} and Neighbors(2) is {0}.
  const std::vector<std::pair<int, double>>& Neighbors(int node);

 private:
  // J'utilise une `unordered_map` qui associe à chaque entier correspondant
  // à un sommet un `vector` qui contient les pairs sommet / longueur de ses
  // voisins.
  std::unordered_map<int, std::vector<std::pair<int, double>>> graph; 

  // Valeur du plus grand sommet utilisé. J'utilise la valeur -1 pour un
  // graphe vide.
  int max_node = -1;
};
