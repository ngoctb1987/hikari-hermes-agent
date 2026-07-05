---
name: hermes-agent-dev
description: Hướng dẫn chuyên sâu về phát triển, vận hành và cấu hình deploy dự án Hermes Agent (Docker, Nginx, WebSocket, Custom Tools, Gateway).
---

# Hermes Agent Development & Deployment Kit

Bộ skill này lưu trữ kiến thức chuyên sâu về kiến trúc codebase, quy trình phát triển và các phương án triển khai dự án Hermes Agent trong môi trường doanh nghiệp.

---

## 1. Bản Đồ Thư Mục (Codebase Map)

- [cli.py](file:///d:/hikari-hermes-agent/cli.py) & [hermes_cli/](file:///d:/hikari-hermes-agent/hermes_cli): Toàn bộ logic giao diện dòng lệnh (TUI), Skin Engine, và các lệnh cấu hình.
- [run_agent.py](file:///d:/hikari-hermes-agent/run_agent.py): Lớp `AIAgent` điều phối vòng lặp gọi API và thực thi tool đồng bộ.
- [gateway/](file:///d:/hikari-hermes-agent/gateway): Quản lý các adapter kết nối ứng dụng chat (Telegram, Discord, Slack) và API server.
- [tools/](file:///d:/hikari-hermes-agent/tools): Các file cài đặt công cụ (tools) đăng ký tập trung qua `tools/registry.py`.
- [hermes_constants.py](file:///d:/hikari-hermes-agent/hermes_constants.py): Định nghĩa biến môi trường `HERMES_HOME` để hỗ trợ cơ chế chạy đa cấu hình (Profiles).

---

## 2. Quy Trình Phát Triển (Development Guide)

### A. Thêm Custom Tool Mới
Để tích hợp thêm một công cụ mới vào Agent, thực hiện 3 bước:
1. **Tạo file tool mới** tại `tools/your_tool.py`:
   ```python
   import json
   from tools.registry import registry

   def custom_tool_handler(param: str, task_id: str = None) -> str:
       # Xử lý logic tại đây
       return json.dumps({"status": "success", "result": "..."})

   registry.register(
       name="custom_tool",
       toolset="custom",
       schema={
           "name": "custom_tool",
           "description": "Mô tả chi tiết chức năng của tool",
           "parameters": {
               "type": "OBJECT",
               "properties": {
                   "param": {"type": "STRING", "description": "Mô tả tham số"}
               },
               "required": ["param"]
           }
       },
       handler=lambda args, **kw: custom_tool_handler(args.get("param", ""), kw.get("task_id")),
   )
   ```
2. **Khai báo import** trong `_discover_tools()` tại [model_tools.py](file:///d:/hikari-hermes-agent/model_tools.py).
3. **Kích hoạt tool** bằng cách thêm tên tool vào danh sách phù hợp (`_HERMES_CORE_TOOLS` hoặc tập hợp mới) tại [toolsets.py](file:///d:/hikari-hermes-agent/toolsets.py).

### B. Thêm Slash Command cho CLI / Gateway
1. Thêm định nghĩa `CommandDef` vào `COMMAND_REGISTRY` tại [hermes_cli/commands.py](file:///d:/hikari-hermes-agent/hermes_cli/commands.py):
   ```python
   CommandDef("mycmd", "Mô tả tính năng", "Configuration", aliases=("mc",), args_hint="[arg]"),
   ```
2. Thêm hàm xử lý `_handle_mycmd` trong class `HermesCLI` tại [cli.py](file:///d:/hikari-hermes-agent/cli.py).
3. Nếu lệnh khả dụng qua Gateway, thêm nhánh xử lý trong `gateway/run.py`.

---

## 3. Triển Khai VPS Doanh Nghiệp (Enterprise Deployment)

### A. Quy Tắc Thiết Lập Môi Trường (Profiles & Homes)
- Luôn sử dụng hàm `get_hermes_home()` từ `hermes_constants` để lấy đường dẫn ghi đè thư mục dữ liệu hệ thống (sessions, logs, config). Không hardcode đường dẫn dạng `~/.hermes`.
- Khi in đường dẫn hiển thị cho người dùng, sử dụng `display_hermes_home()`.

### B. Khắc Phục Lỗi Xung Đột Tiến Trình (Lock Files)
Khi khởi động lại Docker Container chạy Gateway, tiến trình mới thường giữ PID 1 và bị kẹt do lock file cũ (`gateway.pid` và các file trong `locks/`) chưa kịp xóa trên thư mục dùng chung (volume mount).
- **Giải pháp:** Thiết lập script dọn dẹp khóa tự động chạy trước khi khởi động ứng dụng chính (như khai báo trong file cấu hình docker-compose mẫu).

### C. Bảo Mật Truy Cập Dashboard Trên VPS Public
Khi cấu hình domain public truy cập vào Dashboard qua Nginx, việc sử dụng cờ `--insecure` hoặc biến môi trường `HERMES_DASHBOARD_INSECURE=1` sẽ vô hiệu hóa hoàn toàn xác thực. Điều này cho phép bất kỳ ai cũng có thể sử dụng hệ thống của bạn miễn phí.
- **Giải pháp 1 (Khuyên dùng):** Sử dụng Basic Authentication của Nginx bằng cách tạo file `.htpasswd` và cấu hình `auth_basic` trong block `location /` của tệp cấu hình Nginx.
- **Giải pháp 2:** Cấu hình Basic Auth nội bộ của Dashboard bằng cách thêm biến môi trường `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` và `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` vào `docker-compose.yml`, đồng thời loại bỏ cờ `--insecure` khỏi entrypoint.
- **Giải pháp 3:** Giới hạn binding vào loopback (`127.0.0.1`) và truy cập từ xa an toàn bằng SSH Tunnel hoặc VPN (Tailscale).


---

## 4. Xử Lý Sự Cố Thường Gặp (Troubleshooting)

| Triệu chứng | Nguyên nhân chính | Cách khắc phục |
|-------------|-------------------|----------------|
| **502 Bad Gateway** | Dashboard / Gateway chưa chạy ở port tương ứng (ví dụ: 9119) | Chạy lệnh `docker ps` để kiểm tra trạng thái container và log |
| **Trang Dashboard trống hoặc xoay load liên tục** | Nginx chưa hỗ trợ WebSocket hoặc trình duyệt chặn Mixed Content (HTTPS -> WS) | Cập nhật cấu hình Nginx với đầy đủ các header `Upgrade` và `Connection` |
| **Dashboard crash liên tục (Restarting)** | Docker binding vào `0.0.0.0` mà không cấu hình OAuth bảo mật | Thêm tham số `--insecure` vào entrypoint hoặc cấu hình `HERMES_DASHBOARD_INSECURE=1` |
| **Không phản hồi qua Telegram** | Khóa PID hoặc SQLite lock do tắt container không đúng cách | Dọn dẹp thủ công `/opt/data/gateway.pid` hoặc cấu hình dọn dẹp tự động |
