import argparse
from operator import truediv
from dataprocess import data_pro
from tree import DecisionTree
from treePlotter import C45_Tree, CART_Tree, New_Tree
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Decision Tree')
	parser.add_argument('-d', '--dataset', type=str, default='data.txt',
						help='data file name')
	parser.add_argument('-r', '--ratio', type=float, default=0.2, help='test ratio')
	parser.add_argument('-t', '--treetype', type=str, choices=['new', 'c45', 'cart'], default='new')
	parser.add_argument('-pre', '--pre_pruning', action='store_true')
	parser.add_argument('-post', '--post_pruning', action='store_true')

	args = parser.parse_args()
	print(args)

	pre, post = False, False
	if args.pre_pruning:
		pre = True
	#pre = True
	if args.post_pruning:
		post = True
	tree = DecisionTree(tree_type=args.treetype, pre_pruning=pre, post_pruning=post)
	
	testdata, validdata, traindata = data_pro(args.dataset, args.ratio)
	# traindata = traindata[:500]
	# validdata = validdata[:50]
	# testdata = testdata[:2]
	print(len(testdata), len(validdata), len(traindata))
	
	tree.tree = tree.buildtree(traindata, validdata)
	print(tree.tree)
	if args.treetype == 'c45':
		C45_Tree(tree.tree)
	elif args.treetype == 'cart':
		CART_Tree(tree.tree)
	elif args.treetype == 'new':
		New_Tree(tree.tree)
	score = tree.runtree(testdata)
	print(score)
	# print(testdata[:3])