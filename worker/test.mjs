// node worker/test.mjs — the rules for who counts as a reader and where they came from.
import assert from 'node:assert/strict';
import { isPageOpen, sourceOf } from './rules.mjs';

const CHROME = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';
const req = (headers, method = 'GET') => new Request('https://theshipjava.uk/', { method, headers });
const nav = { 'user-agent': CHROME, 'sec-fetch-mode': 'navigate', 'sec-fetch-dest': 'document' };

assert.equal(isPageOpen(req(nav)), true, 'a browser opening a page');
assert.equal(isPageOpen(req({ 'user-agent': CHROME })), true, 'an older browser with no Sec-Fetch headers');
assert.equal(isPageOpen(req(nav, 'HEAD')), false, 'HEAD');
assert.equal(isPageOpen(req({ ...nav, 'user-agent': 'curl/8.4.0' })), false, 'curl');
assert.equal(isPageOpen(req({ ...nav, 'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)' })), false, 'Googlebot');
assert.equal(isPageOpen(req({ ...nav, 'user-agent': CHROME.replace('Chrome', 'HeadlessChrome') })), false, 'headless');
assert.equal(isPageOpen(req({ ...nav, 'sec-fetch-mode': 'no-cors', 'sec-fetch-dest': 'image' })), false, 'hidden <img>');
assert.equal(isPageOpen(req({ ...nav, 'sec-fetch-dest': 'iframe' })), false, 'iframe on another site');
assert.equal(isPageOpen(req({ ...nav, 'sec-purpose': 'prefetch' })), false, 'prefetch');

const from = referer => sourceOf(req(referer ? { referer } : {}));
assert.equal(from(''), 'Direct');
assert.equal(from('https://theshipjava.uk/read/'), 'Direct', 'our own pages are not a source');
assert.equal(from('https://www.google.com.au/'), 'Google');
assert.equal(from('https://l.facebook.com/l.php?u=x'), 'Facebook');
assert.equal(from('https://t.co/abc'), 'X (Twitter)');
assert.equal(from('https://www.wikitree.com/wiki/Java'), 'wikitree.com', 'other sites by hostname, without www');
assert.equal(from('android-app://com.google.android.gm/'), 'Direct', 'not a web page');
assert.equal(from('https://xn--<script>.example/'), 'Direct', 'not a valid address');
assert.equal(from('https://' + 'a'.repeat(70) + '.example/'), 'Other', 'over-long hostname is not stored');
console.log('ok');
