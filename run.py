import schedule
import time
import subprocess


def fetchSchedule():
    print("Starting usefetchSchedule.py")
    subprocess.Popen(["python3", "usefetchSchedule.py"])


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
schedule.every().day.at("03:05").do(fetchSchedule)
schedule.every().day.at("03:07").do(start_collect_arrivals)
schedule.every().day.at("01:00").do(stop_collect_arrivals)

while True:
    schedule.run_pending()
    time.sleep(1)