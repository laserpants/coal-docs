// Shiki-based syntax highlighter for Coal language
// Reads JSON from stdin: { code: string, lang: string }
// Outputs highlighted HTML to stdout

import { readFileSync } from 'node:fs';
import { createHighlighter } from 'shiki';

// Load the Coal TextMate grammar and override the name for correct language ID
const coalGrammar = JSON.parse(
  readFileSync(new URL('./coal.tmLanguage.json', import.meta.url), 'utf-8')
);

// Set name to 'coal' so Shiki uses it as the language identifier (the 'id'
// field is not enough in v3 — the name must match)
coalGrammar.name = 'coal';
coalGrammar.id = 'coal';
coalGrammar.scopeName = 'source.coal';

// Create a highlighter with the custom language registered
const shiki = await createHighlighter({
  themes: ['github-light', 'github-dark'],
  langs: [coalGrammar]
});

// Read input from stdin
const input = JSON.parse(await new Promise((resolve) => {
  let data = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => data += chunk);
  process.stdin.on('end', () => resolve(data));
}));

const { code, lang } = input;

// Highlight the code with both themes
const htmlLight = shiki.codeToHtml(code, { lang: 'coal', theme: 'github-light' });
const htmlDark = shiki.codeToHtml(code, { lang: 'coal', theme: 'github-dark' });

// Extract the code content (without the <pre><code> wrapper)
const extractCode = (html) => {
  const match = html.match(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/);
  return match ? match[1] : html;
};

const codeContent = extractCode(htmlLight);

// Output both light and dark versions with CSS variables for theme switching
// The Material theme uses [data-md-color-scheme="slate"] for dark mode
const output = `<pre class="language-coal"><code class="language-coal language-coal-light">${codeContent}</code><code class="language-coal language-coal-dark" style="display:none">${extractCode(htmlDark)}</code></pre>`;

console.log(JSON.stringify({ html: output }));