const modes = {pillion: 'Bei Kay mitfahren', own: 'Eigenes Motorrad', rental: 'Leihmotorrad'};

export async function notifyEnquiry(env, enquiry) {
  // Acquire a short lease so scheduled retries cannot send concurrently.
  const claim = await env.RIDES_DB.prepare(
    "UPDATE notifications SET attempts = attempts + 1, next_attempt = ? WHERE enquiry_id = ? AND sent_at IS NULL AND next_attempt <= ? AND attempts < 24 RETURNING enquiry_id"
  ).bind(Date.now() + 300000, enquiry.id, Date.now()).first();
  if (!claim) return;
  try {
    await env.RIDES_EMAIL.send({
      from: 'kay@kaylummitsch.com', to: 'lummitsch@gmail.com',
      replyTo: enquiry.email,
      subject: 'Interview Rides – neue Anfrage',
      text: [
        'Eine neue Interview-Rides-Anfrage ist eingegangen.', '',
        `Name: ${enquiry.name}`, `E-Mail: ${enquiry.email}`,
        `Fahrvariante: ${modes[enquiry.mode] || enquiry.mode}`,
        `Region / Zeitraum: ${enquiry.region || 'Keine Angabe'}`, '',
        'Gesprächsthema:', enquiry.topic, '',
        `Eingang: ${enquiry.created}`, `Referenz: ${enquiry.id}`, '',
        'Mit Antworten erreichst Du direkt die anfragende Person.',
        'Die Anfrage ist zusätzlich in Deinem Cloudflare-Dateneingang gespeichert.'
      ].join('\n')
    });
    await env.RIDES_DB.prepare('UPDATE notifications SET sent_at = ?, last_error = NULL WHERE enquiry_id = ?')
      .bind(new Date().toISOString(), enquiry.id).run();
  } catch {
    // Keep personal data and provider errors out of public responses and logs.
    await env.RIDES_DB.prepare('UPDATE notifications SET last_error = ? WHERE enquiry_id = ?')
      .bind('send_failed', enquiry.id).run();
  }
}

export async function retryNotifications(env) {
  const pending = await env.RIDES_DB.prepare(
    'SELECT e.* FROM notifications n JOIN enquiries e ON e.id = n.enquiry_id WHERE n.sent_at IS NULL AND n.next_attempt <= ? AND n.attempts < 24 ORDER BY e.created LIMIT 10'
  ).bind(Date.now()).all();
  for (const enquiry of pending.results) await notifyEnquiry(env, enquiry);
}
