# COBU brand workspace

COBU is a Home & Kitchen e-commerce brand (Instagram: @cobugoods). First product: the Pancake Batter Dispenser (clear tapered bottle, white screw lid, red silicone valve tip, stainless steel whisk ball, white screw-off base). Launching on Amazon.

## Brand rules (full detail in `brand/COBU-Brand-Book.pdf`)
- Logo: "The Pot O" — COBU in Archivo Expanded SemiBold; the O is a pot with a domed lid. Icon = the pot with side handles. Always use the master files in `logos/`; never retype or redraw.
- Colours: Navy `#1E2A44` and Warm White `#F6F1E7` (primary), Mustard `#D8A23E` (accent, small doses), Mist `#C9D3DF` (support), Ink `#141A28` (text).
- Type: Archivo Expanded SemiBold for headlines and labels, Archivo Regular for body. Free on Google Fonts.
- Write the name as COBU in capitals.
- Instagram profile picture: single-colour warm white pot on navy. Highlight covers may use the mustard lid.
- Only make product claims the owner has confirmed (no capacity, materials or dishwasher claims unless stated).

## Folders
- `brand/` brand book (PDF + web page)
- `logos/` wordmark, icon and Instagram profile files (SVG + high-res PNG)
- `instagram/` highlights (1080×1920) and feed posts (1080×1350)
- `product/` product and listing images
- `tools/` Python scripts that rebuild the logos, brand book and stories (`identity.py` holds the logo geometry; fonts in `tools/fonts/`). Need Python, Pillow, fontTools and Playwright with Chromium.

## Skills for images and video
`.claude/settings.json` enables the HyperFrames plugin (HeyGen) for video work, including avatar/lip-sync clips via `media-use`. Remotion, Photoroom and any plugins installed on the owner's claude.ai account load automatically as well.
