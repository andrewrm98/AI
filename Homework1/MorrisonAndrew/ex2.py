def isreverse(s1, s2):
    #  Your code here
    if len(s1) != len(s2):
        return False
    if s1 == "" and s2 == "":
        return True
    if s1[0] == s2[len(s2)-1]:
        return isreverse(s1[1:], s2[:-1])
    else:
        return False
