import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
const port = 18775,
  base = `http://127.0.0.1:${port}`,
  server = spawn(process.env.PYTHON || 'python3', ['-m', 'evidence_atlas', 'serve', String(port)], {
    stdio: ['ignore', 'pipe', 'inherit'],
  });
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {}
    if (server.exitCode !== null) throw Error('server exited');
    if (i === 99) throw Error('server timeout');
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1100 } }),
    errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const lang of ['fr', 'en', 'es']) {
    await page.goto(`${base}/?lang=${lang}`);
    await page.waitForFunction(() => document.querySelectorAll('.card').length >= 12);
    assert.equal(await page.locator('html').getAttribute('lang'), lang);
    const before = await page.locator('#coverage-count').textContent();
    assert.ok(['20/26', '26/26'].includes(before));
    await page.locator('#tab-coverage').click();
    assert.equal(await page.locator('.topic').count(), 26);
    await page.locator('#remove-proof').check();
    await page.waitForFunction(
      (expected) => document.getElementById('coverage-count').textContent === expected,
      `${Number(before.split('/')[0]) - 1}/26`,
    );
    assert.ok((await page.locator('.topic.not_reproduced').count()) >= 1);
    await page.locator('#remove-proof').uncheck();
    await page.waitForFunction(
      (expected) => document.getElementById('coverage-count').textContent === expected,
      before,
    );
    await page.locator('#tab-usage').click();
    assert.equal(await page.locator('#declarations .proof').count(), 1);
    assert.ok((await page.locator('#declarations').textContent()).includes('@typesafe-ai/sdk'));
    await page.locator('#tab-freshness').click();
    await page.locator('#source-changed').check();
    await page.locator('#fresh-check').click();
    await page.waitForFunction(
      () =>
        document.getElementById('fresh-result').dataset.status === 'source_changed_requires_review',
    );
    await page.locator('#source-changed').uncheck();
    await page.locator('#replay-failed').check();
    await page.locator('#fresh-check').click();
    await page.waitForFunction(
      () => document.getElementById('fresh-result').dataset.status === 'reproduction_failed',
    );
    const event = page.waitForEvent('download');
    await page.locator('#download').click();
    assert.equal((await event).suggestedFilename(), 'oss-evidence-ledger.json');
    await page.locator('#tab-projects').click();
    await page.locator('#project-filter').selectOption('jev');
    assert.ok((await page.locator('.card').count()) < 13);
  }
  await page.goto(`${base}/?lang=fr`);
  await page.waitForFunction(() => document.querySelectorAll('.card').length >= 12);
  await mkdir('.local', { recursive: true });
  await page.screenshot({ path: '.local/preview-fr.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.deepEqual(errors, []);
  console.log(
    'FR/EN/ES: project gallery, 26 workstreams, missing-proof detection, declaration limits, stale source and failed reproduction, export, filters and mobile verified.',
  );
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}
