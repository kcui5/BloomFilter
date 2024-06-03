Bloom Filter
------

Bloom Filter with basic functionality to initialize with desired parameters,
add elements, and concurrenty test multiple elements for membership.

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
