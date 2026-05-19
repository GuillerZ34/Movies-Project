import sqlite3

conn = sqlite3.connect('mdb.sqlite')
cur = conn.cursor()
cur_1 = conn.cursor()

ratings = dict()
votes = list()

cur.execute('SELECT id, title FROM Movies')

for i in cur:
    #print(i)
    cur_1.execute('SELECT rating FROM Ratings WHERE movie_id=?',(i[0],))
    data = cur_1.fetchall()
    if len(data) == 0 : continue
    tot = 0
    for j in data:
        tot = tot + j[0]
    avg = tot/len(data)
    num_votes = len(data)
    ratings[i[0]] = (i[1], avg, num_votes)
    votes.append(num_votes)

#print(ratings.get)
votes.sort()
p = 0.9*(len(votes) + 1)
m = votes[int(p-1)]

#print(ratings)

total_avg = 0
for movie_id in ratings:
    title, avg, num_votes = ratings[movie_id]
    total_avg = total_avg + avg

C = total_avg/len(ratings)

scores = dict()

for movie_id in ratings:
    title, R, v = ratings[movie_id]

    score = ((v/(v+m))*R) + ((m/(m+v))*C)
    scores[movie_id] = (title, score, R, v)

x = sorted(scores, key=lambda movie_id: scores[movie_id][1], reverse=True)


for movie_id in x[:10]:
    title, score, average, num_votes = scores[movie_id]
    print(title, score)
