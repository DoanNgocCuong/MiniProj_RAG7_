import json
import time
import logging
import sys
from typing import Dict, List, Any
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from api_client import default_client
from utils.logger import setup_logging
from utils.excel_writer import setup_excel_writer

# Global variables for queues
log_queue = None
excel_queue = None

def run_benchmark(queries: List[Dict[str, str]], output_file: str = "benchmark_results.xlsx") -> List[Dict[str, Any]]:
    """
    Run benchmark tests on a list of queries
    
    Args:
        queries (List[Dict[str, str]]): List of query dictionaries with 'query' and 'expected_answer'
        output_file (str): Path to save benchmark results
        
    Returns:
        List[Dict[str, Any]]: List of benchmark results
    """
    global excel_queue
    results = []
    total_queries = len(queries)
    start_time = time.time()
    
    logging.info(f"Starting benchmark with {total_queries} queries")
    
    for idx, query_data in enumerate(queries, 1):
        query = query_data["query"]
        expected = query_data["expected_answer"]
        
        # Log query information
        logging.info(f"Processing query {idx}/{total_queries}")
        logging.info(f"Query text: {query}")
        print(f"\nQuery {idx}/{total_queries}: {query}")  # Print query to console
        
        try:
            # Call API and measure time
            query_start_time = time.time()
            response = default_client.get_response_text(query)
            query_end_time = time.time()
            
            # Create result entry
            result = {
                "query": query,
                "expected_answer": expected,
                "actual_answer": response,
                "response_time": query_end_time - query_start_time,
                "source_id": query_data.get("source_id", ""),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            results.append(result)
            logging.info(f"Query {idx} completed in {result['response_time']:.2f}s")
            logging.info(f"Response: {response}")
            
            # Save intermediate results every 5 queries
            if idx % 5 == 0:
                excel_queue.put(results.copy())  # Send copy to Excel writer
                logging.info(f"Saved intermediate results after {idx} queries")
                
        except Exception as e:
            logging.error(f"Error processing query {idx}: {str(e)}")
            continue
    
    # Save final results
    excel_queue.put(results)
    
    total_time = time.time() - start_time
    logging.info(f"Benchmark completed in {total_time:.2f}s")
    logging.info("=" * 50)
    
    return results

def print_summary(results: List[Dict[str, Any]]):
    """Print benchmark summary statistics"""
    if not results:
        logging.warning("No results to summarize")
        return
        
    total_queries = len(results)
    avg_time = sum(r["response_time"] for r in results) / total_queries
    min_time = min(r["response_time"] for r in results)
    max_time = max(r["response_time"] for r in results)
    
    summary = f"""
Benchmark Summary:
Total queries: {total_queries}
Average response time: {avg_time:.2f}s
Min response time: {min_time:.2f}s
Max response time: {max_time:.2f}s
"""
    logging.info(summary)
    print(summary)

def main():
    global log_queue, excel_queue
    # Setup logging and Excel writer
    log_writer, log_queue = setup_logging()
    excel_writer, excel_queue = setup_excel_writer()
    
    logging.info("Starting benchmark process")
    
    try:
        # Load benchmark queries
        with open("src/benchmark_query.json", "r", encoding="utf-8") as f:
            queries = json.load(f)
        logging.info(f"Loaded {len(queries)} queries from benchmark_query.json")
        
        # Run benchmark
        results = run_benchmark(queries)
        
        # Print summary
        print_summary(results)
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise
    finally:
        # Stop writer threads
        log_writer.stop()
        excel_writer.stop()
        log_writer.join()
        excel_writer.join()

if __name__ == "__main__":
    main()
