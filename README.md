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
- **Lobby / Start session:** the QR code stays on screen while students join. A list of everyone who has joined builds up (✕ removes someone), and students wait on a "Waiting for your teacher to start" screen. Press **Start session** to open the dashboard and let students begin. Students who join after that go straight in. A teacher page refresh during class skips the lobby; **End room** resets it.
- **Students:** scan the QR code with the iPad camera, enter a name, start drawing. (Or open the site and type the 6-letter room code.)
- **Background picture:** click **Set background** (or drag an image onto the page, or paste one with Ctrl/Cmd+V) to put a worksheet, diagram or photo behind every student's whiteboard. You choose whether to keep or clear what students have already drawn. Students who join later get the picture automatically. The eraser only removes ink, never your picture, and recordings include the picture.
- **Send image as tab:** click **🖼️ Send image as tab** (or *Send as image tab* inside Draw & send) to send a reference picture to every student. It opens in its own browser tab on their iPad, with just the image (they can pinch-zoom it and close the tab when finished). They can't draw on it. Browsers block pop-ups that aren't triggered by a tap, so ClassBoard tries to open the tab automatically and, if blocked, shows an **Open image** button on the student's screen (one tap). Students can allow pop-ups for the site in their browser settings to make it fully automatic. A **📎 Images** button reopens anything sent earlier.
- **Draw & send:** click **✏️ Draw & send** to open a full-screen teacher whiteboard (same tools, zoom and text as students). Draw a diagram, question or example, then **Send to all students**. It becomes every student's background, just like Set background, and you choose whether to keep or clear their current drawings. If a background is already set you can tick *Draw on the current background* to annotate it first.
- **Student photos (📷 Photo):** a student taps **📷 Photo** on their toolbar and chooses *Photo Library*, *Take Photo* or *Choose File* on the iPad. The photo becomes their own whiteboard background, and they can zoom in to look at detail, then draw, circle and write their findings on it. The teacher sees the photo and the drawing live on that student's screen. **Remove photo** puts back the teacher's background (or a blank board). Good for "find it, zoom in, annotate it" tasks. If the teacher sets a new background, it replaces students' photos.
- **Screenshot (📸):** a student taps **📸 Screenshot** (also on the small floating button when the toolbar is hidden) to save a picture of exactly what is on their screen, at their current zoom and pan, including any teacher marks and the background. On an iPad a share sheet opens: tap **Save Image** to put it in the camera roll. If the browser can't open the share sheet, a preview appears with *press and hold → Add to Photos* and a Download button. It's disabled while the teacher has the screen locked.
- **Timer (⏱ Timer):** click **⏱ Timer**, pick minutes and seconds (or a preset), and press Start. The countdown shows on the teacher hub and in the corner of every student iPad, including students who join late. Pause, resume or stop it from the hub. When it reaches zero everyone sees **Time's up!** and hears a beep (iPads play sound once the student has touched the screen at least once).
- **Clear all screens (🧹):** resets every student's screen to a blank canvas: their drawings, your drawings on their screens, their photos and the background are all removed. It asks you to confirm first. The grid overlay and timer are left alone.
- **Zoom and pan:** on student iPads pinch with two fingers to zoom (up to 500%) and drag with two fingers to move around; or use the − / + / Fit buttons and the ✋ Pan tool. Teachers get the same controls (mouse wheel, trackpad pinch, buttons, ✋ Pan) on a maximised screen. Zoom is per-device, so zooming in doesn't change anyone else's view.
- **Full screen and hide toolbar (student):** **▲ Hide toolbar** collapses the toolbar so the whiteboard fills the whole display; a small faded **▼ Tools** button stays in the top-left corner to bring it back (its dot turns red if the connection drops). **⛶ Full screen** hides the browser's address bar and tabs too (tap ✕ or the same button to exit). Full screen works on iPad Safari and desktop browsers; on devices that don't support it the button doesn't appear, and Share → Add to Home Screen gives the same effect. Both can be combined, and a teacher lock still overrides everything.
- **Coordinate graph (▦ Grid → Coordinate graph):** choose **Full (±)** for a graph with all four quadrants (negatives too, origin in the middle) or **Quarter (+)** for positives only (origin bottom-left). Either one switches on a square grid behind labelled x and y axes with numbers, so students can see exactly where coordinates line up. Grid size, colour, line strength and the darker line every 5/10 (counted from the origin) all still work. Choose **None** to go back to an ordinary maths-book grid.
- **Snap to grid (student):** whenever a grid is on, a **☐ Snap to grid** button appears on the student toolbar. Tick it and pens, lines, squares, circles and text land exactly on the nearest grid crossing (on a coordinate graph, exact coordinates). The eraser never snaps.
- **Math tools (🧮):** opens a tray at the bottom with four tabs: **Numicon** (shapes 1–10), **Place value** (tokens for 1, 10, 100, 1,000, 10,000, 100,000 and 1,000,000), **Base ten** (ones, tens and hundreds blocks) and **Protractor** (see-through, 0–180° scales in both directions). Drag a piece onto the board, or tap it to drop it in the middle. Tap a piece with the ↖ Move tool to select it: drag it to move, use the round handle above it to rotate (it snaps to every 15°), the bottom-right handle to resize, and the red ✕ to delete. Pieces sit above pen marks, so the eraser never rubs them out, and the protractor can be laid over drawn angles to measure them. The teacher sees every piece live, and teachers can use the same tray on a maximised screen or in Draw & send.
- **Move tool (↖):** tap a shape, line, pen stroke or piece of text and drag it to a new place. A dashed blue box shows what you've grabbed. You can only move your own marks, and Undo still removes the most recent item. Teachers moving their own marks on a student's screen update live there too.
- **Text tool:** tap **Aa Text**, tap where the text should go, type, and press Add. Text size follows the Size slider.
- **Teacher drawing:** maximise a student's screen (⋮ → Maximise, or Random screen) and a toolbar appears. Anything you draw or type shows live on that student's iPad. **Remove my drawings** deletes only the teacher's marks and keeps the student's work. Students can't erase your marks, and their Clear button doesn't remove them.
- **Random screen:** the dice button shuffles a highlight across the students and then maximises one (it avoids repeating the last pick). Esc returns to the gallery.
- **Lock screens (🔒):** freeze a student's whiteboard so they can't do anything on it. Use **⋮ → Lock screen** on one tile, or **🔒 Lock all** in the top bar (it becomes **🔓 Unlock all**). A locked student sees a dimmed board with a "Screen locked" card; drawing, tools, zoom, text, photos and Clear are all disabled, and any stroke in progress is dropped. They can still see your drawings, messages and the timer. A locked tile shows a **🔒 LOCKED** badge on your hub. You can still maximise a locked screen and draw on it yourself. Students who join or reconnect while **Lock all** is on are locked automatically, and locks survive a teacher page refresh (same room). **End room** clears them.
- **Per-screen menu (⋮):** Maximise / Restore, Message screen, Lock / Unlock screen, Screen record (downloads an MP4), Kick user.
- The room code is remembered, so a teacher refresh keeps the same QR code. **End room** retires it.

