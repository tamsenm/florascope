# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:32:23 2020

@author: tamsen
"""
#libraries
import numpy as np

#import data
file_name = 'plants-csv.csv'
print("fileName: ", file_name)
raw_data = open(file_name, 'rt')
initial = np.loadtxt(raw_data, dtype = np.str, usecols = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), skiprows = 1, delimiter = ",")

#add column for weights
data = np.append(initial, np.zeros([len(initial), 1]), 1)

#takes in a dictionary object and a list and converts the values in the list based on the dictionary
def convert_vals(dict, list):
    for i in range(len(list)):
        list[i] = dict[list[i]]
    return list

#convert all non-numerical data to numbers
vals = {"No":0,"Yes":1,"Moderate":0.5,"Low":0,"High":1,"Full sun":4,"Part sun":3,"Part shade":2,"Full shade":1,"Annual":0,"Perennial":1,"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
for i in [3,4,5,6,7,8,10,11,16,17,18,20]:
    data[:,i] = convert_vals(vals,data[:,i])

#prompt user (these questions and the format of their answers will be changed in the webapp)
plant_season_input = input("When will you be planting your garden? 1 = Spring, 2 = Summer, 3 = Fall ")
season_dict = {"1":range(3,6),"2":range(6,9),"3":range(9,12)}
bloom_season_input = input("When will you be planting your garden? 1 = Spring, 2 = Summer, 3 = Fall ")
dimension_input = input("What are the dimensions of your garden plot (inches x inches) ")
height_bool = input("Do you have any restrictions for the height of your garden? (Y/N) ")
max_height = 0
if height_bool == "Y":
    height_input = input("What is the maximum height the plants in your garden can be? (inches) ")
sun_input = input("How much sun does your garden receive? (1 = full sun, 2 = part sun, 3 = part shade, 4 = full shade ")
print("\n1. Moist\n2. Dry\n3. Sandy\n4. Well-drained\n5. Acidic\n6. Neutral\n7. Clay\n8. Humus-Rich\n9. Loamy\n10. Nutrient-rich\n11. Tolerant")
soil_input = input("Which of these adjectives describe your soil? (ex: 2,5,7,8) ")
deer_input = input("Is your garden at risk for being eaten by deer? (Y/N) ")
enviro_input = input("Environmental issues: 1. Native plants 2. Low water consumption 3. Wildlife attraction 4. Nitrogen fixing. ex: 1,3,4 ")
wildlife_input = 0
if "3" in enviro_input:
    wildlife_input = input("Wildlife: 1. Butterflies, 2. Monarchs, 3. Bees, 4. Birds, 5. Hummingbirds, 6. Toads, 7. Lizards ")

#calculate weights
for i in range(len(data)):
    #seasons
    weight = 0
    plant_season = season_dict[plant_season_input]
    overlap = [value for value in plant_season if value in range(int(data[i,3]),int(data[i,4])+1)]
    if len(overlap) >= 1:
        weight += 4
    else:
        weight -= 8
    bloom_season = season_dict[bloom_season_input]
    overlap = [value for value in bloom_season if value in range(int(data[i,5]),int(data[i,6])+1)]
    if len(overlap) >= 1:
        weight += 4
    else:
        weight -= 8
        
    #dimensions
    dimensions = int(dimension_input.split("x")[0])*int(dimension_input.split("x")[1])
    percent = (float(data[i,9])*float(data[i,9])) / (float(dimensions))
    if percent <= 0.25:
        weight += 3
    else:
        weight -= 5
    if int(height_input) > 0:
        if int(data[i,14]) > int(height_input):
            weight -= 500
            
    #sun
    sun_range = range(int(data[i,11]),int(data[i,10])+1)
    sun_input = int(sun_input)
    if sun_input in sun_range:
        weight += 5
    elif abs(sun_range[0]-sun_input) == 1 or abs(sun_range[len(sun_range)-1]-sun_input) == 1:
        weight += 0
    elif abs(sun_range[0]-sun_input) == 2 or abs(sun_range[len(sun_range)-1]-sun_input) == 2:
        weight -= 5
    else:
        weight -= 15
        
    #soil
    soil_dict = {"moist":"1","dry":"2","sandy":"3","well-drained":"4", "acidic":"5","neutral":"6","clay":"7","humus-rich":"8","loamy":"9","nutrient-rich":"10","tolerant":"11"}
    soil_data = data[i,12].split(" ")
    for j in range(len(soil_data)):
        soil_data[j] = soil_dict[soil_data[j].lower()]
    soil = soil_input.split(",")
    overlap = [value for value in soil_data if value in soil]
    weight += (3/len(soil))*len(overlap)
    
    #deer resistance
    if deer_input == "Y":
        if data[i,16] == "0":
            weight -= 100
        elif data[i,16] == "1":
            weight += 3
            
    #environmental issues
    enviro_data = []
    if data[i,17] == 1:
        enviro_data.append("1")
    if data[i,18] == 0:
        enviro_data.append("2")
    if data[i,20] == 1:
        enviro_data.append("4")
    wildlife_dict = {"butterflies":"1", "monarchs":"2", "bees":"3", "birds":"4", "hummingbirds":"5", "toads":"6", "lizards":"7"}
    wildlife_data = data[i,19].split(" ")
    for j in range(len(wildlife_data)):
        wildlife_data[j] = wildlife_dict[wildlife_data[j].lower()]
    if "3" in enviro_input:
        wildlife = wildlife_input.split(",")
        overlap = [value for value in wildlife_data if value in wildlife]
        if len(overlap) > 0:
            enviro_data.append("4")
    enviro = enviro_input.split(",")
    overlap = [value for value in enviro_data if value in enviro]
    weight += (12/len(enviro))*len(overlap)
    
    #set weight in list
    data[i,21] = weight/25*100
  
#order list
max_idx = 0
for i in range(len(data)):
    for j in range(i,len(data)):
        if float(data[j,21]) > float(data[max_idx,21]):
            max_idx = j
    temp = np.copy(data[i,:])
    data[i,:]= data[max_idx,:]
    data[max_idx,:] = temp
    
#output positive percentages
for i in range(len(data)):
    if float(data[i,21]) > 0:
        print(int(round(float(data[i,21]),1)),"percent match with",data[i,0], "-",data[i,1])