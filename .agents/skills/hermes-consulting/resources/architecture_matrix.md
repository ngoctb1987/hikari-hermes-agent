# Ma Trận Thiết Kế Kiến Trúc & Sizing Hạ Tầng

Bảng này đối chiếu quy mô triển khai dự án Hermes Agent với yêu cầu cấu hình phần cứng và hạ tầng tương ứng trên VPS/Cloud.

---

## 1. Bảng Khuyến Nghị Sizing Hạ Tầng

| Quy mô triển khai | Số người dùng hoạt động | Cấu hình VPS đề xuất (CPU / RAM) | Loại mô hình khuyến nghị | Kênh giao tiếp chính | Môi trường Sandbox |
|---|---|---|---|---|---|
| **Cá nhân (Lite)** | 1 Người | 1 vCPU / 2GB RAM (Cục bộ hoặc VPS rẻ) | DeepSeek-V4-Flash, GPT-4o-mini | CLI, Telegram | Local Docker |
| **Cá nhân (Chuyên sâu)** | 1 Người | 2 vCPU / 4GB RAM (VPS Cloud) | Claude 3.5 Sonnet, DeepSeek-R1 | Telegram, Web Dashboard | Docker Sandbox (Isolated volume) |
| **Nhóm làm việc (Team)** | 2 - 10 Người | 4 vCPU / 8GB RAM (VPS Cloud) | Mô hình Hybrid (Flash + Reasoning) | Slack, Discord, Web Dashboard | Docker Compose (Cấp quyền read-only socket) |
| **Doanh nghiệp (Enterprise)** | 10 - 50+ Người | 8 vCPU+ / 16GB RAM+ (Cloud Cluster) | Dedicated API Keys / On-Premise LLM | Slack, Web Dashboard, ACP (IDE) | Daytona Sandbox, Singularity, VM riêng biệt |

---

## 2. Các Lưu Ý Về Hạ Tầng Doanh Nghiệp

### A. Cô lập Môi trường thực thi mã (Security Sandbox)
- **Tác vụ nguy hiểm:** Khi Agent thực thi tool `execute_code` hoặc `terminal`, nó có quyền chạy các lệnh hệ thống.
- **Giải pháp:** 
  - Tuyệt đối không cho phép container chạy dưới quyền root trên host VPS.
  - Sử dụng môi trường ảo hóa cô lập hoàn toàn như **Daytona** hoặc chạy mã nguồn trong một container Docker con độc lập, không có quyền truy cập vào file hệ thống của host VPS.

### B. Quản lý tệp khóa (Process Locks) trong môi trường Multi-tenant
- Tránh mount chung thư mục `/opt/data/locks` của nhiều container chạy các gateway khác nhau.
- Mỗi profile hoặc tài khoản doanh nghiệp phải sở hữu một thư mục `HERMES_HOME` độc lập (Ví dụ: `/home/hikari/.hermes/profiles/sales`, `/home/hikari/.hermes/profiles/tech`).
