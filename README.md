# jobsity-challenge
Challenge proposed by Jobsity.

# Data Pipeline Architecture
![Data Pipeline Architecture](data-pipeline-architecture.png "Data Pipeline Architecture")

## Requirements
The system requirements to run this project are:
- Running on Linux, Mac or WSL;
- Python 3.8;
- Docker and Docker Compose installed.


## Installation
### Kafka
Enter via terminal into the folder `kafka` and run the command: `bash setup.sh`

This command will download the Kafka binary, unzip and movethe Kafka folder to the home directory.


### Python
Run the command `sudo apt install virtualenv` to install the Python virtual environment.


## Setup
### Kafka
On all these commands, you'll need to navigate to the Kafka folder that was downloaded in the installation process (not the folder in the project!)

In one terminal, run the command to start the Zookeeper: `bin/zookeeper-server-start.sh config/zookeeper.properties`

Once the Zookeeper server is running, open another terminal window, navigate to the Kafka folder and run the Kafka server command: `bin/kafka-server-start.sh config/server.properties`

Once the Zookeeper server is running, open a third terminal window, navigate to the Kafka folder again and run the command to create a *raw_trips_data* topic: `bin/kafka-topics.sh --create --topic raw_trips_data --bootstrap-server localhost:9092`

After the topic is created, you can close that terminal window, but **keep the others running**.

In case something went wrong, just follow Apache Kafka's [quickstart guide](https://kafka.apache.org/quickstart).


### Python
- *api_entrypoint*
- *python_microservice_data_processing*
- *test*

In each of the folders listed above, run the following commands:
1. Open a new terminal window;
2. Enter into the respective folder with the terminal;
3. Create a new virtual environment with the command: `virtualenv venv`
4. Activate the virtual environment with the command: `source venv/bin/activate`
5. Install the required packages with: `pip install -r requirements.txt`
6. [Only for *api_entrypoint*] Run the command: `python manage.py migrate`


### Metabase
To configure Metabase, you'll need to build and run the `docker-compose.yml` in order to access the webserver.

Once the Docker instances are running, you can you go to http://localhost:3000/

You'll need to configure **both** *Postgres* and *ClickHouse* in order for the Data Visualization to work according to the Data Pipeline Architecture.

Once you finish the setup process, you can just go to http://localhost:3000/admin/databases/create and register the databases.

Fill the form fields with the following data:

##### ClickHouse
- **Database type:** ClickHouse
- **Name:** ClickHouse Data Visualization
- **Database Name:** jobsity_challenge
- **Host:** clickhouse
- **Port:** 8123
- **Username:** jobsity
- **Password:** my_password123

##### Postgres
- **Database type:** PostgreSQL
- **Name:** Postgres Data Visualization
- **Host:** postgres
- **Port:** 5432
- **Database name:** docker
- **Username:** docker
- **Password:** my_password123

## Run
For the project to work, you'll need to run the commands **in the following order**, each in one different terminal.

**For all the commands, it will be considered that you are in the project's root directory.**

You'll use 6 terminal windows at total.

1. `docker-compose up`
2. `cd ~/kafka_2.13-2.8.0/ && bin/zookeeper-server-start.sh config/zookeeper.properties`
3. `cd ~/kafka_2.13-2.8.0/ && bin/kafka-server-start.sh config/server.properties`
4. `cd api_entrypoint/ && source venv/bin/activate && python manage.py runserver`
5. `cd python_microservice_data_processing/ && source venv/bin/activate && python main.py`

On the last command, it will be executed a load test of all the data in `trips.csv` file. Pay attention to `api_entrypoint` and `python_microservice_data_processing` windows not to miss the show.

Finally, run the command:
`cd test/ && source venv/bin/activate && python test.py`

## Endpoints
- **Metabase:** http://localhost:3000/
- **API Endpoint:** http://localhost:8000/api/
- **Clickhouse:** clickhouse://jobsity:my_password123@localhost:8124/jobsity_challenge/
- **Postgres:** postgres://docker:my_password123@localhost:8001/docker/
