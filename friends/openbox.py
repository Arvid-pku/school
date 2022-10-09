import json
import random
import argparse

def reset(name): # reset the probability
	f = open(name+'.json', 'w')
	d = {
		'one': 40,
		'two': 20,
		'five': 9,
		'zero': 30,
		'ten': 1,
		'got': 0, 
		'times': 0
	}
	json.dump(d, f)
	f.close()



def get_random(): # get a random number
	return random.randint(0, 100)

def get_pros(fp):
	f = open(fp, 'r')
	d = json.load(f) # get the probability
	f.close()
	
	# add the probability
	pros = [d['zero'], d['zero']+d['one'], d['zero']+d['one']+d['two'], d['zero']+d['one']+d['two']+d['five'], d['zero']+d['one']+d['two']+d['five']+d['ten']]
	return pros

def openbox(name):
	pros = get_pros(name+'.json')
	if p <= pros[0]:
		return 0
	elif p <= pros[1]:
		return 1
	elif p <= pros[2]:
		return 2
	elif p <= pros[3]:
		return 5
	elif p <= pros[4]:
		return 10


def change_pros(name, getting):
	f = open(name+'.json', 'r')
	d = json.load(f)
	f.close()
	print(d)

	# change file
	d['got'] += getting
	d['times'] += 1

	# change probability
	if getting == 0:
		if d['zero'] > 0:
			d['zero'] -= 1
			d['ten'] += 1
	elif getting == 1:
		if d['one'] > 0:
			d['one'] -= 1
			d['five'] += 1
	elif getting == 5:
		if d['five'] > 0:
			d['five'] -= 1
			d['one'] += 1
	elif getting == 10:
		if d['ten'] > 0:
			d['ten'] -= 1
			d['zero'] += 1
	f = open(name+'.json', 'w')
	print(d)
	json.dump(d, f)
	f.close()



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name', help='name of the json file', default='default') # who is using this
	parser.add_argument('-r', '--reset', help='reset the json file', action='store_true') # reset the json file
	parser.add_argument('-g', '--get', help='get the random number', action='store_true') # whether to open the box
	args = parser.parse_args()


	f = open('money'+'.json', 'r') # check money
	d = json.load(f)
	print('money:', d['money'])
	f.close()


	name = args.name
	p = get_random() # get the random number

	if args.reset: # reset the probs file
		reset(name)


	if args.get: # open the box
		get_pros(name+'.json') # read your probs file

		x=openbox(name) # get your reward

		change_pros(name, x) # change your probs file
		print(x)

		d['money'] -= x	# change money number
		f = open('money'+'.json', 'w')
		print('left money:', d['money'])
		json.dump(d, f)
		f.close()
