import difflib

class SpellChecker:
    def __init__(self):
        self.word_list = self.read_words_file('instance/words.txt')
        
    def read_words_file(self, file_path):
        word_list = []
        
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    word = line.strip()  # Remove leading/trailing whitespace
                    word_list.append(word)  # Add the word to the list
            
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    
        return word_list
        
    def suggest(self, word):
        closest_words = difflib.get_close_matches(word, self.word_list)
        print(closest_words)
        if word not in self.word_list and closest_words:
            suggestion = min(closest_words, key=lambda x: self.levenshtein_distance(word, x)) #better?
            print('suggestion: ', suggestion)
            print('word_list: ', self.closest_word(word, self.word_list))
            print('closest_word: ', self.closest_word(word, closest_words))
            return suggestion
        return None
    
    def closest_word(self, input_word, word_list):
        closest_distance = float('inf')
        closest_word = None
        
        for word in word_list:
            distance = self.levenshtein_distance(input_word, word)
            if distance < closest_distance:
                closest_distance = distance
                closest_word = word
        
        return closest_word
    
    def levenshtein_distance(self, s1, s2):
        # Creates a matrix to store distances
        matrix = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]  # creates a 2D list (matrix) of zeros with dimensions (len(s1) + 1) x (len(s2) + 1)
        
        # Initialize the first row and column
        for i in range(len(s1) + 1): 
            matrix[i][0] = i # fill in the first column with range(len(s1) + 1)
        for j in range(len(s2) + 1):
            matrix[0][j] = j # fill in the first row with range(len(s2) + 1)
            
        # Fill in the matrix using dynamic programming
        for i in range(1, len(s1) + 1): 
            for j in range(1, len(s2) + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1 # cost is 0 if the characters are the same, 1 otherwise
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost) # fill in the current cell with the minimum of the three adjacent cells + cost
        
        i, j = len(s1), len(s2) 
        while i > 0 or j > 0: #itierates over the matrix until it reaches the top left corner
            if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]: #if the characters are the same, move diagonally
                i -= 1  #move diagonally
                j -= 1 
            elif i > 0 and matrix[i][j] == matrix[i - 1][j] + 1: #if the cost of the current cell is equal to the cost of the cell above + 1, move up
                i -= 1 #move up
            elif j > 0 and matrix[i][j] == matrix[i][j - 1] + 1: #if the cost of the current cell is equal to the cost of the cell to the left + 1, move left
                j -= 1 #move left
            else:
                i -= 1 #move diagonally
                j -= 1
                
        return matrix[len(s1)][len(s2)] #return the bottom right cell of the matrix (the distance between the two strings)

