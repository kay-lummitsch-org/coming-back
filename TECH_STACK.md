# Website technology and responsibilities

Verified implementation: 18 October 2026. Production feature release: PR #15 and #16, commit `4b023b2621131f3f2841465a56ae0761a0edb693`.

## Components

| Component | Role |
| --- | --- |
| Google Drive / Docs | Editorial originals, invitations, final post copy and approved images. |
| Notion | Authoritative shared decisions, milestones and handover. Credentials and browser sessions do not transfer with notes. |
| GitHub `kay-lummitsch-org/coming-back` | Website source, generated assets, tests, code history and PR review. |
| Python standard library | Local static generation through `build.py`, `build_german.py`, `build_interview_rides.py`; no Python service in production. |
| HTML, CSS, browser JavaScript | EN/DE pages, responsive presentation, language switching, form submission. No front-end framework. |
| Cloudflare Workers / Static Assets | Worker `coming-back` serves the custom domain. Static assets in `public/`; only `/api/*` runs Worker code first. |
| Cloudflare D1 | EU-jurisdiction `interview-rides` database, `RIDES_DB` binding. Enquiries and durable mail outbox. |
| Cloudflare `send_email` | `RIDES_EMAIL`, restricted to verified `lummitsch@gmail.com`; new-enquiry notifications from `kay@kaylummitsch.com`. Visitor email is Reply-To. |
| Cloudflare Cron Triggers | `*/5 * * * *` retries pending mail jobs (10 per run, maximum 24 attempts per job). This is part of the deployed Worker, not a chat reminder. |
| Cloudflare DNS / HTTPS | Domain resolution, mail records and encrypted public website connection. |
| Cloudflare Email Routing | Incoming `kay@kaylummitsch.com` → Gmail; unchanged by the form notification feature. |
| Gmail + SMTP2GO | Gmail is the mailbox/UI; SMTP2GO sends personal mail using the domain address. Separate from form notifications. |
| Sender | Newsletter subscriptions, double opt-in, subscriber group and campaigns. Separate from Interview Rides. |
| Google Search Console | Discovery/indexing diagnostics; generated sitemap, canonical and alternate-language links support discovery. Index inclusion is not guaranteed. |

## Live enquiry flow

1. Visitor submits name, email, ride mode, topic, optional region/dates and permission to contact them.
2. `POST /api/interview-rides` requires same-origin JSON, validates fields, a honeypot and a streamed 20 KB limit.
3. D1 atomically commits `enquiries` plus `notifications`. Only then does the API return success.
4. A background task sends Kay a plain-text mail. A successful provider result is recorded in `sent_at`.
5. Failed jobs remain durable and are retried by the Worker schedule. Errors do not erase the enquiry or create a newsletter subscription.

Enquiry data has no public read endpoint. Admin inspection is through the authenticated Cloudflare dashboard. No visitor confirmation email is sent. No SMTP password or API secret is added to Worker source.

## Languages and editorial boundaries

English: `/interview-rides/`; German: `/de/interview-rides/`. Both homepages link to the corresponding page. Dates start March 2027; interest can be expressed now. This is not a binding tour/rental booking. Both images are labelled AI concept visualisations.

The invitation and LinkedIn post are related but distinct editorial artifacts. The post's opening describes talking **while riding together**, not interviewing a category of people who happen to ride motorcycles. The final Matt Chalmers dirt-bike line must be retained; LinkedIn needs a native mention, which cannot be preserved merely by copying plain text.

## Operations and limits

See [INTERVIEW_RIDES_OPERATIONS.md](INTERVIEW_RIDES_OPERATIONS.md) for schema and mail recovery. A provider success followed by a status-write failure may cause a duplicate; `sent_at` is not proof of inbox delivery. There is no external dead-letter alert, CAPTCHA, dedicated rate limit or automatic retention deletion yet. Review exhausted jobs manually; honour access/deletion requests.

Static deployment does not run `build.py`; generated files must be committed. Branch previews omit production D1/email bindings. The local Python server stores only fictitious tests in a separate SQLite file outside `public/` and never sends these emails. No paid plan was enabled; free-tier limits apply.

## Verification evidence

- API and notification tests passed.
- Both live languages reviewed; fictitious form entry persisted in D1.
- A notification was triggered by a fictitious live enquiry, seen in the Gmail inbox and confirmed received by Kay on 18 October 2026.
- Live data is not a source-code backup: protect/export it separately through Cloudflare as needed. Git rollback must retain required bindings and schema; a deployment rollback does not undo database changes.
