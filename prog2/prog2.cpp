/*
For algorithms A* and RBFS 
    For each heuristic function h, 
        For at least 4 different sizes (number of disks)
            For each of the 20 problems p, 
                Solve p using h or until NMAX nodes are expanded. 
                Record the solution length if successful, the number of nodes 
                 expanded, and the total CPU time spent on evaluating
                 the heuristic and on solving the whole problem. 
*/

#include <iostream>
#include <vector>
#include <stack>
#include <cstdlib>
#include <algorithm>

using namespace std;

const bool A_STAR = true;
const bool RBFS = false;
const bool ADMISSIBLE = true;
const bool NONADMISSIBLE = false;
const int M = 3;
const int NODEMAX = 1000000;

void display(vector< string > p, bool fancy) {
    if(fancy) {
        int max_plates = 0;
        int i;
        for(i = 0; i < p.size(); ++i) {
            if(p[i].size() > max_plates)
                max_plates = p[i].size();
        }
        for(i = max_plates - 1; i >= 0; --i) {
            for(int ii = 0; ii < p.size(); ++ii) {
                if(p[ii].size() > i) {
                    for(int iii = atoi(&p[ii][p[ii].size()-1]); iii > 0; --iii)
                        cout << '-';
                    p[ii].erase(p[ii].size()-1, 1);
                }
                cout << "\t\t";
            }
        cout << endl;
        }
    }
    else {
        for(int i = 0; i < p.size(); ++i) {
            cout << p[i] << endl;
        }
        cout << endl;
    }
}

class Node {
    public:
        Node* parent;
        vector<string> state;
        int g;
        int f;

        Node() {}
        Node(Node* p, int m, string initial, int gcost, bool heuristic) {
            parent = p;
            state.resize(m);
            state[0] = initial;
            g = gcost;
            f = g + evaluate(heuristic);
        }

        bool operator<(Node &other) {
            return f > other.f;
        }

        //TODO 
        int evaluate(bool heuristic) {
            if(heuristic == ADMISSIBLE) {
                return 1;
            }
            else if(heuristic == NONADMISSIBLE) {
                return 1;
            }
        }
};

class Search {
    int n;
    bool heur;
    int expanded;

    public:
        Node astar(Node root) {
            vector<Node> frontier;
            vector< vector<string> > explored;
            frontier.push_back(root);
            Node cur;
            char c;
            vector<string> child;
            bool is_in_frontier_explored;
            while(1) {
                if(frontier.empty()) {
                    Node temp(NULL,0,"",0,0);
                    return temp;
                }
                pop_heap(frontier.begin(), frontier.end());
                cur = frontier[frontier.size()-1];
                frontier.pop_back();

                //DEBUG BEGIN
                expanded++;
                system("clear");
                display(cur.state, true);
                cout << " Nodes expanded: " << expanded << endl;
                char blah;
                cin >> blah;
                //DEBUG END

                if(goaltest(cur)) {
                    cout << endl << "SOLUTION FOUND" << endl << "Press enter to continue";
                    char blah;
                    cin >> blah;
                    return cur;
                }
                explored.push_back(cur.state);

                for(int i = 0; i < cur.state.size(); ++i) {
                    for(int ii = 0; ii < cur.state.size(); ++ii) {
                        if( (i != ii) && (!cur.state[i].empty()) ) {
                            Node child;
                            for(int iii = 0; iii < cur.state.size(); ++iii) {
                                child.state.push_back(cur.state[iii]);
                            }
                            child.parent = &cur;
                            child.g = cur.g + 1;
                            child.f = child.evaluate(heur) + child.g;

                            c = child.state[i][child.state[i].size()-1];
                            child.state[i].erase(child.state[i].size()-1,1);
                            child.state[ii].push_back(c);

                            is_in_frontier_explored = false;
                            for(int iii = 0; iii < frontier.size(); ++iii) {
                                if(equal(child.state.begin(),child.state.end(),frontier[iii].state.begin())) {
                                    is_in_frontier_explored = true;
                                    if(child.f < frontier[iii].f) {
                                        frontier[iii] = child;
                                    }
                                }
                            }
                            for(int iii = 0; iii < explored.size(); ++iii) {
                                if(equal(child.state.begin(),child.state.end(),explored[iii].begin()))  {
                                    is_in_frontier_explored = true;
                                    break;
                                }
                            }
                            if(!is_in_frontier_explored) {
                                frontier.push_back(child);
                            }
                        }
                    }
                }
            }
        }

        Node rbfs(Node node) {

        }

        Search(string initial, bool search, bool heuristic) {
            expanded = 0;
            n = initial.size();
            heur = heuristic;
            Node* root = new Node(NULL, M, initial, 0, heuristic);
            Node solution;

            if(search == A_STAR)
                solution = astar(*root); 
            else if(search == RBFS)
                solution = rbfs(*root);

            if(solution.state.empty()) {
                cout << endl << "FAILURE" << endl;
            }
            else {
                stack<Node*> solution_path;
                Node* cur = &solution;
                while(cur != NULL) {
                    system("clear");
                    display(cur->state, true);
                    char blah;
                    cin >> blah;
                    solution_path.push(cur);
                    cur = cur->parent;
                }
                while(!solution_path.empty()) {
                    //DEBUG BEGIN
                    system("clear");
                    //display(solution_path.top()->state, true);
                    solution_path.pop();
                    cout << endl << "Press enter to continue";
                    char blah;
                    cin >> blah;
                    //DEBUG END
                }
            }
        }
        bool goaltest(Node node) { 
            if(node.state[0].size() == n) {
                for(int i = 0; i < n; ++i) {
                    if(node.state[0][i]-48 != n-i) {
                        return false;
                    }
                }
                return true;
            }
            return false; 
        }
};

int main() {
    string test = "12";
    Search* a = new Search(test, A_STAR, ADMISSIBLE);
}
