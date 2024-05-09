## Module 10 Challenge
Part 1 Analyze and Explore the Climate data:
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:


Precipitation Analysis
Find the most recent date in the dataset.

Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

HINT
Select only the "date" and "prcp" values.

Load the query results into a Pandas DataFrame. Explicitly set the column names.

Sort the DataFrame values by "date".

Plot the results by using the DataFrame plot method, as the following image shows:
![image](https://github.com/Mohammed-a-ali01/sqlalchemy-challenge/assets/81397577/1970a1fa-25ac-49a7-bb7b-3b9147b5c4d8)

Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:

Filter by the station that has the greatest number of observations.

Query the previous 12 months of TOBS data for that station.

Plot the results as a histogram with bins=12, as the following image shows:


![image](https://github.com/Mohammed-a-ali01/sqlalchemy-challenge/assets/81397577/24eb6ac8-87e4-49ac-8230-38472cb805d9)
