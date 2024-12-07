# 图片采样工具

**简体中文** | [English](README.md) | [日本語](README_JA.md)

该工具可以将图像转换为音频文件。它读取图像中的像素数据，将其解释为频率数据，并生成相应的音频信号。这对于创意的视听项目或数据声化非常有用。

## 功能特点

- 将图像（PNG, JPG, JPEG）转换为WAV音频文件。
- 支持多语言：简体中文、英文和日语。
- 简单直观的图形用户界面（GUI）。
- 支持系统托盘功能，便于最小化应用程序。

## 需求

运行此工具需要安装以下Python库：

- `numpy`：用于数值运算和处理图像数据。
- `scipy`：用于将音频数据写入WAV文件。
- `PIL` (Pillow)：用于图像处理。
- `tkinter`：用于创建GUI。
- `pystray`：用于系统托盘功能。
- `base64`：用于处理图标数据。
- `locale`：用于检测系统语言。

你可以使用pip安装这些库：

```bash
pip install numpy scipy pillow pystray
```

对于在中国大陆的用户，可以使用下面的命令：

```bash
pip install numpy scipy pillow pystray -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 从源代码运行

要从源代码运行该工具，请按照以下步骤操作：

1. **克隆仓库**：

   ```bash
   git clone https://github.com/azdyqwo/image-to-audio-python.git
   ```

2. **进入项目目录**：

   ```bash
   cd image-to-audio-python
   ```

3. **运行脚本**：

   确保你的系统上已安装Python。然后运行以下命令：

   ```bash
   python ita.py
   ```

## 打包

要将此工具打包为独立的可执行文件，可以使用`PyInstaller`。请按照以下步骤操作：

1. 如果尚未安装PyInstaller，请安装：

   ```bash
   pip install pyinstaller
   ```

2. 在终端中运行以下命令以创建可执行文件：

   ```bash
   pyinstaller --onefile --windowed ita.py
   ```

3. 可执行文件将生成在`dist`目录中。

## 许可证

该项目使用MIT许可证。有关详细信息，请参阅LICENSE文件。

## 联系方式

如有任何问题或反馈，请随时与项目维护者联系。
