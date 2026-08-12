import re
import os
import time

text_path=os.path.join(os.path.dirname(__file__), 'sample.txt')

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

class Analyzer():
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            text = f.read()
        self.words = re.findall(r"[a-z]+", text.lower())
        self.freq = {}
        for word in self.words:
            if word in self.freq:
                self.freq[word]+=1
            else:
                self.freq[word]=1

    def __len__(self):
        return len(self.words)

    def __str__(self):
        most_common= max(self.freq, key=self.freq.get)

        return (
            f"File Name: {self.file_path}\n"
            f"Total Words: {len(self.words)}\n"
            f"Unique Words: {len(self.freq)}\n"
            f"Most Common Word: '{most_common}' (Frequency: {self.freq[most_common]})"
        )

    def __contains__(self, item):
        return item in self.freq

    @property
    def unique_word_count(self):
        return len(self.freq)

    @property
    def most_common(self):
        most_common_word = max(self.freq, key=self.freq.get)
        return most_common_word

    def get_top_words(self,n):
        sorted_words = sorted(self.freq, key=lambda x: self.freq[x], reverse=True)
        for word in sorted_words[:n]:
           yield word, self.freq[word]

    def search_pattern(self, pattern):
        return [word for word in self.freq if re.search(pattern, word)]

    def make_filter(self, min_freq):
        def filter_func():
           return [word for word in self.freq if self.freq[word] >= min_freq]
        return filter_func


@timer
def main():
    analyzer = Analyzer(text_path)

    # 3. print summary
    print(analyzer)

    # 4. print total words(__len__ needed)
    print(f"\nTotal word count: {len(analyzer)}")

    # 5. most common word (property)
    print(f"Most common word: {analyzer.most_common}")

    # 6. top N words
    n = int(input("\nHow many top words? "))
    print(f"\nTop {n} words:")
    for word, count in analyzer.get_top_words(n):
        print(f"  {word}: {count}")

    # 7. search pattern
    pattern = input("\nEnter search pattern: ")
    matches = analyzer.search_pattern(pattern)
    print(f"Matching words: {matches}")

    # 8. min frequency filter
    min_freq = int(input("\nMin frequency? "))
    filter_func = analyzer.make_filter(min_freq)
    print(f"Words appearing {min_freq}+ times: {filter_func()}")

    # 9. contains check
    word = input("\nEnter a word to search: ")
    if word in analyzer:
        print(f"'{word}' IS in the file ({analyzer.freq[word]} times)")
    else:
        print(f"'{word}' is NOT in the file")


if __name__ == "__main__":
    main()