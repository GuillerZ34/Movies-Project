import sqlite3
import json

conn = sqlite3.connect('mdb.sqlite')
cur = conn.cursor()
cur_1 = conn.cursor()

movies = dict()
votes = dict()

cur.execute('SELECT id, title FROM Movies')

for i in cur:
    #print(i)
    cur_1.execute('SELECT rating FROM Ratings WHERE movie_id=?',(i[0],))
    data = cur_1.fetchall()
    num_votes = len(data)
    #tot = 0
    #for j in data:
        #tot = tot + j[0]
    votes[i[1]] = num_votes

#print(votes)
x = sorted(votes, key=votes.get, reverse=True)

print(x[:100])

highest = None
lowest = None

for k in x[:100]:
    if highest is None or highest < votes[k]:
        highest = votes[k]
    if lowest is None or lowest > votes[k]:
        lowest = votes[k]

print(highest)
print(lowest)


bigsize = 80
smallsize = 20

fhand = open('gtitle.js','w')
fhand.write("gtitle = [")
first = True

for k in x[:100]:
    #print(k)
    if not first : fhand.write(',\n')
    first = False
    size = votes[k]
    size = (size - lowest)/ float(highest-lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write(json.dumps({"text": k, "size": size}))

fhand.write('\n];\n')

print('Output written to gtitle.js')
print('Open gtitle.htm in a browser to see the visualization')