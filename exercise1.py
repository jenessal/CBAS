import time
import random


# 1. Enumeration function
def enum(iterator):
    count = 0
    for el in iterator:
        yield count, el
        count += 1


# 2. Object generator
def stream_objects():
    while True:
        yield Object()


# 3. Timing function
def timetaken(func):
    def timed(*args, **kw):
        time_start = time.time()
        result = func(*args, **kw)
        time_end = time.time()
        print('Run function took {} seconds.' \
              .format(round(time_end - time_start, 8)))
        return result
    return timed


class Object():
    def __init__(self):
        self.complete = random.random() < 0.2

    def is_complete(self):
        return self.complete


@timetaken
def run():
    for index, current in enum(stream_objects()):
        if current.is_complete():
            return index


if __name__ == '__main__':
    print('Expected output:')
    print("Run function took # seconds.")
    print('Final object was at index #.')
    print('Actual output:')
    final_index = run()
    print('Final object was at index {}.'.format(final_index))
