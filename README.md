# Coming Back — Kay Lummitsch

Static website for Cloudflare Pages. Five posts/articles with standalone reading pages an upcoming booklet announcement, and The Digital Journeymen with a full PDF download.

## Cloudflare Pages

- Connect this GitHub repository.
- Production branch: `main`.
- Framework preset: None.
- Build command: leave empty.
- Build output directory: `public`.

No dependencies, database, paid services, tracking or cookies are required.

## Edit

Edit copy and layout in `build.py`, article texts in `content/source-texts.json`, then run `python3 build.py` and commit the generated `public` directory. Cloudflare serves the generated files directly; Python does not run at deployment.

## Before production

- Confirm which articles should be available before their scheduled LinkedIn dates.
- Add each exact LinkedIn article/post URL when available. The current links go to Kay's profile and are labelled accordingly.
- Confirm that the DIN Next licence permits web embedding before uploading the font files to a public repository. The website currently uses a locally installed DIN Next font when available, with system sans-serif fallbacks; it ships no font files.
- The booklet is upcoming and has no checkout or ordering functionality.
- Add any required publisher/contact information appropriate for the final site.

## The Digital Journeymen

The published booklet lives at `/booklets/the-digital-journeymen/`. Its 32-page PDF uses the updated cover; interior pages and acknowledgements remain original. Cover and spread previews are derived from that PDF.
