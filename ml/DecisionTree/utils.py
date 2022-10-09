from cmath import log


def getMajority(dataset):
	vals = getUniVal(dataset, -1)
	majority = None
	maxcount = -1
	for val in vals:
		count = len([d for d in dataset if d[-1] == val])
		if count > maxcount:
			maxcount = count
			majority = val
	return majority

def cal_acc(pred, label):
	if len(pred) == 0:
		return 0
	return sum([1 for p, l in zip(pred, label) if p == l]) / len(pred)



def getUniVal(dataset, idx):
	val = [d[idx] for d in dataset]
	return set(val)

def splitdataset(dataset, idx, val, return_not=False):
	subdataset = []
	notdataset = []
	for d in dataset:
		if d[idx] == val:
			subdataset.append(d[:idx]+d[idx+1:])
		else:
			notdataset.append(d[:idx]+d[idx+1:])
	if return_not:
		return subdataset, notdataset
	return subdataset


def remove_features(dataset, idxs):
	newdataset = []
	for d in dataset:
		newd = []
		for idx in range(len(d)):
			if idx not in idxs:
				newd.append(d[idx])
		newdataset.append(newd)
	return newdataset


def cal_entropy(dataset):
	entropy = 0
	vals = getUniVal(dataset, -1)
	# print(vals)
	for val in vals:
		p = len([d for d in dataset if d[-1] == val]) / len(dataset)
		entropy -= p * log(p, 2).real
		# print(entropy>0)
	return entropy

def cal_infogain(dataset, idx):
	entropy = cal_entropy(dataset)
	# print('entropy')
	empiricalentropy = 0
	vals = getUniVal(dataset, idx)
	for val in vals:
		subset = splitdataset(dataset, idx, val)
		subentropy = cal_entropy(subset)
		empiricalentropy += subentropy * len(subset) / len(dataset)
	return entropy - empiricalentropy, 0

def cal_gainratio(dataset, idx):
	gain, _ = cal_infogain(dataset, idx)
	# print(gain)
	splitinfo = 0
	vals = getUniVal(dataset, idx)
	for val in vals:
		subset = splitdataset(dataset, idx, val)
		p = len(subset) / len(dataset)
		splitinfo -= p * log(p, 2).real
	return (gain / splitinfo), 0

def cal_gini_data(dataset):
	gini = 0
	vals = getUniVal(dataset, -1)
	for val in vals:
		p = len([d for d in dataset if d[-1] == val]) / len(dataset)
		gini += p * (1 - p)
	return gini

def cal_gini(dataset, idx):
	gini = 1000
	vals = getUniVal(dataset, idx)
	bestval = None
	for val in vals:
		subset, notset = splitdataset(dataset, idx, val, True)
		subgini = cal_gini_data(subset)
		notgini = cal_gini_data(notset)
		avg = subgini * len(subset) / len(dataset) + notgini * len(notset) / len(dataset)
		if avg < gini:
			gini = avg
			bestval = val
	return (-gini, val)