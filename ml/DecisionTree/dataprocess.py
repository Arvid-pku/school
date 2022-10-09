import random
def data_pro(fp, ratio):
	cty = ["'United States'", 'Brazil', 'Spain', 'Egypt', "'New Zealand'", 'Bahamas', 'Burundi', 'Austria', 'Argentina', 'Jordan', 'Ireland', "'United Arab Emirates'", 'Afghanistan', 'Lebanon', "'United Kingdom'", "'South Africa'", 'Italy', 'Pakistan', 'Bangladesh', 'Chile', 'France', 'China', 'Australia', 'Canada', "'Saudi Arabia'", 'Netherlands', 'Romania', 'Sweden', 'Tonga', 'Oman', 'India', 'Philippines', "'Sri Lanka'", "'Sierra Leone'", 'Ethiopia', "'Viet Nam'", 'Iran', "'Costa Rica'", 'Germany', 'Mexico', 'Russia', 'Armenia', 'Iceland', 'Nicaragua', "'Hong Kong'", 'Japan', 'Ukraine', 'Kazakhstan', 'AmericanSamoa', 'Uruguay', 'Serbia', 'Portugal', 'Malaysia', 'Ecuador', 'Niger', 'Belgium', 'Bolivia', 'Aruba', 'Finland', 'Turkey', 'Nepal', 'Indonesia', 'Angola', 'Azerbaijan', 'Iraq', "'Czech Republic'", 'Cyprus']
	ethnicity = ["White-European", "Latino", "Others", "Black", "Asian", "'Middle Eastern '", "Pasifika", "'South Asian'", "Hispanic", "Turkish", "?"]
	relation = ["Self", "Parent", "'Health care professional'", "Relative", "Others", "?"]
	form_d = {
		'11': {'f': 0, 'm': 1},
		'12': {x: i for i, x in enumerate(ethnicity)},
		'13': {'no': 0, 'yes': 1},
		'14': {'no': 0, 'yes': 1},
		'15': {x: i for i, x in enumerate(cty)},
		'16': {'no': 0, 'yes': 1},
		'19': {x: i for i, x in enumerate(relation)},
		'20': {'NO': 0, 'YES': 1},
	}
	# remove 10, 17, 18
	def form_it(item):
		new_item = []
		for i, x in enumerate(item):
			if str(i) in form_d:
				new_item.append(form_d[str(i)][x])
			elif i in [10, 17, 18]:
				continue
			else:
				new_item.append(int(x))
		return new_item

	f = open(fp)
	data = f.readlines()
	f.close()
	data = [i.strip().split(',') for i in data]
	data = [[j for j in i if j] for i in data]
	data = [form_it(i) for i in data]
	random.seed(1321)
	random.shuffle(data)
	testlen = int(len(data) * ratio)
	return data[:testlen], data[testlen:2*testlen], data[2*testlen:]
	