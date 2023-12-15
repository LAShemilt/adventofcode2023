import numpy as np





def make_arr_from_file(fname):
    """ make an array from the engine schema_file"""
    with open(fname) as f:
        lines = f.readlines()

    engine = []

    for line in lines:
        line = line.strip('\n')
        prep_array= []
        for char in line:
            
            prep_array.append(char)     

        engine.append(prep_array)   

    engine = np.array(engine)
    return engine

def find_numbers(arr):
    """find the numbers in the array and return a mask"""
    mask = []
    dims = np.shape(arr)
    for i in range(0,dims[0]):
        for j in range(0, dims[1]):
            try: 
                int(arr[i,j])
                mask.append(int(1))
            except ValueError:
                mask.append(int(0))
    mask_arr = np.reshape(np.array(mask,dtype= np.int32 ), dims)
    return(mask_arr)
    

def find_characters(spec_chars, arr):
    """ find the location of special characters and return a mask"""
    dims = np.shape(arr)
    mask = np.zeros(dims)
    for i in range(0,dims[0]):
        for j in range(0, dims[1]):
            if arr[i,j] in spec_chars:
                # making a kernel mask by setting the 8 adjacent pixels to the special character to 10
                mask[i-1:i+2, j-1:j+2] = int(10)

    return(mask)

  


def find_adjacent_ones(mask, mask_dims):
    """ find all the number 1's adjacent to 11's in the mask"""
    for i in range(mask_dims[0]):
        for j in range(mask_dims[1]):
            if mask[i,j] == 11:
                if j-1 >= 0:
                    if mask[i,j-1] ==1:
                        mask[i,j-1] = 11
             
                if j + 1 < mask_dims[1]:
                    if mask[i,j+1] ==1:
                        mask[i,j+1] = 11
              
    return(mask)
    

if __name__=='__main__':
    special_chars= ['$','%','&','*','#','@','/','+','-','=','~',':',';','?','!','(',')','^']
    engine_arr = make_arr_from_file('./engine_schema')

    # create a mask for special characters and another for numbers 
    mask_numbers = find_numbers(engine_arr)
    mask_chars = find_characters(special_chars, engine_arr)

# find all the numbers adjacent to special characters by finding where the masks convolve
    mask = mask_numbers + mask_chars
    ind_all_numbers = np.where(mask==11)
    np.savetxt("mask.csv", mask,fmt="%d", delimiter=',')


# find all digits associcated with the one adjacent to the special characters

    mask_dims = np.shape(mask)

    # need to run this a second time to find those numbers 2 away so if you have *113 this would be in the mask 11,1,1
    for n in range(3):
        mask = find_adjacent_ones(mask, mask_dims)
   
    
    # select out the numbers adjacent to special chars, and set everything else to full stops
    engine_arr[mask!=11] = '.'
    
    # get the consecutive digits and add to a number list 
    numbers= []
    consect_digits =[]
    for line in engine_arr:
        for item in line:         
            if item!='.':
                consect_digits.append(item)
            else:
                if len(consect_digits) > 0:
                    numbers.append(int(''.join(consect_digits)))
                consect_digits = []


    print(numbers)
    # sum the list !!!!
    print(np.sum(np.array(numbers)))

