import numpy as np
from scipy.io.wavfile import write
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import time
import webbrowser
import locale
from pystray import Icon, MenuItem as item, Menu
from PIL import Image as PILImage
import sys
import os
import subprocess

# 定义语言字典
languages = {
    'en': {
        'title': "Image to audio tool - Created by MeowcoQAQ",
        'select_image': "Select Image and Convert",
        'success': "Success",
        'success_msg': "The image has been successfully converted to audio!",
        'error': "Error",
        'error_msg': "An error occurred: ",
        'progress': "Progress",
        'remaining_time': "Remaining Time: ",
        'calculating': "Calculating...",
        'view_on_github': "View source code on GitHub",
        'menu_language': "Language",
        'menu_zh': "中文",
        'menu_en': "English",
        'menu_ja': "日本語",
        'file_types': "Image Files",
        'wav_file': "WAV Files",
        'seconds': "s",
        'close_prompt_title': "Are you sure you want to exit?",
        'close_prompt_message': "Please choose your next action",
        'close': "Exit",
        'background': "Minimize to Tray",
        'cancel': "Cancel",
        'tray_open': "Open",
        'tray_exit': "Exit",
        'open_folder': "Open Folder"
    },
    'zh': {
        'title': "图片采样工具 - 由 MeowcoQAQ 制作",
        'select_image': "选择图像并转换",
        'success': "成功",
        'success_msg': "图像已成功转换为音频！",
        'error': "错误",
        'error_msg': "发生错误：",
        'progress': "进度",
        'remaining_time': "剩余时间: ",
        'calculating': "计算中...",
        'view_on_github': "在 GitHub 上查看源代码",
        'menu_language': "语言",
        'menu_zh': "中文",
        'menu_en': "English",
        'menu_ja': "日本語",
        'file_types': "图像文件",
        'wav_file': "WAV 文件",
        'seconds': "秒",
        'close_prompt_title': "您确定要退出吗？",
        'close_prompt_message': "请选择您接下来的操作",
        'close': "直接退出",
        'background': "最小化到系统托盘",
        'cancel': "取消",
        'tray_open': "打开",
        'tray_exit': "退出",
        'open_folder': "打开文件夹"
    },
    'ja': {
        'title': "画像から音声へのツール - ねこかわ作成",
        'select_image': "画像を選択して変換",
        'success': "成功",
        'success_msg': "画像が音声に正常に変換されました！",
        'error': "エラー",
        'error_msg': "エラーが発生しました：",
        'progress': "進捗",
        'remaining_time': "残り時間：",
        'calculating': "計算中...",
        'view_on_github': "GitHubでソースコードを表示",
        'menu_language': "言語",
        'menu_zh': "中文",
        'menu_en': "English",
        'menu_ja': "日本語",
        'file_types': "画像ファイル",
        'wav_file': "WAV ファイル",
        'seconds': "秒",
        'close_prompt_title': "本当に終了しますか？",
        'close_prompt_message': "次の操作を選択してください",
        'close': "終了",
        'background': "トレイに最小化",
        'cancel': "キャンセル",
        'tray_open': "開く",
        'tray_exit': "終了",
        'open_folder': "フォルダーを開く"
    }
}

# 检测系统语言
def detect_language():
    lang, _ = locale.getdefaultlocale()
    if lang and ('zh' in lang):
        return 'zh'
    elif lang and ('ja' in lang):
        return 'ja'
    else:
        return 'en'

# 当前语言
current_language = detect_language()

# 工作状态标志
is_working = False

# 保存文件夹路径
output_folder = None

def set_language(lang):
    global current_language
    current_language = lang
    root.title(languages[current_language]['title'])
    button.config(text=languages[current_language]['select_image'])
    progress_label.config(text="0.00%")
    time_label.config(text=languages[current_language]['remaining_time'] + languages[current_language]['calculating'])
    link_label.config(text=languages[current_language]['view_on_github'])
    # 更新菜单
    menu_bar.entryconfig(0, label=languages[current_language]['menu_language'])
    language_menu.entryconfig(0, label=languages[current_language]['menu_zh'])
    language_menu.entryconfig(1, label=languages[current_language]['menu_en'])
    language_menu.entryconfig(2, label=languages[current_language]['menu_ja'])

def show_custom_messagebox(title, message, output_path=None, is_error=False):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("300x150")
    dialog.transient(root)
    dialog.grab_set()
    dialog.iconbitmap('')  # 移除图标

    tk.Label(dialog, text=message, fg='red' if is_error else 'black').pack(pady=10)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="OK", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    if output_path:
        def open_folder():
            subprocess.run(f'explorer /select,"{output_path}"')
            dialog.destroy()

        ttk.Button(button_frame, text=languages[current_language]['open_folder'], command=open_folder).pack(side=tk.LEFT, padx=5)

