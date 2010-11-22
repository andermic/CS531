from os import system
from random import randint
from itertools import product

FILE_NAME = 'worlds.txt'

class WumpusWorld:
    world = list()

    def __init__(self, w):
        if w == []:
            self.world = self.make_random_world()
        else:
            self.world = w

    # Generate a random wumpus world
    def make_random_world(self):
        # Make a dictionary for each square, which will hold whether that
        #  square contains a pit, wumpus, breeze, stench, or gold.
        world = [[{'p':False,'w':False,'b':False,'s':False,'g':False} for i in range(4)] for j in range(4)]

        # Make a wumpus and some gold on unique squares.
        e = []
        while len(e) != 2:
            sq = randint(1,15)
            row = sq / 4
            col = sq % 4
            if [row,col] in e:
                continue
            e.append([row,col])

        # Make some pits on unique squares
        for sq in range(1,15):
            row = sq / 4
            col = sq % 4
            if [row,col] in e:
                continue
            if randint(1,5) == 1:
                e.append([row,col])

        # Populate world with wumpus and stenches
        world[e[0][0]][e[0][1]]['w'] = True
        if e[0][0] > 0:
            world[e[0][0] - 1][e[0][1]]['s'] = True
        if e[0][0] < 3:
            world[e[0][0] + 1][e[0][1]]['s'] = True
        if e[0][1] > 0:
            world[e[0][0]][e[0][1] - 1]['s'] = True
        if e[0][1] < 3:
            world[e[0][0]][e[0][1] + 1]['s'] = True

        # Place gold
        world[e[1][0]][e[1][1]]['g'] = True

        # Populate world with pits and breezes
        for i in range(2, len(e)):
            world[e[i][0]][e[i][1]]['p'] = True
            if e[i][0] > 0:
                world[e[i][0] - 1][e[i][1]]['b'] = True
            if e[i][0] < 3:
                world[e[i][0] + 1][e[i][1]]['b'] = True
            if e[i][1] > 0:
                world[e[i][0]][e[i][1] - 1]['b'] = True
            if e[i][1] < 3:
                world[e[i][0]][e[i][1] + 1]['b'] = True
 
        return world

    def display(self, loc):
        system('clear')
        print 'A - Agent'
        print 'P - Pit'
        print 'W - Wumpus'
        print 'B - Breeze'
        print 'S - Stench'
        print 'G - Gold'
        print

        w = self.world
        rows = range(4)
        rows.reverse()
        for r in rows:
            print ' _______ _______ _______ _______'
            rtext = '|'
            for c in range(4):
                rtext += '%d,%d    |' % (c+1,r+1)
            print rtext

            rtext = '|'
            for c in range(4):
                rtext += '   %s   |' % {True:'A', False:' '}[loc == [r,c]]
            print rtext

            rtext = ''
            for c in range(4):
                s = w[r][c]
                rtext += '| '
                for l in ['p','w','b','s','g']:
                    if s[l]:
                        rtext += l.upper()
                    else:
                        rtext += ' '
                rtext += ' '
            rtext += '|'
            print rtext

            print '|_______|_______|_______|_______|'

class HumanAgent:
    def get_action(self, percept):
        return raw_input('Enter next action: ')

class ComputerAgent:
    KB = []
    t = 0
    plan = []

    # Initialize the agent by adding the atemporal physics of the wumpus world
    #  to the KB.
    def __init__(self):
        pass

    # Return a list of facts that correspond to a given percept
    def make_percept_sentence(self, percept):
        facts = []
        return facts

    # Return a list of facts that correpond to a given action
    def make_action_sentence(self, percept):
        pass
        
    # Give the theorem prover a query and the current KB, and see if the query
    #  is provably true
    def ask(self, query):
        result = bool()
        return result

    def tell(self, facts):
        pass

    # Ask the agent to provide the best action given its current KB and the
    #  current percept
    def get_action(self, percept):
        action = str()
        return action

    # Use A* to calculate a sequence of actions that will bring an agent from
    #  the given location to one of the goal locations
    def plan_route(self, current, goals, allowed):
        action_sequence = []
        return action_sequence

    # Use A* to calculate a sequence of actions
    def plan_shot(self, current, possible_wumpus, safe):
        action_sequence = []
        return action_sequence

