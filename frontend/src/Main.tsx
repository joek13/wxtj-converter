import { useState } from "react";
import { Alert, Container, Spinner } from "react-bootstrap";
import Footer from "./components/footer";
import Header from "./components/header"
import Howto from "./components/howto";
import { Options, ConvertParams } from "./components/options";
import axios from "axios";

function Main() {
    const [loading, setLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);
    const [warnings, setWarnings] = useState<string[]>([]);

    let convert = (params: ConvertParams) => {
        // start loading
        setLoading(true);
        // clear error message and any warnings
        setErrorMessage(undefined);
        setWarnings([]);

        // select which API endpoint to use based on format
        const apiEndpoint = params.oldPlaylistEditor ? "/convert_old_playlist" : "/convert_new_playlist";

        // prepare request data for API
        const data = {
            "playlist_url": params.playlistUrl,
            "show_title": params.showTitle,
            "show_date": params.showDate
        };

        axios.post(apiEndpoint, data).then((response) => {
            if (response.data) {
                setWarnings(response.data.warnings);

                // sort of a hack: download the csv file
                // thanks https://stackoverflow.com/questions/44656610/download-a-string-as-txt-file-in-react/44661948
                const element = document.createElement("a");
                const file = new Blob([response.data.body], { type: 'text/plain' });
                element.href = URL.createObjectURL(file);
                element.download = "playlist.csv";
                document.body.appendChild(element); // Required for this to work in FireFox
                element.click();
                element.remove();
            } else {
                setErrorMessage("Malformed response");
            }
        }).catch((err) => {
            // log the error
            console.error(err);
            // and print debug info
            console.log(err);

            if (err.response) {
                if (err.response.data && err.response.data.error) {
                    setErrorMessage(err.response.data.error);
                } else {
                    setErrorMessage("Unknown server error");
                }
            } else if (err.request) {
                setErrorMessage("Unknown request error");
            } else {
                setErrorMessage("Unknown error")
            }
        }).finally(() => {
            setLoading(false);
        });
    };

    return (<>
        <main>
            <Header />
            <Container className="options" fluid="md">
                <Options loading={loading} handleSubmit={convert} />
            </Container>
            <Container className="text-center py-3">
                {loading ?
                    <>
                        <Spinner animation="border" />
                        <p>Converting your tunes...</p>
                    </>
                    : null}
            </Container>
            {/* if we have an error, show an alert box */}
            {errorMessage && (
                <Container className="options" fluid="md">
                    <Alert variant="danger">
                        <Alert.Heading>Conversion error</Alert.Heading>
                        <p>{errorMessage}</p>
                    </Alert>
                </Container>)}
            <Howto />
            <Footer />
        </main>
    </>);
}

export default Main;