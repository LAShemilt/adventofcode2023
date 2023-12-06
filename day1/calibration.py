
import re

with open("./calibration_string") as f:
    lines = f.readlines()

coords = 0
for line in lines:
    numbers = re.findall(r'\d+', str(line))
    if len(numbers) > 1:
        coord= numbers[0][0] + numbers[-1][-1]
    elif len(numbers)==1:
        if len(numbers[0])==1:
            coord= numbers[0][0]+numbers[0][-1]
        else:
            coord= numbers[0][0] + numbers[0][-1]
    else: 
        coord=0
    coords = coords + int(coord)

print(coords)

   