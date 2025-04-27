# FlashRAG UI

A user-friendly interface for configuring and testing FlashRAG implementations.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Faiss:
```bash
conda install -c pytorch faiss-cpu=1.8.0
```

## Usage

1. Prepare your corpus in JSONL format:
```json
{"id": "doc1", "contents": "Your document content here"}
```

2. Build the index:
```bash
python -m flashrag.retriever.index_builder \
  --retrieval_method e5 \
  --model_path /path/to/model/ \
  --corpus_path your_corpus.jsonl \
  --save_dir indexes/
```

3. Start the UI:
```bash
streamlit run app.py
```

## Features

- **Configuration Tab**
  - Load/Save configurations
  - Edit configuration in YAML format

- **Experience Tab**
  - Select corpus and index
  - Configure retriever settings
  - Test queries with different configurations

- **Evaluation Tab**
  - Select evaluation dataset
  - Choose evaluation method
  - Run evaluations

## Configuration Options

### Retriever
- Dense (embedding-based)
- Sparse (BM25)
- Hybrid

### FlashRAG
- Number of queries
- Reranking options

### LLM
- Model selection
- Generation parameters

## Contributing

Feel free to submit issues and enhancement requests. 