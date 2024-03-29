import { Col, Container, Image, Row } from "react-bootstrap";
import help1 from "../img/help1.png";
import help2 from "../img/help2.png";

/**
 * Howto component with brief visual explanation of how to use the app.
 */
export default function Howto() {
    return (<Container className="mt-5">
        <h2 className="h4 mb-3">Quick start</h2>
        <Row>
            <Col className="px-4 text-center" md>
                <Image src={help1} className="mb-2" width="600" height="365" alt="Image of a Spotify playlist. The user is clicking the Share submenu and selecting the option Copy Playlist Link." fluid rounded />
                <p>Right-click your playlist on Spotify. Use Share &gt; Copy Playlist Link, and paste the URL in the box above.</p>
            </Col>
            <Col className="px-4 text-center" md>
                <Image src={help2} className="mb-2" width="600" height="365" alt="Image of the WTJU station interface." fluid rounded />
                <p>Once the <code>.csv</code> file is downloaded, open your show WTJU's playlist editor. Look at "upload playlist", choose the downloaded <code>.csv</code> file, and click "upload".</p>
            </Col>
        </Row>
    </Container>)
}