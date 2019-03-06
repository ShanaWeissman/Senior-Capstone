
# Returns index of x in arr if present, else -1 
def binarySearch_rec (arr, l, r, x):     #https://www.geeksforgeeks.org/binary-search/
  
    # Check base case 
    if r >= l: 
  
        mid = l + (r - l)//2
  
        # If element is present at the middle itself 
        if arr[mid] == x: 
            return mid 
          
        # If element is smaller than mid, then it  
        # can only be present in left subarray 
        elif arr[mid] > x: 
            return binarySearch_rec(arr, l, mid-1, x) 
  
        # Else the element can only be present  
        # in right subarray 
        else: 
            return binarySearch_rec(arr, mid + 1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1

def binarySearch(arr, val):            #To make calling it easier
    return(binarySearch_rec(arr, 0, len(arr)-1, val))
    

def mergeSort(arr): #https://www.geeksforgeeks.org/merge-sort/
    if len(arr) > 1: 
        mid = len(arr)//2
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1
  

#class inverted_list():
    
class inverted_index():
    def __init__(self, lexicon_array=[], n=0):
        self.lexicon_array = lexicon_array
        self.n = n #number of items in lexicon
        
    def sort_lexicon(self):
        mergeSort(self.lexicon_array)
        
    def insert_value(self, timestamp):
        self.lexicon_array.append(timestamp)
        self.n += 1
        self.sort_lexicon()
        
    #def remove_value(self, timestamp):
        

    def point_search(self, target_timestamp):
        target_timestamp_index = binarySearch(self.lexicon_array, target_timestamp)
        return(target_timestamp_index)
        
    def bounded_range_search(self, l, r):
        l_index = binarySearch(self.lexicon_array, l)
        r_index = binarySearch(self.lexicon_array, r)
        return(self.lexicon_array[l_index:r_index])
        
    def unbounded_range_search(self, l, r): #There are many unbounded query options
        l_index = binarySearch(self.lexicon_array, l)
        r_index = binarySearch(self.lexicon_array, r)        
        return(self.lexicon_array[:l_index] + self.lexicon_array[r_index:])
        
    def remove_value(self, timestamp):
        self.n = self.n - 1
        target_timestamp = binarySearch(self.lexicon_array, timestamp)
        #placeholder = self.lexicon_array
        #self.lexicon_array = placeholder[:target_timestamp] + placeholder[target_timestamp + 1:]
        self.lexicon_array.pop(target_timestamp)
    def show_index(self):
        for i in self.lexicon_array:
            print(str(i))
            
    def get_size(self):
    	return(len(self.lexicon_array))

'''
if __name__=="__main__":
    x = [6,2,1,5,8]
    mergeSort(x)
    print(x)
'''