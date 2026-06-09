# AirTracer 🌐

[English](README_EN.md) | **日本語** | [한국어](README_KO.md) | [中文](README.md)

[![FindMy Compatibility](https://img.shields.io/badge/FindMy-Macless_Support-blueviolet.svg?style=flat-square)](#)
[![MQTT Discovery](https://img.shields.io/badge/HomeAssistant-MQTT_Discovery-green.svg?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-Web_%7C_Android-orange.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**AirTracer** は、Apple FindMy ネットワーク（Macレス設計）および複数の GPS データソースに基づく、近代的でスマートな位置追跡およびデバイス管理システムです。このリポジトリは AirTracer の公開メインリポジトリであり、コアクライアントソフトウェア（Android アプリケーションおよびデバイスファームウェア）のリリース、詳細なプラットフォーム利用ガイドの提供、およびカスタマイズや自社サーバー導入（セルフホスト）を希望するユーザー向けのエンタープライズ対応プライベートプロジェクト **Tracer** の紹介を行っています。

🌐 **公式オンライン体験プラットフォーム**: [https://airtracer.us](https://airtracer.us)

---

## 🎨 インターフェースプレビュー

### 💻 PC 向けウェブ端 (Desktop Web)
| **PC 版 InfiTag コントロールセンター** | **PC 版 LoopTag 軌跡詳細** |
|:---:|:---:|
| ![PC 版 InfiTag](images/web/Infitag.png) | ![PC 版 LoopTag 軌跡](images/web/Looptag轨迹线.png) |
| *大画面での多次元マップ追跡と統計ダッシュボード* | *高精度な移動経路の軌跡ラインと滞在点分析* |

---

### 📱 モバイル向けウェブ＆アプリ (Mobile Web & App)
| **InfiTag モバイルアプリ** | **LoopTag モバイルアプリ** |
|:---:|:---:|
| ![InfiTag モバイル](images/mobile/Infitag-phone.png) | ![LoopTag モバイル](images/mobile/looptag-phone.png) |
| *動的ローリングキー：リアルタイム、連動性、高精度* | *固定 Key モード：Apple にフィルタリングされやすく軌跡が途切れやすい* |

| **コントロールセンター（モバイル）** | **デバイス管理（モバイル）** |
|:---:|:---:|
| ![コントロールセンター](images/mobile/控制中心.png) | ![デバイス管理](images/mobile/设备管理.png) |
| *モバイル端末での複数デバイスのリアルタイム位置表示* | *デバイス状態の統合監視とクイック設定* |

| **軌跡の再生と分析** | **電子フェンス（ジオフェンス）設定** |
|:---:|:---:|
| ![軌跡の再生](images/mobile/轨迹线.png) | ![電子フェンス設定](images/mobile/电子围栏.png) |
| *高精度な経路描画と滞在地点の抽出* | *カスタム安全境界線とスマートアラートトリガー* |

| **Home Assistant スマートホーム連携** | **通知センターと設定** |
|:---:|:---:|
| ![HA 連携](images/mobile/打通hass.png) | ![通知と設定](images/mobile/通知.png) |
| *MQTT 経由の自動検出による、ゼロコードでの HA エンティティ追加* | *デバイスアラート通知およびシステム詳細設定* |

---

## 🚀 主な特徴

- 📡 **Mac レス (Macless) FindMy 追跡**：Mac ハードウェアゲートウェイを購入する必要はありません。`anisette-v3` プロトコルスタックとスマートスケジューラーにより、Apple のサーバーから直接位置情報レポートを同期的に取得します。
- 🔄 **スマートキー生成アルゴリズム**：固定キーを使用する従来の LoopTag デバイス（Apple サーバーによってスパムと判定され位置情報が破棄されやすい）とは異なり、AirTracer は InfiTag 向けに **動的ローリングキーアルゴリズム** を開発しました。独自の **スマートウォーターフォール検索戦略** と組み合わせることで、よりリアルタイムの位置、高密度な軌跡ポイント、詳細な経路を非常に高い精度で取得します。
- 🏡 **Home Assistant ネイティブ連携**：MQTT Discovery プロトコルを内蔵。デバイスの位置、ステータス、バッテリー残量が、Home Assistant 内の `device_tracker` および `sensor` エンティティとして自動的にマッピングされます。**厳格な複数ユーザー間のセキュリティ分離** をサポート。
- 🗺️ **高精度な軌跡とジオフェンス分析**：Leaflet および高徳地図（AutoNavi）エンジンを搭載。経路のダイナミック再生、ヒートマップレンダリング、滞在地点の抽出、履歴速度の分析、電子フェンス警告などの機能を備えています。
- 🔔 **マルチチャネルの即時通知**：電子フェンスへの出入り、低バッテリーなどのイベントが発生した際、Telegram Bot またはウェブプッシュ経由で即時に通知を受け取れます。

---

## 📦 ソフトウェアリリースとダウンロード

事前にビルドされたファームウェアとモバイルアプリは、[Releases](../../releases) ページからダウンロードできます。

### 1. Android クライアント (APK)
- **AirTracer Android アプリ**：デスクトップウィジェット、バックグラウンドでの位置報告、リアルタイムマップ閲覧、アラーム通知に対応したモバイル特化型アプリ。
- 👉 [最新の APK をダウンロード](../../releases/latest) (GitHub Releases)

### 2. デバイスファームウェア (Firmware)
- **InfiTag (無極)**：**【推奨】** 動的ローリングキーメカニズムを採用。位置情報の欠落を回避し、リアルタイムで正確なトラッキングを提供します。nRF51822 ビーコンをサポート。
- **LoopTag**：従来の固定パブリックキー（Fixed Key）を使用。簡易テストや低頻度の位置取得に適しています（注意：固定キーモードでは Apple サーバーにより位置情報が破棄される場合があります）。nRF52810/nRF52832 をサポート。
- 👉 [ファームウェアパッケージを入手](../../releases/latest)

---

## 📚 ドキュメント

セットアップに役立つ詳細な分類ガイド：

- 📖 **[ユーザーガイド](docs/user_guide.md)**：アカウント登録、ログイン、GPS/FindMy デバイスの追加、電子フェンスの作成、Telegram Bot の連携方法。
- 🔌 **[ファームウェア書き込み＆ハードウェアガイド](docs/firmware_guide.md)**：配線図、書き込みツール（OpenOCD/J-Flash/PyOCD）、Makefile コンパイルパラメータ、シードキー生成理論について。
- 🏠 **[Home Assistant 連携ガイド](docs/home_assistant.md)**：MQTT Broker への接続、ユーザーごとの分離認証情報の適用、デバイストラッカーの自動追加方法。

---

## 💎 プライベートプロジェクト Tracer 商業展開・個別導入のご案内

AirTracer システムのパフォーマンスに満足し、**社内・個人サーバーにセルフホストで導入したい**場合や、**商用レベルの位置追跡業務向けにカスタマイズしたい**場合は、より強力なプライベートプロジェクト **Tracer** を商用ライセンスで提供いたします。

### 🌟 プライベート版 Tracer の追加機能：
1. **完全なセルフホストバックエンド**：すべてのインフラ（FastAPI + PostgreSQL + TimescaleDB + Redis + Mosquitto）を Docker-compose により一クリックで展開可能。
2. **高スループット最適化**：大量の時系列トラッキングデータを高速に格納するための TimescaleDB スキーマ最適化。
3. **エンタープライズ向け権限管理 (RBAC)**：細分化されたロールベースのアクセス制御、サブアカウント機能、マルチテナント分離。
4. **オリジナルブランド（OEM）のカスタマイズ**：専用のアプリ名、ロゴ、テーマカラー、専用ドメイン、独自マップライセンスの統合。
5. **専用ハードウェアのカスタマイズ対応**：回路設計から組み込みファームウェア（ST17H66B などの低価格国産 SoC への移植を含む）開発までワンストップで対応。

### 📞 お問い合わせ
専用サーバーの構築、カスタムハードウェア、商用ライセンス等にご関心がある方は、以下のチャネルよりご連絡ください：
- 📧 **メール**: [airtagtracer@gmail.com](mailto:airtagtracer@gmail.com)
- 💬 **Telegram**: [@AirTracer](https://t.me/AirTracer)

*要件（セルフホスト導入、カスタムハードウェア開発、企業ライセンス等）を簡単にご記載の上ご連絡ください。通常 24 時間以内に返信いたします。*
