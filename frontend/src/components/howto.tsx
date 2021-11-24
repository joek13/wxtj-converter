import { Col, Container, Image, Row } from "react-bootstrap";
import help1 from "../img/help1.png";
import help2 from "../img/help2.png";

/**
 * Howto component with brief visual explanation of how to use the app.
 */
export default function Howto() {
    return (<Container className="text-center mt-5">
        <h2 className="h4 mb-3">How it works</h2>
        <Row>
            <Col className="px-4" md>
                <Image src={help1} className="mb-2" fluid rounded />
                <p>Right-click your playlist on Spotify. Use Share &gt; Copy Playlist Link, and paste the URL in the box above.</p>
            </Col>
            <Col className="px-4" md>
                <Image src={help2} className="mb-2" fluid rounded />
                <p>Once the <code>.csv</code> file is downloaded, open your show WTJU's playlist editor. Look at "upload playlist", choose the downloaded <code>.csv</code> file, and click "upload".</p>
            </Col>
        </Row>
    </Container>)
}