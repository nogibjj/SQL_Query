'''Module csv provide tools to read in csv file'''
import csv
import sqlite3

# interact db throw cursor
conn = sqlite3.connect('udemy.db')
cursor = conn.cursor()

# create table
DROP_IF_EXISTS = "DROP TABLE IF EXISTS udemy_webdev"
cursor.execute(DROP_IF_EXISTS)

CREATE_UDEMY_TABLE = ''' CREATE TABLE udemy_webdev(
course_id INT,
course_title TEXT,
url TEXT,
price INT,
num_subscribers INT,
num_reviews INT,
num_lectures INT,
level TEXT,
rating DOUBLE,
content_duration DOUBLE,
published_timestamp DATE,
subject TEXT
);
'''
cursor.execute(CREATE_UDEMY_TABLE)

# insert data
INSERTION = "INSERT INTO udemy_webdev \
    (course_id, course_title, url, price, num_subscribers, num_reviews, num_lectures, level, rating, content_duration, published_timestamp, subject)\
     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
udemy_csv = open('./3.1-data-sheet-udemy-courses-web-development.csv', "r", encoding="utf8")
data = csv.reader(udemy_csv)
cursor.executemany(INSERTION, data)

# To see the number of different levels that the course provided
QUERY1='''
SELECT DISTINCT level
FROM udemy_webdev
WHERE LENGTH(level) > 0;
'''
print('-'* 50)
print("Number of different levels that the course provided")
print("Levels:")
diff_level = cursor.execute(QUERY1).fetchall()
for level in diff_level:
    print(level)

# The most popular beginner-level courses
QUERY2='''
SELECT course_title, url, price, num_subscribers, rating
FROM udemy_webdev
WHERE level IS NOT NULL AND level = 'Beginner Level'
AND num_subscribers = (SELECT MAX(num_subscribers + 0) FROM udemy_webdev)
'''
print('-'* 50)
print("The most popular beginner-level courses [title, url, price, num_subscribers, rating]")
most_pop_begin_course = cursor.execute(QUERY2).fetchall()
for course in most_pop_begin_course:
    print(course)


# The numerber of free course and paid course
QUERY3='''
SELECT
(SELECT COUNT(A.price)
FROM udemy_webdev A
WHERE A.price = 0) AS free_course,
(SELECT COUNT(A.price) AS paid_course
FROM udemy_webdev A
WHERE A.price > 0) AS paid_course
'''
print('-'* 50)
print("The numerber of free course and paid course [free course, paid course]")
free_and_paid = cursor.execute(QUERY3).fetchall()
for result in free_and_paid:
    print(result)

# Rate of free and paid courses for the beginners
QUERY4='''
SELECT
(SELECT COUNT(A.price)/134.0
FROM udemy_webdev A
WHERE A.price = 0 AND level = 'Beginner Level') AS beginer_free_course,
(SELECT COUNT(A.price)/1071.0 AS paid_course
FROM udemy_webdev A
WHERE A.price > 0 AND level = 'Beginner Level') AS beginer_paid_course
'''
print('-'* 50)
print("Rate of free and paid courses for the beginners [beginer_free_course, beginer_paid_course]")
free_and_paid_begin = cursor.execute(QUERY4).fetchall()
for rate in free_and_paid_begin:
    print(rate)


# The portion of high rate (over 0.85) in free and paid courses for the beginners
QUERY5='''
SELECT
(SELECT COUNT(A.price)/134.0
FROM udemy_webdev A
WHERE A.price = 0 AND rating > 0.85) AS high_rating_free_course,
(SELECT COUNT(A.price)/1071.0 AS paid_course
FROM udemy_webdev A
WHERE A.price > 0 AND rating > 0.85) AS high_rating_paid_course
'''
print('-'* 50)
print("The portion of high rate (over 0.85) in free\
     and paid courses for the beginners [high_rating_free_course, high_rating_paid_course]")
free_and_paid_rate = cursor.execute(QUERY5).fetchall()
for rate in free_and_paid_rate:
    print(rate)


## Finally: Commit all changes and close the database connection
conn.commit()
conn.close()