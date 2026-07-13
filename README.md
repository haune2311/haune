<h1 align="center">🛡️ Haune</h1>

<h3 align="center">Trình duyệt anti-detect vượt mọi bài test bot.</h3>

<p align="center">
Một bản Chromium 148 <strong>tự build</strong>, fingerprint được xử lý ngay trong lõi
trình duyệt — hệ thống antibot chấm điểm nó như một người dùng thật, vì nó hành xử như
một trình duyệt thật.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Chromium-148-4285F4" alt="Chromium 148">
<img src="https://img.shields.io/badge/build-official-success" alt="official build">
<img src="https://img.shields.io/badge/platform-Windows-0078D6" alt="Windows">
<img src="https://img.shields.io/badge/API-.NET%208%20%C2%B7%20Node-512BD4" alt=".NET 8 / Node">
<img src="https://img.shields.io/badge/FingerprintJS-~99%25%20CLEAN-brightgreen" alt="FingerprintJS ~99% clean">
<img src="https://img.shields.io/badge/license-Proprietary%20%C2%B7%20All%20Rights%20Reserved-red" alt="Proprietary license">
</p>

<p align="center">
<a href="https://github.com/haune2311/haune-antidetect/stargazers"><img src="https://img.shields.io/github/stars/haune2311/haune-antidetect?style=social" alt="GitHub stars"></a>
&nbsp;<a href="https://github.com/haune2311/haune-antidetect/network/members"><img src="https://img.shields.io/github/forks/haune2311/haune-antidetect?style=social" alt="GitHub forks"></a>
&nbsp;<a href="https://github.com/haune2311/haune-antidetect/watchers"><img src="https://img.shields.io/github/watchers/haune2311/haune-antidetect?style=social" alt="GitHub watchers"></a>
</p>

<p align="center"><b>⭐ Star</b> nếu Haune hữu ích — giúp người khác tìm thấy nó · <b>👁 Watch</b> để nhận update<br><sub><b>⭐ Star</b> if Haune helps — it helps others find it · <b>👁 Watch</b> for updates</sub></p>

<table align="center">
<tr>
<td width="50%" align="center"><img src="docs/assets/test-deviceinfo.png" alt="You are human"><br><sub><b>deviceandbrowserinfo</b> — "You are human!" · <code>isBot: false</code></sub></td>
<td width="50%" align="center"><img src="docs/assets/test-browserscan.png" alt="BrowserScan Normal"><br><sub><b>BrowserScan</b> — Test Results: <b>Normal</b></sub></td>
</tr>
<tr>
<td width="50%" align="center"><img src="docs/assets/test-recaptcha.png" alt="reCAPTCHA v3 score 0.9"><br><sub><b>reCAPTCHA v3</b> — score <b>0.9</b> (human level)</sub></td>
<td width="50%" align="center"><img src="docs/assets/demo-sannysoft.png" alt="sannysoft all green"><br><sub><b>bot.sannysoft.com</b> — all green</sub></td>
</tr>
</table>

<p align="center"><em>Real captures — no CAPTCHA solver, no proxy tricks. It just looks human.</em></p>

<h3 align="center">How it compares</h3>

| | playwright-stealth | undetected-chromedriver | Camoufox | **HauneBrowser** |
|---|:---:|:---:|:---:|:---:|
| Patch level | JS injection | config patches | C++ (Firefox) | **C++ (Chromium)** |
| reCAPTCHA v3 | 0.3–0.5 | 0.3–0.7 | 0.7–0.9 | **0.9** |
| Cloudflare Turnstile | sometimes | sometimes | pass | **pass** |
| FingerprintJS | detected | detected | pass | **pass (~99%)** |
| Survives Chrome updates | breaks often | breaks often | yes | **yes** |
| Native Playwright API | yes | no (Selenium) | no | **yes** |

<p align="center"><a href="#-tiếng-việt">🇻🇳 Tiếng Việt</a> · <a href="#-english">🇬🇧 English</a> · <a href="LICENSE">📄 License</a> · <a href="https://haune2311.github.io/haune-antidetect/">🌐 Website</a></p>

---

## 🇻🇳 Tiếng Việt

### Haune là gì?

Haune là trình duyệt chống-nhận-diện của riêng bạn — một bản Chromium 148 tự build, xử lý
fingerprint ở tầng lõi (không phải add-on, không phải script), kèm bộ sinh **danh tính mạch
lạc tái lập từ seed**. Mỗi seed = một thiết bị ổn định, nhất quán từ UA đến GPU, fonts,
timezone. Hơn **6 tỉ** danh tính duy nhất, không trùng.

### Nổi bật

- 🟢 **Sạch mặc định** — chạy là qua, không cần tinh chỉnh.
- 🖐️ **`humanize`** — chuột, gõ phím, cuộn trang như người thật (một cờ là qua behavioral).
- 🌐 **GeoIP tự động** — timezone / locale / geolocation / WebRTC IP tự khớp exit của proxy.
- 🎭 **Danh tính mạch lạc** — canvas, WebGL, WebGPU, audio, fonts, GPU, screen, WebRTC,
  User-Agent, navigator… tất cả nhất quán với nhau.
