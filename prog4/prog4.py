from os import system
from random import randint
from itertools import product

FILE_NAME = 'worlds.txt'
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3



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
    loc = [0,0]
    facing = NORTH

    def get_action(self, percept):
        ri = raw_input('\nTake an action by entering the corresponding letter in square brackets ([f]orward, turn [l]eft, turn [r]ight, [g]rab, [c]limb, [s]hoot): ')
        return {'f':'forward','l':'turn_left','r':'turn_right','g':'grab','c':'climb','s':'shoot'}.get(ri)


class ComputerAgent:
    KB = []
    t = 0
    plan = []
    loc = [0,0]
    facing = NORTH

    KB_LOC = 0
    KB_CUR = 1
    KB_WA = 2
    KB_HA = 3

    # Initialize the agent by adding the atemporal physics of the wumpus world
    #  to the KB.
    def __init__(self):
        # Start the agent at location 0,0
        self.KB.append('at(agent, sq00, t0)')

        # Leave space for the current time
        self.KB.append('cur = t0')

        # In the beginning, the wumpus is alive and the agent has an arrow
        self.KB.append('WumpusAlive')
        self.KB.append('haveArrow')

        # Define squares
        squares = []
        for i in range(4):
            for j in range(4):
                squares.append('sq%d%d' % (i,j))
        self.KB.append('square(x) <-> ((x = %s' % (') | (x = ').join(squares)+ '))')

        # Define adjacency
        adj_list = []
        for r1 in range(4):
            for c1 in range(4):
                for r2 in range(4):
                    for c2 in range(4):
                        if r1 == r2:
                            if abs(c1 - c2) == 1:
                                adj_list.append(['sq%d%d' % (r1,c1), 'sq%d%d' % (r2,c2)])
                        if c1 == c2:
                            if abs(r1 - r2) == 1:
                                adj_list.append(['sq%d%d' % (r1,c1), 'sq%d%d' % (r2,c2)])
        adj_str = ' | '.join(('((x = %s) & (y = %s))' % (i[0],i[1])) for i in adj_list)
        self.KB.append('adjacent(x,y) <-> square(x) & square(y) & (%s)' % adj_str)

        # Define time
        self.KB.append('time(x) <-> (%s)' % ' | '.join([('(x = t%d)' % i) for i in range(100)]) )

        # Define visited
        self.KB.append('visited(x) <-> (exists y ((time(y)) & (at(agent, x, y))))')

        # A square is safe iff it contains no wumpus and no pit
        self.KB.append('ok(x) <-> (-(pit(x)) & -(at(Wumpus, x, cur)))')

        # If there was ever a wumpus in a square, there is no wumpus in any other square
        self.KB.append('(exists x (square(x) & (exists y (time(y) & (at(Wumpus, x, y)))))) -> (all y( all z( (square(z) & (x != z)) -> -(at(Wumpus, z, y)))))')

        # Once a wumpus is found to be at a square, it is always at that square unless it is killed
        self.KB.append('((exists x (square(x) & (exists y (time(y) & (at(Wumpus, x, y)))))) & WumpusAlive) -> (at(Wumpus, x, cur))')

        # If the wumpus is dead then there is no wumpus on any square
        self.KB.append('(-WumpusAlive) -> (all x ((square(x)) -> (-(at(Wumpus, x, cur)))))')

        # A square is breezy iff there is a pit that is adjacent to it
        self.KB.append('breezy(x) <-> (exists y ((adjacent(x,y)) & pit(y)))')

        # A square is smelly iff there is a wumpus that is adjacent to it
        self.KB.append('(smelly(x) & WumpusAlive) <-> (exists y ((adjacent(x,y)) & (at(Wumpus, y, cur))))')

    # Helper function for plan_route. Return the value of the smallest
    #  Manhattan Distance to a goal square from the current square.
    def heur(self, cur_square, goals):
        smallest = -1
        for goal in goals:
            dist = abs(cur_square[0] - goal[0]) + abs(cur_square[1] - goal[1])
            if (smallest == -1) or (dist < smallest):
                smallest = dist
        return smallest

    # Helper function for plan_route. Return the actions possible from the
    #  current square.
    def actions(self, cur_square, facing):
        min_actions = ['turn_left', 'turn_right']
        if facing == NORTH:
            if cur_square[0] == 3:
                return min_actions
        elif facing == EAST:
            if cur_square[1] == 3:
                return min_actions
        elif facing == SOUTH:
            if cur_square[0] == 0:
                return min_actions
        elif facing == WEST:
            if cur_square[1] == 0:
                return min_actions
        return min_actions + ['forward']

    # Helper function for plan_route. Insert a given node into the frontier to
    #  maintain a descending order by f value.
    def insert(self, node, frontier):
        for i in range(len(frontier)):
            if node['f'] >= frontier[i]['f']:
                frontier.insert(i,node)
                return
        frontier.append(node)

    # Use A* to calculate a sequence of actions that will bring an agent from
    #  the given location to one of the goal locations
    def plan_route(self, current, goals, allowed):
        root = {}
        root['sq'] = current[0]
        root['facing'] = current[1]
        root['g'] = 0
        root['f'] = root['g'] + self.heur(root['sq'], goals)
        root['parent'] = None
        root['action'] = None
        frontier = [root]
        explored = []

        while True:
            if frontier == []:
                return False
            node = frontier.pop()
            if node['sq'] in goals:
                solution = []
                while node[parent] != None:
                    solution.append(node['action'])
                    node = node['parent']
                solution.reverse()
                return solution, node['sq'], node['facing']
            explored += [node['sq'], node['facing']]
            for action in self.actions(node['sq'], node['facing']):
                child = {}
                child['sq'] = node['sq']
                child['facing'] = node['facing']
                if action == 'forward':
                    s = child['sq']
                    child['sq'] = {NORTH:[s[0]+1,s[1]], EAST:[s[0],s[1]+1], SOUTH:[s[0]-1,s[1]], WEST:[s[0],s[1]-1]}[child['facing']]
                elif action == 'turn_right':
                    child['facing'] = (child['facing'] + 1) % 4
                elif action == 'turn_left':
                    child['facing'] = (child['facing'] - 1) % 4
                if child['sq'] not in allowed:
                    continue
                child['g'] = node['g'] + 1
                child['f'] = child['g'] + self.heur(child['sq'], goals)
                child['parent'] = node
                child['action'] = action
                if [child['sq'], child['facing']] not in explored + [[i['sq'], i['facing']] for i in frontier]:
                    self.insert(child, frontier)
                for i in range(len(frontier)):
                    if [child['sq'], child['facing']] == [frontier[i]['sq'], frontier[i]['facing']]:
                        if child['f'] < frontier[i]['f']:
                            frontier = frontier[:i] + frontier[i+1:]
                            self.insert(child, frontier)

    # Use A* to calculate a sequence of actions that lines up a shot to a
    #  possible wumpus location, and then shoot.
    def plan_shot(self, current, possible_wumpus, safe):
        goals = []
        for sq in safe:
            if (sq[0] == possible_wumpus[0]) or (sq[1] == possible_wumpus[1]):
                goals.append(safe)
        if goals == []:
            return []

        actions, goal_square, goal_facing = self.plan_route([current[0],current[1]], goals, safe)
        if found_goal[0] == possible_wumpus[0]:
            if found_goal[1] > possible_wumpus[1]:
                need_to_face = WEST
            else:
                need_to_face = EAST
        else:
            if found_goal[0] > possible_wumpus[0]:
                need_to_face = SOUTH
            else:
                need_to_face = NORTH

        if abs(need_to_face - goal_facing) == 2:
            actions += ['turn_right', 'turn_right']
        elif need_to_face - goal_facing == 1:
            actions.append('turn_right')
        elif need_to_face - goal_facing == -1:
            actions.append('turn_left')

        actions.append('shoot')

        return actions

    # Return a list of facts that correspond to a given percept
    def make_percept_sentence(self, percept):
        self.KB[self.KB_CUR] = 'cur = t%d' % self.t
        self.KB[self.KB_LOC] = 'at(agent, sq%d%d, t%d)' % (self.loc[0],self.loc[1],self.t)
        facts = []
        if percept['stench']:
            facts.append('smelly(sq%d%d)' % (self.loc[0], self.loc[1]))
        if percept['breeze']:
            facts.append('breezy(sq%d%d)' % (self.loc[0], self.loc[1]))
        if percept['scream']:
            KB[KB_WA] = '-WumpusAlive'
        return facts

    # Return a list of facts that correpond to a given action
    def make_action_sentence(self, percept):
        if percept['shoot']:
            KB[KB_HA] = '-haveArrow'
        return facts
        
    # Give the theorem prover a query and the current KB, and see if the query
    #  is provably true
    def ask(self, query):
        stream = open('input.txt', 'w')
        stream.write('formulas(assumptions).\n')
        for fact in self.KB:
            stream.write('  %s.\n' % fact)
        stream.write('end_of_list.\n\n')
        stream.write('formulas(goals).\n')
        stream.write('  %s.\n' % query)
        stream.write('end_of_list.')
        stream.close()

        system('./prover9 -f input.txt > output.txt')

        status_line = open('input.txt', 'r').readlines()[-3]
        if 'failure' in status_line:
            return False
        return True

    # Add a set of facts to the KB
    def tell(self, facts):
        self.KB += facts

    # Ask the agent to provide the best action given its current KB and the
    #  current percept
    def get_action(self, percept):
        self.tell(self.make_percept_sentence(percept))
        safe = [[i[0],i[1]] for i in product(range(4),range(4)) if self.ask('ok(sq%d%d)' % (i[0],i[1]))]
        if percept['glitter']:
            self.plan = ['grab'] + plan_route([self.loc,self.facing], [0,0], safe)[0] + ['climb']
        if self.plan == []:
            unvisited = set([])
            for i in product(range(4),range(4)):
                if not self.ask('visited(sq%d%d)' % (i[0],i[1])):
                    unvisted.append([i[0],i[1]])
            self.plan = self.plan_route([self.loc,self.facing], [i for i in unvisited if i in safe], safe)[0]
        if self.plan == [] and self.ask('haveArrow' % self.t):
            possible_wumpus = [[i[0],i[1]] for i in product(range(4),range(4)) if not self.ask('-(at(Wumpus, sq%d%d, cur))' % (i[0],i[1]))]
            self.plan = self.plan_shot([self.loc,self.facing], possible_wumpus, safe)
        if self.plan == []:
            not_unsafe = [[i[0],i[1]] for i in product(range(4),range(4)) if not self.ask('-(ok(sq%d%d))' % (i[0],i[1]))]
            self.plan = self.plan_route([self.loc,self.facing], [i for i in unvisited if i in not_unsafe], safe)[0]
        if self.plan == []:
            self.plan = self.plan_route([self.loc,self.facing], [0,0], safe)[0] + ['climb']
        action = self.plan[0]
        self.plan = self.plan[1:]
        t = t + 1
        return action



