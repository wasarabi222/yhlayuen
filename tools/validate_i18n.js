const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const site = path.join(root, "yhlayuen_site");
const contentPath = path.join(site, "content.js");
const htmlFiles = fs.readdirSync(site).filter((file) => file.endsWith(".html"));
const bannedPatterns = [
  /약력은 제공된/,
  /기존 조사 자료/,
  /최종 원문/,
  /확인을 권장/,
  /provided materials/i,
  /prior research/i,
  /should be confirmed/i,
  /프로필 허브/,
  /이 홈페이지는/,
  /A[h]rayeon/,
];

const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync(contentPath, "utf8"), context, { filename: contentPath });

function getValue(object, key) {
  return key.split(".").reduce((value, part) => value && value[part], object);
}

const content = context.window.YHLAYUEN_CONTENT;
const missing = [];
const banned = [];
const keys = new Set();

for (const file of htmlFiles) {
  const filePath = path.join(site, file);
  const html = fs.readFileSync(filePath, "utf8");

  for (const pattern of bannedPatterns) {
    if (pattern.test(html)) banned.push(`${file}: ${pattern}`);
  }

  for (const match of html.matchAll(/data-i18n(?:-html)?="([^"]+)"/g)) {
    const key = match[1];
    keys.add(key);
    const value = getValue(content, key);
    if (!value) {
      missing.push(`${file}: ${key} is missing`);
      continue;
    }
    for (const lang of ["ko", "en"]) {
      if (typeof value[lang] !== "string" || !value[lang].trim()) {
        missing.push(`${file}: ${key}.${lang} is missing`);
      }
    }
  }
}

for (const pattern of bannedPatterns) {
  if (pattern.test(fs.readFileSync(contentPath, "utf8"))) banned.push(`content.js: ${pattern}`);
}

console.log(`i18n keys used: ${keys.size}`);
console.log(`missing translations: ${missing.length}`);
console.log(`banned phrases: ${banned.length}`);

if (missing.length) console.log(missing.join("\n"));
if (banned.length) console.log(banned.join("\n"));

if (missing.length || banned.length) process.exit(1);
