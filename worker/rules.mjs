// Who counts as a reader, and where they came from. Pure functions: see test.mjs.

export const HOST = 'theshipjava.uk';

// A visit must look like a real browser (allowlist), not name a bot or tool (blocklist),
// AND be a top-level page open.
const BROWSER = /Mozilla\/5\.0 .*(Chrome|Chromium|Firefox|FxiOS|Safari|Edg|OPR|SamsungBrowser)/;
const BOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|embed|fetch|curl|wget|python|httpclient|okhttp|powershell|headless|lighthouse|monitor|uptime|whatsapp|mastodon|signal|telegram|skype|linkedin|pinterest|vkshare|go-http-client|java\/|node|axios|undici|scrapy/i;

// Browsers send Sec-Fetch-* on every request and page scripts cannot forge them, so a
// page pulled in by another site's hidden <img>, <iframe>, fetch() or prefetch is not a
// page open. Older browsers that send no Sec-Fetch headers at all still count.
export function isPageOpen(req) {
  const h = req.headers, ua = h.get('user-agent') || '';
  if (req.method !== 'GET' || !BROWSER.test(ua) || BOT.test(ua)) return false;
  const mode = h.get('sec-fetch-mode'), dest = h.get('sec-fetch-dest');
  if (mode && mode !== 'navigate') return false;
  if (dest && dest !== 'document') return false;
  const purpose = [h.get('sec-purpose'), h.get('purpose'), h.get('x-purpose'), h.get('x-moz')].filter(Boolean).join(' ');
  return !/prefetch|prerender|preview/i.test(purpose);
}

// Search engines and social sites use many hostnames; everything else is shown by hostname.
const SOURCES = [[/(^|\.)google\./, 'Google'], [/(^|\.)bing\.com$/, 'Bing'], [/(^|\.)duckduckgo\.com$/, 'DuckDuckGo'],
  [/(^|\.)(facebook\.com|fb\.com|fb\.me)$/, 'Facebook'], [/(^|\.)(twitter\.com|x\.com)$|^t\.co$/, 'X (Twitter)'],
  [/(^|\.)yahoo\./, 'Yahoo'], [/(^|\.)wikipedia\.org$/, 'Wikipedia']];

export function sourceOf(req) {
  let host;
  try {
    const ref = new URL(req.headers.get('referer') || '');
    if (!/^https?:$/.test(ref.protocol)) return 'Direct';
    host = ref.hostname.toLowerCase().replace(/^www\./, '');
  } catch { return 'Direct'; }
  if (host === HOST || !host) return 'Direct';
  for (const [re, name] of SOURCES) if (re.test(host)) return name;
  // Only a plain hostname is ever stored, so nothing else can be planted in the stats
  return /^[a-z0-9.-]{3,60}$/.test(host) ? host : 'Other';
}
