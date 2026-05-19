import re
import sqlite3
from datetime import datetime, timedelta


conn = sqlite3.connect('mdb.sqlite')
cur = conn.cursor()
conn_1 = sqlite3.connect('mdb.sqlite')
cur_1 = conn_1.cursor()


cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('DROP TABLE IF EXISTS Genres')
cur.execute('DROP TABLE IF EXISTS Movies_Genres')
cur.execute('DROP TABLE IF EXISTS Ratings')

cur.execute('CREATE TABLE IF NOT EXISTS Movies (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)')
cur.execute('CREATE TABLE IF NOT EXISTS Genres(genre_id INTEGER PRIMARY KEY, genre TEXT UNIQUE)')
cur.execute('CREATE TABLE IF NOT EXISTS Movies_Genres (movie_id INT, genre_id INT, PRIMARY KEY(movie_id, genre_id))')
cur.execute('CREATE TABLE IF NOT EXISTS Ratings(id INTEGER PRIMARY KEY AUTOINCREMENT, movie_id INTEGER, rating FLOAT, user_id INTEGER, date DATE)')


ds = open('movielens.csv',encoding='utf-8')
next(ds)
print('Dataset opened!')

movieId = 0
title = None
year = 0
genres = None
user_Id = 0
rating = 0
timestamp = None
genres_sep = list()

c = 0

for i in ds:
    i = i.strip()
    i = re.sub('^[0-9]+,','', i)
    i = re.sub('^rownames,','',i)

    #if '207,0.5' in i : print(i)
    if 'Patrik Age 1.5' in i: continue
    if 'Valachi Papers' in i: continue

    if len(i.split(',')) == 7:
        pieces = i.split(',')
        #print(pieces)

    #if len(pieces)!= 7: print(pieces, len(pieces))


    if len(i.split(',')) > 7:

        if re.search(',000',i) is None :
            #c = c+1
            pieces = re.split(r',(?=\S)',i)
            
            #if len(pieces) != 7:
               #print(i)

        if len(re.split(r',(?=\S)',i))!= 7: 
            #c = c + 1
            #print(i, len(re.split(',(?=\S)',i)))
            #if len(re.split(r',(?=[^\s0])',i)) != 7 : 
            if '207,0.5' not in i:
                pieces = re.split(r',(?=[^\s0])',i)
            else:
                pieces = re.split(r',(?=[^\s0])',i)
                pieces[4] = pieces[4].split(',')
                pieces = pieces[:4] + pieces[4] + pieces[5:]

    try:

        (movieId, title, year, genres, user_Id, rating, timestamp) = (int(pieces[0]), pieces[1], int(pieces[2]), pieces[3], int(pieces[4]), float(pieces[5]), int(pieces[6]))

    except:
        continue
        print(i)

    date = datetime.fromtimestamp(timestamp)
    
    genres = genres.split('|')
    #print(genres)

    cur.execute('INSERT OR IGNORE INTO Movies(id, title, year) VALUES (?,?,?)',(movieId,title,year))
    cur.execute('INSERT OR IGNORE INTO Ratings(movie_id, rating, user_id, date) VALUES (?,?,?,?)',(movieId,rating,user_Id,date))

    #for i in genres:
      # if i not in genres_sep:
            #genres_sep.append(i)
        #else: continue

    for i in genres:
        cur.execute('INSERT OR IGNORE INTO Genres(genre) VALUES (?)',(i,))
    
    conn.commit()

    cur_1.execute('SELECT * FROM Genres')
    for i in cur_1:
        #print(i)
        genre_id = i[0]
        gen = i[1]
        #print(genre_id)
    #print(gen)
        if gen in genres:
            cur.execute('INSERT OR IGNORE INTO Movies_Genres VALUES (?,?)',(movieId,genre_id))

conn.commit()
cur.close()