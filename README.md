# Coming Back — Kay Lummitsch

Bilingual website at https://kaylummitsch.com (English) and https://kaylummitsch.com/de/ (German). Articles, posts, booklets, newsletter signup and Interview Rides. Documentation updated 18 October 2026.

## Production

This is a **Cloudflare Worker with static assets**, not Cloudflare Pages.

- Repository: `kay-lummitsch-org/coming-back`; production branch `main`.
- Cloudflare Worker: `coming-back`, custom domain `kaylummitsch.com`.
- Dashboard build command: empty. Production deploy command: `npx wrangler deploy`; branch previews use `npx wrangler preview`.
- `public/` contains generated, committed pages and assets. Python runs locally before committing, not during Cloudflare deployment.
- `wrangler.jsonc` defines `worker.mjs`, the `ASSETS` binding and `/api/*` Worker routing, D1, email binding and retry schedule.
- Static routes serve assets directly. `/api/interview-rides` validates and stores enquiries, then notifies Kay by email.

## Edit and verify

Edit `build.py`, `build_german.py`, `build_interview_rides.py` and the relevant files in `content/`. Run:

```sh
python3 build.py
node tests/interview-rides.mjs
node tests/notifications.mjs
```

Use a current Node.js with built-in Request/Response for the tests. Commit the relevant source changes and generated `public/` output. Review the PR, check the Cloudflare build, then merge to deploy. Preserve unrelated working-tree changes.

For local visual review: `python3 preview_server.py` → http://127.0.0.1:8765/ . The local server's form uses a separate SQLite test inbox, **not** production D1 or email. Branch previews currently omit production D1/email bindings; they are visual previews, not live-form tests.

## Documentation

- [TECH_STACK.md](TECH_STACK.md): components, data flow and responsibilities.
- [INTERVIEW_RIDES_OPERATIONS.md](INTERVIEW_RIDES_OPERATIONS.md): storage schema, notifications, checks and recovery.
- [INTERVIEW_RIDES_PREVIEW.md](INTERVIEW_RIDES_PREVIEW.md): local-only preview instructions.
- Project decisions and editorial approvals are maintained in the shared Notion handover memo. Editorial Google Docs and approved original images remain in Google Drive.

## Content and services

EN/DE language links are explicit; only the English homepage entry negotiates browser language, with a saved manual language choice taking precedence. English is the fallback.

Newsletter subscriptions use Sender (MORE KAY, form `epYyZ1`) and are separate from Interview Rides. Personal domain mail is routed through Cloudflare to Gmail; personal outgoing domain mail uses SMTP2GO. Interview Rides notifications use Cloudflare's fixed-recipient email binding.

The original 32-page Digital Journeymen PDF is available at `/booklets/the-digital-journeymen/`; the updated cover does not change the interior. Font files are not shipped: DIN Next is used locally when available, with system fallbacks.

No paid plan was added for Interview Rides. Platform free-tier limits still apply. No credentials, private enquiry data or local SQLite databases belong in Git or `public/`.
