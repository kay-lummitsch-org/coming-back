# Interview Rides — local preview

**Production is live.** The earlier preview-only milestone has been completed. Current production behaviour and schema are documented in [INTERVIEW_RIDES_OPERATIONS.md](INTERVIEW_RIDES_OPERATIONS.md) and [TECH_STACK.md](TECH_STACK.md).

Run `python3 preview_server.py`, then open http://127.0.0.1:8765/de/interview-rides/ or http://127.0.0.1:8765/interview-rides/ . Both homepages include an entry before Posts & Articles.

`build_interview_rides.py` is invoked by `build.py` after `build_german.py`. Styles and form behaviour are in `public/interview-rides.css` and `public/interview-rides.js`. Approved AI concept images are `public/assets/interview-rides-{beiz,pass}.png`; visible labels identify them as concepts.

The local server saves test enquiries in the workspace's `output/interview-rides/preview-interest.sqlite3`, outside `public/`. It does not use production D1 or send emails. Generated page text is now production text; local success only proves a local test save. Use fictitious data only. The backend API and notification unit tests are separate Node tests.

Real form/email testing uses the deployed domain and an explicitly labelled fictitious enquiry. Branch previews have no production database/email bindings. Preserve existing working-tree changes and never upload the SQLite test database.
