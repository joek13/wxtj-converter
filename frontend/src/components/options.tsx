import React, { ChangeEvent, useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";

export interface ConvertParams {
    playlistUrl: string;
    oldPlaylistEditor: boolean;
    showTitle?: string;
    showDate?: string
}

export function Options(props: { loading: boolean, handleSubmit: ((options: ConvertParams) => void) }) {
    let { handleSubmit, loading } = props;

    let [playlistUrl, setPlaylistUrl] = useState<string>("");
    let [useOldPlaylistEditor, setUseOldPlaylistEditor] = useState<boolean>(localStorage.getItem("useOldPlaylistEditor") === "true");
    let [showTitle, setShowTitle] = useState<string | undefined>(localStorage.getItem("showTitle") || undefined);
    let [showDate, setShowDate] = useState<string | undefined>(undefined);

    let handleShowTitleChange = (ev: ChangeEvent<HTMLInputElement>) => {
        let showTitle = ev.currentTarget.value;

        // store show title in local storage, since it is likely to be the same across multiple visits
        localStorage.setItem("showTitle", showTitle);
        setShowTitle(showTitle);
    };

    let handleOutputFormatChanged = (ev: ChangeEvent<HTMLInputElement>) => {
        let useOldPlaylistEditor = ev.currentTarget.checked;

        // store preferred output format in local storage, since it is likely to stay the same across multiple visits
        localStorage.setItem("useOldPlaylistEditor", useOldPlaylistEditor.toString());
        setUseOldPlaylistEditor(useOldPlaylistEditor);
    }

    let handleFormSubmit = (ev: React.MouseEvent<HTMLFormElement>) => {
        ev.preventDefault();

        // TODO: validate that URL is actually a Spotify URL?

        // build selected options into ConvertParams
        let params: ConvertParams = {
            "playlistUrl": playlistUrl,
            "oldPlaylistEditor": useOldPlaylistEditor,
            "showTitle": showTitle,
            "showDate": showDate
        };

        handleSubmit(params);
    };

    return (<Form onSubmit={handleFormSubmit}>
        <Form.Group className="mb-3" controlId="playlistUrl">
            <Form.Label>Playlist URL</Form.Label>
            <Form.Control type="url" placeholder="https://open.spotify.com/playlist/4BmW06g5m70HkwZEA1mds9?si=9f6b19eec5fd44e3" value={playlistUrl} onChange={e => setPlaylistUrl(e.currentTarget.value)} required={true} disabled={loading} />
        </Form.Group>
        <Form.Group className="mb-2" controlId="oldPlaylistEditor">
            <Form.Check checked={useOldPlaylistEditor} onChange={handleOutputFormatChanged} label="Format for Old Playlist Editor" disabled={loading} />
        </Form.Group>
        {useOldPlaylistEditor ?
            (<Row>
                <Col>
                    <Form.Group controlId="showTitle">
                        <Form.Label>Show title</Form.Label>
                        <Form.Control placeholder="hot tub listening club" value={showTitle} onChange={handleShowTitleChange} required={true} disabled={loading} />
                        <Form.Text>Your show's title as it appears in the station interface.</Form.Text>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group controlId="showDate">
                        <Form.Label>Show date</Form.Label>
                        <Form.Control type="date" value={showDate} onChange={e => setShowDate(e.currentTarget.value)} required={true} disabled={loading} />
                        <Form.Text>The date this show will air.</Form.Text>
                    </Form.Group>
                </Col>
            </Row>)
            : null}
        <div className="text-center">
            {/* if we are currently loading, disable the button */}
            <Button variant="primary" type="submit" className="mt-3" disabled={loading}>Convert</Button>
        </div>
    </Form>);
}
