# Interview Rides

Source invitation: Google Doc `1RiiOTKiIKZxtmk4sK4VAltYGjCDbnyElZfdTD6DZeR8`, read 18 October 2026. AI concept images were approved for this release.

## Production

- English `/interview-rides/`; German `/de/interview-rides/`.
- Existing Cloudflare Worker `coming-back`; deploy through GitHub main as before.
- Worker handles only `/api/*`; static pages remain on asset serving.
- D1 `interview-rides` (`a155bc82-bbd8-4a37-b80a-069675ea5a2c`), EU jurisdiction, bound as `RIDES_DB`.
- Durable enquiry storage precedes the success response. No public endpoint lists or reads enquiries. No newsletter subscription is created.
- Read enquiries in the authenticated Cloudflare D1 dashboard → interview-rides → Explore Data → enquiries. No automatic email notification is configured in this release.
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
