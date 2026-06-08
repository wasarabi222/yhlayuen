const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("C:/Users/hwaeu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright@1.60.0/node_modules/playwright");

const root = path.resolve(__dirname, "..");
const siteDir = path.join(root, "yhlayuen_site");
const screenshotDir = path.join(root, "qa_screenshots");
const pages = ["index.html", "about.html"];
const widths = [390, 768, 1280];
const languages = ["ko", "en"];

fs.mkdirSync(screenshotDir, { recursive: true });

function pageUrl(fileName) {
  return pathToFileURL(path.join(siteDir, fileName)).href;
}

(async () => {
  const browser = await chromium.launch({
    executablePath: "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  });
  const results = [];

  for (const pageName of pages) {
    for (const width of widths) {
      for (const language of languages) {
        const page = await browser.newPage({ viewport: { width, height: 1200 }, deviceScaleFactor: 1 });
        await page.goto(pageUrl(pageName), { waitUntil: "networkidle" });
        await page.locator(`[data-lang-option="${language}"]`).click();
        await page.screenshot({
          path: path.join(screenshotDir, `${pageName.replace(".html", "")}-${language}-${width}.png`),
          fullPage: true,
        });

        const overflows = await page.evaluate(() => {
          return Array.from(document.querySelectorAll("body *"))
            .map((el) => {
              const rect = el.getBoundingClientRect();
              return {
                tag: el.tagName.toLowerCase(),
                className: typeof el.className === "string" ? el.className : "",
                text: (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 80),
                scrollWidth: Math.ceil(el.scrollWidth),
                clientWidth: Math.ceil(el.clientWidth),
                rectWidth: Math.ceil(rect.width),
              };
            })
            .filter((item) => item.scrollWidth > item.clientWidth + 2 && item.rectWidth > 0)
            .slice(0, 20);
        });

        const htmlLang = await page.locator("html").evaluate((el) => el.lang);
        const bodyLang = await page.locator("body").evaluate((el) => el.dataset.lang);

        results.push({ pageName, width, language, htmlLang, bodyLang, overflows });
        await page.close();
      }
    }
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
