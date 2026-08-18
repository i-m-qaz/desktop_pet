# FreeSpiritedBird

一只会跟随键盘输入做出动作的 Windows 桌面宠物。窗口透明、无边框并保持置顶，可自由拖动。

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

前往本项目的 **Releases** 页面下载 `FreeSpiritedBird.zip`，解压后双击 `FreeSpiritedBird.exe`。

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

```powershell
python -m pip install -r requirements.txt
python main.py
```

项目使用 Python、PyQt5 和 pynput 开发，仅支持 Windows。

## 素材与免责声明

本项目仅供学习与交流使用。项目中的部分图片和动画素材来源于网络，相关权利归原作者或权利人所有，本项目不主张对这些第三方素材享有版权，也无意侵犯任何合法权益。

如果你是相关权利人，并认为本项目使用的素材侵犯了你的权益，请通过 GitHub Issue 联系并注明具体文件；核实后会尽快删除或替换。此声明不构成对相关素材的授权。