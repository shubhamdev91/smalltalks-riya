// the talks: relative times (TLK-009). Each <time data-st-ago="<unix seconds>"> renders "9 Oct" from Liquid; under
// 7 days old it becomes "just now", "n min ago", "nh ago" or "nd ago". The patterns come from locale through data
// attributes on [data-st-ago-strings], so no copy lives here.

const strings = /** @type {HTMLElement | null} */ (document.querySelector('[data-st-ago-strings]'))?.dataset ?? {};

/** @param {string | undefined} pattern @param {number} n */
const fill = (pattern, n) => (pattern ? pattern.replace('__n__', String(n)) : null);

for (const el of /** @type {NodeListOf<HTMLTimeElement>} */ (document.querySelectorAll('time[data-st-ago]'))) {
  const at = Number(el.dataset.stAgo) * 1000;
  if (!at) continue;
  const minutes = Math.floor((Date.now() - at) / 60000);
  if (minutes < 0) continue;
  let text = null;
  if (minutes < 1) text = strings.agoNow ?? null;
  else if (minutes < 60) text = fill(strings.agoMinutes, minutes);
  else if (minutes < 1440) text = fill(strings.agoHours, Math.floor(minutes / 60));
  else if (minutes < 10080) text = fill(strings.agoDays, Math.floor(minutes / 1440));
  if (text) el.textContent = text;
}
