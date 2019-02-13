import re

def wordset(fname):
    """Returns the set of words corresponding to the given file"""
    # Create regexp for character filtering
    regex = re.compile('[^a-zA-Z]')
    # Your code here
    f = open(fname, 'r')
    text = f.read().replace('\n', '-')
    text = regex.sub('-', text)
    text = text.lower()
    x = text.split('-')
    return x

def jaccard(fname1, fname2):
    """Calculate Jaccard index"""
    # Your code here - call wordset()
    text1 = wordset(fname1)
    text2 = wordset(fname2)
    sa = set(text1)
    sb = set(text2)
    print(sa)
    print(sb)
    union = len(sa | sb)
    intersection = len(sa & sb)
    print("intersection: ", intersection, " union: ", union)
    return intersection/union

