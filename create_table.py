import json
import pandas as pd

# Load the completions data
with open('completions.json', 'r') as f:
    completions = json.load(f)

# Define the structure of the original table
data = {
    'ILT Dimension': [
        'DEDICATED',
        '_OYAL',
        '_ATURE',
        'HON__',
        'Intelligent',
        'BRA___',
        '__ART',
        'THOU_____',
        'Dynamic',
        'CHAR_____',
        'L_VLEY',
        '__MBLE',
        'CRE_____',
        'Sensitive*',
        'SENS_____',
        '_OC___',
        '_ALM',
        '_AIR',
        'WA__',
        'Tyrannical*',
        'BRU___',
        '___ONG',
        'FI__',
        'Masculine',
        '_AN_',
        'CO___',
        'CRU__'
    ],
    'ILT Response': [
        '',
        'Loyal',
        'Mature',
        'Honor',
        '',
        'Brainy',
        'Smart',
        'Thoughtful',
        '',
        'Charisma',
        'Lively',
        'Humble',
        'Creative',
        '',
        'Sensitive',
        'Social',
        'Calm',
        'Fair',
        'Warm',
        '',
        'Brutal',
        'Strong',
        'Firm',
        '',
        'Manly',
        'Cocky',
        'Cruel'
    ],
    'Distractor': [
        '',
        'Royal',
        'Nature',
        'Honey',
        '',
        'Branch',
        'Chart/Heart',
        'Thousand',
        '',
        'Charming, Charcoal',
        'Lovely',
        'Gamble',
        'Credible',
        '',
        'Sensation',
        'Docile',
        'Palm',
        'Hair',
        'Wary',
        '',
        'Bruise',
        'Stress',
        'Fire',
        '',
        'Fancy',
        'Corny',
        'Crush'
    ],
    'Correlation': [
        '',
        '.06',
        '.22',
        '.23',
        '',
        '.56',
        '.20',
        '.17',
        '',
        '.35',
        '.43',
        '.27',
        '.05',
        '',
        '.07',
        '.01',
        '.46',
        '.07',
        '.14',
        '',
        '.75',
        '.80',
        '.69',
        '',
        '.79',
        '.16',
        '.04'
    ],
    'Significance': [
        '',
        '.74',
        '.21',
        '.19',
        '',
        '.001',
        '.22',
        '.45',
        '',
        '.04',
        '.01',
        '.13',
        '.77',
        '',
        '.70',
        '.95',
        '.003',
        '.68',
        '.41',
        '',
        '.001',
        '.001',
        '.001',
        '',
        '.001',
        '.36',
        '.82'
    ]
}

# Add frequency scores for ILT Response and Distractor words
def get_word_freq(word, stem_completions):
    if not word or word == '':
        return ''
    # Handle multiple words (e.g., "Chart/Heart")
    words = word.lower().replace(',', '').split('/')
    freqs = []
    for w in words:
        w = w.strip()
        for completion in stem_completions:
            if completion['word'].lower() == w:
                freqs.append(f"{completion['freq_score']:.4f}")
                break
        else:
            freqs.append('N/A')
    return '/'.join(freqs)

# Add frequency columns
data['ILT Response Freq'] = []
data['Distractor Freq'] = []

for i, stem in enumerate(data['ILT Dimension']):
    ilt_word = data['ILT Response'][i]
    distractor = data['Distractor'][i]
    
    stem_completions = completions.get(stem, [])
    
    data['ILT Response Freq'].append(get_word_freq(ilt_word, stem_completions))
    data['Distractor Freq'].append(get_word_freq(distractor, stem_completions))

# Create DataFrame
df = pd.DataFrame(data)

# Format the table
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)

# Save to CSV and display
df.to_csv('word_frequencies_table.csv', index=False)
print("\nTable with Word Frequencies:")
print("=" * 120)
print(df.to_string(index=False))
print("\nTable has been saved to 'word_frequencies_table.csv'") 