import { Container } from "react-bootstrap";

/**
 * App footer with contact info and source code link.
 */
export default function Footer() {
    return <footer>
        <Container className="bg-light text-center p-5" fluid>
            <p>Made with love by Joe Kerrigan</p>
            <p>Check out the <a href="https://github.com/joek13/wxtj-converter">source code</a></p>
            <p>Bugs? Feedback or feature requests? Want me to listen to your show? Reach me at <a href="mailto:joek1301@gmail.com">joek1301@gmail.com</a></p>
        </Container>
    </footer>;
}