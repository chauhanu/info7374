# Q1
lst = [x for x in range(1, 501) if x % 21 == 0]
mean = sum(lst) / len(lst)
q25 = lst[int(len(lst)*0.25)]
q50 = lst[int(len(lst)*0.5)]
q75 = lst[int(len(lst)*0.75)]

# Q2
words = []
with open("ques2.txt", "r") as f:
    words = words + f.read().split()
print(len(words)) #number of words
word_length = [len(w) for w in words]
avg = sum(word_length) / len(word_length)  #average
median = sorted(word_length)[len(word_length)//2]  #median
mode = max(set(word_length), key=word_length.count)  #mode

# Q3
import glob, random
nf_count = 0  # contains "user not found"
userdict = {}
for fname in glob.glob("jsons/*.json"):
    with open(fname, "r") as f:
        id = fname[6:-5]
        if "user not found" in f.read().lower():
            nf_count = nf_count + 1
            userdict[id] = 1 # not found
        else:
            userdict[id] = 0 # found
keys = list(userdict.keys())
for _ in range(5):
    index = random.randint(0, len(userdict)-1)
    print(keys[index], userdict[keys[index]])

# Q4
import re
user_party = {}  #{id : (10, 20) }
for fname in glob.glob("jsons/*.json"):
    with open(fname, "r") as f:
        id = fname[6:-5]
        text = f.read()
        sids = [s.start() for s in re.finditer("segmentUid", text)]
        nfirst = 0
        nthird = 0
        for sid in sids:
            if text[sid+13] == "0":
                nfirst += 1
            elif text[sid+13] == "1":
                nthird += 1
        user_party[id] = (nfirst, nthird)

