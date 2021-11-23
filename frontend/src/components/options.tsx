import React, { ChangeEvent, useState } from "react";
import { Button, Card, Col, Form, FormLabel, Row } from "react-bootstrap";

export interface ConvertParams {
    playlistUrl: string;
    oldPlaylistEditor: boolean;
    showTitle?: string;
    showDate?: string
}

export function Options(_: { handleSubmit: (options: ConvertParams) => void }) {
    let [playlistUrl, setPlaylistUrl] = useState<string>("");
    let [useOldPlaylistEditor, setUseOldPlaylistEditor] = useState<boolean>(localStorage.getItem("useOldPlaylistEditor") == "true");
    let [showTitle, setShowTitle] = useState<string | undefined>(localStorage.getItem("showTitle") || undefined);
    let [showDate, setShowDate] = useState<string | undefined>(undefined);

    let handleShowTitleChange = (ev: ChangeEvent<HTMLInputElement>) => {
        let showTitle = ev.currentTarget.value;

        // store show title in local storage, since it is likely to be the same across multiple visits
        localStorage.setItem("showTitle", showTitle);
        setShowTitle(showTitle);
    };

    let handleOutputFormatChanged = (ev: ChangeEvent<HTMLInputElement>) => {
        // store preferred output format in local storage, since it is likely to stay the same across multiple visits
        let useOldPlaylistEditor = ev.currentTarget.checked;

        localStorage.setItem("useOldPlaylistEditor", useOldPlaylistEditor.toString());
        setUseOldPlaylistEditor(useOldPlaylistEditor);
    }

    let handleSubmit = (ev: React.MouseEvent<HTMLButtonElement>) => {
        ev.preventDefault();
    };

    return <>
        <Form>
            <Form.Group className="mb-3" controlId="playlistUrl">
                <Form.Label>Playlist URL</Form.Label>
                <Form.Control placeholder="https://open.spotify.com/playlist/4BmW06g5m70HkwZEA1mds9?si=9f6b19eec5fd44e3" value={playlistUrl} onChange={e => setPlaylistUrl(e.currentTarget.value)} required={true} />
            </Form.Group>
            <Form.Group className="" controlId="oldPlaylistEditor">
                <Form.Check checked={useOldPlaylistEditor} onChange={handleOutputFormatChanged} label="Format for Old Playlist Editor" />
            </Form.Group>
            {useOldPlaylistEditor ?
                (<Row className="px-2">
                    <Col>
                        <Form.Group controlId="showTitle">
                            <Form.Label>Show title</Form.Label>
                            <Form.Control placeholder="hot tub listening club" value={showTitle} onChange={handleShowTitleChange} required={true} />
                            <Form.Text>Your show's title as it appears in the station interface.</Form.Text>
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group controlId="showDate">
                            <Form.Label>Show date</Form.Label>
                            <Form.Control type="date" value={showDate} onChange={e => setShowDate(e.currentTarget.value)} required={true} />
                            <Form.Text>The date this show will air.</Form.Text>
                        </Form.Group>
                    </Col>
                </Row>)
                : null}
            <Button variant="primary" type="submit" className="mt-3" onClick={handleSubmit}>Convert</Button>
        </Form>
    </>;
}
