# 🚗 DriveAware — Real-Time Driver Fatigue Detection

> AI-powered, in-browser driver fatigue and drowsiness detection using computer vision. No backend. No installs. Just open the page and drive safe.

![Status](https://img.shields.io/badge/status-live-success)
![Stack](https://img.shields.io/badge/stack-MediaPipe%20%2B%20Vanilla%20JS-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Built In](https://img.shields.io/badge/built%20in-2%20hours-red)

---

## ⚠️ The Problem

Drowsy driving kills. According to the [NHTSA](https://www.nhtsa.gov/risky-driving/drowsy-driving), fatigue is a factor in **~100,000 crashes, 50,000 injuries, and 800+ deaths every year** in the United States alone — and those are just the *reported* numbers. The real toll is significantly higher because drowsiness is hard to detect after the fact.

Commercial fleets, ride-share platforms, long-haul trucking, and even ordinary commuters lack a low-cost, hardware-free way to detect fatigue **before** a microsleep happens.

## 💡 The Solution

**DriveAware** turns any laptop, phone, or webcam-equipped device into a real-time driver fatigue detector. It runs entirely **in the browser** — no servers, no installs, no data leaves the device.

Using Google's **MediaPipe Face Mesh** (468 facial landmarks tracked at ~30 FPS), DriveAware computes industry-standard drowsiness metrics including the **Eye Aspect Ratio (EAR)** and **PERCLOS**, and surfaces a composite **0–100 fatigue risk score** with tiered alerts.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Real-time face landmark tracking** | 468-point MediaPipe Face Mesh at 30 FPS |
| 👁️ **Eye Aspect Ratio (EAR)** | Based on the Soukupová & Čech (2016) research formula |
| 🚨 **PERCLOS scoring** | Industry-standard drowsiness metric (% eye closure over rolling 10s window) |
| 💤 **Microsleep detection** | Flags eye closures lasting >0.5 seconds |
| 📊 **Live blink analytics** | Total count, blink rate per minute, eyes-closed duration |
| 🎚️ **Tiered risk scoring** | 0–100 score with 4 levels: Alert → Caution → Warning → Danger |
| 🔴 **Multi-channel alerts** | Flashing screen border, banner overlay, color-coded risk panel |
| 🔒 **100% privacy-preserving** | All inference runs in-browser; no video ever leaves the device |
| 📱 **Zero install** | Single HTML file, works on any modern browser |

---

## 🎬 Demo

> 📹 [**Watch the demo video →**](#) *(link your Loom recording here after submission)*

| Live monitoring | Fatigue alert triggered |
|---|---|
| _(screenshot here)_ | _(screenshot of red DANGER state)_ |

---

## 🧠 How It Works

```
┌──────────────────┐    ┌────────────────────┐    ┌──────────────────┐
│  Webcam Feed     │───▶│  MediaPipe Face    │───▶│  Eye Landmarks   │
│  (30 FPS @ 720p) │    │  Mesh (468 points) │    │  (8 key indices) │
└──────────────────┘    └────────────────────┘    └────────┬─────────┘
                                                            │
                              ┌─────────────────────────────┴─────┐
                              ▼                                    ▼
                    ┌──────────────────┐              ┌──────────────────┐
                    │  EAR Calculation │              │  PERCLOS Rolling │
                    │  (per frame)     │              │  Window (10s)    │
                    └────────┬─────────┘              └────────┬─────────┘
                             │                                  │
                             └──────────┬───────────────────────┘
                                        ▼
                              ┌──────────────────┐
                              │  Composite Risk  │
                              │  Score (0–100)   │
                              └────────┬─────────┘
                                       ▼
                              ┌──────────────────┐
                              │  Multi-Channel   │
                              │  Alert Engine    │
                              └──────────────────┘
```

### Key Metrics Explained

**Eye Aspect Ratio (EAR)** — Ratio of eye height to eye width based on 6 facial landmarks. Open eyes ≈ 0.30; closed eyes < 0.20.

**PERCLOS (Percentage Eye Closure)** — The percentage of time the eyes are closed over a rolling window. Recognized by the U.S. Department of Transportation as the gold-standard fatigue indicator.

**Microsleep Detection** — A continuous eye closure of more than ~0.5 seconds during driving is treated as a critical event, immediately triggering the DANGER alert.

**Composite Risk Score** — Weighted combination of PERCLOS, active eye-closure duration, and abnormal blink rate, capped at 0–100.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **Computer Vision** | MediaPipe Face Mesh |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Typography** | Bricolage Grotesque (display), JetBrains Mono (data), Manrope (body) |
| **Camera Access** | WebRTC `getUserMedia` |
| **Rendering** | HTML5 Canvas API |
| **No dependencies** | No npm, no bundler, no backend |

---

## 🚀 Run It Locally

```bash
# Clone the repo
git clone https://github.com/pranavmekala28/driveaware-fatigue-alert.git
cd driveaware-fatigue-alert

# Open the file
# On Windows:
start index.html

# On macOS:
open index.html

# Or just double-click index.html in your file explorer.
```

That's it. There is no build step. There is no `npm install`. Allow camera permission when prompted and click **Start Monitoring**.

> **Note:** Modern browsers require camera access over `https://` or `localhost` only. If opening the file directly causes a permission issue, serve it via a quick local server: `python -m http.server 8000` then visit `http://localhost:8000`.

---

## 📋 Roadmap

### ✅ Phase 1 — MVP (Shipped)
- [x] MediaPipe Face Mesh integration
- [x] EAR-based blink detection
- [x] PERCLOS scoring
- [x] Composite risk score (0–100)
- [x] Tactical automotive UI
- [x] Microsleep alert
- [x] Visual + flashing alarm

### 🚧 Phase 2 — Presage SmartSpectra Integration (Next)
Integrate the [**Presage SmartSpectra SDK**](https://presagetechnologies.com/) for contactless physiological monitoring:
- 💓 **Pulse rate** — extracted from facial skin color shifts (rPPG)
- 🫁 **Breathing rate** — chest movement signal
- 📈 **Heart Rate Variability (HRV)** — autonomic nervous system stress indicator
- 😰 **Stress detection** — composite physiological stress score
- 😶 **Facial expression analysis** — micro-expression-based fatigue signals

This moves DriveAware from *visual fatigue inference* to *true biometric physiological fatigue detection.*

### 🔮 Phase 3 — Production Features
- [ ] Video file upload mode (post-trip analysis)
- [ ] Session export to PDF report
- [ ] Multi-driver session storage (cloud-optional)
- [ ] Fleet dashboard for trucking / ride-share companies
- [ ] Mobile-native iOS/Android apps via React Native + Presage SDK
- [ ] Real-time audio voice alerts ("Pull over now")
- [ ] Integration with vehicle CAN-bus systems

### 🎯 Phase 4 — Commercial
- [ ] B2B SaaS dashboard for fleet operators
- [ ] Insurance partnership pilots (drowsy-driver risk discounts)
- [ ] OEM integration for in-vehicle infotainment systems

---

## 🎯 Target Markets

- 🚛 **Commercial trucking** — long-haul drivers are 7× more likely to drowse
- 🚕 **Ride-share & taxi fleets** — night-shift driver safety
- 🏢 **Corporate fleet operators** — liability reduction
- 🛡️ **Insurance** — usage-based premiums tied to alertness
- 🚗 **Personal use** — DIY drivers, road-trippers
- 🏥 **Telehealth** — combined fatigue + vitals monitoring (Phase 2)

---

## 🔐 Privacy by Design

DriveAware is built **privacy-first**:

- ✅ All inference runs **in-browser** — no video ever uploaded
- ✅ No data persistence — nothing saved between sessions
- ✅ No tracking, no analytics, no cookies
- ✅ Works fully offline once loaded
- ✅ Open-source and auditable

When Phase 2 (Presage SDK) integrates remote vitals, those measurements are also processed on-device and never sent to a server.

---

## 📚 References

1. **Soukupová, T., & Čech, J.** (2016). *Real-Time Eye Blink Detection using Facial Landmarks.* 21st Computer Vision Winter Workshop.
2. **Wierwille, W.W. et al.** (1994). *Research on Vehicle-Based Driver Status / Performance Monitoring.* NHTSA Technical Report (PERCLOS).
3. **MediaPipe Face Mesh** — Google Research, [google.github.io/mediapipe](https://google.github.io/mediapipe/)
4. **Presage Technologies — SmartSpectra SDK** — [presagetechnologies.com](https://presagetechnologies.com/)

---

## 👨‍💻 Author

**Pranav Mekala**
M.S. Business Analytics · Webster University · Missouri, USA

- 🐙 GitHub: [@pranavmekala28](https://github.com/pranavmekala28)
- 💼 LinkedIn: [Pranav Mekala](https://www.linkedin.com/in/pranavmekala28/)

Built solo during a 2-hour hackathon sprint.

---

## 📄 License

MIT — free to use, modify, and ship.
