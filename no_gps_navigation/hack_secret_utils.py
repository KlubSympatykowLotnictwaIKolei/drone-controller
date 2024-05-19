
class MovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = [0] * window_size
        self.sum = 0
        self.pointer = 0
        self.count = 0

    def add_data(self, new_data):
        removed_data = self.window[self.pointer]
        self.sum -= removed_data

        self.window[self.pointer] = new_data
        self.sum += new_data

        self.pointer = (self.pointer + 1) % self.window_size

        self.count = min(self.count + 1, self.window_size)

    def get_average(self):
        if self.count == 0:
            return 0
        return self.sum / self.count
