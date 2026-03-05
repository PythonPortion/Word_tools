import PyInstaller.__main__
import os
import sys
from datetime import datetime

# --- 配置信息 ---
SCRIPT_NAME = "app_doe_3.py"
APP_NAME = "Naruto"
# TARGET_ARCH = "universal2"
TARGET_ARCH = "arm64"
MODE = "--windowed"

# 新增配置
BUNDLE_ID = "com.lingxiao.word_tool"  # <-- 【配置】您独有的 Bundle ID
ICON_PATH = "app_icon.icns"  # <-- 【配置】您的 .icns 文件路径

# 排除模块列表
EXCLUDE_MODULES = [
]


# ------------------

def get_timestamp():
    """Generate timestamp for directory naming"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_build_directories(timestamp):
    """Create timestamped build and dist directories"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    build_dir = os.path.join(base_dir, "build", timestamp)
    dist_dir = os.path.join(base_dir, "dist", timestamp)

    # Create directories if they don't exist
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(dist_dir, exist_ok=True)

    print(f"📁 Build directory: {build_dir}")
    print(f"📁 Dist directory: {dist_dir}")

    return build_dir, dist_dir


def build_pyqt_app():
    """使用 PyInstaller API 打包 PyQt 应用程序。"""
    print(f"--- 🚀 准备打包应用：{APP_NAME} ---")

    # Generate timestamp and setup directories
    timestamp = get_timestamp()
    build_dir, dist_dir = setup_build_directories(timestamp)

    # 检查图标文件是否存在
    if not os.path.exists(ICON_PATH):
        print(f"⚠️ 警告：找不到图标文件 '{ICON_PATH}'。应用将使用默认图标。")
        # 如果找不到图标，继续执行，但不添加 --icon 参数
        use_icon = False
    else:
        use_icon = True

    if not os.path.exists(SCRIPT_NAME):
        print(f"❌ 错误：找不到主脚本文件 '{SCRIPT_NAME}'。")
        sys.exit(1)

    # 构造 PyInstaller 的参数列表
    pyinstaller_opts = [
        SCRIPT_NAME,
        f'--name={APP_NAME}',
        MODE,
        f'--target-arch={TARGET_ARCH}',
        f'--osx-bundle-identifier={BUNDLE_ID}',  # <-- 添加 Bundle ID
        f'--add-data=logo_ict.png:.',
        '--clean',
        f'--workpath={build_dir}',  # Specify build directory
        f'--distpath={dist_dir}',  # Specify dist directory
    ]

    # 根据检查结果添加图标参数
    if use_icon:
        pyinstaller_opts.append(f'--icon={ICON_PATH}')  # <-- 添加图标路径

    # 添加排除模块参数
    for module in EXCLUDE_MODULES:
        pyinstaller_opts.append(f'--exclude-module={module}')

    print("\n--- 📝 执行的 PyInstaller 参数 ---")
    print(f"pyinstaller {' '.join(pyinstaller_opts)}")
    print("----------------------------------\n")

    # 调用 PyInstaller 的主要入口
    try:
        PyInstaller.__main__.run(pyinstaller_opts)

        print("\n✅ 打包完成！")
        print(f"应用程序位于：{dist_dir}/{APP_NAME}.app")
        print(f"Bundle ID: {BUNDLE_ID}")
        print(f"Build artifacts: {build_dir}")
    except Exception as e:
        print(f"\n❌ 打包失败，发生错误：{e}")


if __name__ == "__main__":
    try:
        import PyInstaller
    except ImportError:
        print("🚨 PyInstaller 未安装。请先运行 'pip install pyinstaller'。")
        sys.exit(1)

    build_pyqt_app()
