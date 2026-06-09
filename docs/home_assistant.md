# 🏠 Home Assistant 与 MQTT 集成指南

AirTracer 系统内置支持 **MQTT Discovery** 协议。一旦完成配置，您在 AirTracer 中管理的设备将作为实体**自动映射**到您的 Home Assistant (HA) 系统中，完全不需要手动编写复杂的 YAML 代码。

---

## 🗺️ 架构与数据流

集成的数据流由以下三部分组成：
1. **AirTracer 后端**：负责接收 GPS 硬件/FindMy 上报，并按照 HA Discovery 格式将坐标数据打包，推送到指定的 MQTT 代理服务器（MQTT Broker）。
2. **MQTT Broker**：消息中转站（如 Mosquitto 或 EMQX），负责数据传递与分发。
3. **Home Assistant**：订阅 MQTT 主题，检测到新配置后自动在后台创建 `device_tracker`（设备追踪器）和 `sensor`（电量传感器）实体，并在地图上渲染位置。

```
[GPS/FindMy 标签] 
     │  (HTTPS / 自动同步)
     ▼
[AirTracer 后端] 
     │  (MQTT 协议上报)
     ▼
[MQTT Broker (Mosquitto/EMQX)] 
     │  (MQTT 订阅推流)
     ▼
[Home Assistant (地图渲染/自动化触发)]
```

---

## ⚙️ 集成步骤

### 1. 配置 AirTracer 后端 (MQTT 生产者)
推荐通过 AirTracer 的网页端进行配置（需要管理员或用户专属配置权限）：
1. 登录 AirTracer，前往 **系统设置 (System Settings)**。
2. 找到 **Home Assistant / MQTT** 配置卡片，点击 **编辑**。
3. 填写您的 MQTT Broker 信息：
   * **Broker 地址**：例如 `192.168.1.100` 或域名。
   * **端口**：默认为 `1883`。
   * **MQTT 专属凭证**：为保证多用户环境下的数据隔离，请使用系统为您分配的专属 MQTT 用户名及密码（如 `user_001`）。
   * **自动发现前缀 (Discovery Prefix)**：默认为 `homeassistant`。
4. 点击 **测试并保存**，后端服务将自动尝试连接 Broker 并向外广播设备配置信息。

---

### 2. 在 Home Assistant 侧配置 (MQTT 消费者)
在您的 Home Assistant 实例中，需要启用 MQTT 集成并订阅对应的隔离前缀：

1. 进入 HA 的 **设置 (Settings)** -> **设备与服务 (Devices & Services)**。
2. 点击右下角 **添加集成**，搜索并选择 **MQTT**。
3. 输入您的 MQTT Broker 连接地址，并在 **用户名** 和 **密码** 处填入 **AirTracer 分配给您的专属 MQTT 凭据**。
4. **配置自动发现前缀 (重要！)**：
   * 在 MQTT 集成卡片上点击 **选项 (Configure)**。
   * 找到 **Discovery prefix** 配置项。
   * 将其修改为：`homeassistant/{您的 User ID}` (如 `homeassistant/user_001`)。
   * 确保“启用自动发现”处于勾选状态，点击提交。

---

## 🎉 集成效果

配置成功后，当 AirTracer 再次接收到设备位置时，系统会自动在 HA 中生成以下两个实体：

| 实体类型 | 命名规则示例 | 说明 |
| :--- | :--- | :--- |
| **设备追踪 (Tracker)** | `device_tracker.tracer_{device_id}` | 包含设备当前经纬度、海拔、精确度等丰富属性，可在 HA Map 卡片中直接渲染。 |
| **电量传感器 (Sensor)** | `sensor.tracer_{device_id}_battery` | 提取设备电量百分比，可作为低电量提醒自动化触发器。 |

---

## 🔄 反向导入：将 HA 设备导入 AirTracer

不仅可以把 AirTracer 追踪的设备推送到 HA，您还可以将在 HA 中已有的追踪器（例如通过手机 HA 客户端、iCloud3 等生成的 `device_tracker`）**反向导入**到 AirTracer 中集中统一管理。

### 导入前提
- HA 侧的设备必须也是通过 MQTT 协议接入的，且遵循标准的 HA MQTT Discovery 规范。
- 确保您的 HA 与 AirTracer 连接的是同一个 MQTT Broker。

### 导入操作
1. 登录 AirTracer 网页端，进入 **设备管理 (Device Management)**。
2. 点击 **添加设备 (Add Device)**。
3. 类别中选择 **Home Assistant 导入**。
4. 系统会扫描当前 MQTT 局域网中广播的符合条件的 HA 追踪器，选择您需要的设备点击 **确认导入** 即可。

---

## 🔍 常见问题与排查指南

### 1. HA 无法自动发现设备
- **检查 Topic**：使用工具 **MQTT Explorer** 连接到您的 MQTT Broker，确认是否有以 `homeassistant/device_tracker/...` 开头的消息在发送。
- **匹配 Prefix**：检查 AirTracer 环境变量或系统设置中的 `MQTT_DISCOVERY_PREFIX`，必须与您在 HA MQTT 集成选项里配置的 `Discovery prefix` 完全一致。

### 2. 连接被拒绝 (Connection Refused)
- 检查您的专属凭证是否填写正确。AirTracer 后端在私有化部署中可能启用了 MQTT 的 ACL（访问控制列表），禁止跨用户订阅 Topic 行为。
- 如果是本地局域网测试，检查防火墙的 `1883` 端口是否已经放行。