def convert_image_to_audio(image_path, output_path, progress_var, progress_label, time_label):
    global is_working
    is_working = True
    try:
        start_time = time.time()
        image = Image.open(image_path).convert('L')
        data = np.array(image)
        sample_rate = 20000
        duration = 5
        frequency_range = (20, 20000)
        min_freq, max_freq = frequency_range
        frequencies = np.interp(data.flatten(), (0, 255), frequency_range)
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)
        audio = np.zeros(num_samples, dtype=np.float32)
        block_size = 1000
        num_blocks = len(frequencies) // block_size + 1

        for i in range(num_blocks):
            start = i * block_size
            end = min((i + 1) * block_size, len(frequencies))
            block_frequencies = frequencies[start:end]
            block_audio = np.sum(np.sin(2 * np.pi * block_frequencies[:, None] * t), axis=0)
            audio += block_audio.astype(np.float32)
            progress = (i + 1) / num_blocks * 100
            progress_var.set(progress)
            progress_label.config(text=f"{progress:.2f}%")
            elapsed_time = time.time() - start_time
            estimated_total_time = elapsed_time / (progress / 100)
            remaining_time = estimated_total_time - elapsed_time
            remaining_time_text = f"{languages[current_language]['remaining_time']}{remaining_time:.2f} {languages[current_language]['seconds']}"
            time_label.config(text=remaining_time_text)
            root.update_idletasks()

        write(output_path, sample_rate, audio)
        show_custom_messagebox(languages[current_language]['success'], languages[current_language]['success_msg'], output_path=output_path)
    except Exception as e:
        show_custom_messagebox(languages[current_language]['error'], languages[current_language]['error_msg'] + str(e), is_error=True)
    finally:
        is_working = False

def open_file():
    global output_folder
    file_path = filedialog.askopenfilename(filetypes=[(languages[current_language]['file_types'], "*.png;*.jpg;*.jpeg")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[(languages[current_language]['wav_file'], "*.wav")])
        if output_path:
            output_folder = os.path.dirname(output_path)
            progress_var.set(0)
            progress_label.config(text="0.00%")
            time_label.config(text=languages[current_language]['remaining_time'] + languages[current_language]['calculating'])
            threading.Thread(target=convert_image_to_audio, args=(file_path, output_path, progress_var, progress_label, time_label)).start()

def open_github_link(event):
    webbrowser.open_new("https://github.com/azdyqwo/image-to-audio-python")

def on_closing():
    if not is_working:
        root.quit()
        sys.exit()
    else:
        root.bell()

        dialog = tk.Toplevel(root)
        dialog.title(languages[current_language]['close_prompt_title'])
        dialog.geometry("300x150")
        dialog.transient(root)
        dialog.grab_set()
        dialog.iconbitmap('')  # 移除图标

        dialog.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text=languages[current_language]['close_prompt_message']).pack(pady=10)

        button_frame = tk.Frame(dialog)
        button_frame.pack(expand=True)

        def close_app():
            dialog.destroy()
            root.quit()
            sys.exit()

        def minimize_to_tray():
            dialog.destroy()
            root.withdraw()
            create_tray_icon()

        ttk.Button(button_frame, text=languages[current_language]['close'], command=close_app).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(button_frame, text=languages[current_language]['background'], command=minimize_to_tray).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(button_frame, text=languages[current_language]['cancel'], command=dialog.destroy).pack(side=tk.LEFT, padx=10, pady=10)

def create_tray_icon():
    icon_image = PILImage.open("icon.ico")
    menu = Menu(
        item(languages[current_language]['tray_open'], show_window),
        item(languages[current_language]['tray_exit'], exit_app)
    )
    icon = Icon("ImageToAudio", icon_image, menu=menu)
    icon.run()

def show_window(icon, item):
    icon.stop()
    root.deiconify()

def exit_app(icon, item):
    icon.stop()
    root.quit()
    sys.exit()

root = tk.Tk()
root.title(languages[current_language]['title'])

# 设置窗口不可调整大小和最大化
root.resizable(False, False)

# 添加图标
root.iconbitmap('icon.ico')

# 设置窗口宽度为450，高度自适应
root.geometry("450x400")
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
x = screen_width // 2 - size[0] // 2
y = screen_height // 2 - size[1] // 2
root.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 创建语言菜单
language_menu = tk.Menu(menu_bar, tearoff=0)
language_menu.add_command(label=languages[current_language]['menu_zh'], command=lambda: set_language('zh'))
language_menu.add_command(label=languages[current_language]['menu_en'], command=lambda: set_language('en'))
language_menu.add_command(label=languages[current_language]['menu_ja'], command=lambda: set_language('ja'))
menu_bar.add_cascade(label=languages[current_language]['menu_language'], menu=language_menu)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=20)

progress_label = tk.Label(root, text="0.00%")
progress_label.pack()

time_label = tk.Label(root, text=languages[current_language]['remaining_time'] + languages[current_language]['calculating'])
time_label.pack()

button = ttk.Button(root, text=languages[current_language]['select_image'], command=open_file)
button.pack(pady=20)

link_label = tk.Label(root, text=languages[current_language]['view_on_github'], fg="blue", cursor="hand2")
link_label.pack(pady=10)
link_label.bind("<Button-1>", open_github_link)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()