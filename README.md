# FreeSpiritedBird

一只会跟随键盘输入做出动作的桌面宠物。窗口透明、无边框并保持置顶，可自由拖动。
支持 **Windows** 和 **macOS**。

<p align="center">
  <img src="resources/standby.gif" alt="FreeSpiritedBird 待机动画" width="258">
</p>

## 功能

- 根据左右手按键播放对应动画
- `Space` 播放空格动画
- `Backspace` 播放删除动画
- 动画结束后自动恢复待机状态
- 同时按下 `5 + 6 + 7` 退出程序

## 下载

前往本项目的 **Releases** 页面下载对应平台的压缩包。

| 平台 | 文件 | 使用方法 |
|------|------|----------|
| Windows | `FreeSpiritedBird.zip` | 解压后双击 `FreeSpiritedBird.exe` |
| macOS | `FreeSpiritedBird-macOS.zip` | 解压后双击 `FreeSpiritedBird.app` |

### macOS 重要提示

macOS 的安全机制要求首次运行后必须授予「辅助功能」权限才能监听键盘：

1. 首次运行时应用会自动弹出提示框，并跳到 **系统设置 → 隐私与安全性 → 辅助功能**
2. 点击下方的 `+` 号，将 `FreeSpiritedBird.app` 添加到列表并勾选开关
3. **完全退出应用**（Cmd+Q 或活动监视器里结束进程），重新打开即可生效

如果从终端运行源码，则需要把使用的终端（Terminal、iTerm2 等）加到辅助功能列表里。

## 动画预览

### 空格动画

<p align="center">
  <img src="resources/blank.gif" alt="FreeSpiritedBird 空格动画" width="210">
</p>

### 退格动画

<p align="center">
  <img src="resources/del.gif" alt="FreeSpiritedBird 退格删除动画" width="210">
</p>

## 从源码运行

```bash
pip3 install -r requirements.txt
python3 main.py
```

项目使用 Python、PyQt5 和 pynput 开发，支持 Windows 和 macOS。

## 素材与免责声明

本项目仅供学习与交流使用。项目中的部分图片和动画素材来源于网络，相关权利归原作者或权利人所有，本项目不主张对这些第三方素材享有版权，也无意侵犯任何合法权益。

如果你是相关权利人，并认为本项目使用的素材侵犯了你的权益，请通过 GitHub Issue 联系并注明具体文件；核实后会尽快删除或替换。此声明不构成对相关素材的授权。