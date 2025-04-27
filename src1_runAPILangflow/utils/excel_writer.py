import pandas as pd
import queue
import threading
from typing import List, Dict, Any
from datetime import datetime

class ExcelWriter(threading.Thread):
    """Thread that writes results to Excel file"""
    def __init__(self, excel_queue, output_file):
        super().__init__()
        self.excel_queue = excel_queue
        self.output_file = output_file
        self.daemon = True
        self.running = True

    def run(self):
        while self.running:
            try:
                results = self.excel_queue.get(timeout=1)
                if results is None:
                    break
                
                # Convert results to DataFrame
                df = pd.DataFrame(results)
                
                # Write to Excel
                df.to_excel(self.output_file, index=False, engine='openpyxl')
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error writing to Excel: {str(e)}")
                continue

    def stop(self):
        self.running = False

def setup_excel_writer(output_file: str = "benchmark_results.xlsx"):
    """Setup asynchronous Excel writer"""
    excel_queue = queue.Queue()
    excel_writer = ExcelWriter(excel_queue, output_file)
    excel_writer.start()
    return excel_writer, excel_queue 