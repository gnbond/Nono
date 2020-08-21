#! /usr/bin/env python3

from nonogram import Game, Infeasible

import sys

def main():
    if len(sys.argv) != 2:
        print("usage: %s gamefile" % sys.argv[0], file=sys.stderr)
        sys.exit(1)

    g = Game.fromfile(sys.argv[1])
    
    for rc in g.rowscols:
        print(rc.name, rc.clue, ",", len(rc.possible), "possibles") 
    #print(g)
    g.solve()
       

if __name__ == "__main__":
    main()
