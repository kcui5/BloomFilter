# Tests the Bloom Filter's false positive error rate using the 2of12 dictionary
# from http://wordlist.aspell.net/12dicts/
import main

import argparse
import random

def test_main():
    parser = argparse.ArgumentParser(description="Test the Bloom Filter")
    parser.add_argument('error_rate', type=float, help="The target error rate of the Bloom Filter, epsilon")
    parser.add_argument('num_add', type=int, help="The number of elements to add to the Bloom Filter")
    parser.add_argument('num_test', type=int, help="The number of elements not in the Bloom Filter to test membership for")
    parser.add_argument('--shuffle', action='store_true', help="Flag to shuffle the word list or not")
    args = parser.parse_args()

    main.main(["init", "--max_elems", str(args.num_add), "--error_rate", str(args.error_rate)])
    
    with open("2of12.txt", "r") as f:
        words = f.read().split('\n')
        if args.shuffle:
            random.shuffle(words)

    for i in range(args.num_add):
        main.main(["add", "--add_elem", words[i]])
    
    test_words = [words[i] for i in range(args.num_add, args.num_add + args.num_test)]
    test_args = ["test_membership", "--test_elems"]
    test_args.extend(test_words)

    results = main.main(test_args)
    num_pos = 0
    for res in results:
        if res[1]:
            num_pos += 1
    print(f"False positive rate: {100 * num_pos/args.num_test}%")


if __name__ == "__main__":
    test_main()