USING VAMPIRE:

1. You need to be in the directory that contains the logic/ subdirectory for Vampire.
2. Write the input file from inside the agent program, e.g., infile.
3. call java logic.kb.fol.AskVampire infile > outfile
4. Read outfile to find either *NOT PROVED* or *PROVED* in it

The input file should be in the following format (without the #s). 
#################
KNOWLEDGE BASE
fact 1
fact 2
:
:
:
:
percept 1
percept 2
:
:
:
:
END KNOWLEDGE BASE

QUERY
safe(cell)
#################
Note: safe(cell1) is an example. This can be anything you want to query. 

The facts should be written in First-Order syntax with the following notation:

!A = universal quantification
!E = Existential quantification
=> = implication
^ = and
| = or
~ = not
All variables must start with a ? E.g. ?v1, ?v2 etc. Arguments not  
starting with a ? are assumed to be constants.



E.g.
All men are mortal
!A ?x man(?x) => mortal(?x)

Every dog has his day
!A ?x (dog(?x) => (!E ?y day(?y) ^ has(?x, ?y)))

Use parentheses as needed to represent the fact correctly.
