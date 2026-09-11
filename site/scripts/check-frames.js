// Fail the build when a page hand-rolls its own container.
//
// The site had six page widths and a nav that agreed with none of them, because `<main>`
// carried no container and every page invented one. That was fixed by declaring `.site-frame`
// once — and then reintroduced within hours by a new section whose six pages each wrote
// `max-w-4xl mx-auto px-4 sm:px-6` again. A convention nothing enforces is a convention that
// decays at the speed new pages are written, so this enforces it.
//
// The signature of a frame is the three together: a max-width, horizontal auto margins, and
// a horizontal gutter. An inner reading measure (`max-w-3xl` on a paragraph) has none of the
// other two and is not touched.

import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const roots = [join(here, '../src/pages'), join(here, '../src/layouts'), join(here, '../src/components')];

// Starlight owns its own shell; its pages are not ours to frame.
const EXEMPT = [/\/content\/docs\//];

const files = [];
const walk = (dir) => {
  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (/\.(astro|tsx|jsx)$/.test(e.name)) files.push(p);
  }
};
for (const r of roots) if (safeStat(r)) walk(r);
function safeStat(p) { try { return statSync(p); } catch { return null; } }

const CLASS_ATTR = /class(?:Name)?=["'`]([^"'`]+)["'`]/g;
const findings = [];

for (const file of files) {
  if (EXEMPT.some(re => re.test(file))) continue;
  const src = readFileSync(file, 'utf8');
  const lines = src.split('\n');
  lines.forEach((line, i) => {
    for (const m of line.matchAll(CLASS_ATTR)) {
      const cls = m[1];
      const hasMax = /\bmax-w-[\w[\]./-]+/.test(cls);
      const hasAuto = /\bmx-auto\b/.test(cls);
      const hasGutter = /\bp[xl]-\d/.test(cls) || /\bpx-\[/.test(cls);
      if (hasMax && hasAuto && hasGutter) {
        findings.push({ file: relative(join(here, '../..'), file), line: i + 1, cls: cls.trim() });
      }
    }
  });
}

if (findings.length) {
  console.error('\n  Hand-rolled page container(s) found. Use `site-frame` instead.\n');
  for (const f of findings) {
    console.error(`    ${f.file}:${f.line}`);
    console.error(`      class="${f.cls}"\n`);
  }
  console.error('  `.site-frame` is declared in src/styles/global.css and used by the nav and');
  console.error('  every page, so they share one gutter. Add `column` for a page that is a');
  console.error('  single column of prose. See the comment above that rule for why.\n');
  process.exit(1);
}

console.log(`Frames: ${files.length} files checked, no hand-rolled containers`);
