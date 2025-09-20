# WXTJ (&WTJU) Playlist Converter
A React web application that converts Spotify playlists to the `.csv` format used by [WTJU](http://wtju.net/)'s station interface.

Access the webapp [here](https://joek13.github.io/wxtj-converter).

## Rewrite notice!
This project was rewritten from the ground up to use a single-page app. The legacy application is written with Django, and the legacy application's source code is still available on the `legacy` branch.


## Project structure

### Frontend
The `frontend/` subdirectory contains code for the frontend. It's a static web application, built using React and TypeScript based on the `create-react-app` template.

### Backend

Lambda functions dispatch calls to the [Spotify Web API](https://developer.spotify.com/documentation/web-api/), serialize playlists to the appropriate format, and return the generated `.csv`.

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
TODO

## Features/TODO
- [x] Convert Spotify playlists to old/new playlist editor format
- [ ] Integrate with a music database to provide information about tracks from local library
    - [ ] ...and solve issues discriminating between composer/performer
- [x] Optimize to use Spotify Bulk APIs and avoid ratelimits
