import schedule
import time
import subprocess

# Global variable to keep the process reference
process = None

def start_collect_arrivals():
    global process
    if process is None:
        print("Starting collectArrivals.py")
        process = subprocess.Popen(["python3", "collectArrivals.py"])

def stop_collect_arrivals():
    global process
    if process is not None:
        print("Stopping collectArrivals.py")
        # Terminate the process
        process.terminate()
        process.wait()
        process = None

# Schedule tasks
schedule.every().day.at("03:00").do(start_collect_arrivals)
schedule.every().day.at("01:30").do(stop_collect_arrivals)

while True:
    schedule.run_pending()
    time.sleep(1)