// Generic cardinality counter for hashable objects.
// It counts how many times a given object was inserted, all
// in constant time.
#include <iostream>
#include <unordered_map>
#include <unordered_set>

template<class T>
class CardinalityCounter {
   public:
    // Adds an object once, i.e. increments its cardinality count.
    void Add(const T& t) {
        int new_value = UpdateElement(t, 1); 

        if (new_value > most_frequent_value) {
            most_frequent_value = new_value;
        }
    }

    void Remove(const T& t) {
        // Si `t` n'est pas dans la map, on ne fait rien
        if (object_map.find(t) == object_map.end()) {return;}

        // S'il y est, on décrémente la valeur correspondante
        int new_value = UpdateElement(t, -1);

        // Dans le cas où c'était la valeur la plus fréquente, il faut
        // vérifier si elle le reste ou non.
        if (   new_value + 1 == most_frequent_value 
            && value_map[most_frequent_value].size() == 0) {

            most_frequent_value = new_value;
        }
        
        // Si une valeur arrive à 0, il faut la supprimer.
        if (new_value == 0) {
            DeleteElement(t);
        }
    }

    // Returns the current cardinality count of object t, i.e. the number of
    // times Add(t) was called. Can be 0 if t was never added.
    int NumOccurences(const T& t) const {
        try {return object_map.at(t);}
        catch(...) {return 0;}
    }

    int Size() const{
        return object_map.size();
    }

    // Retourne un des éléments les plus fréquents.
    const T& MostFrequent() const{
        return *(value_map.at(most_frequent_value).begin());
    }


   private:

    // Affiche le contenu de object_map (debug).
    void Print() const {
        std::cout << "-----------------" << std::endl;
        for (const auto& e : object_map) {
            std::cout << e.first << " : " << e.second << std::endl;
        }
    }

    // Met à jours les deux maps pour un changement delta du nombre
    // d'occurence (en pratique ici, toujours +1 ou -1).
    // Retourne le nouveau nombre d'occurence.
    int UpdateElement(const T& t, int delta) {
        int& value = object_map[t];
        value_map[value].erase(t);
        value += delta;
        value_map[value].insert(t);

        return value;
    } 

    // Suprimme l'élément t des deux maps.
    // Suppose que t a un nombre d'occurence égale à 0 !
    void DeleteElement(const T& t) {
        object_map.erase(t);
        value_map[0].erase(t);
    }

    // ---- Attributs ---- 
    // Clé : les objets de type T. Valeur : nombre d'occurence (int).
    std::unordered_map<T, int> object_map;

    // Clé : le nombre d'occurence (int). Valeur : un ensemble d'éléments
    // de type T, qui correspondent à ce nombre d'occurence.
    std::unordered_map<int, std::unordered_set<T> > value_map;

    // Nombre d'occurences de l'élément le plus fréquent.
    int most_frequent_value = 0;
    // (on a plus besoin de stocker l'élément auquel il correspond,
    // grace à value_map)
 };
