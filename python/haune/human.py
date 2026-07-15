"""Human-like interaction for the Haune Python client (sync Playwright).

Prefers the binary's NATIVE humanizer CDP commands
(``Input.synthesizeHumanMouseGesture`` / ``synthesizeHumanScrollGesture``) — these give
``movementX/Y != 0``, ``screenX != clientX``, real hover with no ``kFromDebugger``, and
``getCoalescedEvents() > 1``, which Playwright's own ``page.mouse`` cannot. Falls back to
``page.mouse`` / ``page.keyboard`` transparently if the running binary predates them.

    from haune import launch
    from haune.human import Human

    b = launch(); p = b.new_page(); p.goto("https://example.com")
    h = Human(p, seed=12345)
    h.show_cursor()                       # visible OS-style arrow (watching/demo)
    h.type_into("#q", "hello world")      # human typing (variable rhythm)
    h.click_selector("button[type=submit]")

Keyboard timing is the only keyboard automation tell (the event objects are already
indistinguishable), so typing shapes the rhythm: variable inter-key gaps, key-hold,
pauses after spaces/punctuation, occasional typos + correction.
"""
from __future__ import annotations

import random

_SPECIAL = {" ": "Space", "\n": "Enter", "\t": "Tab"}

_WIN_CURSOR = (
    '<svg width="22" height="30" viewBox="0 0 22 30" xmlns="http://www.w3.org/2000/svg"'
    ' style="display:block;filter:drop-shadow(0 1px 1px rgba(0,0,0,.45))">'
    '<path d="M1 1 L1 22 L6.4 16.9 L10 25.3 L13.4 23.9 L9.8 15.7 L17 15.7 Z"'
    ' fill="#000" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>'
)
_MAC_CURSOR = (
    '<svg width="20" height="30" viewBox="0 0 20 30" xmlns="http://www.w3.org/2000/svg"'
    ' style="display:block;filter:drop-shadow(0 1px 2px rgba(0,0,0,.5))">'
    '<path d="M1 1 L1 21.5 L6 16.7 L9.2 24.5 L12 23.3 L8.9 15.7 L15.4 15.7 Z"'
    ' fill="#111" stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/></svg>'
)

# IIFE so it self-runs both as an init script (every navigation) and via evaluate (now).
_CURSOR_SCRIPT = """(() => {
  const svg = '__SVG__';
  const mk = () => {
    const root = document.body || document.documentElement;
    if (!root || document.getElementById('__hauneCursor')) return;
    const st = document.createElement('style'); st.textContent = '*{cursor:none !important}'; (document.head || root).appendChild(st);
    const c = document.createElement('div'); c.id = '__hauneCursor';
    c.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;width:22px;height:30px;transform:translate(-200px,-200px)';
    c.innerHTML = svg; root.appendChild(c);
    let x=-200,y=-200,down=false;
    const place = () => { c.style.transform = 'translate('+x+'px,'+y+'px)'+(down?' scale(0.82)':''); };
    const track = e => { x=e.clientX; y=e.clientY; place(); };
    document.addEventListener('pointermove', track, true);
    document.addEventListener('mousemove', track, true);
    document.addEventListener('pointerdown', e => { down=true; x=e.clientX; y=e.clientY; place(); }, true);
    document.addEventListener('pointerup', () => { down=false; place(); }, true);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mk); else mk();
})()"""


