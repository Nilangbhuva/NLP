import re

def gujarati_word_tokenizer(text):
    # Patterns for URLs, emails, dates, numbers with commas/periods
    url_pattern = r'https?://[^\s]+'
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s*[જાન્યુઆરી|ફેબ્રુઆરી|માર્ચ|એપ્રિલ|મે|જૂન|જુલાઈ|ઑગસ્ટ|સપ્ટેમ્બર|ઑક્ટોબર|નવેમ્બર|ડિસેમ્બર]+\s*\d{2,4}'
    # Numbers with commas or periods (English and Gujarati)
    num_pattern = r'(?:[\d\u0AE6-\u0AEF]+(?:[\.,][\d\u0AE6-\u0AEF]+)+)'
    # English numbers followed by a dot (e.g., 49.)
    eng_num_dot_pattern = r'\d+\.'
    # Gujarati numbers (standalone)
    guj_num_pattern = r'[\u0AE6-\u0AEF]+'
    # English numbers (standalone)
    eng_num_pattern = r'\d+'
    # Gujarati words
    guj_word_pattern = r'[\u0A80-\u0AFF]+(?:[\u0ABE-\u0ACC\u0A81-\u0A83\u0ACD]*)'
    # Punctuation
    punct_pattern = r'[\.।\u0964,!?…]' # includes . | danda | gujarati full stop | , ! ? …
    # Ellipsis
    ellipsis_pattern = r'\.\.\.'

    # Combine all patterns
    combined_pattern = f'({url_pattern})|({email_pattern})|({date_pattern})|({eng_num_dot_pattern})|({num_pattern})|({ellipsis_pattern})|({punct_pattern})|({guj_num_pattern})|({eng_num_pattern})|({guj_word_pattern})'
    words = [w for w in re.findall(combined_pattern, text)]
    # Flatten and filter empty
    flat_words = []
    for tup in words:
        for w in tup:
            if w:
                flat_words.append(w)
    return flat_words

if __name__ == "__main__":
    with open("gu.txt", encoding="utf-8") as f:
        text = f.read()
    words = gujarati_word_tokenizer(text)
    with open("gu_words.txt", "w", encoding="utf-8") as out:
        for word in words:
            # Only start a new line for sentence-ending punctuation, not for numbers with .
            # If word matches English number followed by dot, do not end line
            if re.match(r'^\d+\.$', word):
                out.write(word + ' ')
            elif word in ['.', '।', '\u0964', '…', '...']:
                out.write(word + '\n')
            else:
                out.write(word + ' ')
    # --- Metrics calculation ---
    total_words = len(words)
    total_chars = sum(len(w) for w in words)
    # Words per sentence: count lines in gu_words.txt that end with sentence-ending punctuation
    sentence_endings = ['.', '।', '\u0964', '…', '...']
    with open("gu_words.txt", encoding="utf-8") as f:
        lines = f.readlines()
    sentences = [line.strip() for line in lines if any(p in line for p in sentence_endings)]
    num_sentences = len(sentences)
    words_per_sentence = total_words / num_sentences if num_sentences else 0
    avg_chars_per_word = total_chars / total_words if total_words else 0
    ttr = len(set(words)) / total_words if total_words else 0
    with open("gu_words_metrics.txt", "w", encoding="utf-8") as m:
        m.write(f"Total words: {total_words}\n")
        m.write(f"Total characters: {total_chars}\n")
        m.write(f"Number of sentences (approx): {num_sentences}\n")
        m.write(f"Words per sentence (approx): {words_per_sentence:.2f}\n")
        m.write(f"Average characters per word: {avg_chars_per_word:.2f}\n")
        m.write(f"Type-Token Ratio (TTR): {ttr:.4f}\n")