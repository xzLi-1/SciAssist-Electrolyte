import os
import subprocess
import sys

def check_dependencies():
    """检查必要的依赖"""
    try:
        import streamlit
        import pymupdf
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    """启动Streamlit应用"""
    print("🔋 启动电解液研究智能助手...")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 启动Streamlit应用
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动应用时出错: {e}")

if __name__ == "__main__":
    main()
