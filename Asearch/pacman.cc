#include <iostream>
#include <vector>
#include <stack>
#include <set>
#include <sstream>

using namespace std;
/* Head ends here */
struct point{
    int x, y, d; //distance 'd' is not necessary, remove soon
    
    friend bool operator < (const point &p1 , const point &p){
        return (p1.x != p.x)? (p1.x < p.x) : (p1.y < p.y);
    }
    friend ostream& operator << (ostream& os, const point & p){
        os << p.x << ' ' << p.y << '\n' ;
        return os;    
    }
    point(int x1, int y1, int d1) : x(x1), y(y1), d(d1){
        //initialise point
    }
};


void dfs( int x, int y, int pacman_x, int pacman_y, int food_x, int food_y, vector <string> grid){
    //your logic here
    set<point> explored;
    stack<point> frontier;
    frontier.push(point(pacman_x, pacman_y, 0));
    ostringstream trace;
    stack<point> path;
    while(!frontier.empty()){
        const point p = frontier.top();
        //frontier.pop();
        pair<set<point>::iterator, bool> ret =  explored.insert(p);
        if(ret.second){
            trace << p;
            path.push(p);
        }
        else{
            frontier.pop();
            path.pop();
            continue;
        }
        //get the point in grid 
        const string &r = grid[p.x];
        //cout << r[p.y] << '\n';
        if (r[p.y] == '.'){
            break;
        }
        //cout << "p.x = " << p.x;
        if (p.x > 0){
            const string &u = grid[p.x -1];
            if(u[p.y] == '-'){
                point np(p.x - 1, p.y, p.d + 1);
                if(explored.find(np) == explored.end()){
                    //cout << "-- before , p = " << p ;
                    //cout << " u " << u[p.y] << ' ' << np; 
                    frontier.push(np);
                    //cout << "inside u , p " << p;
                }
            }
            else if(u[p.y] == '.'){
               point food(p.x -1 , p.y, p.d + 1);
               path.push(food);
               trace << food;

               break; 
            }
        }
        //cout << "p.x = " << p.x;
        //LEFT 
        if (p.y > 0 && r[p.y - 1] == '-'){
            point np(p.x , p.y -1 , p.d + 1);
            if (explored.find(np) == explored.end()){
                frontier.push(np);
            }
        }
        else if(p.y > 0 && r[p.y -1] == '.'){
            point food(p.x , p.y -1 , p.d + 1);
            path.push(food);
            trace << food;
            break;
        }
        //RIGHT
        if ( p.y < (r.size() - 1) && r[p.y + 1] == '-'){
            point np(p.x , p.y +1 , p.d + 1);
            if (explored.find(np) == explored.end()){
                frontier.push(np);
            }
        }
        else if  ( p.y < (r.size() - 1) && r[p.y + 1] == '.'){
            point food(p.x , p.y +1 , p.d + 1);
            path.push(food);
            trace << food;
            break;
        }

        if (p.x < (grid.size() - 1)){
            const string &d = grid[p.x + 1];
            if(d[p.y] == '-'){
                point np(p.x + 1, p.y, p.d + 1);
                if (explored.find(np) == explored.end()){
                    //cout << " d " << d[p.y] << ' ' << np;
                    frontier.push(np); 
                }
            }
            else if(d[p.y] == '.'){
                point food(p.x + 1, p.y, p.d + 1);
                trace << food;
                path.push(food);
                break;
            }
        }
       
    }
    cout << ( explored.size() + 1) << '\n';     
    cout << trace.str();    
    cout << (path.size() - 1) << '\n';
    stack<point> ps;
    for(; !path.empty(); path.pop()){
       ps.push(path.top());
    }
    for (;!ps.empty(); ps.pop()){
        cout << ps.top();
    }
}
/* Tail starts here */
int main(void) {
    int x,y, pacman_x, pacman_y, food_x, food_y;
    cin >> pacman_x >> pacman_y;
    cin >> food_x >> food_y;
    cin >> x >> y;
                            
    vector <string> grid;

    for(int i=0; i<x; i++) {
        string s; cin >> s;
        grid.push_back(s);
    }

    dfs( x, y, pacman_x, pacman_y, food_x, food_y, grid);

    return 0;
}
