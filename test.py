import time
import sys

def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r{i}... ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rTime's up!    \n")

# Example usage
countdown(15*60)
