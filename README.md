# WXTJ (&WTJU) Playlist Converter
The WXTJ/WTJU Playlist Converter is a web application that accepts Spotify playlist URLs and converts them to a CSV file suitable for uploading on the station interface at [WTJU](http://wtju.net/), the radio station at the University of Virginia.

## Project structure

### Frontend
The `frontend/` subdirectory contains code for the frontend. It's a static web application, built using React and TypeScript based on the `create-react-app` template.

### Backend
The `backend` subdirectory contains code for the backend. Right now, it's a [Serverless Framework](https://www.serverless.com/) project made of two functions, which are backed by AWS Lambda and API Gateway.