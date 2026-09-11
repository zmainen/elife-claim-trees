import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

export const collections = {
  // The formats comparison is loaded straight out of exports/ — the artifact
  // `scripts/formats_report.py` writes, not a copy of it. The site renders that
  // file so a figure here cannot disagree with the export it describes; the two
  // came apart twice when the page restated the numbers.
  formats: defineCollection({
    loader: glob({
      pattern: '*.formats.md',
      base: '../exports',
      // The default id slugifies the filename, which eats the dot and yields
      // `gadeke-2026-guilt-insulaformats`. The entry id is the paper slug.
      generateId: ({ entry }) => entry.replace(/\.formats\.md$/, ''),
    }),
  }),
};
