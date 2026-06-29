---
name: hermes-consulting
description: Hướng dẫn chuyên sâu và phương pháp luận tư vấn triển khai giải pháp Hermes Agent cho cá nhân và doanh nghiệp.
---

# Hermes Agent Solutions Consulting Kit

Bộ skill này hướng dẫn quy trình, phương pháp luận và các công cụ khảo sát chuẩn hóa để tư vấn triển khai Hermes Agent cho khách hàng cá nhân và doanh nghiệp (tương tự quy trình tư vấn giải pháp ERP).

---

## 1. Quy Trình Tư Vấn 5 Bước

### Bước 1: Khảo sát & Xác định yêu cầu (Discovery)
- **Mục tiêu:** Hiểu rõ bài toán nghiệp vụ, luồng công việc hiện tại và các hệ thống dữ liệu doanh nghiệp đang sử dụng.
- **Tài nguyên sử dụng:** [discovery_questionnaire.md](file:///d:/hikari-hermes-agent/.agents/skills/hermes-consulting/resources/discovery_questionnaire.md)

### Bước 2: Phân tích Khả thi & Đánh giá mức độ đáp ứng (Fit-Gap Analysis)
- **Mục tiêu:** Đối chiếu yêu cầu của doanh nghiệp với các tính năng sẵn có của Hermes. Xác định các khoảng trống (gaps) cần phát triển thêm Custom Tool hoặc Skill đặc thù.
- **Lựa chọn Model:** Xác định các mô hình phù hợp với bài toán (ví dụ: DeepSeek-R1 cho lập luận logic phức tạp, DeepSeek-V4-Flash cho tác vụ nhanh/tổng hợp dữ liệu).
- **Tài nguyên sử dụng:** [fit_gap_template.md](file:///d:/hikari-hermes-agent/.agents/skills/hermes-consulting/resources/fit_gap_template.md)

### Bước 3: Thiết kế Kiến trúc (Solution Design)
- **Kiến trúc mạng & Hosting:** Sử dụng container Docker trên VPS Cloud (AWS, GCP, DigitalOcean). Đối với doanh nghiệp, cấu hình môi trường sandbox cô lập hoàn toàn cho agent thực thi mã code (Daytona/Docker Socket).
- **Cấu hình phần cứng:** Lựa chọn dung lượng CPU/RAM phù hợp với tải hệ thống và số lượng người dùng.
- **Tài nguyên sử dụng:** [architecture_matrix.md](file:///d:/hikari-hermes-agent/.agents/skills/hermes-consulting/resources/architecture_matrix.md)

### Bước 4: Thử nghiệm thực tế (Trial & PoC)
- **Mục tiêu:** Triển khai một phiên bản thử nghiệm giới hạn (PoC) sử dụng các API key thử nghiệm.
- **Nội dung kiểm tra:** Đo lường thời gian phản hồi (latency), tỷ lệ thành công của việc gọi tool (tool success rate), và ước tính chi phí token dựa trên thực tế.

### Bước 5: Triển khai & Chuyển giao (Handover & Optimization)
- **Giám sát:** Cấu hình log lỗi tập trung tại `/logs/errors.log`.
- **Tối ưu hóa:** Thiết lập giới hạn quota token trên mỗi session hoặc rate limit để kiểm soát ngân sách. Bàn giao tài liệu vận hành và tập huấn nhân sự.

---

## 2. Quy Tắc Triển Khai Doanh Nghiệp (Enterprise Rules)

- **Quy tắc an toàn dữ liệu:** Tuyệt đối không lưu trữ hoặc in khóa API ra log hệ thống. Mọi khóa cấu hình phải được khai báo qua biến môi trường hoặc file `.env` được phân quyền chặt chẽ (`chmod 600`).
- **Quy tắc cô lập môi trường:** Mọi tác vụ chạy terminal/code trong doanh nghiệp phải được thực thi trong sandbox ảo để bảo vệ hệ thống máy chủ chính khỏi các lệnh nguy hiểm.
