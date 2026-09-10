// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://zmainen.github.io',
  base: '/elife-claim-trees',
  integrations: [
    react(),
    starlight({
      title: 'eLife Claim Trees',
      description: 'Documentation for the elife-claim-trees extraction pipeline',
      // Mount Starlight at /docs/ — coexists with /papers/, /method/, /findings/.
      routeMiddleware: undefined,
      logo: undefined,
      customCss: ['./src/styles/starlight-overrides.css'],
      // Match the existing site's nav style: minimal, tight.
      components: {
        Header: './src/components/StarlightHeader.astro',
      },
      sidebar: [
        {
          label: 'Overview',
          items: [
            { label: 'What this system is', slug: 'docs/overview/what-this-is' },
            { label: 'Quick demo — one paper end to end', slug: 'docs/overview/quick-demo' },
            { label: 'When to use it', slug: 'docs/overview/when-to-use' },
          ],
        },
        {
          label: 'Methodology',
          items: [
            { label: 'The 8-step process', slug: 'docs/methodology/eight-step' },
            { label: 'The claim schema', slug: 'docs/methodology/schema' },
            { label: 'What the curator does, what the system does', slug: 'docs/methodology/division-of-labor' },
          ],
        },
        {
          label: 'Architecture',
          items: [
            { label: 'The pipeline at a glance', slug: 'docs/architecture/pipeline' },
            { label: 'The three-agent partition', slug: 'docs/architecture/three-agent-partition' },
            { label: 'Reconciliation', slug: 'docs/architecture/reconciliation' },
            { label: 'The external reviewer (Step 4.5)', slug: 'docs/architecture/external-reviewer' },
            { label: 'The review gate', slug: 'docs/architecture/review-gate' },
          ],
        },
        {
          label: 'Using the CLI',
          items: [
            { label: 'Install and configure', slug: 'docs/cli/install' },
            { label: 'One paper end to end', slug: 'docs/cli/first-paper' },
            { label: 'The seven subcommands', slug: 'docs/cli/subcommands' },
            { label: 'Coverage and marks', slug: 'docs/cli/coverage-and-marks' },
            { label: 'Review modes — when to use each', slug: 'docs/cli/review-modes' },
            { label: 'Batch operation', slug: 'docs/cli/batch' },
            { label: 'Cost and performance', slug: 'docs/cli/cost' },
          ],
        },
        {
          label: 'Validation',
          items: [
            { label: 'How we measure quality', slug: 'docs/validation/methodology' },
            { label: 'The 10-paper sweep results', slug: 'docs/validation/results' },
            { label: 'Known limitations', slug: 'docs/validation/limitations' },
            { label: 'Iteration discipline', slug: 'docs/validation/iteration' },
          ],
        },
        {
          label: 'Reference',
          items: [
            { label: 'Configuration reference', slug: 'docs/reference/config' },
            { label: 'The 9 roles', slug: 'docs/reference/roles' },
            { label: 'The 14 edge types', slug: 'docs/reference/edges' },
            { label: 'The prompts', slug: 'docs/reference/prompts' },
            { label: 'API reference', slug: 'docs/reference/api' },
            { label: 'Glossary', slug: 'docs/reference/glossary' },
          ],
        },
        {
          label: 'For contributors',
          items: [
            { label: 'Code structure', slug: 'docs/contributing/code-structure' },
            { label: 'Adding a prompt variant', slug: 'docs/contributing/prompt-variant' },
            { label: 'Running validation', slug: 'docs/contributing/validation' },
            { label: 'Design decisions', slug: 'docs/contributing/design-decisions' },
          ],
        },
      ],
      // Render Starlight under /docs/ — this is the prefix.
      // (Starlight content lives at src/content/docs/; the URL prefix is set by
      // the integration's default behavior + base in astro config.)
    }),
  ],

  vite: {
    plugins: [tailwindcss()]
  }
});
