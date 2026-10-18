# Interview Rides

Source invitation: Google Doc `1RiiOTKiIKZxtmk4sK4VAltYGjCDbnyElZfdTD6DZeR8`, read 18 October 2026. AI concept images were approved for this release.

## Production

- English `/interview-rides/`; German `/de/interview-rides/`.
- Existing Cloudflare Worker `coming-back`; deploy through GitHub main as before.
- Worker handles only `/api/*`; static pages remain on asset serving.
- D1 `interview-rides` (`a155bc82-bbd8-4a37-b80a-069675ea5a2c`), EU jurisdiction, bound as `RIDES_DB`.
- Durable enquiry storage precedes the success response. No public endpoint lists or reads enquiries. No newsletter subscription is created.
- Read enquiries in the authenticated Cloudflare D1 dashboard → interview-rides → Explore Data → enquiries. New enquiries trigger an email from kay@kaylummitsch.com to the verified lummitsch@gmail.com inbox (the same inbox used by kay@ forwarding). Reply-To is the visitor’s email. A durable notifications outbox retries failed sends every five minutes, up to 24 attempts; sent_at records provider acceptance. Delivery is at-least-once: a provider success followed by a database failure may produce a duplicate.
- Only use submissions to arrange Interview Rides; honour access/deletion requests at kay@kaylummitsch.com. Review and remove stale enquiries once no longer needed.

## Schema

```sql
CREATE TABLE IF NOT EXISTS enquiries (
 id TEXT PRIMARY KEY, created TEXT NOT NULL, name TEXT NOT NULL,
 email TEXT NOT NULL, mode TEXT NOT NULL, topic TEXT NOT NULL,
 region TEXT NOT NULL DEFAULT '', language TEXT NOT NULL,
 consent_version TEXT NOT NULL
);
```

## Validation

`python3 build.py` regenerates both pages, homepage teasers and sitemap.
`node tests/interview-rides.mjs` covers successful saving, validation, consent, origin checking, body limits, storage failure and static routing. Browser-check a clearly labelled fictitious enquiry after deployment and verify it in D1.

`preview_server.py` is local development only. Its SQLite test data under workspace output are never production data and must not be uploaded.

## Notification migration (applied 18 October 2026)

```sql
CREATE TABLE IF NOT EXISTS notifications (
 enquiry_id TEXT PRIMARY KEY REFERENCES enquiries(id),
 attempts INTEGER NOT NULL DEFAULT 0,
 next_attempt INTEGER NOT NULL DEFAULT 0,
 sent_at TEXT, last_error TEXT
);
CREATE INDEX IF NOT EXISTS notifications_pending ON notifications (sent_at, next_attempt);
```

No visitor data is sent before the enquiry and notification job commit together. Mail errors do not erase or reject a saved enquiry. The email binding is restricted to Kay’s verified Gmail destination. No paid outbound plan or visitor confirmation email is enabled. Check `last_error` for unresolved notifications.
