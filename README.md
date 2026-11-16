# ClassBoard

A live classroom whiteboard hub. Students scan a QR code on their iPad, enter their name, and draw on a whiteboard. The teacher sees every student's screen in a live gallery.

No server of your own is needed: it is one static file (`index.html`).

## Deploy on GitHub Pages

1. Create a new GitHub repository (e.g. `classboard`).
2. Upload `index.html` (and this README) to the repo root.
3. Go to **Settings → Pages**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
4. After a minute your app is live at `https://<your-username>.github.io/classboard/`.

## Using it

- **Teacher:** open the site on a laptop, click **Open teacher hub**. A room is created and a QR code appears. Keep this tab open and visible during class.
- **Students:** scan the QR code with the iPad camera, enter a name, start drawing. (Or open the site and type the 6-letter room code.)
- **Background picture:** click **Set background** (or drag an image onto the page, or paste one with Ctrl/Cmd+V) to put a worksheet, diagram or photo behind every student's whiteboard. You choose whether to keep or clear what students have already drawn. Students who join later get the picture automatically. The eraser only removes ink, never your picture, and recordings include the picture.
- **Random screen:** the dice button shuffles a highlight across the students and then maximises one (it avoids repeating the last pick). Esc returns to the gallery.
- **Per-screen menu (⋮):** Maximise / Restore, Message screen, Screen record (downloads an MP4), Kick user.
- The room code is remembered, so a teacher refresh keeps the same QR code. **End room** retires it.

## How it works

Students connect to the teacher directly over WebRTC using [PeerJS](https://peerjs.com). The free public PeerJS server is used only for the initial handshake; drawing data goes device-to-device. Each stroke/shape is sent as a small message, and the teacher's page redraws it on a per-student canvas.

## Notes and limits

- **Recording format:** MP4 works in Safari and Chrome/Edge 126+. Older browsers fall back to WebM. Recording captures what the teacher's browser is showing, so keep the tab visible (background tabs throttle).
- **School networks:** some block peer-to-peer traffic. If students can't connect, add a TURN server in `PEER_OPTS` at the top of the script, or self-host a PeerServer (options are commented there).
- **Reliability of the public PeerJS server:** it is free and best-effort. For heavy daily use, self-host `peerjs-server`.
- Anyone with the room code can join, so only show the QR to your class. Kick removes a user, and **End room** closes everything.

## Ideas for later

Multi-page PDF worksheets, portrait-shaped boards, message all students, lock/unlock all boards, save a student's board as PNG, pages/backgrounds (grid, lined), student raise-hand button.
