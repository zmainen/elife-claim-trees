// Rendering markdown the site owns, and filling its figures from the corpus.
//
// Two pages render repository markdown: /method from docs/method.md, and /docs/*
// from docs/cli/*.md. They shared nothing, which is how a convention gets applied to one of
// them — so the substitution, the guard, and the shiki configuration live here once.
//
// Every countable figure in that prose is a {{token}} filled from corpus-facts.json, which
// scripts/corpus_facts.py computes from the claim files. This exists because every stale
// number this site has shipped — "12 papers", "310 claims", "231 claims · 503 relations" —
// was one somebody typed into a page, while the counts that stayed right were generated at
// build. The numbers are no longer in the prose to go stale.
//
// An unknown token throws rather than rendering as {{...}}: a build that fails is a problem
// someone fixes, and a page that quietly shows its own placeholder is one nobody notices.
import { readFileSync } from 'fs';
import { join } from 'path';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeShiki from '@shikijs/rehype';
import rehypeStringify from 'rehype-stringify';

// Paths resolve against site/, which is process.cwd() at build.
const ROOT = join(process.cwd(), '..');

let cachedFacts: Record<string, unknown> | null = null;

export function facts(): Record<string, unknown> {
  if (!cachedFacts) {
    cachedFacts = JSON.parse(
      readFileSync(join(process.cwd(), 'src/data/corpus-facts.json'), 'utf8'));
  }
  return cachedFacts!;
}

/**
 * Read a markdown file from the repository and fill its {{token}}s.
 *
 * A token may name a nested value — `{{relation_counts.entails}}` — because the counts worth
 * quoting are often one entry of a generated map, and the alternative is a page that types
 * the number beside a table generated from the same file.
 */
export function readDoc(relPath: string): string {
  const raw = readFileSync(join(ROOT, relPath), 'utf8');
  const f = facts();
  // A backslash escapes a token, so a page can name the convention without invoking it.
  // Without this the guard fires on any prose that explains what a {{token}} is — which it
  // did, on the contributors' page, which is a good sign about the guard and a bad one about
  // having no way to quote.
  // The key charset includes `-`, because half the relation names have one. Without it a
  // token like {{relation_counts.derived-from}} did not match the pattern at all, so it was
  // not substituted *and* not caught by the guard below — it rendered as its own placeholder,
  // which is the exact failure this guard exists to prevent.
  return raw.replace(/(\\)?\{\{([\w.-]+)\}\}/g, (_m, esc: string | undefined, key: string) => {
    if (esc) return `{{${key}}}`;
    let v: unknown = f;
    for (const part of key.split('.')) {
      if (v === null || typeof v !== 'object' || !(part in (v as object))) {
        throw new Error(
          `${relPath} uses {{${key}}}, which corpus-facts.json does not define. ` +
          `Add it to scripts/corpus_facts.py or fix the token.`);
      }
      v = (v as Record<string, unknown>)[part];
    }
    if (v !== null && typeof v === 'object') {
      throw new Error(
        `${relPath} uses {{${key}}}, which is a ${Array.isArray(v) ? 'list' : 'map'} rather ` +
        `than a figure. Name one of its entries.`);
    }
    return String(v);
  });
}

// allowDangerousHtml is fine here — the source is the repository's own prose.
const processor = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeShiki, { theme: 'github-dark', fallbackLanguage: 'text' })
  .use(rehypeStringify, { allowDangerousHtml: true });

export async function renderMd(md: string): Promise<string> {
  return String(await processor.process(md));
}

/** The first `# Heading` of a document, which is its title. */
export function titleOf(md: string, fallback: string): string {
  return md.match(/^#\s+(.+)$/m)?.[1].trim() ?? fallback;
}

/** Everything after the leading `# Heading`, so a layout can render the title itself. */
export function bodyOf(md: string): string {
  return md.replace(/^#\s+.+$/m, '').trim();
}
