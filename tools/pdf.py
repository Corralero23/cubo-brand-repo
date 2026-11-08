import pathlib
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1123, "height": 794})
    pg.goto("file://" + str(R / "print.html")); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.pdf(path=str(R.parent / "brand" / "COBU-Brand-Book.pdf"), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True)
    b.close()