## How it works

Students connect to the teacher directly over WebRTC using [PeerJS](https://peerjs.com). The free public PeerJS server is used only for the initial handshake; drawing data goes device-to-device. Each stroke/shape is sent as a small message, and the teacher's page redraws it on a per-student canvas.

## Notes and limits

- **Recording format:** MP4 works in Safari and Chrome/Edge 126+. Older browsers fall back to WebM. Recording captures what the teacher's browser is showing, so keep the tab visible (background tabs throttle).
- **School networks:** some block peer-to-peer traffic. If students can't connect, add a TURN server in `PEER_OPTS` at the top of the script, or self-host a PeerServer (options are commented there).
- **Reliability of the public PeerJS server:** it is free and best-effort. For heavy daily use, self-host `peerjs-server`.
- Anyone with the room code can join, so only show the QR to your class. Kick removes a user, and **End room** closes everything.

## Ideas for later

Multi-page PDF worksheets, portrait-shaped boards, message all students, save a student's board as PNG, pages/backgrounds (grid, lined), student raise-hand button.

## Editing and resizing text

- **Edit:** double-click (or double-tap) any text on the board to change it. With the **Aa Text** tool a single click on existing text edits it.
- **Resize:** with **↖ Move**, tap text to select it, then drag the blue corner handle to make it bigger or smaller. Drag the text itself to move it.
- In the text box, **Enter** starts a new line; press the **Add text / Save** button to finish.

## Unlimited canvas (per student)

Each student has an **∞ Unlimited canvas** tickbox in their toolbar. Unticked is the normal fixed page.

- **Ticked:** the canvas has no edges. Drag with two fingers (or the ✋ Pan tool, or scroll / trackpad) to move around, pinch or ctrl+scroll to zoom, and keep drawing anywhere. **Fit all** zooms to show everything they have drawn.
- **Switching back:** work outside the page is hidden (not deleted) in Page mode, and the student is warned first. Ticking again brings it back.
- **Teacher:** the student's tile in the gallery shows the part of the canvas they are working on (with an ∞ badge). Maximising a tile opens on that same spot and follows the student as they move. If the teacher drags or zooms, they stop following and can look around freely; **⟲ Follow student** snaps back. Teacher drawings use the same coordinates, so the student sees them in the right place.
- **Worksheets:** a teacher background sits where the page is (with a thin outline).
- **Under the hood:** marks are stored in unbounded "world" coordinates; a camera (`board.cam`) decides what is drawn. Students send `{t:'mode'}` and `{t:'cam'}` messages; page-mode students are unchanged.
