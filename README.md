# Log Analysis Tool - Udacity

This project referes to Udacity fullstack web development Log Analysis Tool Project.

## Requirements

* Virtual Box.
* Vagrant.
* Python 2.
* Postgresql.
* psycopg2.

## How to run

* Checkout and run Udacity vagrant file ( This step is optional You can configure it in       your own machine as well).
  (https://github.com/udacity/fullstack-nanodegree-vm)
* Install virtual box and vagrant ( This step is optional You can configure it in             your own machine as well).
* Install postgresql (If not using VM above).
* Install the dataset newsdata.sql by psql -d news -f newsdata.sql (If not using VM above).
* Install psycopg2 (If not using VM above).
* Create views specified below.
* Run reporting-tool.py (python reporting-tool.py).

## Design

* Name of the database is configured in the variable called DATABASE_NAME.
* Questions array will consists of all the questions Answered by reporting tool.
* Queries for each question is specified seperately.
* Application will start execute with the main method that will prepare each question and     answers by calling its relavant queries.
* For the first and second questions, view is prepared by grouping the visit count for each   unique path.
* Answer for first question is obtained by the articles table and above mentioned view in     order to get the views and article title.
* Same view can be used to Answer the second question as well since it requirement as well    since it requires the most popular aurthors. But need to join with authors as well.
* Seperate view is created in order to answer the 3rd question which requires to have days    which have more than 1% of errors. failed_requests view is created adding all requests      which was not 200 OK grouped by date.Then that view is used to get errors which is more     than 1.0%.

## Views to be created

* create view path_count as select path,count(*) as visits  from log group by path;
* create view failed_requests as select time::date as date,round(100.0 * sum(case when        status != '200 OK' then 1 else 0 end)/count(*),2) as pct from log group by time::date;

