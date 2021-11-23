import { useState } from "react";
import { Container, Row } from "react-bootstrap";
import Header from "./components/header"
import { Options, ConvertParams } from "./components/options";

function Main() {

    let convert = (params: ConvertParams) => {

    };

    return (<>
        <Header />
        <Container className="options" fluid="md">
            <Options handleSubmit={convert} />
        </Container>
    </>);
}

export default Main;