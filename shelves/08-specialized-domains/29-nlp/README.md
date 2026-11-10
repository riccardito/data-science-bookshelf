# 29 · Natural Language Processing

*Shelf VIII · Specialized Domains · FHNW modules: npr*

## Why It Matters

Language is data. Every clinical note, every doctor's letter, every patient complaint, every diagnostic report — it's all text. NLP is what turns unstructured language into structured, processable data. It's the bridge between "handwritten notes in a folder" and "structured data a program can work with."

## Key Concepts

### Text Preprocessing
- Tokenization: splitting text into words/subwords/characters
- Lowercasing, stopword removal, stemming, lemmatization
- Regular expressions for pattern extraction
- Sentence segmentation

### Text Representation
- Bag of Words (BoW): count word occurrences
- TF-IDF: weight by term frequency × inverse document frequency
- Word embeddings: Word2Vec, GloVe — words as dense vectors
- Contextual embeddings: BERT, GPT — same word, different meaning depending on context
- Sentence/document embeddings: for semantic similarity

### Classical NLP Tasks
- Text classification (spam, sentiment, topic)
- Named Entity Recognition (NER): extracting names, dates, medications from text
- Part-of-Speech tagging
- Information extraction
- Text summarization
- Machine translation

## Tools & Libraries

| Tool | Use Case |
|------|----------|
| `nltk` | Classical NLP: tokenization, stemming, corpora |
| `spacy` | Industrial NLP: NER, POS, dependency parsing |
| `transformers` (HuggingFace) | Pre-trained models: BERT, GPT, T5, etc. |
| `sentence-transformers` | Sentence embeddings for semantic search |
| `anthropic` | Claude API — chat, tool use, structured output |
| `tiktoken` / `tokenizers` | Token counting, subword tokenization |
| `regex` / `re` | Pattern extraction from clinical text |

## Chapters

Read in order: each chapter builds on the one before it.

1. Text as data
2. Tokenisation
3. Embeddings
4. Classification
5. LLMs and prompting
6. Evaluating text systems

## Challenge

→ [`fedlex-rag`](https://github.com/riccardito/fedlex-rag)

## Where it was learned

`FHNW-Projects/nlp`
