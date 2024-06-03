import os
import pickle
import math
import argparse
from bitarray import bitarray
import mmh3
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor

#Testing: 3000000 max_elems results in 5 bit array files
DEBUG_MODE = False

# File path where BloomFilter instance is saved to
FILE_PATH = "bloom.pkl"
# Folder where bit array files are stored
BIT_FOLDER = "bfbits/"
# Maximum number of bits in the bit array for each file, 8e6 is ~1MB per file
MAX_FILE_BITS = int(8e6)

class BloomFilter:
    def __init__(self, max_elems, error_rate):
        self.n_max_elems = max_elems
        self.e_error_rate = error_rate
        self.m_size = math.ceil(max_elems * -2.08 * math.log(error_rate))
        self.k_hash = math.ceil(-math.log(error_rate) / math.log(2))
        if DEBUG_MODE:
            print("Initialized Bloom Filter: ")
            print(self)
        self.serialize()
        self.create_files()

    def create_files(self):
        """Create files to store bit arrays, initialized all to 0s"""
        num_files = math.ceil(self.m_size / MAX_FILE_BITS)
        if DEBUG_MODE:
            print(f"Creating {num_files} bit array files...")
        if not os.path.isdir(BIT_FOLDER):
            os.mkdir(BIT_FOLDER)
        for i in range(num_files):
            bits = bitarray(MAX_FILE_BITS)
            bits.setall(0)
            with open(f"{BIT_FOLDER}{i}.bin", "wb") as f:
                bits.tofile(f)

    def add_elem(self, elem):
        """Add given element to Bloom Filter"""
        # Compute k hashes as bit positions
        bit_positions = []
        for i in range(self.k_hash):
            mmh3hash = mmh3.hash(elem)
            sha256hash = int(sha256(elem.encode('utf-8')).hexdigest(), 16)
            pos = mmh3hash + i*sha256hash
            pos = pos % self.m_size
            bit_positions.append(pos)
        if DEBUG_MODE:
            print(f"Computed bit positions: {bit_positions}")

        # Set those k bit positions to 1 and write-back to disk
        for pos in bit_positions:
            file_index = pos // MAX_FILE_BITS
            file_bit_pos = pos % MAX_FILE_BITS
            byte_index = file_bit_pos // 8
            bit_pos = file_bit_pos % 8
            with open(f"{BIT_FOLDER}{file_index}.bin", "rb") as f:
                f.seek(byte_index)
                byte = f.read(1)[0]
                byte |= (1 << (7 - bit_pos))
            with open(f"{BIT_FOLDER}{file_index}.bin", "r+b") as f:
                f.seek(byte_index)
                f.write(bytes([byte]))
    
    def test_membership(self, elem):
        """Test whether the given element is in the Bloom Filter"""
        bit_positions = []
        for i in range(self.k_hash):
            mmh3hash = mmh3.hash(elem)
            sha256hash = int(sha256(elem.encode('utf-8')).hexdigest(), 16)
            pos = mmh3hash + i*sha256hash
            pos = pos % self.m_size
            bit_positions.append(pos)
        if DEBUG_MODE:
            print(f"Computed bit positions: {bit_positions}")

        for pos in bit_positions:
            file_index = pos // MAX_FILE_BITS
            file_bit_pos = pos % MAX_FILE_BITS
            byte_index = file_bit_pos // 8
            bit_pos = file_bit_pos % 8
            with open(f"{BIT_FOLDER}{file_index}.bin", "rb") as f:
                f.seek(byte_index)
                byte = f.read(1)[0]
                bit = (byte >> (7 - bit_pos)) & 1
                if bit == 0:
                    return elem, False
        return elem, True

    def serialize(self):
        with open(FILE_PATH, 'wb') as file:
            pickle.dump(self, file)
        if DEBUG_MODE:
            print(f"Serialized to {FILE_PATH}")

    @classmethod
    def deserialize(cls):
        with open(FILE_PATH, 'rb') as file:
            instance = pickle.load(file)
        if DEBUG_MODE:
            print(f"Instance deserialized from {FILE_PATH}")
        return instance

    def __repr__(self):
        return f"BloomFilter (max_elems={self.n_max_elems}, error_rate={self.e_error_rate}, size={self.m_size}, k={self.k_hash})"


def main(args=None):
    parser = argparse.ArgumentParser(description="Create and Use Bloom Filter")
    parser.add_argument('arg', type=str, choices=['init', 'add', 'test_membership'], help="Basic Bloom Filter functions")
    parser.add_argument('--max_elems', type=int, help="The maximum number of elements to be added to the Bloom Filter, n")
    parser.add_argument('--error_rate', type=float, help="The target error rate of the Bloom Filter, epsilon")
    parser.add_argument('--add_elem', type=str, help="Element to add to the Bloom Filter")
    parser.add_argument('--test_elems', nargs='+', type=str, help="Element(s) to test membership for in the Bloom Filter")

    # Parse the arguments
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.arg == 'init' and (not args.max_elems or not args.error_rate):
        print("Need to specify max_elems and error_rate!")
        return
    if args.arg == 'add' and not args.add_elem:
        print("Need to specify the element to add!")
        return
    if args.arg == 'test_membership' and not args.test_elems:
        print("Need to specify the element(s) to test membership for!")
        return
    
    if args.arg == 'init':
        BloomFilter(args.max_elems, args.error_rate)
        print("Initialized the Bloom Filter!")
    elif args.arg == 'add':
        bloom = BloomFilter.deserialize()
        bloom.add_elem(args.add_elem)
        print(f"Added {args.add_elem}")
    elif args.arg == 'test_membership':
        bloom = BloomFilter.deserialize()
        with ThreadPoolExecutor() as executor:
            running_tasks = {executor.submit(bloom.test_membership, elem): elem for elem in args.test_elems}
            results = [running_task.result() for running_task in running_tasks]
        for res in results:
            if res[1]:
                print(f"The element {res[0]} is probably in the set")
            else:
                print(f"The element {res[0]} is definitely not in the set")
        return results
        

if __name__ == "__main__":
    main()