"""Captures the app screenshots used in the report and slides.

Needs: pip install playwright, Microsoft Edge installed, and the page served at
http://localhost:8765 (python -m http.server 8765). Start the backend first
(node backend/server.js) to capture AI-written lessons instead of samples.

    python scripts/capture_screenshots.py
"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("LC_SHOT_DIR", os.path.join(ROOT, "results", "screenshots"))
URL = "http://localhost:8765/index.html"
os.makedirs(OUT, exist_ok=True)


def wait_ready(page, topic=None):
    cond = ("!document.getElementById('btnCreate').disabled && "
            "!document.getElementById('quizCard').classList.contains('hidden')")
    if topic:
        cond += f" && document.getElementById('quizCard').dataset.topic === {topic!r}"
    page.wait_for_function(cond, timeout=90000)
    page.wait_for_timeout(600)


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    page = browser.new_page(viewport={"width": 1366, "height": 900}, device_scale_factor=1.5)

    # 1. Learn tab, Grade 5 water cycle
    page.goto(URL)
    wait_ready(page)
    page.click("#gradeButtons button:has-text('5')")
    page.click("button[data-topic='The water cycle']")
    wait_ready(page, "The water cycle")
    page.evaluate("window.scrollTo(0, 0)")
    page.screenshot(path=os.path.join(OUT, "app_home.png"))

    # 2. Quiz answered and graded (last answer wrong on purpose)
    right = page.evaluate("state.quiz.map(q => q[2])")
    page.click(f"#q0o{right[0]}")
    page.click(f"#q1o{right[1]}")
    page.click(f"#q2o{(right[2] + 1) % 4}")
    page.click("#btnCheck")
    page.locator("#quizCard").screenshot(path=os.path.join(OUT, "app_quiz.png"))
    # tighter crop for the report: last question + result box
    page.locator("#questions fieldset").last.scroll_into_view_if_needed()
    box_q = page.locator("#questions fieldset").last.bounding_box()
    box_r = page.locator("#quizResult").bounding_box()
    sy = page.evaluate("window.scrollY")       # bounding boxes are viewport-relative
    page.screenshot(path=os.path.join(OUT, "app_quiz_result.png"), full_page=True, clip={
        "x": box_q["x"] - 12, "y": box_q["y"] + sy - 12, "width": box_q["width"] + 24,
        "height": box_r["y"] + box_r["height"] - box_q["y"] + 24})

    # 3. Check-any-text tab with the hard sample
    page.click("#tabCheck")
    page.click("text=Hard sample")
    page.select_option("#checkGrade", "6")
    page.click("details summary")
    page.wait_for_timeout(300)
    page.locator("#checkPanel").screenshot(path=os.path.join(OUT, "app_inspector.png"))

    browser.close()
print("saved screenshots to", OUT)
