import json

# Load the completions data
with open('completions.json', 'r') as f:
    completions = json.load(f)

# Create a readable summary
with open('word_completions_summary.txt', 'w') as f:
    f.write("Word Stem Completion Results\n")
    f.write("==========================\n\n")
    
    for stem, results in completions.items():
        f.write(f"Stem Pattern: {stem}\n")
        f.write("-" * 40 + "\n")
        
        if results:
            # Sort by frequency score
            sorted_results = sorted(results, key=lambda x: x['freq_score'], reverse=True)
            
            # Show top 10 completions
            f.write("Top completions (sorted by frequency):\n")
            for i, result in enumerate(sorted_results[:10], 1):
                freq = result['freq_score']
                if freq > 0:
                    freq_note = "very common" if freq > 0.9 else \
                               "common" if freq > 0.7 else \
                               "moderately common" if freq > 0.4 else \
                               "less common"
                else:
                    freq_note = "rare"
                
                f.write(f"{i}. {result['word']} (frequency: {result['freq_score']:.4f} - {freq_note})\n")
        else:
            f.write("No completions found\n")
        
        f.write("\n\n")

print("Results have been formatted and saved to 'word_completions_summary.txt'")

# Also create a CSV version with different columns for different frequency ranges
with open('word_completions_by_frequency.csv', 'w') as f:
    f.write("Stem,Very Common (>0.9),Common (0.7-0.9),Moderate (0.4-0.7),Less Common (0-0.4),Rare (0)\n")
    
    for stem, results in completions.items():
        very_common = []
        common = []
        moderate = []
        less_common = []
        rare = []
        
        for result in results:
            freq = result['freq_score']
            word = result['word']
            
            if freq > 0.9:
                very_common.append(word)
            elif freq > 0.7:
                common.append(word)
            elif freq > 0.4:
                moderate.append(word)
            elif freq > 0:
                less_common.append(word)
            else:
                rare.append(word)
        
        # Take top 3 from each category
        very_common = very_common[:3]
        common = common[:3]
        moderate = moderate[:3]
        less_common = less_common[:3]
        rare = rare[:3]
        
        # Format for CSV
        f.write(f'{stem},')
        f.write(f'"{"/".join(very_common)}",')
        f.write(f'"{"/".join(common)}",')
        f.write(f'"{"/".join(moderate)}",')
        f.write(f'"{"/".join(less_common)}",')
        f.write(f'"{"/".join(rare)}"\n')

print("Results have also been saved in CSV format to 'word_completions_by_frequency.csv'") 