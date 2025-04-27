import time
from typing import List, Dict, Any
from sklearn.metrics import precision_recall_fscore_support
from langchain.chains import RetrievalQA

def evaluate_qa_system(qa_chain: RetrievalQA, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate QA system performance"""
    results = []
    correct_predictions = 0
    total_queries = len(test_data)
    total_time = 0
    
    # Store actual and predicted for metrics calculation
    actual_ids = []
    predicted_ids = []
    
    for i, test_case in enumerate(test_data, 1):
        query = test_case["query"]
        expected_id = test_case["expected_answer_id"]
        expected_answer = test_case["expected_answer"]
        
        # Time the response
        start_time = time.time()
        response = qa_chain.invoke({"query": query})
        end_time = time.time()
        
        # Get the response and source documents
        answer = response['result']
        source_docs = response.get('source_documents', [])
        
        # Get the ID of the first retrieved document
        if source_docs:
            predicted_id = source_docs[0].metadata.get('id')
        else:
            predicted_id = None
            
        # Calculate timing
        response_time = end_time - start_time
        total_time += response_time
        
        # Check if the prediction is correct
        is_correct = predicted_id == expected_id
        if is_correct:
            correct_predictions += 1
            
        # Store for metrics calculation
        actual_ids.append(expected_id)
        predicted_ids.append(predicted_id if predicted_id is not None else -1)
        
        # Store detailed results
        result = {
            "query": query,
            "expected_id": expected_id,
            "predicted_id": predicted_id,
            "expected_answer": expected_answer,
            "actual_answer": answer,
            "is_correct": is_correct,
            "response_time": response_time
        }
        results.append(result)
        
        # Print progress
        print(f"\nProcessing query {i}/{total_queries}")
        print(f"Query: {query}")
        print(f"Expected Answer: {expected_answer}")
        print(f"Actual Answer: {answer}")
        print(f"Correct: {is_correct}")
        print(f"Response Time: {response_time:.2f}s")
        print("-" * 80)
    
    # Calculate metrics
    accuracy = correct_predictions / total_queries
    precision, recall, f1, _ = precision_recall_fscore_support(
        actual_ids, 
        predicted_ids, 
        average='weighted',
        zero_division=0
    )
    avg_response_time = total_time / total_queries
    
    metrics = {
        "total_queries": total_queries,
        "correct_predictions": correct_predictions,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "average_response_time": avg_response_time,
        "detailed_results": results
    }
    
    return metrics

def print_evaluation_results(metrics: Dict[str, Any]):
    """Print evaluation results in a formatted way"""
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Total Queries: {metrics['total_queries']}")
    print(f"Correct Predictions: {metrics['correct_predictions']}")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"Precision: {metrics['precision']:.2%}")
    print(f"Recall: {metrics['recall']:.2%}")
    print(f"F1 Score: {metrics['f1_score']:.2%}")
    print(f"Average Response Time: {metrics['average_response_time']:.2f}s")
    print("\nDetailed Results:")
    print("-"*50)
    
    for result in metrics['detailed_results']:
        print(f"\nQuery: {result['query']}")
        print(f"Expected ID: {result['expected_id']}")
        print(f"Predicted ID: {result['predicted_id']}")
        print(f"Correct: {result['is_correct']}")
        print(f"Response Time: {result['response_time']:.2f}s")
        print("-"*30) 