- 🧩 **SDK riêng** — thư viện `.NET 8` + launcher Node, tích hợp trong vài dòng.
- 🔒 **Ổn định qua các bản Chrome update** — vá ở source, không vỡ như các tool chèn JS.

### Kết quả

Kiểm thử trên 30+ dịch vụ nhận diện bot:

| Dịch vụ | Kết quả |
|---|---|
| **FingerprintJS** (demo.fingerprint.com) | ✅ **~99% CLEAN** (thường 100% trên IP sạch) |
| **reCAPTCHA v3** | ✅ 0.9 (mức người thật, verify server-side) |
| **Cloudflare Turnstile** | ✅ Pass |
| bot.sannysoft.com · CreepJS · BrowserScan · rebrowser · deviceandbrowserinfo | ✅ Pass hết |
| `navigator.webdriver` · UA · TLS (JA3/JA4) | ✅ như Chrome thật, không lộ automation/headless |

### Bắt đầu nhanh

Lần chạy đầu **tự tải browser** (self-contained, cache lại) — không cần cấu hình.

**Python** — `pip install haune`

```python
from haune import launch

browser = launch(proxy="http://user:pass@host:port")  # geoip tự bật khi có proxy
page = browser.new_page()
page.goto("https://example.com")
browser.close()
```

**.NET 8** — `dotnet add package Haune`

```csharp
using Haune;

await using var browser = await HauneLauncher.LaunchAsync(new LaunchOptions {
    Proxy    = "http://user:pass@host:port",  // GeoIP + WebRTC tự bật khi có proxy
    Headless = false,
});
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");
```

Mỗi `seed` tái lập một thiết bị. Cần chống bot mạnh: thêm proxy residential. Xong.

### Bản quyền & giấy phép

© 2026 Haune Builder (github.com/haune2311). **All Rights Reserved.** Phần mềm **độc quyền**
— KHÔNG ai được sao chép, clone, fork, chỉnh sửa, phân phối hay dùng lại dưới bất kỳ hình
thức nào nếu không có văn bản cho phép của chủ sở hữu. Xem [`LICENSE`](LICENSE).

---

## 🇬🇧 English

### What is Haune?

Haune is your own anti-detect browser — a self-built Chromium 148 that handles fingerprints
in the browser core (not an add-on, not a script), with a generator of **coherent,
seed-reproducible identities**. One seed = one stable device, consistent from UA to GPU,
fonts and timezone. **6 billion+** unique, non-colliding identities.

### Highlights

- 🟢 **Clean by default** — it just passes, no tuning needed.
- 🖐️ **`humanize`** — human-like mouse, typing and scroll (one flag clears behavioral checks).
- 🌐 **Automatic GeoIP** — timezone / locale / geolocation / WebRTC IP auto-match the proxy exit.
- 🎭 **Coherent identity** — canvas, WebGL, WebGPU, audio, fonts, GPU, screen, WebRTC,
  User-Agent, navigator… all consistent with each other.
- 🧩 **First-class SDK** — `.NET 8` library + Node launcher, integrate in a few lines.
- 🔒 **Survives Chrome updates** — patched at the source, doesn't break like JS-injection tools.

### Results

Tested against 30+ bot-detection services:

| Service | Result |
|---|---|
| **FingerprintJS** (demo.fingerprint.com) | ✅ **~99% CLEAN** (often 100% on fresh IPs) |
| **reCAPTCHA v3** | ✅ 0.9 (human level, server-verified) |
| **Cloudflare Turnstile** | ✅ Pass |
| bot.sannysoft.com · CreepJS · BrowserScan · rebrowser · deviceandbrowserinfo | ✅ All pass |
| `navigator.webdriver` · UA · TLS (JA3/JA4) | ✅ real Chrome, no automation/headless leak |

### Quick start

First run **auto-downloads the browser** (self-contained, cached) — zero config.

**Python** — `pip install haune`

```python
from haune import launch

browser = launch(proxy="http://user:pass@host:port")  # geoip auto-enables with a proxy
page = browser.new_page()
page.goto("https://example.com")
browser.close()
```

**.NET 8** — `dotnet add package Haune`

```csharp
using Haune;

await using var browser = await HauneLauncher.LaunchAsync(new LaunchOptions {
    Proxy    = "http://user:pass@host:port",  // GeoIP + WebRTC auto-enable with a proxy
    Headless = false,
});
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");
```

Every `seed` reproduces a device. For heavily-protected sites: add a residential proxy. Done.

### License

© 2026 Haune Builder (github.com/haune2311). **All Rights Reserved.** Proprietary software —
no copying, cloning, forking, modification, redistribution, or reuse in any form without the
copyright holder's written permission. See [`LICENSE`](LICENSE).

---

## ⭐ Star History

<p align="center">
<a href="https://star-history.com/#haune2311/haune-antidetect&Date">
<img src="https://api.star-history.com/svg?repos=haune2311/haune-antidetect&type=Date" alt="Star History Chart" width="600">
</a>
</p>

<p align="center">Thấy hữu ích? <b><a href="https://github.com/haune2311/haune-antidetect">⭐ Star repo</a></b> &amp; <b>👁 Watch</b> để ủng hộ · Found it useful? <b>⭐ Star</b> &amp; <b>👁 Watch</b> to support.</p>
