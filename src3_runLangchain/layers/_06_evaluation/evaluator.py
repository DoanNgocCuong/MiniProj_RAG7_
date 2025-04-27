import time
from typing import List, Dict, Any
from sklearn.metrics import precision_recall_fscore_support
from langchain.chains import RetrievalQA

class Evaluation:
    @staticmethod
    def evaluate_qa_system(qa_chain: RetrievalQA, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate QA system performance"""
        results = []
        correct_predictions = 0
        total_queries = len(test_data)
        total_time = 0
        
        actual_ids = []
        predicted_ids = []
        
        for i, test_case in enumerate(test_data, 1):
            query = test_case["query"]
            expected_id = test_case["expected_answer_id"]
            expected_answer = test_case["expected_answer"]
            
            start_time = time.time()
            response = qa_chain.invoke({"query": query})
            end_time = time.time()
            
            answer = response['result']
            source_docs = response.get('source_documents', [])
            
            predicted_id = source_docs[0].metadata.get('id') if source_docs else None
            
            response_time = end_time - start_time
            total_time += response_time
            
            is_correct = predicted_id == expected_id
            if is_correct:
                correct_predictions += 1
            
            actual_ids.append(expected_id)
            predicted_ids.append(predicted_id if predicted_id is not None else -1)
            
            results.append({
                "query": query,
                "expected_id": expected_id,
                "predicted_id": predicted_id,
                "expected_answer": expected_answer,
                "actual_answer": answer,
                "is_correct": is_correct,
                "response_time": response_time
            })
        
        accuracy = correct_predictions / total_queries
        precision, recall, f1, _ = precision_recall_fscore_support(
            actual_ids, 
            predicted_ids, 
            average='weighted',
            zero_division=0
        )
        avg_response_time = total_time / total_queries
        
        return {
            "total_queries": total_queries,
            "correct_predictions": correct_predictions,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "average_response_time": avg_response_time,
            "detailed_results": results
        }

    @staticmethod
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