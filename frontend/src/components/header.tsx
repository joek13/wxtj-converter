import { Container } from "react-bootstrap";

/**
 * Header component with snazzy title and subtitle.
 */
function Header() {
    return (
        <header>
            <section className="jumbotron text-center">
                <Container>
                    <h1>wxtju/wtju playlist converter</h1>
                    <p className="lead">Quickly convert your Spotify playlists to <code>.csv</code></p>
                </Container>
            </section>
        </header>
    );
}

export default Header;