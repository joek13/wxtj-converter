import { Container } from "react-bootstrap";

function Header() {
    return (
        <header>
            <section className="jumbotron text-center">
                <Container>
                    <h1>wxtju/wtju playlist converter</h1>
                    <p>Quickly convert your Spotify playlists to .csv</p>
                </Container>
            </section>
        </header>
    );
}

export default Header;