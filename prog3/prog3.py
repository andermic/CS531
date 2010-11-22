from os import system # For clearing the screen
from itertools import product # product() takes the cartesian product of two lists
from copy import deepcopy # deepcopy() returns a deepcopy of an object

class Board:
    b = list()
    most_constrained = bool()
    nakes_triples = bool()
    no_calls = int()

    def __init__(self, board, naked, mc):
        self.b = board
        self.naked_triples = naked
        self.most_constrained = mc
        no_calls = 0

    def display(self):
        #system('clear')
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

    # Calculate the domain of cell with row r and column c, by subtracting
    #  already assigned values in the same row, column, and box.
    def get_domain(self, r, c):
        # If the cell is already assigned, return the value assigned as the
        #  only value in that cell's domain.
        if self.b[r][c] != '-':
            return [self.b[r][c]]

        # Domain initially contains all digits 1-9
        result = [str(i) for i in range(1,10)]

        # Filter out values in the same row
        result = [i for i in result if i not in [self.b[r][j] for j in range(9)]]

        # Filter out values in the same column
        result = [i for i in result if i not in [self.b[j][c] for j in range(9)]]

        # Filter out values in the same box
        box_rows = range(r/3*3,(r/3+1)*3)
        box_cols = range(c/3*3,(c/3+1)*3)
        result = [i for i in result if i not in [self.b[j][k] for j,k in product(box_rows,box_cols)]]

        return result

    def get_domains(self):
        domains = []
        for i in range(9):
            domains.append([])
            for j in range(9):
                domain = self.get_domain(i,j)
                if domain == []:
                    return False
                else:
                    domains[i].append(domain)
        return domains

    def apply_rule1(self):
        # Calculate the domains of empty cells using get_domain(),
        #  which applies the row, column, and box constraints. When a cell has
        #  only one value in its domain, assign the cell that value. If after
        #  an iteration no assignments occur, then this technique has done all
        #  it can do, and so return. If a cell ever has an empty domain, return
        #  failure.
        keep_going = True
        inferences = []
        while(keep_going):
            keep_going = False
            domains = self.get_domains()
            if domains == False:
                return [False] + inferences
            if self.naked_triples:
                domains = self.apply_naked_triples(domains)
            for i in range(9):
                for j in range(9):
                    if self.b[i][j] == '-':
                        if len(domains[i][j]) == 1:
                            self.b[i][j] = domains[i][j][0]
                            inferences.append([i,j])
                            keep_going = True
        return [True] + inferences

    def apply_rule2(self):
        # Calculate the domain of all empty cells using get_domain(). If a
        #  value is only in the domain of one cell within a row, column, or
        #  box, assign that value to that cell. Return after no assignments
        #  are made, and return failure if an empty domain is found, as in
        #  apply_rule1().

        # For every row, column, and box, see if there are values in the domain
        #  of one cell that are not in the domains of other cells in that row,
        #  column, or box.
        keep_going = True
        inferences = []
        # Get the initial domain of every cell. Return failure if any are
        #  empty.
        domains = self.get_domains()
        if domains == False:
            return [False] + inferences

        if self.naked_triples:
            domains = self.apply_naked_triples(domains)

        for i in range(1,10):
            si = str(i)
            for j in range(9):
                # Check for single domain instance of i in rows
                row_doms = [domains[j][c] for c in range(9) if len(domains[j][c]) != 1]
                if row_doms == []:
                    continue
                count = reduce(lambda x,y: x+y, row_doms).count(si)
                if count == 1:
                    for c in range(9):
                        if si in domains[j][c]:
                            self.b[j][c] = si
                            inferences.append([j,c])
                            keep_going = True
                            break
            for j in range(9):
                # "                                   " in columns
                col_doms = [domains[r][j] for r in range(9) if len(domains[r][j]) != 1]
                if col_doms == []:
                    continue
                count = reduce(lambda x,y: x+y, col_doms).count(si)
                if count == 1:
                    for r in range(9):
                        if si in domains[r][j]:
                            self.b[r][j] = si
                            inferences.append([r,j])
                            keep_going = True
                            break
            for j,k in product(range(3),range(3)):
                # "                                   " in boxes
                box_rows = range(j*3,(j+1)*3)
                box_cols = range(k*3,(k+1)*3)
                box_doms = [domains[l][m] for l,m in product(box_rows,box_cols) if len(domains[l][m]) != 1]
                if box_doms == []:
                    continue
                count = reduce(lambda x,y: x+y, box_doms).count(si)
                if count == 1:
                    for l,m in product(box_rows,box_cols):
                        if si in domains[l][m]:
                            self.b[l][m] = si
                            inferences.append([l,m])
                            keep_going = True
                            break
        return [True] + inferences

    def apply_naked_triples(self,domains):
        # k=2
        for i in range(1,9):
            for j in range(i+1,10):
                si = str(i)
                sj = str(j)
                # Check rows/columns
                for k in range(9):
                    col_list = []
                    row_list = []
                    for l in range(9):
                        if domains[k][l] == [si,sj]:
                            col_list.append(l)
                        if domains[l][k] == [si,sj]:
                            row_list.append(l)
                    if len(col_list) == 2:
                        for m in range(9):
                            if si in domains[k][m] and m not in col_list:
                                domains[k][m].remove(si)
                            if sj in domains[k][m] and m not in col_list:
                                domains[k][m].remove(sj)
                    if len(row_list) == 2: 
                        for m in range(9):
                            if si in domains[m][k] and m not in row_list:
                                domains[m][k].remove(si)
                            if sj in domains[m][k] and m not in row_list:
                                domains[m][k].remove(sj)

                # Check boxes
                for k,l in product(range(3),range(3)):
                    box_rows = range(k*3,(k+1)*3)
                    box_cols = range(l*3,(l+1)*3)
                    box_list = []
                    for m,n in product(box_rows,box_cols):
                        if domains[m][n] == [si,sj]:
                            box_list.append([m,n])
                    if len(box_list) == 2:
                        for m,n in product(box_rows,box_cols):
                            if si in domains[m][n] and [m,n] not in box_list:
                                domains[m][n].remove(si)
                            if sj in domains[m][n] and [m,n] not in box_list:
                                domains[m][n].remove(sj)

        # k=3
        for h in range(1,8):
            for i in range(h+1,9):
                for j in range(i+1,10):
                    sh = str(h)
                    si = str(i)
                    sj = str(j)

                    # Check rows/columns
                    for k in range(9):
                        col_list = []
                        row_list = []
                        for l in range(9):
                            if domains[k][l] in [[sh,si,sj], [sh,si], [sh,sj], [si,sj]]:
                                col_list.append(l)
                            if domains[l][k] in [[sh,si,sj], [sh,si], [sh,sj], [si,sj]]:
                                row_list.append(l)
                        if len(col_list) == 3:
                            for m in range(9):
                                if sh in domains[k][m] and m not in col_list:
                                    domains[k][m].remove(sh)
                                if si in domains[k][m] and m not in col_list:
                                    domains[k][m].remove(si)
                                if sj in domains[k][m] and m not in col_list:
                                    domains[k][m].remove(sj)
                        if len(row_list) == 3: 
                            for m in range(9):
                                if sh in domains[m][k] and m not in row_list:
                                    domains[m][k].remove(sh)
                                if si in domains[m][k] and m not in row_list:
                                    domains[m][k].remove(si)
                                if sj in domains[m][k] and m not in row_list:
                                    domains[m][k].remove(sj)
                    # Check boxes
                    for k,l in product(range(3),range(3)):
                        box_rows = range(k*3,(k+1)*3)
                        box_cols = range(l*3,(l+1)*3)
                        box_list = []
                        for m,n in product(box_rows,box_cols):
                            if domains[m][n] in [[sh,si,sj], [sh,si], [sh,sj], [si,sj]]:
                                box_list.append([m,n])
                        if len(box_list) == 3:
                            for m,n in product(box_rows,box_cols):
                                if sh in domains[m][n] and [m,n] not in box_list:
                                    domains[m][n].remove(sh)
                                if si in domains[m][n] and [m,n] not in box_list:
                                    domains[m][n].remove(si)
                                if sj in domains[m][n] and [m,n] not in box_list:
                                    domains[m][n].remove(sj)
 
        return domains

    def backtrack(self):
        if self.is_solved():
            return

        domains = self.get_domains()
        if domains == False:
            return

        # Select a square to try
        sq = []
        if self.most_constrained:
            least_len = [10,-1,-1]
            for i,j in product(range(9),range(9)):
                leng = len(domains[i][j])
                if leng < least_len[0] and self.b[i][j] == '-':
                    least_len = [leng,i,j]
                    if leng == 2:
                        break
            sq = least_len[1],least_len[2]
        else:
            for i in range(9):
                for j in range(9):
                    if self.b[i][j] == '-':
                        sq = i,j

        # Try each value in sq's domain until one works
        for val in domains[sq[0]][sq[1]]:
            self.b[sq[0]][sq[1]] = val
            
            inferences = [[sq[0],sq[1]]]
            r1 = self.apply_rule1()
            r2 = self.apply_rule2()
            if len(r1) > 1:
                inferences += r1[1:]
            if len(r2) > 1:
                inferences += r2[1:]

            if r1[0] and r2[0]:
                self.no_calls += 1
                self.backtrack()
            if self.is_solved():
                return
            for inf in inferences:
                self.b[inf[0]][inf[1]] = '-'

    def is_solved(self):
        # If any square is not yet assigned a number, return false. Else return
        #  true.
        for i in range(9):
            for j in range(9):
                if self.b[i][j] == '-':
                    return False
        return True

# Read in the contents of the sudoku repository. Use some python voodoo to
#  parse out all of the sudokus into a list, and parse out their corresponding
#  difficulties.
repo = open('repository.txt','r').readlines()
difficulties = [repo[line_num].split()[1].lower() for line_num in range(len(repo)) if line_num % 11 == 0]
repo = [[i for i in line.replace('0','-') if i in ([str(j) for j in range(1,10)] + ['-'])] for line in repo]
sudokus = [repo[i*11+1:i*11+10] for i in range(len(repo)/11)]

a = []
c = []
for i in range(len(sudokus)):
    print 'Processing sudoku %d' % i
    sudoku = Board(sudokus[i],naked=True,mc=True)
    sudoku.backtrack()
    a += [[sudoku.is_solved(),sudoku.no_calls]]
    c += [sudoku]
print
print a
print len([i for i in a if i[0] == False])

#16/77 still unsolved after applying rule 1. 26/77 with naked triples
#54/77 still unsolved after applying rule 1, then rule 2. 26/77 with naked triples
#51/77 still unsolved after applying the two rules repeatedly. 23/77 with naked triples

