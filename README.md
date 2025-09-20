# WXTJ (&WTJU) Playlist Converter
A React web application that converts Spotify playlists to the `.csv` format used by [WTJU](http://wtju.net/)'s station interface.

Access the webapp [here](https://joek13.github.io/wxtj-converter).

## Project structure

### Frontend
The `frontend/` subdirectory contains code for the frontend. It's a static web application, built using React and TypeScript based on the `create-react-app` template.

### Backend
An AWS CDK application. Deploys the convert Lmabda, which calls the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) to read information about your playlist and write out the corresponding CSV.

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
1. Navigate to `./backend`
2. `npm run build && npm run cdk deploy`

## Features/TODO
- [x] Convert Spotify playlists to old/new playlist editor format
- [ ] Integrate with a music database to provide information about tracks from local library
    - [ ] ...and solve issues discriminating between composer/performer
- [x] Optimize to use Spotify Bulk APIs and avoid ratelimits
