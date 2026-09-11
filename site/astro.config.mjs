// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
// Running a layer needs a server, and the published site is static. Rather than ship an
// adapter for one endpoint, the route is injected only under `astro dev` — so the capability
// exists where it can work and is simply absent where it cannot, which is what the pages
// assume when they show copy-and-run text instead of a button.
const devRun = {
  name: 'pipeline-dev-run',
  hooks: {
    'astro:config:setup': ({ command, injectRoute }) => {
      if (command !== 'dev') return;
      injectRoute({ pattern: '/dev-run.json', entrypoint: './src/dev/run-endpoint.ts' });
    },
  },
};

export default defineConfig({
  site: 'https://zmainen.github.io',
  base: '/elife-claim-trees',
  integrations: [
    react(),
    devRun,
  ],

  // /docs was 33 MDX pages under Starlight, and what replaced them is ten. The retired ones
  // are redirected rather than left to 404: they are what four months of external links point
  // at, and a reader who followed one is better served by the page that took over its subject
  // than by a 404 that makes the section look abandoned.
  //
  // Where a page's subject moved out of /docs entirely — the corpus, the schema, the layer
  // model — the target is the page that owns it now. That is most of them, which is the point
  // the issue was making: /docs had been describing things it did not own.
  // Destinations carry the base explicitly: Astro applies `base` to a redirect's source but
  // not to its target, so a bare '/docs/layers/' sends the reader to the domain root.
  redirects: {
    // Overview — the system, not the tools. The site's own front door, and the graph.
    '/docs/overview/what-this-is': '/elife-claim-trees/docs/',
    '/docs/overview/quick-demo': '/elife-claim-trees/docs/first-paper/',
    '/docs/overview/when-to-use': '/elife-claim-trees/docs/',

    // Methodology — docs/method.md renders at /pipeline/method, generated and current.
    '/docs/methodology/eight-step': '/elife-claim-trees/pipeline/method/',
    '/docs/methodology/schema': '/elife-claim-trees/pipeline/vocabulary/',
    '/docs/methodology/division-of-labor': '/elife-claim-trees/pipeline/method/',

    // Architecture — "the pipeline at a glance" meant the extraction run. The layer graph
    // means the whole thing, and the extraction run is the induction group within it.
    '/docs/architecture/pipeline': '/elife-claim-trees/pipeline/',
    '/docs/architecture/three-agent-partition': '/elife-claim-trees/pipeline/induction/',
    '/docs/architecture/reconciliation': '/elife-claim-trees/pipeline/reconcile/',
    '/docs/architecture/external-reviewer': '/elife-claim-trees/pipeline/external-review/',
    '/docs/architecture/review-gate': '/elife-claim-trees/docs/runner/',

    // Using the CLI — the pages that survived, renamed.
    '/docs/cli/install': '/elife-claim-trees/docs/install/',
    '/docs/cli/first-paper': '/elife-claim-trees/docs/first-paper/',
    '/docs/cli/subcommands': '/elife-claim-trees/docs/layers/',
    '/docs/cli/coverage-and-marks': '/elife-claim-trees/docs/layers/',
    '/docs/cli/review-modes': '/elife-claim-trees/docs/runner/',
    '/docs/cli/batch': '/elife-claim-trees/docs/batch/',
    '/docs/cli/cost': '/elife-claim-trees/docs/batch/',

    // Validation — one page now, on the tool that produces the numbers.
    '/docs/validation/methodology': '/elife-claim-trees/docs/evaluate/',
    '/docs/validation/results': '/elife-claim-trees/docs/evaluate/',
    '/docs/validation/limitations': '/elife-claim-trees/docs/evaluate/',
    '/docs/validation/iteration': '/elife-claim-trees/docs/evaluate/',

    // Reference — roles and edges are schema, and moved to the layers that ask about them.
    '/docs/reference/config': '/elife-claim-trees/docs/config/',
    '/docs/reference/prompts': '/elife-claim-trees/docs/prompts/',
    '/docs/reference/roles': '/elife-claim-trees/pipeline/vocabulary/',
    '/docs/reference/edges': '/elife-claim-trees/pipeline/vocabulary/',
    '/docs/reference/glossary': '/elife-claim-trees/pipeline/vocabulary/',
    '/docs/reference/api': '/elife-claim-trees/docs/layers/',

    // Contributing.
    '/docs/contributing/code-structure': '/elife-claim-trees/docs/contributing/',
    '/docs/contributing/prompt-variant': '/elife-claim-trees/docs/prompts/',
    '/docs/contributing/validation': '/elife-claim-trees/docs/evaluate/',
    '/docs/contributing/design-decisions': '/elife-claim-trees/docs/contributing/',
  },

  vite: {
    plugins: [tailwindcss()]
  }
});
