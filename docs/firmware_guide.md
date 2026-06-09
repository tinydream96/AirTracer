# 🔌 固件烧录与硬件接入指引

AirTracer 支持利用低功耗蓝牙 (BLE) 芯片自制 FindMy 追踪标签。本文档将指导您如何为常用蓝牙芯片（以 Nordic nRF51/nRF52 系列为例）配置、编译和烧录 AirTracer 兼容固件，以及如何管理设备密钥。

---

## 1. 硬件选型与准备

### 支持的芯片
- **nRF51822**：低成本经典芯片（如 InfiTag）。
- **nRF52810 / nRF52832**：新一代低功耗芯片（如 LoopTag），功耗表现更优，时钟稳定性更好。
- **ST17H66B**（实验性支持）：国产极低成本 SoC。

### 烧录工具
- **硬件调试器**：ST-Link V2、J-Link 或 DAPLink 仿真器。
- **接线连接**：使用 SWD 接口，通常需要连接 4 根线：
  * **VCC (3.3V)** -> 标签电源
  * **GND** -> 标签接地
  * **SWDIO** -> 标签 SWDIO 数据脚
  * **SWCLK** -> 标签 SWDCLK 时钟脚

---

## 2. 解锁与擦除芯片 (重要)

市售的许多蓝牙标签或手环出厂时带有“读保护 (Readout Protection)”，在烧录新固件前必须进行强制擦除和解锁。

使用 `nrfjprog` (Nordic 命令行工具) 或 `pyocd` 进行操作：

### 方案 A：使用 nrfjprog (需安装 Nordic Command Line Tools)
```bash
# 解锁并擦除整个芯片 (去除读保护)
nrfjprog --recover
```

### 方案 B：使用 pyocd (Python 开源工具，支持各种仿真器)
```bash
# 安装 pyocd
pip install pyocd

# 恢复/解锁芯片
pyocd erase -c --target nrf51
# 或如果是 nrf52
pyocd erase -c --target nrf52810
```

---

## 3. 固件编译宏参数配置

在编译固件时，可以通过传入 Makefile 宏参数自定义标签的行为。以下是关键参数说明：

| 编译参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `DYNAMIC_KEYS` | `1` | 启用动态密钥滚动机制。若为 `1` 则启用 **InfiTag** 模式（基于 Seed 滚动生成密钥，定位更实时、轨迹点更多更连贯、防丢弃，推荐）；若为 `0` 则退回为 **LoopTag** 传统固定公钥模式（固定公钥较易被苹果服务器过滤或丢弃）。 |
| `KEY_ROTATION_INTERVAL` | `900` | 密钥滚动周期（秒）。默认 `900` 即 15 分钟更换一次广播公钥（仅在 InfiTag 模式下生效）。 |
| `ADVERTISING_INTERVAL` | `2060` | 蓝牙广播间隔（毫秒）。根据 Apple FindMy 规范，通常设在 `2000` 毫秒左右以节省电量。 |
| `LFCLK_SOURCE` | `0` | 低频时钟源。`0` 表示使用内部 RC 振荡器（免外部晶振，适合廉价防丢器）；`1` 表示使用外部高精度 32.768kHz 晶振（功耗更低，时钟更准）。 |
| `HAS_BATTERY` | `1` | 开启电池电压测量功能，定时将电池电量状态编入广播或在连接时上报。 |
| `DEVICE_NAME_STRING` | `"InfiTag_TAG"` | 设备的本地蓝牙广播名称，便于在手机 App 搜索时识别。 |

### 编译示例命令：
```bash
make -C heystack-nrf5x_infi/nrf51822/armgcc \
  nrf51822_xxab \
  HAS_DCDC=1 \
  HAS_DEBUG=0 \
  HAS_BATTERY=1 \
  KEY_ROTATION_INTERVAL=900 \
  ADVERTISING_INTERVAL=2060 \
  LFCLK_SOURCE=0 \
  DYNAMIC_KEYS=1 \
  DEVICE_NAME_STRING=InfiTag_TAG06 \
  GNU_INSTALL_ROOT=/usr/local/bin/
```

---

## 4. 固件烧录

编译完成后，您将获得 `app.hex` (应用程序固件) 以及对应的 SoftDevice 协议栈。

### 使用 pyocd 一键烧录应用合并包：
```bash
pyocd flash -t nrf51 --erase sector combined_firmware.hex
```

---

## 5. 密钥管理与 Seed 配置

FindMy 定位依赖非对称加密。设备在广播时使用的是 **椭圆曲线公钥 (ECC Public Key)** 的特定哈希值。

### 🔑 密钥滚动与 Seed (种子) 原理
1. **种子生成**：在配置设备时，系统或您会生成一个 32 字节的随机种子（Seed）。
2. **本地密钥派生**：设备端固件会烧录或保存这个 Seed，并根据公式 `Key_i = SHA256(Seed + i)` 定时生成新的私钥，并派生出对应的公钥进行蓝牙广播。
3. **云端拉取**：在 AirTracer 网页端添加设备时，您只需提交该 **Seed**。AirTracer 后端会使用相同的算法同步推算当前时刻（`Index i`）设备正在广播的公钥，并向 Apple 接口发起查询请求，从而检索到定位报告。

> [!WARNING]
> **请务必安全保管您的 Seed！**
> 一旦 Seed 泄露，任何人都可以计算出您标签的广播序列并实时追踪您的位置。反之，若丢失 Seed，您将无法在平台中重新绑定并找回您的历史轨迹。
