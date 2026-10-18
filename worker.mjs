const json = (body, status = 200) => Response.json(body, {
  status, headers: {'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'}
});

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(request);
    if (url.pathname !== '/api/interview-rides') return json({error: 'Not found'}, 404);
    if (request.method !== 'POST') return json({error: 'Method not allowed'}, 405);
    if (request.headers.get('Origin') !== url.origin ||
        request.headers.get('Sec-Fetch-Site') === 'cross-site') return json({error: 'Forbidden'}, 403);
    if (!(request.headers.get('Content-Type') || '').startsWith('application/json')) return json({error: 'JSON required'}, 415);
    try {
      // Bound the stream before parsing, including requests without Content-Length.
      const reader = request.body?.getReader();
      if (!reader) return json({error: 'Empty request'}, 400);
      let size = 0; const chunks = [];
      while (true) {
        const {done, value} = await reader.read();
        if (done) break;
        size += value.byteLength;
        if (size > 20000) { await reader.cancel(); return json({error: 'Too large'}, 413); }
        chunks.push(value);
      }
      const bytes = new Uint8Array(size); let offset = 0;
      for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
      let data;
      try { data = JSON.parse(new TextDecoder().decode(bytes)); }
      catch { return json({error: 'Invalid JSON'}, 400); }
      if (!data || typeof data !== 'object' || Array.isArray(data)) return json({error: 'Invalid form'}, 400);
      if (data.company) return json({error: 'Invalid form'}, 400);
      const limits = {name: 100, email: 254, topic: 3000, region: 200};
      const clean = {};
      for (const [key, max] of Object.entries(limits)) {
        if (key === 'region' && data[key] == null) data[key] = '';
        if (typeof data[key] !== 'string') return json({error: 'Invalid field'}, 400);
        clean[key] = data[key].trim();
        if (clean[key].length > max || (key !== 'region' && !clean[key])) return json({error: 'Invalid field'}, 400);
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clean.email) ||
          !['pillion', 'own', 'rental'].includes(data.mode) ||
          !['de', 'en'].includes(data.language) || data.consent !== true) return json({error: 'Invalid form'}, 400);
      const id = crypto.randomUUID();
      // Parameters keep visitor content separate from SQL. No public read endpoint.
      const result = await env.RIDES_DB.prepare(
        'INSERT INTO enquiries (id, created, name, email, mode, topic, region, language, consent_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
      ).bind(id, new Date().toISOString(), clean.name, clean.email, data.mode,
        clean.topic, clean.region, data.language, '2026-10-18').run();
      if (!result.success) return json({error: 'Storage unavailable'}, 503);
      return json({saved: true, id}, 201);
    } catch {
      // Never log personal form contents or report success on a storage failure.
      return json({error: 'Storage unavailable'}, 503);
    }
  }
};
