list1 = [['a','b','c'],['d','e','f'],['g','h','i']]
list2 = [['b'],['e','f'],['g']]

for idx, sublist2 in enumerate(list2):
    match_idx = []
    for i, elem2 in enumerate(sublist2):
        for j, elem1 in enumerate(list1[idx]):
            if elem2 == elem1:
                pos = j
                match_idx.append(j)
    if len(match_idx) == len(sublist2):
        print("Sublist2", sublist2, "in List2 matches with Sublist1", list1[idx], "in List1 at index", pos)
    else:
        print("Sublist2", sublist2, "in List2 does not match with any Sublist in List1")
