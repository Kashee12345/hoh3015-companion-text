/* Render print.html to the distributable PDF.
     node make-pdf.js   */
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage();
  await p.goto('file:///root/hoh3015-companion-text/print.html', { waitUntil: 'load' });
  await p.emulateMedia({ media: 'print' });
  await p.waitForTimeout(1500);
  await p.pdf({ path: 'HOH3015_Companion_Text.pdf', format: 'Letter',
    printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await b.close();
})();