class Human:
    """Human-like mouse / keyboard / scroll over a sync Playwright ``Page``."""

    def __init__(self, page, seed: int | None = None):
        self.page = page
        self._rng = random.Random(seed)
        self._x, self._y = 8.0, 8.0
        self._cdp = None
        self._native = True

    # ---- native humanizer gestures (with transparent fallback) ----
    def _session(self):
        if self._cdp is None:
            self._cdp = self.page.context.new_cdp_session(self.page)
        return self._cdp

    def _native_move(self, x, y, click, button="left", speed=None):
        if not self._native:
            return False
        try:
            self._session().send("Input.synthesizeHumanMouseGesture", {
                "x": self._x, "y": self._y, "targetX": x, "targetY": y,
                "click": click, "button": button,
                "speed": speed if speed is not None else self._rng.randint(600, 1500),
                "seed": self._rng.randint(1, 2 ** 31 - 1),
            })
            return True
        except Exception:
            self._native = False
            return False

    def _native_scroll(self, dy, speed=800):
        if not self._native:
            return False
        try:
            self._session().send("Input.synthesizeHumanScrollGesture", {
                "x": self._x, "y": self._y, "yDistance": -int(dy),
                "speed": speed, "seed": self._rng.randint(1, 2 ** 31 - 1),
            })
            return True
        except Exception:
            self._native = False
            return False

    # ---- mouse ----
    def move_to(self, x, y, speed=None):
        """Move to (x, y) in viewport coordinates along a human curve."""
        x, y = round(x), round(y)
        if not self._native_move(x, y, False, speed=speed):
            self.page.mouse.move(x, y, steps=self._rng.randint(18, 34))
        self._x, self._y = x, y

    def click(self, x, y, button="left", speed=None):
        """Curve to (x, y) and click there (no teleport)."""
        x, y = round(x), round(y)
        if not self._native_move(x, y, True, button, speed):
            self.page.mouse.move(x, y, steps=self._rng.randint(18, 34))
            self.page.mouse.click(x, y, button=button)
        self._x, self._y = x, y

    def click_selector(self, selector, button="left"):
        """Scroll the element into view, curve to a random interior point, click it."""
        loc = self.page.locator(selector).first
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(self._rng.randint(120, 320))
        box = loc.bounding_box()
        if not box:
            raise RuntimeError(f"human: no bounding box for {selector!r}")
        tx = box["x"] + box["width"] * self._rng.uniform(0.3, 0.7)
        ty = box["y"] + box["height"] * self._rng.uniform(0.3, 0.7)
        self.click(tx, ty, button=button)

    def scroll(self, dy, speed=800):
        """Scroll by dy px (positive = down) with a human accelerate/decelerate profile."""
        if self._native_scroll(dy, speed):
            return
        sign = 1 if dy >= 0 else -1
        remaining = abs(int(dy))
        while remaining > 0:
            step = min(remaining, self._rng.randint(40, 110))
            self.page.mouse.wheel(0, sign * step)
            remaining -= step
            self.page.wait_for_timeout(self._rng.randint(20, 70))

    # ---- keyboard ----
    def _gauss(self):
        # Irwin-Hall approx of a standard normal (mean 0).
        return sum(self._rng.random() for _ in range(4)) - 2.0

    def type(self, text, wpm=52, mistakes=True):
        """Type text with a human rhythm (variable gaps, key-hold, pauses, typos)."""
        per_char = 60000 / (wpm * 5)
        neighbors = "asdfghjklqwertyuiopzxcvbnm"
        prev = ""
        for ch in text:
            if mistakes and ch.isalpha() and self._rng.random() < 0.04:
                wrong = neighbors[self._rng.randrange(len(neighbors))]
                self.page.keyboard.press(wrong, delay=self._rng.randint(45, 100))
                self.page.wait_for_timeout(self._rng.randint(90, 200))
                self.page.keyboard.press("Backspace", delay=self._rng.randint(40, 90))
                self.page.wait_for_timeout(self._rng.randint(60, 160))
            hold = self._rng.randint(45, 100)
            key = _SPECIAL.get(ch, ch)
            try:
                self.page.keyboard.press(key, delay=hold)
            except Exception:
                self.page.keyboard.type(ch)
            d = per_char * (0.5 + abs(self._gauss()) * 0.85)
            if prev == " ":
                d += self._rng.uniform(20, 65)
            if ch in ".,!?;:":
                d += self._rng.uniform(55, 185)
            if ch == "\n":
                d += self._rng.uniform(140, 400)
            if self._rng.random() < 0.03:
                d += self._rng.uniform(220, 780)
            self.page.wait_for_timeout(max(15, int(d - hold)))
            prev = ch

    def type_into(self, selector, text, clear=True, **kw):
        """Click the field, optionally clear it, then type with a human rhythm."""
        self.click_selector(selector)
        if clear:
            self.page.locator(selector).first.select_text()
            self.page.wait_for_timeout(self._rng.randint(40, 110))
            self.page.keyboard.press("Delete")
            self.page.wait_for_timeout(self._rng.randint(40, 120))
        self.type(text, **kw)

    # ---- visible OS cursor (cosmetic; page-visible DOM node — off for stealth) ----
    def show_cursor(self, os="windows"):
        """Inject a visible OS-style cursor that follows the synthetic mouse (all pages)."""
        script = _CURSOR_SCRIPT.replace("__SVG__", _MAC_CURSOR if os == "macos" else _WIN_CURSOR)
        self.page.add_init_script(script)   # re-applies on every navigation
        try:
            self.page.evaluate(script)      # and now
        except Exception:
            pass

    def idle_wander(self, moves=3):
        """A few idle micro-movements, as a hand drifts while reading."""
        vp = self.page.viewport_size or {"width": 1280, "height": 800}
        for _ in range(moves):
            self.move_to(self._rng.uniform(vp["width"] * 0.2, vp["width"] * 0.8),
                         self._rng.uniform(vp["height"] * 0.2, vp["height"] * 0.8))
            self.page.wait_for_timeout(self._rng.randint(200, 700))
