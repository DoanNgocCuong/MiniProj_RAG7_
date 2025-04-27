import streamlit as st
import yaml
import os
from pathlib import Path
import json
from flashrag import FlashRAG

# Set page config
st.set_page_config(
    page_title="FlashRAG UI",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'config' not in st.session_state:
    st.session_state.config = {}

# Sidebar
st.sidebar.title("FlashRAG UI")
st.sidebar.markdown("---")

# Main tabs
tab1, tab2, tab3 = st.tabs(["Configuration", "Experience", "Evaluation"])

with tab1:
    st.header("Configuration")
    
    # Load/Save Configuration
    col1, col2 = st.columns(2)
    with col1:
        config_file = st.file_uploader("Load Configuration", type=['yaml'])
        if config_file:
            st.session_state.config = yaml.safe_load(config_file)
    
    with col2:
        if st.button("Save Configuration"):
            with open("config.yaml", "w") as f:
                yaml.dump(st.session_state.config, f)
            st.success("Configuration saved!")
    
    # Config Editor
    st.subheader("Config Editor")
    config_text = st.text_area("Edit Configuration", value=yaml.dump(st.session_state.config))
    if st.button("Update Config"):
        try:
            st.session_state.config = yaml.safe_load(config_text)
            st.success("Configuration updated!")
        except Exception as e:
            st.error(f"Error updating config: {str(e)}")

with tab2:
    st.header("Experience")
    
    # Corpus Selection
    st.subheader("Corpus Selection")
    corpus_path = st.text_input("Corpus Path", "data/corpus.jsonl")
    index_path = st.text_input("Index Path", "indexes/")
    
    # Component Configuration
    st.subheader("Component Configuration")
    
    # Retriever Configuration
    retriever_type = st.selectbox(
        "Retriever Type",
        ["dense", "sparse", "hybrid"]
    )
    
    # FlashRAG Configuration
    st.subheader("FlashRAG Configuration")
    num_queries = st.slider("Number of Queries", 1, 10, 3)
    use_reranking = st.checkbox("Use Reranking", True)
    
    # LLM Configuration
    st.subheader("LLM Configuration")
    model_name = st.text_input("Model Name", "gpt-3.5-turbo")
    
    # Test Query
    st.subheader("Test Query")
    query = st.text_input("Enter your query")
    if st.button("Run Query"):
        if query:
            try:
                # Initialize FlashRAG
                flashrag = FlashRAG(
                    retriever_type=retriever_type,
                    model_name=model_name,
                    num_queries=num_queries,
                    use_reranking=use_reranking
                )
                
                # Run query
                result = flashrag.query(query)
                st.json(result)
            except Exception as e:
                st.error(f"Error running query: {str(e)}")

with tab3:
    st.header("Evaluation")
    
    # Dataset Selection
    st.subheader("Dataset Selection")
    dataset_path = st.text_input("Dataset Path", "data/eval_dataset.jsonl")
    
    # Method Selection
    st.subheader("Method Selection")
    method = st.selectbox(
        "Evaluation Method",
        ["exact_match", "f1", "bleu"]
    )
    
    if st.button("Run Evaluation"):
        try:
            # Run evaluation
            # Add evaluation code here
            st.success("Evaluation completed!")
        except Exception as e:
            st.error(f"Error running evaluation: {str(e)}")

# Footer
st.markdown("---")
st.markdown("FlashRAG UI - Powered by Streamlit") 