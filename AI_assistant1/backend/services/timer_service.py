import threading
import time

class TimerService:

    def __init__(self):
        self.active_timers = []

    def start_timer(self, seconds, callback):

        def worker():
            time.sleep(seconds)
            callback()

        t = threading.Thread(
            target=worker,
            daemon=True
        )

        t.start()

        self.active_timers.append(t)

timer_service = TimerService()