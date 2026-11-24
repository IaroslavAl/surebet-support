# Surebet Stake Calculator support

Surebet Stake Calculator helps iPhone and iPad users split a total stake across outcomes and see the result for each one. This repository publishes the app’s support website on GitHub Pages. Visitors can learn how the calculator works, read the FAQ, or contact the developer.

[English](https://iaroslaval.github.io/surebet-support/en/) · [Русский](https://iaroslaval.github.io/surebet-support/ru/) · [Français](https://iaroslaval.github.io/surebet-support/fr/)

[Privacy policy](https://iaroslaval.github.io/surebet-support/en/privacy/) · [Download on the App Store](https://apps.apple.com/app/id1667102550)

## Updating the site

Edit the page text in `tools/build.py` and the privacy policies in `tools/content/privacy-*.html`. From the repository root, rebuild the pages and commit the generated HTML alongside the source changes.

```sh
python3 tools/build.py
```

The site uses paths under `/surebet-support/`. To preview it locally, serve the parent directory and open the [local English page](http://localhost:8765/surebet-support/en/).

```sh
cd ..
python3 -m http.server 8765
```

## Privacy and assets

- Keep all page resources on this site. The privacy policy commits the site to using no analytics, cookies, external fonts, CDNs, or other third-party requests.
- Screenshots follow the pattern `assets/{iphone,mini,duo}-{lang}[-dark].webp`. The build selects available localized and dark variants and uses English as the fallback.
- Use the official App Store badges from Apple Marketing Tools in `assets/badges/`. When CSS or images change, update `ASSET_VERSION` in `tools/build.py`.
- The build generates `assets/pattern.svg` from the four SF Symbols in `tools/symbols/`. The app icon and App Store header use the same artwork. Apple’s terms apply to SF Symbols.
