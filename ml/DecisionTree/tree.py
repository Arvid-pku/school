import random
from re import S
from this import d
from utils import cal_entropy, cal_infogain, cal_gini, cal_gainratio, getMajority
from utils import getUniVal, splitdataset, cal_acc, remove_features, cal_gini_data

class DecisionTree():
	def __init__(self, tree_type='c45', pre_pruning=True, post_pruning=False) -> None:
		self.tree_type = tree_type
		self.pre_pruning = pre_pruning
		self.post_pruning = post_pruning
		self.tree = None
		self.feature_metric = {'c45': cal_gainratio, 'id3': cal_infogain, 'cart': cal_gini, 'new': cal_gainratio}[tree_type]

	def buildtree(self, traindata, testdata):
		if len(traindata[0]) == 1:
			return getMajority(traindata)
		if len(getUniVal(traindata, -1)) == 1:
			return traindata[0][-1]
		rms = []
		for idx in range(len(traindata[0]) - 1):
			if len(getUniVal(traindata, idx)) == 1:
				rms.append(idx)
		traindata = remove_features(traindata, rms)
		testdata = remove_features(testdata, rms)
		bestFeature, bestvalue = self.findfeature(traindata)

		tmpvals = getUniVal(traindata, bestFeature)
		vals = []
		for val in tmpvals:
			subtestdataset = splitdataset(testdata, bestFeature, val)
			if len(subtestdataset) > 0:
				vals.append(val)
		tree = {bestFeature: {}}

		labels = [d[-1] for d in testdata]
		trylabel = getMajority(testdata)
		trylabels = [trylabel for _ in range(len(labels))]
		notsplit_acc = cal_acc(trylabels, labels)
		split_pred = []
		split_labels = []
		notsplitpreds = []
		notsplitvallist = []
		valgini = {}
		valclass = {}
		notsplitclass2val = {}
		if self.pre_pruning:
			if self.tree_type == 'c45':
				for val in vals:
					subtestdataset = splitdataset(testdata, bestFeature, val)
					split_label = getMajority(subtestdataset)
					split_pred += [split_label for _ in range(len(subtestdataset))]
					split_labels += [d[-1] for d in subtestdataset]
			elif self.tree_type == 'cart':
				subset, notset = splitdataset(testdata, bestFeature, bestvalue, True)
				split_label = getMajority(subset)
				split_pred += [split_label for _ in range(len(subset))]
				split_labels += [d[-1] for d in subset]
				split_label = getMajority(notset)
				split_pred += [split_label for _ in range(len(notset))]
				split_labels += [d[-1] for d in notset]
			elif self.tree_type == 'new':
				for val in vals:
					subtestdataset = splitdataset(testdata, bestFeature, val)
					valgini[val] = cal_gini_data(subtestdataset)
					a = [d[-1] for d in subtestdataset]
					# a = [1,2,3,4,2,3,2]
					try:
						valclass[val] = max(a,key=a.count)
					except:
						print(a)
						print(testdata)
						print(subtestdataset, val)
						print(bestFeature)
						raise
					# print('v: ', valclass)
				valgini = sorted(valgini.items(), key=lambda x: x[1])
				# print(subtestdataset, valgini)
				noclass = valclass[valgini[0][0]]
				for val, gini in valgini:
					if gini > 0.15:
						break
					subtestdataset = splitdataset(testdata, bestFeature, val)
					split_labels += [d[-1] for d in subtestdataset]
					split_pred += [valclass[val] for _ in range(len(subtestdataset))]

					notsplitpreds += [valclass[val] for _ in range(len(subtestdataset))]
					# print(cal_acc(notsplitpreds, split_labels) , cal_acc(split_pred, split_labels))
					if cal_acc(notsplitpreds, split_labels) >= cal_acc(split_pred, split_labels):
						notsplitvallist.append(val)
						print(notsplitvallist)
						if valclass[val] not in notsplitclass2val:
							notsplitclass2val[valclass[val]] = []
						notsplitclass2val[valclass[val]].append(val)
					else:
						break


			if self.tree_type in ['c45', 'cart']:
				split_acc = cal_acc(split_pred, split_labels)
				if split_acc < notsplit_acc:
					return trylabel

		if self.tree_type == 'c45':
			for val in vals:
				subset = splitdataset(traindata, bestFeature, val)
				subtestdataset = splitdataset(testdata, bestFeature, val)
				tree[bestFeature][val] = self.buildtree(subset, subtestdataset)
		elif self.tree_type == 'cart':
			subset, notset = splitdataset(traindata, bestFeature, bestvalue, True)
			subtestdataset, nottestdataset = splitdataset(testdata, bestFeature, bestvalue, True)
			tree[bestFeature][bestvalue] = self.buildtree(subset, subtestdataset)
			tree[bestFeature]['N'] = self.buildtree(notset, nottestdataset)
		elif self.tree_type == 'new':
			for cls in notsplitclass2val:
				idx = '-'.join([str(v) for v in notsplitclass2val[cls]])
				tree[bestFeature][idx] = valclass[notsplitclass2val[cls][0]]
			for val in vals:
				if val not in notsplitvallist:
					subset = splitdataset(traindata, bestFeature, val)
					subtestdataset = splitdataset(testdata, bestFeature, val)
					if len(subtestdataset) > 0:
						tree[bestFeature][val] = self.buildtree(subset, subtestdataset)
		if self.post_pruning:
			split_pred = [self.predict(d, tree) for d in testdata]
			split_acc = cal_acc(split_pred, labels)
			if split_acc < notsplit_acc:
				return trylabel


		return tree


	def runtree(self, testdata):
		pre = [self.predict(d) for d in testdata]
		# print(pre)
		labels = [d[-1] for d in testdata]
		return cal_acc(pre, labels)

	def predict(self, data, tmptree=None):
		tree = tmptree if tmptree else self.tree
		while isinstance(tree, dict):
			feature = list(tree.keys())[0]
			node = data[feature]
			fs = []
			for k in tree[feature]:
				if isinstance(k, int) or isinstance(k, float):
					fs.append(k)
				if isinstance(k, str):
					if '-' in k:
						fs += [int(v) for v in k.split('-')]
					else:
						fs.append(k)
			if data[feature] not in tree[feature]:
				if 'N' in tree[feature]:
					node = 'N'
				elif data[feature] in fs:
					for k in tree[feature]:
						if isinstance(k, str) and str(data[feature]) in k:
							node = k
							break
				else:
					node = random.choice(list(tree[feature].keys())) 
			try:
				tree = tree[feature][node]
			except:
				print(feature, data[feature])
				print(tree)
				raise
		return tree

	def findfeature(self, dataset):
		bestfeaturevalue = -10000000
		bestfeature = None
		bestvalue = None
		for idx in range(len(dataset[0]) - 1):
			try:
				idxvalue, givalue = self.feature_metric(dataset, idx)
			except:
				print(idx)
				print(self.tree)
				print(set([d[idx] for d in dataset]))
				raise

			if idxvalue > bestfeaturevalue:
				bestfeaturevalue = idxvalue
				bestfeature = idx
				bestvalue = givalue
		return bestfeature, bestvalue
