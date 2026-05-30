# 🚗 DriveAware — Real-Time Driver Fatigue Detection

> **A SmartSpectra-Ready, In-Browser Driver Fatigue Platform.** AI-powered drowsiness detection that runs entirely in the browser, designed from day one to plug into Presage SmartSpectra SDK for true biometric fatigue scoring.

![Status](https://img.shields.io/badge/status-live-success) <img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/28d9603e-31a3-47bf-98e5-430eace50560" />

![Stack](https://img.shields.io/badge/stack-MediaPipe%20%2B%20Vanilla%20JS-orange) <img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/367aa86e-b95b-4299-9a45-90cb2eb7be53" />

![SmartSpectra](https://img.shields.io/badge/SmartSpectra-Phase%202%20Ready-purple)<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/f62dd94f-9ec7-402c-b6f1-898ddf0e27ae" />

![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📸 Screenshots

> Add 3 screenshots here after taking them. Take with Win+Shift+S, save into the repo folder, then reference them like below.

```markdown
![DriveAware Main UI](screenshot-1.png)
![Caution State](screenshot-2.png)
![DANGER Alert](screenshot-3.png)
```

---

## 💡 Inspiration

According to the [NHTSA](https://www.nhtsa.gov/risky-driving/drowsy-driving), drowsy driving contributes to roughly **100,000 crashes, 50,000 injuries, and 800+ deaths every year** in the United States alone — and conservative estimates suggest the real toll is multiples higher because drowsiness is nearly impossible to verify post-crash.

Commercial trucking, ride-share platforms, and long-haul logistics fleets all face this problem head-on. Existing solutions require **expensive in-vehicle hardware** ($500–$2,000 per dashcam), invasive wearables, or aftermarket cameras drivers refuse to install.

When I learned about Presage's **SmartSpectra SDK** — a contactless biometric sensor that extracts pulse rate, HRV, breathing waveforms, and stress from standard camera video — I realized this was the missing piece. Combined with classical eye-tracking metrics, SmartSpectra unlocks a **biometric-grade fatigue detection system that can run on any device with a camera.**

**DriveAware is the platform built to host that integration.** The MVP demonstrates the visual-cue detection layer (EAR + PERCLOS). Phase 2 plugs in SmartSpectra for the physiological layer — pulse, HRV, breathing, stress — to produce a true composite fatigue score.

---

## 🎯 What It Does

DriveAware is a **real-time driver fatigue and drowsiness detection system** that runs entirely in the browser. Open the page, allow camera access, and within seconds it begins computing fatigue metrics that fleet-grade systems sell for thousands of dollars.

### Current Capabilities (Phase 1)

| Feature | Description |
|---|---|
| 🎯 **Face landmark tracking** | 468-point MediaPipe Face Mesh at 30 FPS |
| 👁️ **Eye Aspect Ratio (EAR)** | Based on the Soukupová & Čech (2016) research formula |
| 🚨 **PERCLOS scoring** | U.S. Department of Transportation's gold-standard drowsiness metric |
| 💤 **Microsleep detection** | Flags eye closures lasting >0.5 seconds |
| 📊 **Live blink analytics** | Total count, blink rate per minute, eyes-closed duration |
| 🎚️ **Tiered risk scoring** | 0-100 score with 4 levels: Alert → Caution → Warning → Danger |
| 🔴 **Multi-channel alerts** | Flashing screen border, banner overlay, color-coded risk panel |
| 🔒 **100% privacy-preserving** | All inference runs in-browser; no video ever leaves the device |

### Planned Capabilities (Phase 2 with SmartSpectra)

| Feature | SmartSpectra API |
|---|---|
| 💓 **Pulse rate** | `sdk.metrics?.cardio.pulseRate` |
| 📈 **Heart Rate Variability** | `sdk.metrics?.cardio.hrv` |
| 🫁 **Breathing rate** | `sdk.metrics?.breathing.rate` |
| 😰 **Stress score** | Derived from HRV + facial expressions |
| 😶 **Facial expressions** | `sdk.metrics?.face.expression` |
| 🗣️ **Talking detection** | `sdk.metrics?.face.talking` |

---

## 🚀 How To Use It

```bash
# Clone the repo
git clone https://github.com/pranavmekala28/driveaware-fatigue-alert.git
cd driveaware-fatigue-alert

# Open the file (Windows)
start index.html

# Or just double-click index.html in your file explorer
```

There is no build step, no `npm install`, no backend. Just allow camera access and click **▶ Start Monitoring**.

> **Note on local file permissions:** Some browsers require HTTPS or `localhost` for camera access. If opening `index.html` directly causes a permission issue, serve it via a one-line local server: `python -m http.server 8000` then visit `http://localhost:8000`.

### Testing the Fatigue Detection

1. Click **▶ Start Monitoring** and allow camera permission
2. Look at the camera normally — your risk score stays green (ALERT level)
3. **Close your eyes for 2+ seconds** — risk score spikes, screen flashes red, DANGER alert fires
4. Click **↻ Reset Metrics** to start a new session

---

## 🧠 How It Was Built

### Architecture

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

### Tech Decisions

**Why MediaPipe Face Mesh?** Google's production-grade face landmark detector — 468 points, 30 FPS on commodity hardware, runs entirely in-browser via WebAssembly. No server round-trip means privacy AND latency wins simultaneously.

**Why Eye Aspect Ratio (EAR)?** The Soukupová & Čech (2016) formula is the gold standard for blink detection from video. It uses simple geometric ratios that are robust to head pose, lighting, and camera angle.

**Why PERCLOS?** The U.S. Department of Transportation explicitly identifies PERCLOS as the most validated drowsiness metric in commercial vehicle research. Building on it means we ship a metric judges (and fleet operators) immediately recognize.

**Why vanilla JS instead of React?** Zero dependencies = zero build step = ship in 2 hours. The entire app is a single self-contained HTML file.

### Tech Stack

| Layer | Tools |
|---|---|
| **Computer Vision** | MediaPipe Face Mesh (468-point tracking) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Typography** | Bricolage Grotesque, JetBrains Mono, Manrope |
| **Camera Access** | WebRTC `getUserMedia` |
| **Rendering** | HTML5 Canvas API |
| **Dependencies** | None — single self-contained file |

---

## 🧬 SmartSpectra Integration Architecture (Phase 2)

This is the **core of DriveAware's value proposition**: a platform purpose-built to host Presage SmartSpectra SDK and fuse its physiological signals with the visual fatigue cues already being computed.

### Integration Plan

```
┌──────────────────────────────────────────────────────────┐
│                    DRIVEAWARE PLATFORM                    │
│                                                            │
│  ┌─────────────────┐         ┌──────────────────────┐    │
│  │ Phase 1 (Live)  │         │ Phase 2 (Next)       │    │
│  │ Visual Layer    │         │ Physiological Layer  │    │
│  │ ─────────────── │         │ ───────────────────  │    │
│  │ • EAR           │         │ • Pulse rate         │    │
│  │ • PERCLOS       │         │ • HRV (stress proxy) │    │
│  │ • Microsleep    │  ◀───▶  │ • Breathing rate     │    │
│  │ • Blink rate    │  fusion │ • Facial expressions │    │
│  │                 │  layer  │ • Talking detection  │    │
│  │ (MediaPipe)     │         │ (SmartSpectra SDK)   │    │
│  └─────────────────┘         └──────────────────────┘    │
│                       │                                    │
│                       ▼                                    │
│           ┌─────────────────────────┐                     │
│           │   Composite Fatigue     │                     │
│           │   Score (0-100)         │                     │
│           │   + Confidence Interval │                     │
│           └─────────────────────────┘                     │
└──────────────────────────────────────────────────────────┘
```

### Native Integration (Swift / iOS Example)

DriveAware's web frontend will be wrapped in a thin iOS shell using `WKWebView`. The Swift layer hosts SmartSpectra SDK and streams metrics to the web layer via JavaScript bridge:

```swift
import SwiftUI
import SmartSpectra

@main
struct DriveAwareApp: App {
    init() {
        // Configure SmartSpectra with API key from Presage portal
        SmartSpectraSDK.shared.config.apiKey = "YOUR_API_KEY"
        SmartSpectraSDK.shared.config.cameraPosition = .front

        // Request the exact metric groups DriveAware needs for fatigue scoring
        SmartSpectraSDK.shared.config.requestedMetrics =
            SmartSpectraConfig.cardioMetrics +
            SmartSpectraConfig.breathingMetrics +
            [.expressions]
    }

    var body: some Scene {
        WindowGroup {
            DriveAwareWebView()  // hosts the existing HTML
                .onAppear { startBiometricCapture() }
        }
    }

    func startBiometricCapture() {
        Task {
            for await metrics in SmartSpectraSDK.shared.metricsStream {
                // Bridge SmartSpectra metrics to the web layer's risk engine
                let payload: [String: Any] = [
                    "pulseRate": metrics?.cardio.pulseRate?.value ?? 0,
                    "hrv": metrics?.cardio.hrv?.value ?? 0,
                    "breathingRate": metrics?.breathing.rate?.value ?? 0,
                    "stressScore": computeStressScore(metrics)
                ]
                webView.evaluateJavaScript("window.updateBiometrics(\(payload))")
            }
        }
    }
}
```

### Metric Fusion Algorithm

The Phase 2 composite risk score fuses visual + physiological signals:

```
visualRisk = (PERCLOS_weight * perclos_score) +
             (microsleep_weight * microsleep_active) +
             (blinkRate_weight * abnormal_blink_rate)

physioRisk = (hrv_weight * hrv_stress_index) +
             (breathing_weight * breathing_variability) +
             (pulse_weight * elevated_pulse_pattern)

compositeRisk = (0.6 * visualRisk) + (0.4 * physioRisk)
```

The weighting reflects that visual cues are leading indicators (eyes close before the body fully fatigues), while physiological signals confirm sustained fatigue states with much higher confidence.

### Why This Architecture Wins

1. **DriveAware's existing fatigue-scoring engine** has a clean injection point at the risk-score calculation step. SmartSpectra metrics drop in via `window.updateBiometrics()`.
2. **No re-architecture required** — Phase 1 already computes a risk score from visual cues. Phase 2 layers physiological cues on top of the same scoring pipeline.
3. **Privacy-preserving** stays intact — SmartSpectra runs on-device. Combined with our in-browser MediaPipe inference, the entire fatigue detection pipeline operates without sending video off-device.

---

## 🎯 Target Markets

- 🚛 **Commercial trucking** — long-haul drivers are 7× more likely to drowse
- 🚕 **Ride-share & delivery fleets** — night-shift driver safety
- 🏢 **Corporate fleet operators** — liability reduction
- 🛡️ **Insurance carriers** — usage-based premiums tied to alertness
- 🚗 **Personal use** — DIY drivers, road-trippers
- 🏥 **Telehealth + fleet wellness** — fatigue + vitals monitoring (Phase 2)

---

## 🔐 Privacy by Design

- ✅ All inference runs **in-browser** — no video upload, no server processing
- ✅ Zero data persistence — nothing saved between sessions
- ✅ No tracking, no analytics, no cookies
- ✅ Works fully offline after first load
- ✅ Open source, MIT licensed — fully auditable
- ✅ Phase 2 SmartSpectra integration also processes everything on-device

---

## 📚 References

1. Soukupová, T., & Čech, J. (2016). *Real-Time Eye Blink Detection using Facial Landmarks.* Computer Vision Winter Workshop.
2. Wierwille, W.W. et al. (1994). *Research on Vehicle-Based Driver Status / Performance Monitoring.* NHTSA Technical Report introducing PERCLOS.
3. NHTSA — Drowsy Driving statistics, [nhtsa.gov/risky-driving/drowsy-driving](https://www.nhtsa.gov/risky-driving/drowsy-driving)
4. Google MediaPipe Face Mesh — [google.github.io/mediapipe](https://google.github.io/mediapipe/)
5. **Presage SmartSpectra SDK** — [presagetechnologies.com](https://presagetechnologies.com/)
6. **SmartSpectra Swift SDK Examples** — [github.com/Presage-Security/SmartSpectraSwiftSDK-Examples](https://github.com/Presage-Security/SmartSpectraSwiftSDK-Examples)

---

## 👨‍💻 Author

**Pranav Mekala**
M.S. Business Analytics · Webster University · Missouri, USA

- 🐙 GitHub: [@pranavmekala28](https://github.com/pranavmekala28)
- 💼 LinkedIn: [linkedin.com/in/pranavmekala28](https://www.linkedin.com/in/pranavmekala28/)

Built solo during a 2-hour hackathon sprint for the Presage SmartSpectra Hackathon, May 2026.

---

## 📄 License

MIT — free to use, modify, and ship.
