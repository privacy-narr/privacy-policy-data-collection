#! /usr/bin/env python3
import os, random

ASCII_0 = 48
ASCII_9 = 57
ASCII_a = 97
ASCII_z = 122

codes = list(range(ASCII_0, ASCII_9 + 1)) + list(range(ASCII_a, ASCII_z + 1))
sample_size = 5757

with open('random-words.txt', 'w') as f:
    while (sample_size > 0):
        chars = [chr(c) for c in random.choices(codes, k=5)]
        f.write(''.join(chars)+'\n')
        sample_size = sample_size - 1
