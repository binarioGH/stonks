from json import dumps


DATA = {}

with open("owo.csv", "r") as f:
	content = f.read().split("\n")

	for line in content:
		sep = line.split("-")
		print(sep)
		print(line)
		try:
			symbol = sep[0]
			desc = sep[1]
			if 'Common Stock' in desc:
				desc = desc.split('Common Stock')[0]
		except:
			continue
		else:
			DATA[desc] = symbol


with open("symbol.json", "w") as f:
	f.write(dumps(DATA, indent=4))