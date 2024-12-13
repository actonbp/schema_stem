from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import CommaSeparatedListOutputParser
import os

# Template for completing leadership word stems
LEADERSHIP_PROMPT = """You are helping complete a measure of implicit leadership traits.
Given a word fragment with underscores (_) representing missing letters, provide possible completions
that relate to leadership characteristics.

Consider these aspects:
1. The word should fit the exact pattern (underscores represent exact letter positions)
2. The word should relate to leadership traits or characteristics
3. Provide a brief explanation of how the word relates to leadership

Word fragment to complete: {stem}
Required pattern: Each _ represents exactly one letter

Please provide:
1. Your top word completion
2. How this word relates to leadership
3. Alternative completions (if any)
4. Brief explanation of why this is a good leadership-related completion

Format your response as:
COMPLETION: [primary word]
LEADERSHIP RELEVANCE: [explanation]
ALTERNATIVES: [other possible words]
REASONING: [brief explanation]"""

class LeadershipStemBot:
    def __init__(self, api_key=None):
        """Initialize the bot with OpenAI API key."""
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7
        )
        
        self.prompt = ChatPromptTemplate.from_template(LEADERSHIP_PROMPT)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def complete_stem(self, stem):
        """Complete a single word stem."""
        return self.chain.run(stem=stem)
    
    def process_stems(self, stems):
        """Process multiple stems and return results."""
        results = []
        for stem in stems:
            completion = self.complete_stem(stem)
            results.append({
                'stem': stem,
                'completion': completion
            })
        return results

def main():
    # Example stems from your measure
    stems = [
        "_ OY A L",
        "_ ATURE",
        "HON _ _",
        "BRA _ _ _",
        "_ _ ART",
        "THOU _ _ _ _ _ _",
        "CHAR _ _ _ _",
        "L _ VLEY",
        "_ _ MBLE",
        "CRE _ _ _ _ _",
        "SENS _ _ _ _ _",
        "_ OC _ _ _",
        "_ A L M",
        "_ A I R",
        "W A _ _",
        "BRU _ _ _",
        "_ _ _ ONG",
        "F I _ _",
        "_ AN _ _",
        "C O _ _ _",
        "C R U _ _"
    ]
    
    # You'll need to provide your OpenAI API key
    bot = LeadershipStemBot(api_key="your-api-key-here")
    
    print("Processing leadership word stems...")
    results = bot.process_stems(stems)
    
    # Print results
    print("\nCompletion Results:")
    print("=" * 50)
    for result in results:
        print(f"\nStem: {result['stem']}")
        print(f"Response:\n{result['completion']}")
        print("-" * 50)
    
    # Save results to file
    with open('leadership_completions.txt', 'w') as f:
        f.write("LEADERSHIP WORD STEM COMPLETIONS\n")
        f.write("==============================\n\n")
        for result in results:
            f.write(f"Stem: {result['stem']}\n")
            f.write(f"Response:\n{result['completion']}\n")
            f.write("-" * 50 + "\n")

if __name__ == "__main__":
    main() 