class Simulation:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    ww = None
    agent = None

    loc = [0,0]
    facing = NORTH

    has_arrow = True    

    # Initialize the simulation by storing the wumpus world given, and then
    #  run the simulation
    def __init__(self, ww, computer):
        self.ww = ww
        if computer:
            self.agent = ComputerAgent()
        else:
            self.agent = HumanAgent()
        self.run()

    # Run the simulation by giving the agent percepts and asking for actions,
    #  until the agent dies or climbs out.
    def run(self):
        scream = False
        
        self.ww.display(self.loc)
        print
        print 'Agent is facing %s' % {0:'north', 1:'east', 2:'south', 3:'west'}[self.facing]
        print 'Press enter to continue...'
        raw_input()

        bump = False
        while True:
            # Construct a percept
            percept = {}
            percept['stench'] = self.ww.world[self.loc[0]][self.loc[1]]['s']
            percept['breeze'] = self.ww.world[self.loc[0]][self.loc[1]]['b']
            percept['glitter'] = self.ww.world[self.loc[0]][self.loc[1]]['g']
            percept['scream'] = scream
            percept['bump'] = bump
            print 'Current percept: %s' % str(percept)

            # Get an action based on current percept
            action = self.agent.get_action(percept)

            # Process action
            scream = False
            bump = False
            if action == 'forward':
                if self.facing == self.NORTH:
                    if self.loc[0] == 3:
                        bump = True
                    else:
                        self.loc[0] += 1
                if self.facing == self.EAST:
                    if self.loc[1] == 3:
                        bump = True
                    else:
                        self.loc[1] += 1
                if self.facing == self.SOUTH:
                    if self.loc[0] == 0:
                        bump = True
                    else:
                        self.loc[0] -= 1
                if self.facing == self.WEST:
                    if self.loc[1] == 0:
                        bump = True
                    else:
                        self.loc[1] -= 1
                agent_sq = self.ww.world[self.loc[0]][self.loc[1]]
                if agent_sq['w']:
                    self.ww.display(self.loc)
                    print '\nYou were killed by the wumpus\n'
                    return
                if agent_sq['p']:
                    self.ww.display(self.loc)
                    print '\nYou fell to your death down a pit\n'
                    return

            elif action == 'turn_left':
                self.facing = (self.facing - 1) % 4
            elif action == 'turn_right':
                self.facing = (self.facing + 1) % 4
            elif action == 'grab':
                if self.ww.world[self.loc[0]][self.loc[1]]['g']:
                    self.ww.world[self.loc[0]][self.loc[1]]['g'] = False
            elif action == 'shoot':
                dir = {self.NORTH:(self.loc[0]+1,4), self.EAST:(self.loc[1]+1,4), self.SOUTH:(0,self.loc[0]), self.WEST:(0,self.loc[1])}[self.facing]
                if self.has_arrow:
                    self.has_arrow = False
                    for i in range(*dir):
                        if self.facing % 2 == 0:
                            if self.ww.world[i][self.loc[1]]['w']:
                                self.ww.world[i][self.loc[1]]['w'] = False
                                scream = True
                        else:
                            if self.ww.world[self.loc[0]][i]['w']:
                                self.ww.world[self.loc[0]][i]['w'] = False
                                scream = True
            elif action == 'climb':
                if self.loc == [0,0]:
                    return

            self.ww.display(self.loc)
            print
            print 'Last action: %s' % action
            print 'Agent is facing %s' % {0:'north', 1:'east', 2:'south', 3:'west'}[self.facing]
            print 'Press enter to continue...'
            raw_input()

# Generate 100 random wumpus worlds and write them to a file
def generate_worlds():
    fstream = open(FILE_NAME, 'w')
    for i in range(100):
        w = WumpusWorld([])
        fstream.write('%d\n' % i)
        w.world.reverse()
        for row in w.world:
            for s in row:
                fstream.write('|')
                for l in ['p','w','b','s','g']:
                    if s[l]:
                        fstream.write(l.upper())
                    else:
                        fstream.write(' ')
            fstream.write('\n')
        fstream.write('\n')
    fstream.close()

# Read pre-generated worlds from file
def read_worlds():
    lines = open(FILE_NAME, 'r').readlines()
    worlds = []
    for w in range(100):
        worlds.append([])
        for r in range(4):
            worlds[w].append([])
            line = lines[w*6+r+1]
            for c in range(4):
                worlds[w][r].append({})
                for l in range(5):
                    if line[c*6+1+l] == ' ':
                        worlds[w][r][c][['p','w','b','s','g'][l]] = False
                    else:
                        worlds[w][r][c][['p','w','b','s','g'][l]] = True
        worlds[w].reverse()
        worlds[w] = WumpusWorld(worlds[w])
    return worlds

Simulation(read_worlds()[0],False)
