import time
from file_handler import clear_folder

class file_name_counter:
    def __init__(self, capacity = 100, clear_threshold = 60) -> None:
        self.capacity = capacity
        self.clear_threshold = clear_threshold
        self.reset_counter()
    
    def add_file_index(self):
        self.current_index += 1

    def get_current_index(self):
        return str(self.current_index)
    
    def check_reset_time(self):
        if time.time() - self.start_time_tick >= self.clear_threshold:
            self.reset_counter()
            print('File name reset.')
        else:
            pass

    def reset_counter(self):
        self.current_index = 0
        clear_folder()
        self.start_time_tick = time.time()