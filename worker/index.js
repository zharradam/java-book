/*
  theshipjava.uk, served by a Cloudflare Worker: the static site (built into _site/) plus a
  readership counter that runs on the server, so ad blockers cannot hide visits.

    GET  any page          served from _site/; real page opens are tallied afterwards
    GET  /download/<file>  tallies the download, then redirects to the GitHub release
    GET  /api/stats        the tallies, as JSON, for /stats/

  What is counted (table stat, one row per day + metric + key):
    views     a page opened in a real browser, keyed by path
    visits    a run of page opens with no gap longer than 30 minutes
    source    where each visit came from (the referring site's hostname)
    country   each visit's country, from Cloudflare's own geolocation
    download  each download link followed, keyed by file

  Privacy: no cookies, and nothing that identifies anyone is kept. To tell one visit from
  the next, the visitor's IP address and browser name are scrambled with a random salt into
  a code that cannot be reversed (table seen). The salt is replaced every day and the codes
  are deleted within a day; neither the IP address nor the browser name is ever stored.

  Only real browsers opening a page count. Bots, link previews, scripts and pages loaded
  invisibly by other websites do not, and cost no database work. Counting happens after
  the page has been sent, and if the database fails the site is served exactly as before:
  a counter must never be the reason the book is unavailable.
*/

import { HOST, isPageOpen, sourceOf } from './rules.mjs';

const RELEASE = 'https://github.com/zharradam/java-book/releases/latest/download/';
const DOWNLOADS = { 'the-java.pdf': 'pdf', 'the-java.epub': 'epub', 'the-java.m4b': 'audiobook' };
const VISIT_GAP = 30 * 60 * 1000;
const DAY = 24 * 60 * 60 * 1000;

// Counted on the real site and in local development, never on a preview address.
const isCounted = host => host === HOST || host === 'localhost' || host === '127.0.0.1';

// Days are Adelaide days: the book's home, and most of its readers.
const dayFmt = new Intl.DateTimeFormat('en-CA', { timeZone: 'Australia/Adelaide' });
const dayOf = ms => dayFmt.format(new Date(ms));

let saltCache = { day: '', value: '' };   // per Worker instance; the database holds the truth

// The day's salt, created on first use. Yesterday's salt and stale codes go at the same time.
async function saltFor(db, day, now) {
  if (saltCache.day === day) return saltCache.value;
  const out = await db.batch([
    db.prepare('INSERT OR IGNORE INTO salt (day, value) VALUES (?, ?)').bind(day, crypto.randomUUID()),
    db.prepare('DELETE FROM salt WHERE day < ?').bind(day),
    db.prepare('DELETE FROM seen WHERE last < ?').bind(now - DAY),
    db.prepare('SELECT value FROM salt WHERE day = ?').bind(day),
  ]);
  saltCache = { day, value: out[3].results[0].value };
  return saltCache.value;
}

async function visitorCode(salt, req) {
  const text = [salt, req.headers.get('cf-connecting-ip') || '', req.headers.get('user-agent') || ''].join('|');
  const bytes = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)));
  return Array.from(bytes.slice(0, 16), b => b.toString(16).padStart(2, '0')).join('');
}

const BUMP = 'INSERT INTO stat (day, m, k, n) VALUES (?, ?, ?, 1) ON CONFLICT (day, m, k) DO UPDATE SET n = n + 1';

// Tally one page open (metric 'views') or download. A visit that crosses midnight counts
// as two, because the salt changes: the price of not keeping codes longer than a day.
async function tally(env, req, metric, key) {
  const db = env.DB, now = Date.now(), day = dayOf(now);
  const code = await visitorCode(await saltFor(db, day, now), req);
  const bump = (m, k) => db.prepare(BUMP).bind(day, m, k);
  const batch = [bump(metric, key)];
  if (metric === 'views') {
    const seen = await db.prepare('SELECT last FROM seen WHERE code = ?').bind(code).first();
    batch.push(db.prepare('INSERT INTO seen (code, last) VALUES (?1, ?2) ON CONFLICT (code) DO UPDATE SET last = ?2').bind(code, now));
    if (!seen || now - seen.last > VISIT_GAP) {
      const country = req.cf && /^[A-Z]{2}$/.test(req.cf.country || '') ? req.cf.country : '??';
      batch.push(bump('visits', ''), bump('source', sourceOf(req)), bump('country', country));
    }
  }
  await db.batch(batch);
}

