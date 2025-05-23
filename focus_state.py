import threading

class FocusState:
    def __init__(self):
        self._lock = threading.Lock()
        self._focused = False

    def set(self, focused: bool):
        with self._lock:
            self._focused = focused

    def get(self) -> bool:
        with self._lock:
            return self._focused