class Simulation:
    ww = None
    agent = None

    loc = [0,0]
    facing = NORTH

    has_arrow = True    

    # Initialize the simulation by storing the wumpus world given, and then
    #  run the simulation
    def __init__(self, ww, agent):
        self.ww = ww
        self.agent = agent
        self.run()

    # Run the simulation by giving the agent percepts and asking for actions,
    #  until the agent dies or climbs out.
    def run(self):
        self.ww.display(self.loc)
        print
        print 'Agent is facing %s' % {0:'north', 1:'east', 2:'south', 3:'west'}[self.facing]
        print 'Press enter to continue...'
        raw_input()

        scream = False
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
                if self.facing == NORTH:
                    if self.loc[0] == 3:
                        bump = True
                    else:
                        self.loc[0] += 1
                if self.facing == EAST:
                    if self.loc[1] == 3:
                        bump = True
                    else:
                        self.loc[1] += 1
                if self.facing == SOUTH:
                    if self.loc[0] == 0:
                        bump = True
                    else:
                        self.loc[0] -= 1
                if self.facing == WEST:
                    if self.loc[1] == 0:
                        bump = True
                    else:
                        self.loc[1] -= 1
                self.agent.loc = self.loc

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
                self.agent.facing = self.facing
            elif action == 'turn_right':
                self.facing = (self.facing + 1) % 4
                self.agent.facing = self.facing
            elif action == 'grab':
                if self.ww.world[self.loc[0]][self.loc[1]]['g']:
                    self.ww.world[self.loc[0]][self.loc[1]]['g'] = False
            elif action == 'shoot':
                dir = {NORTH:[self.loc[0]+1,4], EAST:[self.loc[1]+1,4], SOUTH:[0,self.loc[0]], WEST:[0,self.loc[1]]}[self.facing]
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
            else:
                print 'INVALID ACTION TAKEN'
                exit()

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

system('clear')
print 'Who will solve a wumpus world?'
print '   1 - Human'
print '   2 - Computer'
select = raw_input('Select: ')
if select not in ['1','2']:
    print 'ERROR: INVALID SELECTION'
    exit()
else:
    select2 = raw_input('\nWhich wumpus world? [0-99] ')
    if int(select2) not in range(100):
        print 'ERROR: INVALID SELECTION'
    else:
        if select == '1':        
            Simulation(read_worlds()[int(select2)],HumanAgent())
        if select == '2':        
            Simulation(read_worlds()[int(select2)],ComputerAgent())
