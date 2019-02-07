
def mergeSort(arr): #https://www.geeksforgeeks.org/merge-sort/
    if len(arr) >1: 
        mid = len(arr)//2 #Finding the mid of the array 
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
  


class inverted_index():
	def __init__(self, lexicon_array=[]):
		self.lexicon_array = lexicon_array
		
	def sort_lexicon(self):
		self.lexicon_array = mergeSprt(self.lexicon_array)
		
	def add_to_lexicon(self, timestamp):
		if type(timestamp) == str:
			self.lexicon_array.append
		if type(timestamp) == list:
			self.lexicon_array = self.lexicon_array + timestamp
		self.sort_lexicon()
	
		