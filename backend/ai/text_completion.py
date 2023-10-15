from fast_autocomplete import AutoComplete

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        
    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

class TextCompletion:
    trie = Trie()
    
    def main(self, word_list):
        trie = Trie()
        for word in word_list:
            trie.insert(word)
            
        current_input = ""
        while True:
            user_input = input("Enter text: ")
            current_input += user_input
            
            suggested_words = self.complete_text(current_input, trie)
            print(f"Suggested words: {suggested_words}")
            
            if user_input == "":
                break

    def complete_text(self, prefix, trie, max_suggestions=5):
        node = trie.search(prefix)
        if not node:
            return []
        
        def find_words(node, current_word, suggestions):
            if len(suggestions) >= max_suggestions:
                return
            
            if node.is_end_of_word:
                suggestions.append(current_word)
            
            for char, child_node in node.children.items():
                find_words(child_node, current_word + char, suggestions)
                
        suggestions = []
        find_words(node, prefix, suggestions)
        return suggestions


    # Define a function to read and process the text file
    def read_words_file(self, file_path):
        word_dict = {}
        
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    word = line.strip()  # Remove leading/trailing whitespace
                    word_dict[word] = {}  # Create an empty dictionary for each word
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        
        return word_dict

    def suggest_word(self, sentence):
        word = sentence.split()[-1]
        words = self.read_words_file('instance/1-1000.txt')
        autocomplete = AutoComplete(words=words)
        return autocomplete.search(word=word, max_cost=3, size=3)
    