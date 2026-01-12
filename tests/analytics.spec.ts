import { test, expect } from '@playwright/test';
import path from 'path';

const fileUrl = (p: string) => `file://${path.join(process.cwd(), p)}`;

test.describe('Analytics instrumentation', () => {
  test('index CTAs and nav emit events', async ({ page }) => {
    await page.goto(fileUrl('docs/index.html'));
    // Enable debug mode before the script initializes
    await page.evaluate(() => { window.__SIMPLENALYTICS_DEBUG__ = true; });
    await page.reload();

    // Click nav 'Paper'
    await page.click('a[data-simple-nav-item="paper"]');
    // Click paper CTA card
    await page.click('a[data-cta-id="paper_card"]');

    const events = await page.evaluate(() => window.__SIMPLENEVENTS__ || []);
    // Expect events: click_nav and click_cta, and ensure no download_asset for .html
    const names = events.map((e: any) => e.name);
    expect(names).toContain('click_nav');
    expect(names).toContain('click_cta');
    expect(names).not.toContain('download_asset');

    // Verify payload keys
    const nav = events.find((e: any) => e.name === 'click_nav');
    expect(nav.payload.item).toBe('paper');
    const cta = events.find((e: any) => e.name === 'click_cta');
    expect(cta.payload.cta_id).toBe('paper_card');
  });

  test('outbound and download detection', async ({ page }) => {
    await page.goto(fileUrl('docs/index.html'));
    await page.evaluate(() => { window.__SIMPLENALYTICS_DEBUG__ = true; });
    await page.reload();

    // Click GitHub repo card (outbound + cta)
    await page.click('a[data-cta-id="repo_card"]');

    const events = await page.evaluate(() => window.__SIMPLENEVENTS__ || []);
    const outbound = events.find((e: any) => e.name === 'click_outbound');
    expect(outbound).toBeTruthy();
    expect(outbound.payload.host).toBe('github.com');
  });
});
