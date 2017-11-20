#!/usr/bin/env python

import psycopg2

DATABASE_NAME = "news"

questions = ["\n 1. What are the most popular three articles of all time?",
             "\n 2. Who are the most popular article authors of all time?",
             """\n 3. On which days did more than 1% of requests lead
             to errors?"""]

query_for_question1 = """select title,visits from articles, path_count
                         where path_count.path like '%' || articles.slug
                          order by visits desc limit 3;"""
query_for_question2 = """select sum(visits),name from authors,articles,
                         path_count where path_count.path like '%' ||
                         articles.slug and authors.id = articles.author
                         group by name order by sum desc;"""
query_for_question3 = """select date, pct from failed_requests where pct > 1.0
                         order by pct desc;"""


def connect_to_db():
    """ This will be used to connect to the database news. Any connection error
         will be notified"""
    try:
        database = psycopg2.connect("dbname={}".format(DATABASE_NAME))
        return database
    except psycopg2.Error:
        print "Databse Conection failed"
        exit(1)


def run_query(query):
    """ This will run a particular query and return the results.
        Connection will be established and closed after fectching
        the results"""
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return results


def get_answer_for_question(question_number):
    """ This will give the answer by getting the question number
        as an input and running the query and prepareing the answer by
        formatting it"""
    if question_number == 1:
        results = run_query(query_for_question1)
        return prepare_answer1(results)

    if question_number == 2:
        results = run_query(query_for_question2)
        return prepare_answer2(results)

    if question_number == 3:
        results = run_query(query_for_question3)
        return prepare_answer3(results)


def prepare_answer1(results):
    """ This will format the answer suitable to the question 1"""
    answer = "\n"
    for result in results:
        answer = answer + str(result[0]) + " ---- " + str(result[1]) + \
                 " views \n"
    return answer


def prepare_answer2(results):
    """ This will format the answer suitable to the question 2"""
    answer = "\n"
    for result in results:
        answer = answer + str(result[1]) + " ---- " + str(result[0]) + \
                 " views \n"
    return answer


def prepare_answer3(results):
    """ This will format the answer suitable to the question 3"""
    answer = "\n"
    for result in results:
        answer = answer + str(result[0]) + " ---- " + str(result[1]) + \
                 "% errors \n"
    return answer


def main():
    """ This is the main method of the application which prints
        the question, get the answer and print it."""
    for x in range(0, len(questions)):
        print(questions[x])
        answer = get_answer_for_question(x+1)
        print(answer)


main()
