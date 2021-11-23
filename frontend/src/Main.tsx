import { useState } from "react";
import { Container, Row } from "react-bootstrap";
import Header from "./components/header"
import Howto from "./components/howto";
import { Options, ConvertParams } from "./components/options";

function Main() {

    let convert = (params: ConvertParams) => {

    };

    return (<>
        <main>
            <Header />
            <Container className="options" fluid="md">
                <Options handleSubmit={convert} />
            </Container>
            <Howto />
        </main>
    </>);
}

export default Main;