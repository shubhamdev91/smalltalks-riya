// Relative talk times for pages that don't load st-talks.js (the landing's talks teaser, LND-065). Every
// time[data-st-ago] (snippets/st-talk-time.liquid) inside a [data-st-ago-strings] host takes that host's patterns:
// data-ago-now, data-ago-minutes, data-ago-hours, data-ago-days ("__n__" = the number). Under 7 days only; older times
// keep the server date. The copy lives with the host's section, so this file holds no shopper-visible text.
// st-talks.js does the same on the talks pages (TLK-009); keep the thresholds in step.

const fill = (pattern, n) => (pattern ? pattern.replace('__n__', String(n)) : null);

for (const host of document.querySelectorAll('[data-st-ago-strings]')) {
  const s = /** @type {HTMLElement} */ (host).dataset;
  for (const el of host.querySelectorAll('time[data-st-ago]')) {
    const at = Number(/** @type {HTMLElement} */ (el).dataset.stAgo) * 1000;
    if (!at) continue;
    const minutes = Math.floor((Date.now() - at) / 60000);
    let text = null;
    if (minutes < 1) text = s.agoNow ?? null;
    else if (minutes < 60) text = fill(s.agoMinutes, minutes);
    else if (minutes < 1440) text = fill(s.agoHours, Math.floor(minutes / 60));
    else if (minutes < 10080) text = fill(s.agoDays, Math.floor(minutes / 1440));
    if (text) el.textContent = text;
  }
}
