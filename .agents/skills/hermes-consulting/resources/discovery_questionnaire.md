# Phiếu Khảo Sát & Xác Định Yêu Cầu Triển Khai Hermes Agent

Bảng câu hỏi này được sử dụng trong giai đoạn khảo sát ban đầu (Discovery Phase) để thu thập thông tin thiết kế giải pháp cho khách hàng cá nhân hoặc doanh nghiệp.

---

## 1. Thông Tin Nghiệp Vụ & Bài Toán Cần Giải Quyết

1. **Quy trình nghiệp vụ nào đang tốn nhiều thời gian nhất của bạn/nhân viên?**
   - *Ví dụ:* Tự động quét và phân tích mã lỗi log, tổng hợp dữ liệu báo cáo hàng ngày từ các nguồn Git/Database, hỗ trợ trả lời khách hàng qua chat.
2. **Kỳ vọng lớn nhất đối với việc triển khai AI Agent là gì?**
   - *Ví dụ:* Tiết kiệm thời gian lập trình, tự động hóa 80% tác vụ báo cáo, cải thiện độ chính xác khi phân tích dữ liệu.

---

## 2. Dữ Liệu & Hệ Thống Tích Hợp

1. **Hệ thống dữ liệu hiện tại đang sử dụng là gì?**
   - [ ] Cơ sở dữ liệu (PostgreSQL, MySQL, MongoDB, ...)
   - [ ] Kho chứa mã nguồn (GitHub, GitLab, ...)
   - [ ] Công cụ quản lý công việc (Jira, Trello, Notion, ...)
   - [ ] File lưu trữ nội bộ (Google Drive, Local Files, ...)
2. **Agent có cần quyền đọc/ghi (read/write) vào các hệ thống này hay chỉ đọc?**
3. **Các công cụ/API nội bộ nào của doanh nghiệp cần Agent gọi trực tiếp (Custom Tools)?**
   *(Vui lòng cung cấp tài liệu API hoặc mô tả tham số đầu vào/đầu ra).*

---

## 3. Hạ Tầng & Bảo Mật

1. **Nơi lưu trữ và vận hành Agent mong muốn:**
   - [ ] VPS Cloud (AWS, GCP, DigitalOcean, ...)
   - [ ] Máy chủ vật lý nội bộ (On-Premise) để bảo mật dữ liệu tuyệt đối
   - [ ] Chạy trực tiếp trên máy tính cá nhân (Local)
2. **Yêu cầu bảo mật dữ liệu:**
   - Dữ liệu có chứa thông tin khách hàng nhạy cảm (PII) không?
   - Doanh nghiệp có yêu cầu cô lập hoàn toàn môi trường chạy code (Sandbox) của Agent không?
3. **Kênh tương tác chính mong muốn:**
   - [ ] CLI (Giao diện dòng lệnh dành cho nhà phát triển)
   - [ ] Telegram / Signal (Tiện lợi cho cá nhân/quản trị viên)
   - [ ] Slack / Discord / MS Teams (Kênh làm việc nhóm của doanh nghiệp)
   - [ ] Web Dashboard (Giao diện trực quan trên trình duyệt)

---

## 4. Ngân Sách & Chi Phí

1. **Mức chi phí vận hành API ước tính hàng tháng mong muốn:**
   - [ ] Dưới $50 / tháng (Tận dụng các mô hình nguồn mở hoặc giá rẻ)
   - [ ] $50 - $200 / tháng (Sử dụng kết hợp Claude / OpenAI / DeepSeek chuyên sâu)
   - [ ] Không giới hạn ngân sách (Ưu tiên độ chính xác và chất lượng phản hồi cao nhất)
