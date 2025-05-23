import threading
import time
from oled_display import OLEDDisplay

class FocusTimerThread(threading.Thread):
    def __init__(self, focus_state, reset_threshold=10, refocus_threshold=3):
        super().__init__(daemon=True)
        self.focus_state = focus_state
        self.reset_threshold = reset_threshold
        self.refocus_threshold = refocus_threshold
        self.display = OLEDDisplay()

        self.elapsed = 0
        self.status = "Distracted"
        self.active = False
        self.last_focus_state = False
        self.last_state_change = time.time()

    def run(self):
        next_tick = time.time()
        blink_state = True  # start ON
        blink_active = False

        while True:
            now = time.time()
            is_focused = self.focus_state.get()

            if is_focused != self.last_focus_state:
                self.last_focus_state = is_focused
                self.last_state_change = now

            duration = now - self.last_state_change

            # --- Timer logic ---
            # Start counting when initially focused
            if is_focused and not self.active:
                if duration >= self.refocus_threshold:
                    self.active = True

            # Stop and reset if distracted too long
            if not is_focused and self.active and duration >= self.reset_threshold:
                self.elapsed = 0
                self.active = False

            # If we're active, always count — even if not currently focused
            if self.active:
                self.elapsed += 1

            # --- Blink logic ---
            blink_active = not is_focused and self.active and duration >= 2

            if blink_active:
                blink_state = not blink_state  # flip every second
                display_args = [f"{self.elapsed // 60:02}:{self.elapsed % 60:02}", 24, 14, 32] if blink_state else ["DISTRACTED", 2, 20, 22]
                
            else:
                display_args = [f"{self.elapsed // 60:02}:{self.elapsed % 60:02}", 24, 14, 32]

            # display_text = f"{self.elapsed // 60:02}:{self.elapsed % 60:02}"
            self.display.display_status(display_args[0], display_args[1], display_args[2], font_size=display_args[3])

            # Calculate exact next 1-second tick
            next_tick += 1
            sleep_time = max(0, next_tick - time.time())
            time.sleep(sleep_time)

