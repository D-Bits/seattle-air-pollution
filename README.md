
# Seattle Air Pollution

An Apache Airflow and Postgres project to track and analyze Seattle air pollution over time.

## Local Setup

*First, you need both the [Astronomer CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart) and [Docker](https://www.docker.com/) installed. You will also need an OpenWeatherMap API key.*

To run the project locally:

- Clone the repo
- Create a `.env` file in the root directory with the following environment variables:

```
EXECUTOR=LocalExecutor
API_KEY=(your_open_weather_map_api_key)
DB_CONN=postgresql+psycopg2://postgres:postgres@postgres/climate
```

Then, run `make start` from the root of the project directory, and you should be good to go.