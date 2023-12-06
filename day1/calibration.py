
import re
import numpy as np

numbers_as_words={'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9'}

def simple_int_calibration():
    with open("./calibration_string") as f:
        lines = f.readlines()

    coords = 0
    with open("./output_simple",'+w') as f:
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

            f.write(f'{line} {coord} \n')

def complex_int_word_calibration():
       
    sum_coords = []
    with open("./calibration_string") as f:
        lines = f.readlines()

    with open("./ouput", "w+") as f:
        for line in lines:
            # create int mask to find position of integers
            int_mask=[]
            for n in range(0,len(line)):
                try:
                    int(line[n])
                    int_bool=1
                except ValueError:
                    int_bool = 0
                int_mask.append(int_bool)
            
        
            where_int = np.where(int_mask)[0]
            
            # find all the words
            where_word={}
            for key in numbers_as_words.keys():
                if key in line:
                    # you need both if the word is in the line twice!
                    min_idx = str(line).index(key)
                    max_idx = str(line).rindex(key)
                    if max_idx == min_idx:
                        where_word[min_idx] = numbers_as_words[key]
                    else:
                         where_word[min_idx] = numbers_as_words[key]
                         where_word[max_idx] = numbers_as_words[key]

        
            if len(where_word) > 0:
                min_word_pos  =sorted(where_word.keys())[0]   
                min_num_pos = where_int[0]
                if min_num_pos < min_word_pos:
                    coord_1 = line[min_num_pos]
                else:
                    coord_1 = where_word[min_word_pos]
                
                max_word_pos =sorted(where_word.keys())[-1]  
                max_num_pos = where_int[-1]
                if max_num_pos > max_word_pos:
                    coord_2 = line[max_num_pos]
                else:
                    coord_2 = where_word[max_word_pos]
            else:
                coord_1 = line[where_int[0]]
                coord_2 = line[where_int[-1]]
            
            coords = str(coord_1) + str(coord_2)
            sum_coords.append(int(coords))

            f.write(f'{line} : {where_word}: {coords}\n')

    print(np.sum(sum_coords))
        




if __name__ == '__main__':
    simple_int_calibration()
    complex_int_word_calibration()

   