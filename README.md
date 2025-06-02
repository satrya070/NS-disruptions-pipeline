# NS Disruptions Pipeline
This project is a simple end-to-end data pipeline that automatically collects data from the official NS api in an orchestrated manner, transforms and stores the data, does some simple aggregations, and displays them in a simple front-end. Note that emphasis of the project was on setting up simple good working data infrastructure, rather than creating insightful aggregations and a dashboard. 

The NS api was chosen as it’s something that everybody in the Netherlands will know. Note that as it’s just a personal project, aggregations could have errors as I’m not deeply involved with the data, and so possibly could have interpreted things wrongly.

## Design
I had to use a setup that was based on free tools as it’s just a personal project, so I had to be more creative in terms of using tooling, which means less common data engineering tools in this project.

<b>Data provider:</b> The official NS disruptions API. <br/>
<b>Database:</b> PostgreSQL is used here as it's a well known relational database that I’m familiar with.<br/>
<b>Orchestration and ETL:</b> Github actions is a nice tool with free tier options which in this case I used to perform ETL. In this case the ETL is in the form of Python scripts fetching data from the API, transforming the data, and loading it into the database. I also used Github actions to orchestrate the data load, fetching and processing the data every 3 hours on 12-3-6-9. <br/>
<b>Frontend:</b> I used Streamlit as a front-end, which is a tool that can be used to easily setup web based applications like dashboards, and load data from something like a Postgres database.
<b>Data monitoring: </b> This is yet to be implmented, but will be consist of ...
