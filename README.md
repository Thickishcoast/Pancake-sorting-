Write a program that receives an order of 4 bottom-burnt pancakes and prints the solution that BFS and A* search will find for going 
from the Start state to the Goal (ordered pancakes and all burnt-side down).
each of the pancakes has an ID number that is consistent with their size followed by a letter “w” or “b”. 
This way, the largest pancake has an ID of 4, the next largest 3, the next 2, and the smallest has an ID of 1. 
The letter “w” refers to the unburnt (white) side being up, and “b” shows that the burnt side is up. 
The goal is to reach “1w2w3w4w”.
The input should consist of pairs of four digits and one character, a hyphen, and one last character (#C#C#C#C-X),
where the first digit indicates the ID of the top pancake and the first character indicates whether the burnt side is down (“w”) or not (“b”), 
the second number indicates the second-highest pancake followed by a character, etc. 
The last character (X) would be “b” or “a” characters, which refer to the Breadth-First (BFS) or A* search algorithms respectively.
The cost associated with each flip is equal to the number of pancakes that are being flipped. 
For instance, the cost of one flip between pancake 3b and 2w from the state “4w1b2w3b” to “2b1w4b3b” is equal to 3 (spatula between 2 and 3).
For each state, use the same heuristic function (h(x)) : “the ID of the largest pancake that is still out of place”. 
For BFS, you don’t need to consider a cost and a heuristic function. 
Use the graph version of the algorithms, meaning that use some type of list (closed set) to avoid visiting the nodes multiple times.
When needed for any of the search algorithms, use the following tie-breaking mechanism:
"when there is a tie between two nodes, replace “w” with 1 and “b” with 0 to obtain an eight-digit number. 
After that pick the node with a larger numerical ID chosen."
For instance, if there is a tie between 4b3w2b1b and 3w4w2b1b, then 4b3w2b1b will be chosen as 40312010>31412010.