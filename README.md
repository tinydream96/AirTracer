# AirTracer 🌐

[English](README_EN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | **中文**

[![FindMy Compatibility](https://img.shields.io/badge/FindMy-Macless_Support-blueviolet.svg?style=flat-square)](#)
[![MQTT Discovery](https://img.shields.io/badge/HomeAssistant-MQTT_Discovery-green.svg?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-Web_%7C_Android-orange.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**AirTracer** 是一个基于 Apple FindMy 网络（免 Mac 架构）及多种 GPS 数据源的现代化智能追踪与设备管理系统。本项目是 AirTracer 的公开主仓库，用于发布核心客户端软件（包括 Android 客户端与设备端固件）、提供详细的平台使用说明，以及为有定制和自托管需求的用户推广企业级私有项目 **Tracer**。

🌐 **官方在线体验平台**：[https://airtracer.us](https://airtracer.us)

---

## 🎨 界面预览

### 💻 PC 网页端 (Desktop Web)
| **PC 端 InfiTag 控制中心** | **PC 端 LoopTag 轨迹线详情** |
|:---:|:---:|
| ![PC 端 InfiTag](images/web/Infitag.png) | ![PC 端 LoopTag 轨迹线](images/web/Looptag轨迹线.png) |
| *大屏多维度地图定位与统计仪表盘* | *高精度完整路径轨迹线与点位分析* |

---

### 📱 手机网页端与移动 App (Mobile Web & App)
| **InfiTag 手机端** | **LoopTag 手机端** |
|:---:|:---:|
| ![InfiTag 手机端](images/mobile/Infitag-phone.png) | ![LoopTag 手机端](images/mobile/looptag-phone.png) |
| *动态密钥滚动：定位实时，轨迹更精准* | *固定 Key 模式：易被过滤导致轨迹缺失* |

| **控制中心移动端** | **设备管理移动端** |
|:---:|:---:|
| ![控制中心](images/mobile/控制中心.png) | ![设备管理](images/mobile/设备管理.png) |
| *移动端多设备地图定位展示* | *统一设备状态监控与快捷配置* |

| **轨迹回放与分析** | **电子围栏设置** |
|:---:|:---:|
| ![轨迹回放](images/mobile/轨迹线.png) | ![电子围栏](images/mobile/电子围栏.png) |
| *高精度路径渲染与停留点分析* | *自定义安全围栏与告警触发* |

| **Home Assistant 智能家居联动** | **通知中心与设置** |
|:---:|:---:|
| ![打通 HA](images/mobile/打通hass.png) | ![通知与设置](images/mobile/通知.png) |
| *通过 MQTT 自动发现接入 HA 实体* | *设备告警通知及系统选项设置* |

---

## 🚀 核心特性

- 📡 **免 Mac (Macless) FindMy 追踪**：无需购买 Mac 电脑作为网关，通过 `anisette-v3` 协议栈和智能调度器，直接与 Apple 服务器交互获取设备定位报告。
- 🔄 **智能密钥派生算法**：抛弃了类似 LoopTag 的传统固定 Key 模式（固定 Key 模式极易被苹果公司过滤或丢弃位置信息）。AirTracer 独创的 **动态滚动密钥算法** 配合 **智能瀑布流检索策略**，能够获取到更实时的定位、更多的轨迹点以及更详细的轨迹线，定位精确度大幅提升。
- 🏡 **Home Assistant 原生打通**：内置 MQTT Discovery 协议。设备位置、状态和电池电量可自动映射为 Home Assistant 中的 `device_tracker` 和 `sensor` 实体。支持**多用户安全隔离**，互不干扰。
- 🗺️ **高精度轨迹与围栏分析**：内置高德地图与 Leaflet 引擎，支持实时追踪、轨迹热力图、停留点提取、历史速度剖析以及电子围栏告警。
- 🔔 **多渠道即时通知**：支持进出电子围栏、电量低等事件通过 Telegram Bot 或系统通知推送。

---

## 📦 软件发布与下载

我们为用户提供现成的硬件固件和移动客户端下载，您可以在 [Releases](../../releases) 页面找到以下内容：

### 1. Android 客户端 (APK)
- **AirTracer Android App**：专为移动端优化的客户端，支持桌面小组件、后台持续定位上报、实时地图查看和设备报警推送。
- 👉 [下载最新版 APK](../../releases/latest) (GitHub Releases)

### 2. 硬件端固件 (Firmware)
- **InfiTag (无极)**：**【推荐】** 基于动态滚动密钥机制，定位更实时、轨迹点更多更连贯、轨迹线更详细，规避了苹果丢弃位置的问题，定位更精准。支持基于 nRF51822 芯片的硬件。
- **LoopTag**：基于固定公钥（Fixed Key）机制。适合简易测试或低频定位（注：固定 Key 模式可能会被苹果公司丢弃一些位置）。支持基于 nRF52810 / nRF52832 等硬件。
- 👉 [获取烧录固件包](../../releases/latest)

---

## 📚 说明文档

为了帮助您快速上手，我们准备了详细的分类指南：

- 📖 **[用户使用指南](docs/user_guide.md)**：教你如何注册、登录、添加你的第一个硬件或手机追踪设备、配置电子围栏与 Telegram 通知。
- 🔌 **[固件烧录与硬件接入指引](docs/firmware_guide.md)**：针对 nRF51/nRF52 芯片的接线、烧录工具（OpenOCD/J-Flash）以及公钥 Seed 生成指南。
- 🏠 **[Home Assistant 集成指南](docs/home_assistant.md)**：详细阐述如何配置 MQTT、使用你的专属凭证将定位数据无缝推送到智能家居中心。

---

## 💎 私有项目 Tracer 推广与商业合作

如果您觉得 AirTracer 系统表现优异，并希望在您的**个人服务器上私有化部署**，或针对**企业级定位监控业务进行定制开发**，我们为您提供更强大、更完整的私有项目 **Tracer** 商业版本。

### 🌟 商业私有版 Tracer 额外优势：
1. **完全自托管后端**：支持一键 Docker 部署全套后端环境（FastAPI + PostgreSQL + TimescaleDB + Redis + Mosquitto）。
2. **高并发与性能优化**：针对 TimescaleDB 进行时序轨迹数据存储优化，轻松应对成百上千台设备同时在线的高频上报。
3. **企业级权限管理**：支持多租户、细粒度的角色权限控制（RBAC）和子账号分配。
4. **独立品牌定制 (OEM)**：定制专属 App 名称、Logo、主题颜色、专属域名和独立的地图授权。
5. **专有硬件定制**：提供从硬件选型、PCB 设计到定制蓝牙固件编写的一站式解决方案（包含对 ST17H66B 等超低成本国产蓝牙 SoC 的移植支持）。

### 📞 取得联系
如果您对私有部署、企业合作或硬件定制感兴趣，请通过以下渠道与我联系：
- 📧 **商务邮箱**：[airtagtracer@gmail.com](mailto:airtagtracer@gmail.com)
- 💬 **Telegram**：[@AirTracer](https://t.me/AirTracer)

*请在来信中简要描述您的需求（如：个人私有部署、硬件定制开发、企业版授权等），我们会在 24 小时内回复您。*