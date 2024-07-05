import signal
import time
import os


def handle_sigurg(signum, frame):
    print("SIGURG sinyali alındı!")

# SIGURG sinyali için işleyici ayarlayın


signal.signal(signal.SIGURG, handle_sigurg)


print(f"PID: {os.getpid()}")
print("SIGURG sinyalini bekliyor...")

# Süreci sonsuz döngüde tutun
while True:
    time.sleep(1)
