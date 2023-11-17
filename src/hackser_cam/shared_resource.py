import threading

# Shared data and lock
data_lock = threading.Lock()
global_fuzzies = list()