const count = (ctx, env, req, metric, key) =>
  ctx.waitUntil(tally(env, req, metric, key).catch(e => console.error('count failed:', e.message)));

const top = (rows, m, limit) => rows.filter(r => r.m === m).slice(0, limit).map(r => ({ name: r.k, n: r.n }));

async function stats(env) {
  const now = Date.now(), today = dayOf(now);
  const days = Array.from({ length: 30 }, (_, i) => dayOf(now - (29 - i) * DAY));
  const [totals, daily, parts, since] = await env.DB.batch([
    env.DB.prepare(`SELECT m, SUM(n) AS allTime, SUM(CASE WHEN day >= ?1 THEN n ELSE 0 END) AS month,
                    SUM(CASE WHEN day = ?2 THEN n ELSE 0 END) AS today
                    FROM stat WHERE m IN ('visits', 'views') GROUP BY m`).bind(days[0], today),
    env.DB.prepare("SELECT day, n FROM stat WHERE m = 'visits' AND day >= ?").bind(days[0]),
    env.DB.prepare("SELECT m, k, SUM(n) AS n FROM stat WHERE m NOT IN ('visits') GROUP BY m, k ORDER BY n DESC, k"),
    env.DB.prepare("SELECT MIN(day) AS day FROM stat WHERE m = 'visits'"),
  ]);
  const byDay = Object.fromEntries(daily.results.map(r => [r.day, r.n]));
  const total = m => { const t = totals.results.find(r => r.m === m); return { allTime: t?.allTime || 0, month: t?.month || 0, today: t?.today || 0 }; };
  const rows = parts.results;
  return {
    since: since.results[0].day, today,
    visits: total('visits'), views: total('views'),
    daily: days.map(day => ({ day, n: byDay[day] || 0 })),
    pages: top(rows, 'views', 30), sources: top(rows, 'source', 12), countries: top(rows, 'country', 12),
    downloads: Object.values(DOWNLOADS).map(k => ({ name: k, n: (rows.find(r => r.m === 'download' && r.k === k) || { n: 0 }).n })),
  };
}

// Files are served at exactly their own paths (wrangler.toml: html_handling "none"), so
// every address stays as it has always been; folders get their index.html here.
async function page(env, req, url) {
  const asset = path => env.ASSETS.fetch(new Request(new URL(path, url), req));
  const path = url.pathname;
  const res = await asset(path.endsWith('/') ? path + 'index.html' : path);
  const isFolderName = !path.endsWith('/') && !path.split('/').pop().includes('.');
  if (res.status === 404 && isFolderName && (await asset(path + '/index.html')).ok) {
    return Response.redirect(url.origin + path + '/' + url.search, 301);   // /read -> /read/
  }
  return res;
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    if (url.hostname === 'www.' + HOST || (url.hostname === HOST && url.protocol === 'http:')) {
      return Response.redirect(`https://${HOST}${url.pathname}${url.search}`, 301);
    }
    const counted = isCounted(url.hostname);

    if (url.pathname === '/api/stats') {
      try {
        return Response.json(await stats(env), { headers: { 'cache-control': 'no-store' } });
      } catch (e) {
        console.error('stats failed:', e.message);
        return Response.json({ error: 'unavailable' }, { status: 503, headers: { 'cache-control': 'no-store' } });
      }
    }

    const file = url.pathname.startsWith('/download/') && url.pathname.slice(10);
    if (file && Object.hasOwn(DOWNLOADS, file)) {
      if (counted && isPageOpen(req)) count(ctx, env, req, 'download', DOWNLOADS[file]);
      return new Response(null, { status: 302, headers: { location: RELEASE + file, 'cache-control': 'no-store' } });
    }

    let res = await page(env, req, url);
    const isPage = /\/$|\.html$/.test(url.pathname) && !url.pathname.startsWith('/stats/');
    if (counted && isPage && (res.status === 200 || res.status === 304) && isPageOpen(req)) {
      count(ctx, env, req, 'views', url.pathname.replace(/\/index\.html$/, '/'));
    }
    if (url.hostname !== HOST) {   // a preview address must never compete with the real site in search results
      res = new Response(res.body, res);
      res.headers.set('x-robots-tag', 'noindex');
    }
    return res;
  },
};
