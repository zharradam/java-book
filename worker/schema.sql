-- D1 (SQLite) schema for the readership counter in worker/index.js.
-- Applied on every deploy by .github/workflows/build.yml. Safe to re-run.

-- Every tally: one row per Adelaide day, metric and key, e.g.
--   ('2026-11-24', 'views', '/read/introduction.html') -> 12
--   ('2026-11-24', 'visits', '') -> 7        ('2026-11-24', 'country', 'AU') -> 5
CREATE TABLE IF NOT EXISTS stat (
  day TEXT NOT NULL,                -- YYYY-MM-DD, Australia/Adelaide
  m   TEXT NOT NULL,                -- views | visits | source | country | download
  k   TEXT NOT NULL,                -- key within the metric
  n   INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, m, k)
) WITHOUT ROWID;

-- Visits in progress: an irreversible code per visitor and when they last opened a page.
-- Rows are deleted within a day; see the privacy note in worker/index.js.
CREATE TABLE IF NOT EXISTS seen (
  code TEXT PRIMARY KEY,
  last INTEGER NOT NULL             -- ms since epoch
) WITHOUT ROWID;

-- The random salt behind today's codes. Only today's row is kept.
CREATE TABLE IF NOT EXISTS salt (
  day   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) WITHOUT ROWID;

-- Downloads GitHub had counted (11-23 November 2026) before the site began counting its own.
INSERT OR IGNORE INTO stat (day, m, k, n) VALUES
  ('2026-11-11', 'download', 'pdf', 3),
  ('2026-11-11', 'download', 'epub', 6);
