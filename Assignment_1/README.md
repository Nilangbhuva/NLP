# NLP
NLP lab assignments
# Assignment 1 - NLP Tokenization

## Objective
Tokenize paragraphs into sentences and sentences into words, then store each tokenized sentence as a line in a compressed `.parquet` file.

## Steps:
1. Read raw data (text file with paragraphs).
2. Tokenize paragraphs into sentences using regex.
3. Tokenize each sentence into words.
4. Join word tokens with space to form tokenized sentences.
5. Store all tokenized sentences line-by-line in a `.parquet` file (compressed using Snappy).

## Output
- `tokenized_sentences.parquet`: Contains tokenized sentences in compressed format.

## Requirements
- Python 3.x
- pandas
- pyarrow
