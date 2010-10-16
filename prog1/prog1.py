import os
import random

class Floor:
	squares = []

	def display(self, agent_loc):
		for row in range(len(self.squares)):
			for col in range(len(self.squares[row])):
				print '[' + self.squares[row][col] + {True:'R', False:' '}[agent_loc == [row, col]] + ']',
			print
		print
		raw_input('Press enter to continue simulation')
		os.system('clear')

class Simulation:
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3
	agent_facing = NORTH

	FLOOR_HEIGHT = 10
	FLOOR_WIDTH = 10
	floor = Floor()
	agent_loc = [FLOOR_HEIGHT - 1, 0]
	action_count = 0
	log_results = False
	def __init__(self, log_results):
		self.floor.squares = [self.FLOOR_WIDTH * ['D'] for i in range(self.FLOOR_HEIGHT)]
		self.log_results = log_results
		if self.log_results:
			agent_type = 2
		else:
			os.system('clear')
			print '1 - Deterministic agent without memory'
			print '2 - Non-deterministic agent'
			print '3 - Deterministic agent with 3 bits of memory'

			agent_type = None
			while agent_type not in [1,2,3]:
				agent_type = input('Pick an agent type (1,2,3): ')

		os.system('clear')
		if agent_type == 1:
			self.run(MemorylessAgent())
		elif agent_type == 2:
			self.run(RandomAgent())
		elif agent_type == 3:
			self.run(MemoryAgent())			
	
	def run(self, agent):
		while True:
			if not self.log_results:
				print "Squares marked 'D' are dirty"
				print "Robot occupies the square marked 'R'"
				print 'Robot is currently facing %s\n' % \
				 {0:'NORTH',1:'EAST',2:'SOUTH',3:'WEST'}[self.agent_facing]
				self.floor.display(self.agent_loc)

			is_facing_wall = (self.agent_loc[0] == 0 and self.agent_facing == self.NORTH) or \
			 (self.agent_loc[1] == self.FLOOR_WIDTH - 1 and self.agent_facing == self.EAST) or \
			 (self.agent_loc[0] == self.FLOOR_HEIGHT - 1 and self.agent_facing == self.SOUTH) or \
			 (self.agent_loc[1] == 0 and self.agent_facing == self.WEST)
			is_on_dirt = (self.floor.squares[self.agent_loc[0]][self.agent_loc[1]] == 'D')
			is_on_home = (self.agent_loc == [self.FLOOR_HEIGHT - 1, 0])

			action = None
			grid_size = self.FLOOR_HEIGHT * self.FLOOR_WIDTH
			cleanliness = len(reduce(lambda x,y: x+y, [[j for j in i if j == ' '] for i in self.floor.squares])) * 100 / grid_size
			if isinstance(agent, RandomAgent) and cleanliness >= 90:
				action = 'Turn off'
			else:
				action = agent.action(is_facing_wall, is_on_dirt, is_on_home)

			self.action_count += 1
			if not self.log_results:
				print 'Action taken: ' + action
				print 'Number of actions so far taken: ' + str(self.action_count)

			if action == 'Turn left':
				self.agent_facing = (self.agent_facing + 3) % 4
			elif action == 'Turn right':
				self.agent_facing = (self.agent_facing + 1) % 4
			elif action == 'Forward' and not is_facing_wall:
				if self.agent_facing == self.NORTH:
					self.agent_loc[0] -= 1
				elif self.agent_facing == self.EAST:
					self.agent_loc[1] += 1
				elif self.agent_facing == self.SOUTH:
					self.agent_loc[0] += 1
				elif self.agent_facing == self.WEST:
					self.agent_loc[1] -= 1
			elif action == 'Suck':
				self.floor.squares[self.agent_loc[0]][self.agent_loc[1]] = ' '
			elif action == 'Turn off':
				if self.log_results:
					fstream = open('prog1.txt', 'a')
					fstream.write('%d\n' % (self.action_count))
					fstream.close()
				else:
					print 'Simulation finished, robot took %d actions and left floor %d%% clean' % (self.action_count, cleanliness)
				return

class Agent:
	pass

class MemorylessAgent(Agent):
	def action(self, is_facing_wall, is_on_dirt, is_on_home):
		if is_on_dirt:
			return 'Suck'
		elif is_facing_wall:
			return 'Turn right'
		else:
			return 'Forward'

class RandomAgent(Agent):
	def action(self, is_facing_wall, is_on_dirt, is_on_home):
		if is_on_dirt:
			return 'Suck'
		elif is_facing_wall:
			return {1:'Turn left', 2:'Turn right'}[random.randint(1,2)]
		else:
			return {1:'Turn left', 2:'Turn right'}.get(random.randint(1,20), 'Forward')

class MemoryAgent(Agent):
	left_or_right = False
	just_hit_wall = False
	just_just_hit_wall = False

	def action(self, is_facing_wall, is_on_dirt, is_on_home):
		if is_on_dirt:
			return 'Suck'
		elif is_facing_wall:
			if is_on_home:
				return 'Turn off'
			if self.just_just_hit_wall:
				self.just_hit_wall = True
				return {False:'Turn left', True:'Turn right'}[self.left_or_right]
			else:
				self.left_or_right = not self.left_or_right
				self.just_hit_wall = True
			return {False:'Turn left', True:'Turn right'}[self.left_or_right]
		else:
			if self.just_hit_wall and not self.just_just_hit_wall:
				self.just_hit_wall = False
				self.just_just_hit_wall = True
			elif self.just_just_hit_wall and not self.just_hit_wall:
				self.just_just_hit_wall = False
				return {False:'Turn left', True:'Turn right'}[self.left_or_right]
			return 'Forward'
		
os.system('clear')
print '1 - Run simulation once'
print '2 - Run simulation multiple times and log results to prog1.txt'
selection = None
while selection not in [1,2]:
	selection = input('(1,2): ')

if selection == 1:
	Simulation(log_results=False)
else:
	if 'prog1.txt' in os.listdir('.'):
		os.remove('prog1.txt')
	number_of_times = None
	while type(number_of_times) != int and number_of_times < 1:
		number_of_times = input('\nHow many times would you like to run the simulation? ')
	for i in range(number_of_times):
		Simulation(log_results=True)
	
	fstream = open('prog1.txt', 'r')
	action_counts = [int(i) for i in fstream.readlines()]

	print
	print 'Results are logged in prog1.txt'
	print 'Average number of actions taken: %d' % (sum(action_counts) / len(action_counts))
