# AirTracer 🌐

**English** | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README.md)

[![FindMy Compatibility](https://img.shields.io/badge/FindMy-Macless_Support-blueviolet.svg?style=flat-square)](#)
[![MQTT Discovery](https://img.shields.io/badge/HomeAssistant-MQTT_Discovery-green.svg?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-Web_%7C_Android-orange.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**AirTracer** is a modern smart tracking and device management system based on the Apple FindMy network (Macless architecture) and various GPS data sources. This repository is the public hub for AirTracer, hosting core client software (including the Android application and device firmwares), detailed usage guides, and introducing the enterprise-grade private project **Tracer** for those with customization or self-hosting needs.

🌐 **Official Live Platform**: [https://airtracer.us](https://airtracer.us)

---

## 🎨 Interface Preview

### 💻 Desktop Web (PC)
| **PC InfiTag Control Center** | **PC LoopTag Trajectory Details** |
|:---:|:---:|
| ![PC InfiTag](images/web/Infitag.png) | ![PC LoopTag Trajectory](images/web/Looptag轨迹线.png) |
| *Large screen multi-dimensional map tracking & dashboard* | *High-precision detailed trajectory line & point analysis* |

---

### 📱 Mobile Web & App
| **InfiTag Mobile App** | **LoopTag Mobile App** |
|:---:|:---:|
| ![InfiTag Mobile](images/mobile/Infitag-phone.png) | ![LoopTag Mobile](images/mobile/looptag-phone.png) |
| *Dynamic rolling keys: Real-time, continuous, and more precise* | *Fixed Key mode: Easily filtered by Apple, causing track loss* |

| **Mobile Dashboard** | **Mobile Device Management** |
|:---:|:---:|
| ![Mobile Dashboard](images/mobile/控制中心.png) | ![Mobile Device Management](images/mobile/设备管理.png) |
| *Mobile multi-device real-time positioning* | *Unified device status monitoring & quick config* |

| **Trajectory Playback** | **Geofence Settings** |
|:---:|:---:|
| ![Trajectory Playback](images/mobile/轨迹线.png) | ![Geofence Settings](images/mobile/电子围栏.png) |
| *High-precision path rendering & dwell points analysis* | *Custom geofences & smart alarm triggers* |

| **Home Assistant Integration** | **Notification Settings** |
|:---:|:---:|
| ![HA Integration](images/mobile/打通hass.png) | ![Notification Settings](images/mobile/通知.png) |
| *Zero-code HA entity auto-discovery via MQTT* | *Custom alarm notifications & system preferences* |

---

## 🚀 Core Features

- 📡 **Macless FindMy Tracking**: Retrieve device location reports directly from Apple servers via the `anisette-v3` stack and smart scheduler—no Mac hardware gateway required.
- 🔄 **Smart Key Derivation Algorithm**: Unlike traditional LoopTag devices using fixed keys (which are prone to being discarded as spam by Apple servers), AirTracer utilizes a **Dynamic Rolling Key Algorithm** for InfiTag. Combined with a **Smart Waterfall Strategy**, it fetches more real-time locations, dense track points, and detailed path lines with significantly higher precision.
- 🏡 **Native Home Assistant Integration**: Built-in MQTT Discovery protocol. Device locations, status, and battery levels map automatically as `device_tracker` and `sensor` entities. Supports **strict multi-user security isolation**.
- 🗺️ **High-Precision Track & Geofencing**: Powered by Leaflet & Amap (AutoNavi) engines. Features path playback, heatmap rendering, dwell point extraction, and geofence alarms.
- 🔔 **Multi-Channel Alerts**: Trigger immediate push alerts via Telegram Bot or web notifications upon entering/leaving geofences or low battery events.

---

## 📦 Software Releases & Downloads

Pre-built hardware firmwares and mobile clients are available on our [Releases](../../releases) page:

### 1. Android Client (APK)
- **AirTracer Android App**: Optimized mobile client featuring desktop widgets, background background-position reporting, real-time map viewing, and alarm notifications.
- 👉 [Download Latest APK](../../releases/latest)

### 2. Device Firmware (Firmware)
- **InfiTag (無極)**: **[Recommended]** Based on the dynamic rolling key mechanism. Delivers more real-time positions, continuous tracking, and detailed paths without location report loss. Supports nRF51822 beacons.
- **LoopTag**: Based on the traditional fixed public key mechanism. Suitable for simple tests or low-frequency tracking (Note: Fixed key locations may be filtered/discarded by Apple). Supports nRF52810/nRF52832 beacons.
- 👉 [Download Firmware Package](../../releases/latest)

---

## 📚 Documentation

Detailed sub-guides to help you get started quickly:

- 📖 **[User Guide](docs/user_guide.md)**: Steps on registering, logging in, adding GPS/FindMy devices, configuring geofences, and linking Telegram bots.
- 🔌 **[Firmware Flashing & Hardware Guide](docs/firmware_guide.md)**: Wiring schematic, flashing tools (OpenOCD/J-Flash/PyOCD), Makefile compilation flags, and seed key derivation theory.
- 🏠 **[Home Assistant Integration Guide](docs/home_assistant.md)**: Connecting to MQTT Broker, applying your isolated user credentials, and mapping/importing device trackers.

---

## 💎 Private Project "Tracer" Promotion & Commercial Cooperation

If you love AirTracer and need a **private self-hosted environment**, or want to build a **commercial-grade tracking system** for your business, we offer the private enterprise-grade project **Tracer**.

### 🌟 Extra Advantages of Private Tracer:
1. **Fully Self-Hosted Backend**: Simple Docker-compose setup for the entire infrastructure (FastAPI + PostgreSQL + TimescaleDB + Redis + Mosquitto).
2. **High-Throughput Optimization**: Optimized TimescaleDB schema for large-scale time-series trajectory writes.
3. **Enterprise Role-Based Access (RBAC)**: Fine-grained permissions, sub-accounts, and multi-tenant isolation.
4. **Custom Branding (OEM)**: Custom App name, logo, color palette, custom domain, and independent map integration.
5. **Custom Hardware Integration**: One-stop solution from schematic design to firmware coding (including support for ultra-low-cost SOCs like ST17H66B).

### 📞 Contact Us
If you are interested in self-hosting, custom branding, or hardware integration, reach out to us:
- 📧 **Email**: [airtagtracer@gmail.com](mailto:airtagtracer@gmail.com)
- 💬 **Telegram**: [@AirTracer](https://t.me/AirTracer)

*Please briefly describe your requirements (e.g., self-hosting, custom hardware, enterprise licensing), and we will reply within 24 hours.*
