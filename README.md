# Schema Stem - Leadership Word Completion Tool

This repository contains tools for completing word stems related to implicit leadership traits using two different approaches:

1. **Frequency-Based Approach**: Uses BERT embeddings and word frequency data to find completions
2. **LangChain-GPT Approach**: Uses LangChain and GPT-4 to generate context-aware completions

## Features

- Complete word stems with exact letter position matching
- Two complementary approaches for word completion:
  - Statistical approach using word frequencies and BERT
  - AI-powered approach using GPT-4 and LangChain
- Detailed output with leadership relevance explanations
- Frequency rankings for word completions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/schema_stem.git
cd schema_stem
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
For frequency-based approach:
```bash
pip install -r requirements.txt
```

For LangChain-GPT approach:
```bash
pip install -r requirements_langchain.txt
```

## Usage

### Frequency-Based Approach

1. Prepare your word stems in `word_stems.txt` (one per line)
2. Run the stem completer:
```bash
python stem_completer.py
```

The output will be saved in multiple formats:
- `frequency_ranked_stems.txt`: Ranked completions with frequencies
- `stem_summary.txt`: Summary of all completions

### LangChain-GPT Approach

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

2. Run the LangChain bot:
```bash
python leadership_stem_bot.py
```

The output will be saved in `leadership_completions.txt` with detailed explanations of leadership relevance.

## File Structure

- `stem_completer.py`: Main script for frequency-based completions
- `leadership_stem_bot.py`: LangChain-based completion script
- `create_table.py`: Creates word frequency tables
- `format_results.py`: Formats and ranks completion results
- `word_stems.txt`: Input file for word stems
- `requirements.txt`: Dependencies for frequency-based approach
- `requirements_langchain.txt`: Dependencies for LangChain approach

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details
