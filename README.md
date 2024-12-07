# Image to Audio Tool

[中文自述文件](README_ZH_CN.md) | [日本語のREADME](README_JA.md)

This tool allows you to convert an image into an audio file. It reads the pixel data from an image, interprets it as frequency data, and generates a corresponding audio signal. This can be useful for creative audio-visual projects or data sonification.

## Features

- Convert images (PNG, JPG, JPEG) to WAV audio files.
- Support for multiple languages: English, Chinese, and Japanese.
- Simple and intuitive graphical user interface (GUI).
- System tray functionality for minimizing the application.

## Requirements

To run this tool, you need to have the following Python libraries installed:

- `numpy`: For numerical operations and handling image data.
- `scipy`: For writing the audio data to WAV files.
- `PIL` (Pillow): For image processing.
- `tkinter`: For creating the GUI.
- `pystray`: For system tray functionality.
- `base64`: For handling icon data.
- `locale`: For detecting system language.

You can install these libraries using pip:

```bash
pip install numpy scipy pillow pystray
```

## Running from Source

To run the tool from the source code, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/azdyqwo/image-to-audio-python.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd image-to-audio-python
   ```

3. **Run the script**:

   Make sure you have Python installed on your system. Then run the following command:

   ```bash
   python ita.py
   ```

## Packaging

To package this tool into a standalone executable, you can use `PyInstaller`. Follow these steps:

1. Install PyInstaller if you haven't already:

   ```bash
   pip install pyinstaller
   ```

2. Run the following command in the terminal to create an executable:

   ```bash
   pyinstaller --onefile --windowed ita.py
   ```

3. The executable will be generated in the `dist` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For any questions or feedback, feel free to reach out to the project maintainer.
