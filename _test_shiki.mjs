import { readFileSync } from 'node:fs';
import { createHighlighter } from 'shiki';

const coalGrammar = JSON.parse(
  readFileSync(new URL('./shiki/coal.tmLanguage.json', import.meta.url), 'utf-8')
);

// Override the name to match our desired id
const highlighter = await createHighlighter({
  themes: ['github-light', 'github-dark'],
  langs: [
    {
      ...coalGrammar,
      name: 'coal',
      id: 'coal',
      scopeName: 'source.coal'
    }
  ]
});

console.log('Loaded langs:', highlighter.getLoadedLanguages());

const code = 'module Main {\n  import IO(println_string)\n  fun main() = println_string("Hello, Coal!")\n}';
try {
  const html = highlighter.codeToHtml(code, { lang: 'coal', theme: 'github-light' });
  console.log('HIGHLIGHTED:', html.substring(0, 200));
} catch(e) {
  console.log('Highlight failed:', e.message);
}