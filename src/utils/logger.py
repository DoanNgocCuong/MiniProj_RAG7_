import logging
import queue
import threading
from pathlib import Path
from datetime import datetime

class LogWriter(threading.Thread):
    """Thread that writes logs to file"""
    def __init__(self, log_queue, log_file):
        super().__init__()
        self.log_queue = log_queue
        self.log_file = log_file
        self.daemon = True
        self.running = True

    def run(self):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            while self.running:
                try:
                    record = self.log_queue.get(timeout=1)
                    if record is None:
                        break
                    f.write(record + '\n')
                    f.flush()  # Ensure immediate write
                except queue.Empty:
                    continue
                except Exception:
                    break

    def stop(self):
        self.running = False

def setup_logging():
    """Setup asynchronous logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = str(log_dir / f"benchmark_{timestamp}.log")
    
    # Create queue for log records
    log_queue = queue.Queue()
    
    # Create and start log writer thread
    log_writer = LogWriter(log_queue, log_file)
    log_writer.start()
    
    # Clear any existing handlers
    logging.getLogger().handlers = []
    
    # Create console handler
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    
    # Log startup information
    logging.info("=" * 50)
    logging.info(f"Starting new benchmark session at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Log file: {log_file}")
    logging.info("=" * 50)
    
    return log_writer, log_queue 