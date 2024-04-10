import json
import csv

# Create the dictionary here
zip_code_data = {}
file =  open("data/data_original.csv", "r", newline="")
reader = csv.reader(file)
header = next(reader)  

for row in reader:
    borough, zip_code, date_collected, *data_values = row
    if zip_code not in zip_code_data:
       zip_code_data[zip_code] = {}
    if borough not in zip_code_data[zip_code]:
        zip_code_data[zip_code][borough] = {}
    zip_code_data[zip_code][borough][date_collected] = data_values

#Save the json object to a file
f2 = open("micro.json", "w")
json.dump(zip_code_data, f2, indent=4)

f2.close()