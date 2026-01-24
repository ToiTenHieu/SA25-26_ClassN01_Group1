
# 📚 Hệ thống Quản lý Thư viện Online
## 👨‍💻 Thành viên nhóm

| STT | Họ và tên          | Mã SV            |
|-----|--------------------|----------------------|
| 1   | Nguyễn Trường Sơn  | 23010313          |
| 2   | Nguyễn Đăng Hiếu   |   23010049 |


## 🎯 Mục tiêu hệ thống
Hệ thống hỗ trợ quản lý thư viện trực tuyến:
- Người dùng có thể tìm kiếm, mượn, trả và đánh giá sách.
- Thủ thư quản lý hoạt động mượn/trả, thêm mới sách, cập nhật thông tin sách, xử lý yêu cầu từ người dùng.
- Quản trị viên quản lý toàn bộ hệ thống thư viện, phân quyền cho các thủ thư, theo dõi thống kê.
- Hệ thống cung cấp báo cáo, thống kê và gửi thông báo tự động.

---

## 👥 Các Actor chính
- **Người dùng (User / Độc giả)**
- **Thủ thư(Librarian / Nhân viên quản lý thư viện)**
- **Quản trị viên (Admin)**
- **Hệ thống** (tác nhân phụ trợ: xử lý, gửi thông báo)

---

## 📌 Use Case

### Người dùng (User)
- Đăng ký / Đăng nhập
- Tìm kiếm sách
- Xem danh sách và chi tiết sách
- Mượn sách
- Trả sách
- Gia hạn sách
- Viết đánh giá / nhận xét

### Thủ thư (Librarian)
- Quản lý sách (thêm, cập nhật, xóa)
- Quản lý người dùng (tạo, khóa, mở tài khoản)
- Quản lý phiếu mượn – trả
- Kiểm tra tình trạng sách

### Quản trị viên (Admin)
- Xem báo cáo thống kê (sách mượn nhiều, tồn kho, người dùng vi phạm)
- Quản lý thủ thư (tạo/sửa/xoá tài khoản thủ thư)
- Quản lý hệ thống

---

## ⚙️ Yêu cầu chức năng (Functional Requirements)
- Hệ thống cho phép người dùng đăng ký/đăng nhập tài khoản.
- Người dùng tìm kiếm sách theo tên, tác giả, thể loại.
- Người dùng mượn/trả/gia hạn sách trong thời gian quy định.
- Người dùng có thể viết nhận xét, đánh giá sách.
- Quản trị viên quản lý dữ liệu sách và người dùng.
- Quản trị viên theo dõi phiếu mượn – trả và xuất báo cáo.

---

## 🔒 Yêu cầu phi chức năng (Non-Functional Requirements)
- **Hiệu năng**: Thời gian phản hồi ≤ 2 giây khi tra cứu.
- **Bảo mật**: Mật khẩu mã hóa, phân quyền User/Admin.
- **Khả dụng**: Hoạt động 24/7, downtime < 1%.
- **Thân thiện**: Giao diện dễ sử dụng, hỗ trợ tìm kiếm nhanh.
- **Mở rộng**: Hỗ trợ số lượng lớn sách và người dùng.

---

## 🔗 Mối quan hệ Actor – Use Case

| **Actor**    | **Use Case**                                                                 |
|--------------|------------------------------------------------------------------------------|
| Người dùng   | Đăng ký/Đăng nhập, Tìm kiếm sách, Xem chi tiết, Mượn, Trả, Gia hạn, Đánh giá |
| Quản trị viên| Quản lý sách, Quản lý người dùng, Quản lý mượn – trả, Xem báo cáo           |

---

## 📊 Biểu đồ Use Case (mô tả)
- **Người dùng** ↔ (Đăng ký/Đăng nhập, Tìm kiếm sách, Xem chi tiết, Mượn, Trả, Gia hạn, Đánh giá)  

