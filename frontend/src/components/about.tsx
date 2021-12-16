import { Accordion, Container } from "react-bootstrap";

/**
 * "About" accordion
 */
export default function About() {
    return (<Container className="mt-3 container-md">
        <h2 className="h4 mb-3">More info</h2>
        <h3 className="h5">How it works</h3>
        <p>When you paste your playlist URL in the box above, the application connects to the <a href="https://developer.spotify.com/documentation/web-api/">Spotify Web API</a> to collect details about each track's title, duration, record label, release year, etc. It collects each track's info, assembles them in the appropriate format, and gives you the completed <code>.csv</code> file to download.</p>
        <p>If you're curious (and code-literate), you can find technical details about the implementation in the <a href="https://github.com/joek13/wxtj-converter">source code repository</a>.</p>
        <h3 className="h5">Known issues</h3>
        <ul>
            <li><strong>Classical composers.</strong> Due to limitations in the <a href="https://developer.spotify.com/documentation/web-api/">Spotify Web API</a>, the converter does not know the difference between artists and composers. The <code>performer</code> column will be filled with the first listed artist, and <code>composer</code> will be left blank. (You can fix these issues manually in the WTJU playlist editor.)</li>
            <li><strong>Local files.</strong> The converter cannot find information about <a href="https://support.spotify.com/us/article/local-files/">local files</a> in your library. If you try to convert a playlist with local files, most columns will be blank.</li>
        </ul>
    </Container>);
}