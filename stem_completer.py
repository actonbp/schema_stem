import re
import json
import requests
import os
from collections import defaultdict

class StemCompleter:
    def __init__(self):
        """
        Initialize the StemCompleter with a comprehensive word list.
        """
        print("Loading word list...")
        self.words = self._load_word_list()
        self.word_frequencies = self._load_word_frequencies()
        
    def _load_word_list(self):
        """
        Load a comprehensive word list from multiple sources.
        """
        word_file = 'word_list.txt'
        
        if os.path.exists(word_file):
            with open(word_file, 'r') as f:
                return set(word.strip().lower() for word in f)
        
        print("Downloading word lists...")
        words = set()
        
        # Multiple word list sources for better coverage
        urls = [
            "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt",
            "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        ]
        
        for url in urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    new_words = set(word.strip().lower() for word in response.text.split())
                    print(f"Added {len(new_words)} words from {url}")
                    words.update(new_words)
            except Exception as e:
                print(f"Error downloading from {url}: {str(e)}")
        
        # Save word list for future use
        with open(word_file, 'w') as f:
            f.write('\n'.join(sorted(words)))
        
        return words
        
    def _load_word_frequencies(self):
        """
        Load word frequency data for ranking results.
        """
        freq_file = 'word_frequencies.json'
        
        if os.path.exists(freq_file):
            with open(freq_file, 'r') as f:
                return json.load(f)
        
        print("Creating frequency dictionary...")
        frequencies = {}
        
        url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                words = response.text.split()
                total_words = len(words)
                for i, word in enumerate(words):
                    frequencies[word.lower()] = 1 - (i / total_words)
        except Exception as e:
            print(f"Error loading frequencies: {str(e)}")
        
        with open(freq_file, 'w') as f:
            json.dump(frequencies, f)
        
        return frequencies
    
    def _create_pattern_regex(self, stem_pattern):
        """
        Convert a stem pattern with spaces and underscores to a regex pattern.
        Example: '_ OY A L' -> '^.oy.l$'
        """
        # Remove spaces and convert to lowercase
        pattern = stem_pattern.lower()
        # Create pattern where _ matches exactly one character
        pattern = pattern.replace('_', '.')
        # Remove spaces and add start/end anchors
        pattern = '^' + ''.join(pattern.split()) + '$'
        return pattern
    
    def get_completions_for_stem(self, stem_pattern, top_k=50):
        """
        Get word completions for a given stem pattern using pattern matching.
        Now handles patterns with exact letter positions.
        """
        # Convert stem pattern to regex
        regex_pattern = self._create_pattern_regex(stem_pattern)
        regex = re.compile(regex_pattern, re.IGNORECASE)
        
        # Find matching words
        matches = []
        for word in self.words:
            # Remove spaces from word for matching
            word_clean = ''.join(word.split())
            if regex.match(word_clean):
                freq_score = self.word_frequencies.get(word, 0.0)
                matches.append({
                    'word': word,
                    'freq_score': freq_score
                })
        
        # Sort by frequency score
        matches.sort(key=lambda x: x['freq_score'], reverse=True)
        return matches[:top_k]

    def process_stem_file(self, input_file, output_file):
        """
        Process a file containing word stems and save results to a JSON file.
        """
        with open(input_file, 'r') as f:
            stems = [line.strip() for line in f if line.strip()]
        
        results = {}
        total_stems = len(stems)
        
        for i, stem in enumerate(stems, 1):
            print(f"\nProcessing stem {i}/{total_stems}: {stem}")
            completions = self.get_completions_for_stem(stem)
            results[stem] = completions
            
            if completions:
                print(f"\nTop completions for '{stem}':")
                for completion in completions[:5]:
                    print(f"  {completion['word']} (frequency score: {completion['freq_score']:.4f})")
            else:
                print(f"No completions found for '{stem}'")
        
        print(f"\nSaving results to {output_file}...")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

def main():
    """
    Main function to run the stem completion process.
    """
    print("Initializing StemCompleter...")
    completer = StemCompleter()
    
    results = completer.process_stem_file('word_stems.txt', 'completions.json')
    
    print("\nFinal Results Summary:")
    print("=" * 80)
    
    for stem, completions in results.items():
        if completions:
            print(f"\nCompletions for pattern '{stem}':")
            print("-" * 40)
            print(f"{'Word':<15} {'Frequency':>10}")
            print("-" * 40)
            
            for completion in completions[:10]:
                print(f"{completion['word']:<15} {completion['freq_score']:>10.4f}")
            print("=" * 80)
        else:
            print(f"\nNo completions found for pattern '{stem}'")
            print("=" * 80)

if __name__ == "__main__":
    main() 