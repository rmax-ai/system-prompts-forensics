import { test, expect } from '@playwright/test';
import path from 'path';
const fileUrl = (p: string) => `file://${path.join(process.cwd(), p)}`;

test('helper functions exposed on window', async ({ page }) => {
  await page.goto(fileUrl('docs/index.html'));
  await page.evaluate(() => { window.__SIMPLENALYTICS_DEBUG__ = true; });
  await page.reload();

  const helpers = await page.evaluate(() => ({
    host: window.AnalyticsHelpers.normalizeHost('www.GitHub.com'),
    ext: window.AnalyticsHelpers.fileTypeFromPath('/path/to/file.PDF?download=1'),
    extHtml: window.AnalyticsHelpers.fileTypeFromPath('/paper.html'),
    email: window.AnalyticsHelpers.sanitizeEmail('mailto:hello@rmax.ai')
  }));

  expect(helpers.host).toBe('github.com');
  expect(helpers.ext).toBe('pdf');
  expect(helpers.extHtml).toBeUndefined();
  expect(helpers.email).toBe('@rmax.ai');
});
