# WXTJ (&WTJU) Playlist Converter
A React web application that converts Spotify playlists to the `.csv` format used by [WTJU](http://wtju.net/)'s station interface.

Access the webapp [here](https://joek13.github.io/wxtj-converter).

## Rewrite notice!
This project was rewritten from the ground up to use a single-page app. The legacy application is written with Django, and the legacy application's source code is still available on the `legacy` branch.


## Project structure

### Frontend
The `frontend/` subdirectory contains code for the frontend. It's a static web application, built using React and TypeScript based on the `create-react-app` template.

### Backend
The `backend` subdirectory contains code for the backend. Right now, it's a [Serverless Framework](https://www.serverless.com/) project made of two functions, which are backed by AWS Lambda and API Gateway.

## Deploying
NB: eventually, both of these steps will happen automatically on pushes to `main`.

### Deploying the frontend
Currently, you can deploy the frontend by navigating to `./frontend/` and running:

```bash
yarn run deploy
```

This will:
1. Generate an optimized production build of the static React app.
2. Publish it on the `gh-pages` branch of the GitHub repository.

### Deploying the backend
Before deploying the backend you will need to [configure the Serverless Framework to access your AWS account](https://www.serverless.com/framework/docs/providers/aws/guide/credentials). You will also need to set environment variables for your Spotify API keys, for instance by running the following commands:

```bash
export SPOTIFY_API_CLIENT_ID="<your api client id>"
export SPOTIFY_API_CLIENT_SECRET="<your api client secret>"
```

You can deploy the backend by navigating to `./backend` and running:

```bash
serverless deploy --stage prod
```