"""Captures the app screenshots used in the report and slides.

Needs: pip install playwright, Microsoft Edge installed, and the page served at
http://localhost:8765 (python -m http.server 8765). Start the backend first
(node backend/server.js) to capture AI-written lessons instead of samples.

    python scripts/capture_screenshots.py
"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "screenshots")
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

    # 3. Check-any-text tab with the hard sample
    page.click("#tabCheck")
    page.click("text=Hard sample")
    page.select_option("#checkGrade", "6")
    page.click("details summary")
    page.wait_for_timeout(300)
    page.locator("#checkPanel").screenshot(path=os.path.join(OUT, "app_inspector.png"))

    browser.close()
print("saved screenshots to", OUT)
