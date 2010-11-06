import os

class Board:
    b = list()

    def __init__(self, board):
        self.b = board

    def display(self):
        print '   a b c   d e f   g h i'
        for i in range(3):
            for j in range(3):
                print '%s ' % (i*3+j+1),
                for k in range(3):
                    for l in range(3):
                        print self.b[i*3+j][k*3+l],
                    if k != 2:
                        print '|',
                print
            if i != 2:
                print '------------------------'

    def get_domain(self, r, c):
        result = [str(i) for i in range(1,10)]
        result = [i for i in result if i not in [self.b[j][c] for j in range(0,9)]]
        result = [i for i in result if i not in [self.b[r][j] for j in range(0,9)]]
        return result

    def apply_rule1(self):
        pass

    def apply_rule2(self):
        pass

    def apply_naked_triples(self):
        pass
        

repo = open('repository.txt','r').readlines()
difficulties = [repo[line_num].split()[1].lower() for line_num in range(len(repo)) if line_num % 11 == 0]
repo = [[i for i in line.replace('0','-') if not i in (' ','\n')] for line in repo]
sudokus = [repo[i*11+1:i*11+10] for i in range(len(repo)/11)]
sudoku = Board(sudokus[0])
sudoku.display()
print sudoku.get_domain(0,0)
