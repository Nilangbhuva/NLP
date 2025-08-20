import re

class GujaratiSentenceTokenizer:
    def __init__(self):
        # Patterns to protect
        self.protection_patterns = {
            'url': r'https?://[^\s]+\.\w+',
            'email': r'[\w\.-]+@(\w\.)+\w+',
            'date': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s*(જાન્યુઆરી|ફેબ્રુઆરી|માર્ચ|એપ્રિલ|મે|જૂન|જુલાઈ|ઑગસ્ટ|સપ્ટેમ્બર|ઑક્ટોબર|નવેમ્બર|ડિસેમ્બર)+\s*\d{2,4}',
            'ellipsis': r'\.\.\.',
            'num_dot': r'(?:\d+|[\u0AE6-\u0AEF]+)\.',
            'guj_matra_dot': r'([\u0A80-\u0AFF]+[\u0ABE-\u0ACC\u0A81-\u0A83\u0ACD]+)\.'
        }
        
        # Protect abbreviations (e.g., Dr., Mr., શ્રી. , etc. and Gujarati abbreviations)
        self.abbreviations = [
            r'Dr\.', r'Mr\.', r'Mrs\.', r'Ms\.', r'Prof\.', r'Sr\.', r'Jr\.', r'St\.', r'vs\.', r'etc\.', r'e\.g\.', r'i\.e\.', r'a\.m\.', r'p\.m\.',
            r'એલ\.સી\.બી\.', r'પી\.એસ\.આઇ\.', r'શ્રી\.', r'શ્રીમતી\.', r'કું\.', r'શ્રીમ\.', r'ડૉ\.', r'પ્રો\.', r'સ્વ\.'
        ]
        
        # Use a more reliable method to split sentences
        # Split at sentence ending punctuation
        self.sentence_boundary_pattern = r'([\.!?।\u0964])\s+'
        
        self.protected_items = []

    def _create_placeholder(self, match):
        # Protect URLs, emails, dates, ellipsis by replacing them with placeholders
        self.protected_items.append(match.group(0))
        return f"__PROTECTED_{len(self.protected_items)-1}__"

    def _protect_special_patterns(self, text):
        # Protect ellipsis (three dots)
        text = re.sub(self.protection_patterns['ellipsis'], self._create_placeholder, text)
        text = re.sub(self.protection_patterns['url'], self._create_placeholder, text)
        text = re.sub(self.protection_patterns['email'], self._create_placeholder, text)
        text = re.sub(self.protection_patterns['date'], self._create_placeholder, text)
        
        abbr_pattern = r'(' + '|'.join(self.abbreviations) + r')'
        text = re.sub(abbr_pattern, self._create_placeholder, text)
        
        # Protect numbers (Gujarati/English) followed by dot (e.g., 18. or ૧૮.)
        text = re.sub(self.protection_patterns['num_dot'], self._create_placeholder, text)
        
        # Protect words with matra followed by dot (e.g., "તા.")
        text = re.sub(self.protection_patterns['guj_matra_dot'], self._create_placeholder, text)
        
        return text

    def _restore_protected_items(self, text):
        # Restore protected items
        for idx, item in enumerate(self.protected_items):
            text = text.replace(f"__PROTECTED_{idx}__", item)
        return text

    def _split_into_sentences(self, text):
        # Split the text but keep the punctuation
        parts = re.split(self.sentence_boundary_pattern, text)
        
        sentences = []
        i = 0
        while i < len(parts) - 1:
            if i + 1 < len(parts):
                sentence = parts[i] + parts[i + 1]
            else:
                sentence = parts[i]
            
            sentence = self._restore_protected_items(sentence.strip())
            if sentence:
                sentences.append(sentence)
            i += 2
        
        # Handle the last part if there's no ending punctuation
        if len(parts) % 2 == 1 and parts[-1].strip():
            last_part = self._restore_protected_items(parts[-1].strip())
            if last_part:
                sentences.append(last_part)
        
        return sentences

    def _merge_short_sentences(self, sentences):
        # Merge sentences with less than 3 words with previous sentence
        merged = []
        for sentence in sentences:
            if merged and len(sentence.split()) < 3:
                merged[-1] = merged[-1].rstrip() + ' ' + sentence
            else:
                merged.append(sentence)
        return merged

    def tokenize(self, text):
        self.protected_items = []  # Reset for each tokenization
        
        protected_text = self._protect_special_patterns(text)
        raw_sentences = self._split_into_sentences(protected_text)
        final_sentences = self._merge_short_sentences(raw_sentences)
        
        return final_sentences

def gujarati_sentence_tokenizer(text):
    tokenizer = GujaratiSentenceTokenizer()
    return tokenizer.tokenize(text)

# Example usage:
if __name__ == "__main__":
    def read_input_file(filename):
        with open(filename, encoding="utf-8") as f:
            return f.read()
    
    def write_sentences_to_file(sentences, filename):
        # Write sentences to a new file, each on a new line
        with open(filename, "w", encoding="utf-8") as out:
            for s in sentences:
                out.write(s + "\n")
    
    def calculate_text_metrics(sentences):
        # --- Metrics calculation ---
        total_sentences = len(sentences)
        total_words = sum(len(s.split()) for s in sentences)
        total_chars = sum(len(s) for s in sentences)
        words_per_sentence = total_words / total_sentences if total_sentences else 0
        avg_chars_per_word = total_chars / total_words if total_words else 0
        
        # TTR for sentence tokenizer: unique words divided by total words
        all_words = []
        for s in sentences:
            all_words.extend(s.split())
        ttr = len(set(all_words)) / total_words if total_words else 0
        
        return {
            'total_sentences': total_sentences,
            'total_words': total_words,
            'total_chars': total_chars,
            'words_per_sentence': words_per_sentence,
            'avg_chars_per_word': avg_chars_per_word,
            'ttr': ttr
        }
    
    def write_metrics_to_file(metrics, filename):
        with open(filename, "w", encoding="utf-8") as m:
            m.write(f"Total sentences: {metrics['total_sentences']}\n")
            m.write(f"Total words: {metrics['total_words']}\n")
            m.write(f"Total characters: {metrics['total_chars']}\n")
            m.write(f"Words per sentence: {metrics['words_per_sentence']:.2f}\n")
            m.write(f"Average characters per word: {metrics['avg_chars_per_word']:.2f}\n")
            m.write(f"Type-Token Ratio (TTR): {metrics['ttr']:.4f}\n")
    
    # Main execution flow
    text = read_input_file("gu.txt")
    sentences = gujarati_sentence_tokenizer(text)
    write_sentences_to_file(sentences, "gu_sentences.txt")
    
    metrics = calculate_text_metrics(sentences)
    write_metrics_to_file(metrics, "gu_sentences_metrics.txt")