#!/usr/bin/python3
import os
import re
import random
import numpy as np
from tqdm import tqdm as tq
from utils.database import Database
from utils.User import Profile
from models import taunet, fpnet

db = Database(256)

def generate_arr(num):
    #generate arrays based on img and txt
    fp = fpnet.generate('images4/png/' + str(num) + '_keystrokes_1.png').tolist()
    tn = taunet.generate('images4/txt/' + str(num) + '_keystrokes_1.txt').tolist()
    
    #combine the two arrays for 256-length
    arr = np.array(fp + tn)
    return (arr/np.linalg.norm(arr)).tolist()

def exit_handler():
    print("Processing Exit Tasks...")
    db.export_database()
    print("Program is exiting.")

def read_random_files(directory, num_files=10000):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory)
                 if os.path.isfile(os.path.join(directory, f)) and f.endswith('_1.png')]
    
    # Check if there are enough files
    if len(all_files) < num_files:
        raise ValueError(f"Only {len(all_files)} files found in directory, but {num_files} files requested.")
    
    # Select num_files random files from all_files
    files = random.sample(all_files, num_files)
    pattern = re.compile(r'images4/png/(\d+)_keystrokes_1.png')
    return [pattern.search(path).group(1) for path in files if pattern.search(path)]

print("Getting 10000 random files...")
numbers = read_random_files('images4/png')

print("Adding files to db...")
for num in tq(numbers):
    arr = generate_arr(num)
    pf = Profile('test_' + str(num))
    db.insert(arr, profile=pf)
    
exit_handler()