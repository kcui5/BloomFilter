Bloom Filter
------

Bloom Filter with basic functionality to initialize with desired parameters,
add elements, and concurrently test multiple elements for membership.

Initialize a Bloom Filter with:
`python main.py init --max_elems <INSERT MAX ELEMS> --error_rate <INSERT ERROR RATE>`

Add elements with:
`python main.py add --add_elem <INSERT ELEMENT TO ADD>`

Test elements for membership with:
`python main.py test_membership --test_elems <INSERT ELEMENTS TO TEST>`

For example,  
`python main.py init --max_elems 3000000 --error_rate 0.003`  
`python main.py add --add_elem apple`  
`python main.py test_membership --test_elems apple orange`  
will initialize the Bloom Filter for 3000000 maximum elements, a target error rate of 0.3%, add "apple", then test "apple" and "orange" for membership.  
  
  
  
Testing
-----
The Bloom Filter's false positive rate can be tested with the test.py file using words in 2of12.txt taken from the 2of12 dictionary at http://wordlist.aspell.net/12dicts/.
To run a test, use  
`python test.py <INSERT TARGET ERROR RATE> <INSERT NUM ADD> <INSERT NUM TEST> <SHUFFLE>`  
where the target error rate is the target error rate to initialize the Bloom Filter with, num add is the number of words from 2of12.txt to add to the Bloom Filter and also the max number of elements the Bloom Filter is initialized with, num test is the number of words to test membership for where none of the words to test for were previously inserted, and shuffle is an optional flag to indicate whether the words in the dictionary should be shuffled before being used. This might help allude to problems with nonuniformity of the hash functions if words in alphabetical order result in similar hashes.  
For example,  
`python test.py 0.003 30000 3000 --shuffle`  
will initialize a Bloom Filter for 30000 maximum elements and a target error rate of 0.3%, then will shuffle the word dictionary, add 30000 words to the Bloom Filter, then test membership for 3000 other words and print the false positive rate.

