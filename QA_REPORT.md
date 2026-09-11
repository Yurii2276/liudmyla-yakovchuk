# QA Report — Final Release

Date: 2026-09-11

Automated checks performed on the final build:

- Mobile 390 px: hamburger visible, desktop navigation hidden
- Mobile hamburger opens and contains 6 links
- EN/УКР switch works on Home and Media
- Language persistence logic exists on both pages (localStorage + URL sync)
- No horizontal overflow on Home or Media at mobile width
- Media page contains 6 rendered images (hero + 5 gallery photos)
- All Media images decode successfully
- All Media source images are high-resolution (minimum longest side: 940 px)
- Tablet 834 px: hamburger visible, no horizontal overflow
- Desktop 1440 px: full navigation visible, hamburger hidden, no horizontal overflow
- Desktop Media images decode successfully

Result: 24/24 checks passed.

Media gallery uses the original high-quality source photographs with new filenames to bypass old browser/CDN caches.
