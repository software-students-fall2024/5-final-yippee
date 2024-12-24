![Web App](https://github.com/software-students-fall2024/5-final-yippee/actions/workflows/web-app.yaml/badge.svg)

# Final Project: Movie Recommendation App

## Description

A web app that recommends a movie to a user everyday. Users can keep track of the movies they've watched. Experience the app by visiting (https://swe-final-web-app-m232t.ondigitalocean.app/)

## Team Members

- Madison Phung, [Github](https://github.com/mkphung29)
- Stephen Spencer-Wong, [Github](https://github.com/StephenS2021)
- William Xie, [Github](https://github.com/seeyeh)
- May Zhou, [Github](https://github.com/zz4206)

## Container Images for Each Subsystem

- Web App: [Dockerhub](https://hub.docker.com/r/teamyippee/web-app)
- MongoDB: Hosted on Mongo Atlas.

## How to Configure the Project

### Setting Up the Database

Paste the connection string we've sent you over Discord, or set up your own database using Mongo Atlas and copy your connection string into a .env file in the `web-app` folder with the following format:

```bash
MONGO_URI=[your connection string]
MONGO_DBNAME=movie_db
```

### Setting Up the Web App

Build the web app image from the Dockerfile. While in the `web-app` directory:

```bash
docker build -t web-app .
```

Now that you have the `web-app` image (check by running `docker images` and it should appear in the list), instantiate a new container called `webapp`:

```bash
docker run --name webapp -d -p 5000:5000 web-app
```

## How to Set up Environment Variables

Necessary .env variables for connection to the Mongo database have been described above.
