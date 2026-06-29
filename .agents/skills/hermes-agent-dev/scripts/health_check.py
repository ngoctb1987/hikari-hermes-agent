#!/usr/bin/env python3
# ==============================================================================
# File: health_check.py
# Purpose: Kiểm tra trạng thái hoạt động và chuẩn đoán lỗi cho Hermes Agent.
#          Phát hiện khóa stale (locks), cổng bận (port 9119), cấu hình thiếu
#          và cảnh báo trong file log.
# ==============================================================================

import os
import sys
import socket
import json
import yaml
from pathlib import Path

# Hỗ trợ in tiếng Việt và unicode có dấu trên console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def print_status(icon, message, color="\033[0m"):
    """In thông báo trạng thái có màu sắc định dạng."""
    # Chỉ bật mã màu trên TTY
    if sys.stdout.isatty():
        reset = "\033[0m"
        print(f"{color}{icon} {message}{reset}")
    else:
        print(f"{icon} {message}")

def check_port(port, host="127.0.0.1"):
    """Kiểm tra xem một cổng có đang lắng nghe (LISTEN) hay không."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def check_process_alive(pid):
    """Kiểm tra xem PID có đang thực sự chạy trên hệ thống không."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, SystemError):
        return False

def main():
    print_status("[*]", "Đang bắt đầu kiểm tra sức khỏe Hermes Agent...", "\033[1;36m")
    
    # 1. Xác định thư mục dữ liệu HERMES_HOME
    hermes_home_env = os.environ.get("HERMES_HOME")
    if hermes_home_env:
        hermes_home = Path(hermes_home_env)
        print_status("[i]", f"Sử dụng HERMES_HOME từ biến môi trường: {hermes_home}")
    else:
        hermes_home = Path.home() / ".hermes"
        print_status("[i]", f"HERMES_HOME không được thiết lập, mặc định: {hermes_home}")

    if not hermes_home.exists():
        print_status("[x]", f"Thư mục HERMES_HOME không tồn tại tại: {hermes_home}", "\033[1;31m")
        sys.exit(1)

    # 2. Kiểm tra file cấu hình config.yaml
    config_path = hermes_home / "config.yaml"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            provider = config.get("memory", {}).get("provider", "built-in")
            model = config.get("model", "default")
            print_status("[+]", f"Đã đọc file cấu hình config.yaml (Model: {model}, Memory: {provider})", "\033[1;32m")
        except Exception as e:
            print_status("[!]", f"Không thể phân tích cú pháp config.yaml: {e}", "\033[1;33m")
    else:
        print_status("[!]", "Không tìm thấy file config.yaml. Hệ thống sẽ sử dụng cấu hình mặc định.", "\033[1;33m")

    # 3. Kiểm tra các file khóa (Locks)
    print_status("[*]", "Đang quét các file khóa (process locks)...")
    pid_file = hermes_home / "gateway.pid"
    if pid_file.exists():
        try:
            content = pid_file.read_text().strip()
            # Thử parse JSON trước (phiên bản mới lưu dạng JSON)
            try:
                data = json.loads(content)
                pid = data.get("pid")
            except json.JSONDecodeError:
                pid = int(content)
                
            if check_process_alive(pid):
                print_status("[+]", f"Gateway đang hoạt động với PID: {pid}", "\033[1;32m")
            else:
                print_status("[!]", f"Phát hiện file gateway.pid tồn dư (stale lock) với PID {pid} không tồn tại trên hệ thống.", "\033[1;33m")
                print_status("[i]", "Khuyên dùng: Xóa file '/opt/data/gateway.pid' (hoặc '~/.hermes/gateway.pid') trước khi restart.")
        except Exception as e:
            print_status("[!]", f"Lỗi đọc gateway.pid: {e}", "\033[1;33m")
    else:
        print_status("[i]", "Không có file khóa gateway.pid đang hoạt động.")

    locks_dir = hermes_home / "locks"
    if locks_dir.exists():
        lock_files = list(locks_dir.glob("*"))
        if lock_files:
            print_status("[!]", f"Tìm thấy {len(lock_files)} file trong thư mục locks/.", "\033[1;33m")
            for lf in lock_files:
                try:
                    lf_content = lf.read_text().strip()
                    print_status("  ", f"- File lock: {lf.name} (Nội dung: '{lf_content}')")
                except Exception:
                    pass
        else:
            print_status("[+]", "Thư mục locks/ trống.", "\033[1;32m")

    # 4. Kiểm tra cổng lắng nghe (Ports)
    print_status("[*]", "Đang kiểm tra cổng lắng nghe của Dashboard (mặc định: 9119)...")
    dashboard_active = check_port(9119)
    if dashboard_active:
        print_status("[+]", "Cổng 9119 đang lắng nghe (Dashboard/API đang chạy).", "\033[1;32m")
    else:
        print_status("[!]", "Cổng 9119 không hoạt động. Dashboard hoặc API Server chưa được khởi chạy.", "\033[1;33m")

    # 5. Kiểm tra log lỗi gần đây
    print_status("[*]", "Đang quét log lỗi gần đây...")
    error_log = hermes_home / "logs" / "errors.log"
    if error_log.exists():
        try:
            # Lấy 5 dòng lỗi cuối cùng, dùng errors="replace" để tránh crash do ký tự không chuẩn
            with open(error_log, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
            if lines:
                print_status("[!]", f"Phát hiện các lỗi gần đây trong errors.log:", "\033[1;33m")
                for line in lines[-5:]:
                    print(f"   | {line.strip()}")
            else:
                print_status("[+]", "errors.log trống.", "\033[1;32m")
        except Exception as e:
            print_status("[!]", f"Không thể đọc file errors.log: {e}", "\033[1;33m")
    else:
        print_status("[+]", "Không tìm thấy file errors.log (Không có lỗi hệ thống được ghi nhận).", "\033[1;32m")

    print_status("[*]", "Hoàn tất kiểm tra sức khỏe hệ thống.", "\033[1;36m")

if __name__ == "__main__":
    main()