![Alt text](https://github.com/ToiTenHieu/PTTKPM25-26_N05_Nhom10/blob/main/SRC/Images/A%CC%89nh%20ma%CC%80n%20hi%CC%80nh%202025-09-03%20lu%CC%81c%2020.36.20.png)

- **Admin** ↔ (Quản lý sách, Quản lý người dùng, Quản lý mượn – trả, Xem báo cáo)

![Alt text](https://github.com/ToiTenHieu/PTTKPM25-26_N05_Nhom10/blob/main/SRC/Images/A%CC%89nh%20ma%CC%80n%20hi%CC%80nh%202025-09-03%20lu%CC%81c%2020.37.48.png)
# 📚 Use Case - Quản lý thư viện

## 📘 Use Case 1: Mượn sách

**🎯 Mục tiêu**  
Độc giả mượn thành công sách từ thư viện.  

**👤 Tác nhân chính**  
- Độc giả (hoặc thủ thư nếu hệ thống cho phép mượn qua quầy).  

**⚡ Điều kiện tiên quyết**  
- Độc giả đã đăng nhập vào hệ thống.  
- Sách cần mượn còn trong kho (chưa bị mượn hết).  

**📑 Kịch bản chính (Primary Scenario)**  
1. Độc giả chọn chức năng **"Mượn sách"**.  
2. Hệ thống hiển thị danh sách sách hiện có (tên, mã sách, tác giả, số lượng còn lại).  
3. Độc giả nhập hoặc chọn mã sách muốn mượn.  
4. Hệ thống kiểm tra:  
   - Độc giả có còn hạn thẻ thư viện không.  
   - Độc giả có vi phạm quy định (nợ sách, quá hạn) không.  
   - Sách còn số lượng không.  
5. Nếu hợp lệ, hệ thống ghi nhận giao dịch mượn sách (ngày mượn, ngày phải trả).  
6. Hệ thống trừ đi số lượng sách còn trong kho.  
7. Hệ thống thông báo ✅ **“Mượn sách thành công”**.  

---

## 📕 Use Case 2: Trả sách

**🎯 Mục tiêu**  
Độc giả trả sách đã mượn.  

**👤 Tác nhân chính**  
- Độc giả (hoặc thủ thư).  

**⚡ Điều kiện tiên quyết**  
- Độc giả đã mượn sách trước đó.  

**📑 Kịch bản chính (Primary Scenario)**  
1. Độc giả chọn chức năng **"Trả sách"**.  
2. Hệ thống hiển thị danh sách sách mà độc giả đang mượn.  
3. Độc giả chọn sách cần trả.  
4. Hệ thống cập nhật trạng thái sách là **“đã trả”**.  
5. Hệ thống tăng số lượng sách còn lại trong kho.  
6. Nếu trả đúng hạn → Thông báo ✅ **“Trả sách thành công”**.  
7. Nếu trả trễ hạn → Hệ thống tính phí phạt 💰 và thông báo cho độc giả.  

---

## 📗 Use Case 3: Quản lý sách (Thêm sách mới)

**🎯 Mục tiêu**  
Thủ thư/Quản trị viên thêm sách mới vào hệ thống.  

**👤 Tác nhân chính**  
- Thủ thư / Quản trị viên.  

**⚡ Điều kiện tiên quyết**  
- Người dùng có quyền quản trị.  

**📑 Kịch bản chính (Primary Scenario)**  
1. Thủ thư chọn chức năng **"Thêm sách mới"**.  
2. Hệ thống hiển thị form nhập thông tin sách (mã sách, tên sách, tác giả, thể loại, số lượng, năm xuất bản).  
3. Thủ thư nhập đầy đủ thông tin và xác nhận.  
4. Hệ thống kiểm tra dữ liệu (mã sách có trùng không, số lượng hợp lệ).  
5. Nếu hợp lệ, hệ thống lưu thông tin sách vào cơ sở dữ liệu.  
6. Hệ thống thông báo ✅ **“Thêm sách thành công”**.  
7. Sách mới xuất hiện trong danh mục để độc giả có thể tra cứu/mượn.  


