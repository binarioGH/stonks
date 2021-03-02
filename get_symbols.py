from datapackage import Package

package = Package('https://datahub.io/core/nyse-other-listings/datapackage.json')

# print list of all resources:
print(package.resource_names)

# print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
    	output = ""
    	for line in resource.read():
    		output += ','.join(line)
    		output += "\n"

    	with open("owo.csv", "w") as f:
    		f.write(output)