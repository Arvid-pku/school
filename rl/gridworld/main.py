import numpy as np



class GridWorld(object):
	def __init__(self, world_size=5, discount_factor=0.9, special_states_list=None):
		self.world_size = world_size
		self.discount_factor = discount_factor
		self.actions = ['up', 'down', 'left', 'right']
		self.value_table = np.zeros((world_size, world_size))
		self.special_states_list = special_states_list

	def get_newpos(self, x, y, action):
		for special_state in self.special_states_list:
			if x == special_state[0][0] and y == special_state[0][1]:
				return special_state[1][0], special_state[1][1]
		if action == 'up':
			return x-1, y
		elif action == 'down':
			return x+1, y
		elif action == 'left':
			return x, y-1
		elif action == 'right':
			return x, y+1
	def get_reward(self, x, y):
		for special_state in self.special_states_list:
			if x == special_state[0][0] and y == special_state[0][1]:
				return special_state[2]
		if x < 0 or x >= self.world_size or y < 0 or y >= self.world_size:
			return -1
		return 0
	def run(self):
		i = 0
		while True:
			i+=1
			new_value_table = np.zeros((self.world_size, self.world_size))
			for x in range(self.world_size):
				for y in range(self.world_size):
					for action in self.actions:
						pre_reward = self.get_reward(x, y)
						new_x, new_y = self.get_newpos(x, y, action)
						new_reward = self.get_reward(new_x, new_y)
						if new_reward < 0:
							new_x, new_y = x, y
						elif new_reward > 0:
							new_reward = 0
						new_value_table[x, y] += 0.25 * (pre_reward + new_reward + self.discount_factor * self.value_table[new_x, new_y])
			if np.sum(np.abs(new_value_table - self.value_table)) < 1e-4:
				print(i)
				break
			self.value_table = new_value_table
		return self.value_table


if __name__ == '__main__':
	special_states_list = [
		((0, 1), (4, 1), 10),
		((0, 3), (2, 3), 5)
	]
	grid_world = GridWorld(world_size=5, discount_factor=0.9, special_states_list=special_states_list)
	value_table = grid_world.run()
	print(value_table)