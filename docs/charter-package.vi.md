<div class="cover" markdown="1">

# PHẦN MỀM QUẢN LÝ TRUNG TÂM ĐÀO TẠO

<div class="subtitle">Đặc tả yêu cầu &amp; Tuyên bố dự án (Project Charter)</div>

<table>
<tr><td>Dự án</td><td>Xây dựng và triển khai phần mềm quản lý trung tâm đào tạo</td></tr>
<tr><td>Tên sản phẩm</td><td><mark>[tên sản phẩm — sẽ quyết định sau]</mark></td></tr>
<tr><td>Ngân sách</td><td>700.000.000 VNĐ (700 triệu đồng)</td></tr>
<tr><td>Thời gian</td><td>5 tháng — 14/09/2026 đến 05/02/2027</td></tr>
<tr><td>Quy mô nhân sự</td><td>5 người toàn thời gian (1 PM/BA, 3 lập trình viên, 1 kiểm thử)</td></tr>
<tr><td>Khách hàng</td><td>Đỗ Thị Bích Ngọc — chủ sở hữu kiêm giám đốc trung tâm đào tạo</td></tr>
<tr><td>Phiên bản tài liệu</td><td>1.0</td></tr>
<tr><td>Ngày lập</td><td>02/09/2026</td></tr>
</table>

</div>

<p class="note">Phạm vi tài liệu: Phần 1 là đặc tả yêu cầu bản rút gọn; Phần 2 là tuyên bố dự án, trình bày trước theo danh mục thành phần của Bảng 1.1 trong <em>A Project Manager's Book of Forms</em> (ấn bản 3), sau đó theo đúng biểu mẫu PROJECT CHARTER 4 trang. Tên khách hàng và toàn bộ số liệu là giả định cho bài tập học phần, được liệt kê ở mục 1.7.</p>

<div class="pagebreak"></div>

## Phần 1 — Đặc tả yêu cầu (bản rút gọn)

### 1.1 Mô tả sản phẩm

Khách hàng, Đỗ Thị Bích Ngọc, sở hữu và điều hành một trung tâm đào tạo ngoài giờ tư nhân với khoảng 1.200 học viên đang học, 35 giáo viên và 3 cơ sở trong cùng một thành phố. Trung tâm dạy tiếng Anh, toán và kỹ năng tin học theo các khóa cố định từ 24 đến 48 buổi. Hiện nay trung tâm vận hành bằng sổ giấy, bảng tính và nhóm chat: danh sách học viên nằm trong Excel, điểm danh ghi trên phiếu in, công nợ học phí do kế toán theo dõi ở một tệp riêng, phụ huynh được thông báo bằng tin nhắn thủ công. Hệ quả là dữ liệu bị nhập trùng lặp, phòng học và giáo viên bị xếp trùng lịch, học phí thu trễ, và không có bức tranh tin cậy về doanh thu hay tỷ lệ lấp đầy lớp.

Hệ thống (tên sản phẩm <mark>[tên sản phẩm — sẽ quyết định sau]</mark>) là một ứng dụng web thay thế các bảng tính đó bằng một cơ sở dữ liệu dùng chung, bao phủ toàn bộ chu trình vận hành của trung tâm: danh mục khóa học, mở lớp và xếp lịch, ghi danh học viên, điểm danh, học phí và thanh toán, hồ sơ giáo viên và tính lương theo giờ dạy, đánh giá kết quả, thông báo cho phụ huynh, và báo cáo quản trị. Nhân viên trung tâm sử dụng trên trình duyệt máy tính; giáo viên và phụ huynh sử dụng trên trình duyệt điện thoại.

Dự án bàn giao phần mềm, triển khai trên máy chủ đám mây của trung tâm, chuyển đổi dữ liệu học viên và khóa học hiện có, đào tạo nhân sự và bảo hành một tháng sau khi vận hành chính thức.

### 1.2 Phạm vi

**Trong phạm vi**

- Ứng dụng web đáp ứng đa thiết bị, giao diện tiếng Việt, gồm 11 chức năng ở mục 1.4, dùng cho 3 cơ sở hiện có.
- Cơ sở dữ liệu quan hệ là nguồn dữ liệu duy nhất cho học viên, khóa học, lớp, buổi học, điểm danh, hóa đơn, thanh toán và giờ dạy.
- Phân quyền theo vai trò cho 6 nhóm người dùng (mục 1.3).
- Chuyển đổi dữ liệu hiện có từ các tệp Excel của trung tâm: hồ sơ học viên, danh mục khóa học, các lớp đang hoạt động và công nợ học phí còn tồn.
- Gửi thông báo cho phụ huynh và giáo viên qua email và SMS thông qua một nhà cung cấp dịch vụ bên thứ ba.
- Triển khai trên máy chủ ảo đám mây, gồm tên miền, HTTPS và sao lưu tự động hằng đêm.
- Tài liệu hướng dẫn sử dụng, hướng dẫn quản trị và triển khai, đào tạo tại chỗ cho nhân sự trung tâm, bàn giao mã nguồn.
- Bảo hành (sửa lỗi) một tháng sau khi vận hành chính thức.

**Ngoài phạm vi**

- Ứng dụng di động gốc (native) cho iOS hoặc Android. Giao diện web đáp ứng đa thiết bị; không có sản phẩm trên kho ứng dụng.
- Các chức năng dạy học trực tuyến: lớp học video trực tiếp, soạn nội dung bài giảng, hệ thống thi trắc nghiệm, phát học liệu trực tuyến.
- Tích hợp cổng thanh toán trực tuyến hoặc ví điện tử. Hệ thống ghi nhận thanh toán và đối chiếu nội dung chuyển khoản thủ công; không khởi tạo hay xử lý giao dịch thẻ.
- Tích hợp phần mềm kế toán hoặc thuế, kê khai thuế và báo cáo bảo hiểm xã hội. Hệ thống tính số liệu lương theo giờ dạy và kết xuất ra ngoài; kế toán hạch toán ở hệ thống khác.
- Thiết bị điểm danh sinh trắc học hoặc quẹt thẻ, và mọi hạng mục mua sắm phần cứng.
- Vận hành SaaS đa khách hàng cho các trung tâm khác, và hợp nhất cấp chuỗi ngoài 3 cơ sở của khách hàng này.
- Chuyển đổi dữ liệu lịch sử cũ hơn hai kỳ học gần nhất.

### 1.3 Người dùng và vai trò

| Vai trò | Là ai | Sử dụng hệ thống để làm gì |
| --- | --- | --- |
| Giám đốc trung tâm | Chủ sở hữu / nhà tài trợ | Bảng điều khiển, báo cáo doanh thu và tuyển sinh, phê duyệt |
| Quản lý đào tạo | Điều hành hoạt động giảng dạy | Danh mục khóa học, mở lớp, xếp lịch, phân công giáo viên, giám sát đánh giá |
| Nhân viên tư vấn / lễ tân | Quầy tiếp nhận | Hồ sơ học viên, ghi danh, hóa đơn, ghi nhận thanh toán, giải đáp phụ huynh |
| Giáo viên | Đội ngũ giảng dạy | Danh sách lớp, điểm danh, nhập điểm, bảng giờ dạy của bản thân |
| Kế toán | Tài chính | Theo dõi công nợ học phí, xác nhận thanh toán, số liệu lương theo giờ dạy, báo cáo tài chính |
| Học viên / phụ huynh | Khách hàng cuối | Lịch học cá nhân, lịch sử điểm danh và điểm số, số dư học phí, thông báo |
| Quản trị hệ thống | Nhân sự CNTT của trung tâm | Tài khoản, phân quyền, cấu hình, sao lưu, nhật ký truy vết |

### 1.4 Danh sách chức năng

<div class="fnlist" markdown="1">

| Mã | Chức năng | Tác nhân chính | Mô tả |
| --- | --- | --- | --- |
| F01 | Xác thực và phân quyền | Quản trị hệ thống | Tạo tài khoản, đăng nhập bằng tên đăng nhập/mật khẩu, đặt lại mật khẩu, tự đăng xuất khi hết phiên, và phân quyền theo vai trò để mỗi vai trò chỉ thấy màn hình và dữ liệu của mình. Mỗi tài khoản thuộc đúng một vai trò và, với nhân sự, thuộc một hoặc nhiều cơ sở. |
| F02 | Hồ sơ học viên và ghi danh | Nhân viên tư vấn | Lưu hồ sơ học viên (thông tin cá nhân, người giám hộ và liên hệ, nguồn khách, ghi chú) và ghi danh học viên vào lớp đã mở. Hỗ trợ chuyển lớp, bảo lưu, thôi học kèm tính hoàn phí; chặn ghi danh khi lớp đã đủ sĩ số hoặc lịch học trùng với lớp khác của chính học viên đó. |
| F03 | Danh mục khóa học và chương trình | Quản lý đào tạo | Định nghĩa khóa học: mã khóa, trình độ, số buổi, thời lượng mỗi buổi, học phí chuẩn, khóa học tiên quyết và đề cương theo từng buổi. Khóa học được quản lý theo phiên bản để lớp đã mở trước đó giữ nguyên định nghĩa tại thời điểm mở. |
| F04 | Mở lớp, xếp lịch và phân công | Quản lý đào tạo | Mở lớp từ một khóa học (cơ sở, ngày khai giảng, khung giờ trong tuần, sĩ số tối đa), sinh toàn bộ lịch buổi học, gán phòng và giáo viên cho từng buổi. Phát hiện và chặn trùng lịch phòng, giáo viên và lớp; hỗ trợ hoãn buổi và xếp lại lịch kèm tính lại lịch tự động. |
| F05 | Điểm danh và học bù | Giáo viên | Ghi nhận từng học viên trong buổi học là có mặt, vắng có phép, vắng không phép hoặc đi muộn, kèm ghi chú. Hỗ trợ đăng ký buổi học bù ở lớp khác cho học viên vắng và hiển thị tỷ lệ chuyên cần theo học viên và theo lớp. |
| F06 | Học phí, hóa đơn và công nợ | Nhân viên tư vấn / kế toán | Sinh hóa đơn học phí khi ghi danh dựa trên học phí khóa học, áp dụng chính sách ưu đãi (anh chị em, đóng sớm, giới thiệu, mã khuyến mãi) và kế hoạch trả góp. Ghi nhận thanh toán tiền mặt và chuyển khoản theo hóa đơn, in phiếu thu, duy trì số dư còn nợ và danh sách công nợ theo tuổi nợ cho từng học viên, lớp và cơ sở. |
| F07 | Hồ sơ giáo viên và lương theo giờ dạy | Kế toán | Quản lý hồ sơ giáo viên, bằng cấp, loại hợp đồng và đơn giá giờ dạy theo trình độ khóa học. Tổng hợp các buổi đã dạy từ F05 thành bảng giờ dạy hằng tháng cho từng giáo viên, áp dụng phụ cấp và khấu trừ, kết xuất số liệu lương ra Excel cho kế toán. |
| F08 | Đánh giá và báo cáo kết quả học tập | Giáo viên | Nhập điểm cho các đầu điểm do khóa học quy định (kiểm tra, giữa kỳ, cuối kỳ, điểm kỹ năng) và nhận xét từng học viên. Tính kết quả cuối khóa và đạt/không đạt theo quy tắc của khóa học, in phiếu kết quả cho từng học viên và bảng tổng hợp kết quả theo lớp. |
| F09 | Thông báo cho phụ huynh và giáo viên | Nhân viên tư vấn | Gửi email và SMS theo mẫu cho các sự kiện quan trọng: xác nhận ghi danh, nhắc buổi học, cảnh báo vắng mặt, nhắc học phí đến hạn và quá hạn, thay đổi lịch học, công bố kết quả. Hỗ trợ gửi thủ công cho nhóm được chọn, gửi tự động theo lịch, và nhật ký mọi tin nhắn kèm trạng thái gửi. |
| F10 | Báo cáo và bảng điều khiển quản trị | Giám đốc trung tâm | Cung cấp góc nhìn quản trị: doanh thu và tình hình thu theo kỳ và theo cơ sở, công nợ tồn, số học viên mới và tái tục, tỷ lệ lấp đầy lớp, tải giảng dạy và giờ dạy của giáo viên, tỷ lệ chuyên cần. Mọi báo cáo lọc được theo kỳ, cơ sở, khóa học và kết xuất ra Excel, PDF. |
| F11 | Quản trị hệ thống và truy vết | Quản trị hệ thống | Quản lý dữ liệu danh mục và cấu hình của trung tâm (cơ sở, phòng học, kỳ học, chính sách học phí và ưu đãi, mẫu thông báo, ngày nghỉ lễ), thực hiện và phục hồi sao lưu, ghi nhật ký truy vết mọi thao tác thêm, sửa, xóa trên dữ liệu tài chính và học viên kèm người thực hiện và thời điểm. |

</div>

### 1.5 Yêu cầu phi chức năng

| Mã | Nhóm | Yêu cầu |
| --- | --- | --- |
| N01 | Hiệu năng | Mọi màn hình phản hồi trong 3 giây với 50 người dùng đồng thời; báo cáo trong một kỳ học sinh ra trong 10 giây. |
| N02 | Sức chứa | Hệ thống lưu tối thiểu 5.000 hồ sơ học viên, 200 lớp mỗi kỳ và lịch sử 3 năm buổi học mà không cần thiết kế lại. |
| N03 | An toàn thông tin | Chỉ dùng HTTPS; mật khẩu lưu dạng băm một chiều có muối; kiểm tra quyền phía máy chủ cho mọi yêu cầu; dữ liệu cá nhân học viên xử lý theo Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân. |
| N04 | Truy vết | Thao tác thêm, sửa, xóa trên dữ liệu tài chính và học viên được ghi vào nhật ký không sửa được, lưu tối thiểu 3 năm. |
| N05 | Tính sẵn sàng | Sẵn sàng 99% trong khung 07:00–22:00; sao lưu tự động hằng đêm với RPO 24 giờ và RTO 4 giờ. |
| N06 | Tính dễ dùng | Giao diện tiếng Việt; các tác vụ hằng ngày (điểm danh, thu học phí, ghi danh) thao tác được trong tối đa 3 lần bấm từ màn hình chính; nhân viên dùng được sau nửa ngày đào tạo. |
| N07 | Tương thích | Hai phiên bản mới nhất của Chrome, Edge, Firefox trên máy tính; bố cục đáp ứng dùng được trên máy tính bảng và trên điện thoại cho màn hình giáo viên và phụ huynh. |
| N08 | Khả năng bảo trì | Kiến trúc phân lớp, tuân thủ quy ước lập trình, bàn giao tài liệu triển khai và mô tả lược đồ cơ sở dữ liệu kèm mã nguồn. |

### 1.6 Hướng tiếp cận kỹ thuật

Hệ thống được xây dựng dưới dạng ứng dụng web với kiến trúc phân lớp phía máy chủ và cơ sở dữ liệu quan hệ, triển khai gồm một máy chủ ứng dụng và một máy chủ cơ sở dữ liệu trên một máy chủ ảo đám mây, kèm một môi trường thứ hai dành cho kiểm thử và UAT. Phương pháp bàn giao theo lặp: hai vòng lặp xây dựng dài 4–5 tuần, mỗi vòng kết thúc bằng buổi demo cho khách hàng, sau đó là kiểm thử chấp nhận người dùng trên toàn hệ thống. Yêu cầu được chốt đường cơ sở khi kết thúc giai đoạn phân tích; thay đổi sau đó đi qua quy trình quản lý thay đổi nêu trong tuyên bố dự án.

### 1.7 Giả định và ràng buộc

**Ràng buộc**

- Ngân sách cố định 700.000.000 VNĐ, bao gồm phần mềm, triển khai, đào tạo và bảo hành.
- Thời gian cố định 5 tháng, từ 14/09/2026 đến 05/02/2027, bắt buộc vận hành chính thức trước kỳ nghỉ Tết Nguyên đán.
- Nhân sự gồm 5 người toàn thời gian; không bổ sung thêm người.
- Hệ thống phải dùng tiếng Việt và chạy trong ngân sách hạ tầng hiện có của khách hàng là một máy chủ ảo.

**Giả định**

- Trung tâm của khách hàng (1.200 học viên, 35 giáo viên, 3 cơ sở) và toàn bộ số liệu trong tài liệu này là giả định cho bài tập học phần; không sử dụng dữ liệu khách hàng thật.
- Tên thương mại của sản phẩm chưa được quyết định; mọi vị trí cần tên sản phẩm đều được tô nền vàng và sẽ điền ở phiên bản sau của tài liệu.
- Quản lý đào tạo và kế toán dành tối thiểu 4 giờ mỗi tuần cho các buổi làm việc lấy yêu cầu, demo và UAT.
- Các tệp Excel hiện có của trung tâm dùng được làm nguồn chuyển đổi và được trung tâm làm sạch trước khi chuyển đổi.
- Trung tâm cung cấp và chi trả một tài khoản dịch vụ SMS/email; API của dịch vụ ổn định và có tài liệu.
- Quy tắc nghiệp vụ về ưu đãi và hoàn phí được chốt trong giai đoạn phân tích và đóng băng tại mốc phê duyệt yêu cầu.
- Ngoài kỳ nghỉ Tết Nguyên đán tháng 02/2027, không có ngày lễ nào ảnh hưởng đáng kể đến tiến độ.

<div class="pagebreak"></div>

## Phần 2 — Tuyên bố dự án (Project Charter)

### 2A. Các thành phần của tuyên bố dự án (theo Bảng 1.1 — Book of Forms)

#### Mục đích dự án (Project purpose)

Cách vận hành thủ công dựa trên giấy tờ và bảng tính khiến trung tâm tốn khoảng 60 giờ công mỗi tháng cho việc nhập trùng dữ liệu, thường xuyên xếp trùng phòng học và giáo viên, và để khoảng 8% học phí thu quá hạn vì không ai có danh sách công nợ đáng tin cậy. Dự án được thực hiện để loại bỏ tổn thất vận hành đó và cung cấp cho giám đốc một góc nhìn duy nhất, cập nhật về tuyển sinh, doanh thu và năng lực giảng dạy trên cả 3 cơ sở, phục vụ kế hoạch mở cơ sở thứ tư trong năm 2027.

#### Mô tả tổng quan dự án (High-level project description)

Phân tích, thiết kế, lập trình, kiểm thử và triển khai một ứng dụng web tiếng Việt quản lý toàn bộ chu trình vận hành của trung tâm — khóa học, mở lớp và xếp lịch, học viên và ghi danh, điểm danh, học phí và thanh toán, giáo viên và lương theo giờ dạy, đánh giá kết quả, thông báo cho phụ huynh, báo cáo quản trị — kèm chuyển đổi dữ liệu từ các tệp Excel hiện có, đào tạo nhân sự và bảo hành một tháng sau vận hành chính thức. Bàn giao theo lặp, gồm hai vòng lặp xây dựng và một giai đoạn UAT, do 5 nhân sự thực hiện trong 5 tháng với 700 triệu đồng.

#### Ranh giới dự án (Project boundaries)

Bao gồm: 11 chức năng F01–F11 ở mục 1.4 cho 3 cơ sở hiện có, chuyển đổi dữ liệu hai kỳ học gần nhất, triển khai trên một máy chủ ảo đám mây, đào tạo, tài liệu và bảo hành một tháng.

Không bao gồm: ứng dụng di động gốc; dạy học trực tuyến, video và học liệu điện tử; tích hợp cổng thanh toán hoặc ví điện tử; tích hợp kế toán, thuế và bảo hiểm xã hội; thiết bị điểm danh và mọi hạng mục mua sắm phần cứng; vận hành đa khách hàng cho trung tâm khác; dữ liệu lịch sử cũ hơn hai kỳ học.

Dự án kết thúc tại cuộc họp tổng kết sau tháng bảo hành; việc vận hành và thuê hạ tầng về sau thuộc trách nhiệm của trung tâm.

#### Sản phẩm bàn giao chính (Key deliverables)

| # | Sản phẩm bàn giao | Bàn giao tại |
| --- | --- | --- |
| D1 | Tài liệu đặc tả yêu cầu phần mềm đã phê duyệt và chốt đường cơ sở | M1 |
| D2 | Đường cơ sở thiết kế: kiến trúc, lược đồ cơ sở dữ liệu, thiết kế giao diện | M2 |
| D3 | Bản phát hành vòng lặp 1: F01–F05 (phân quyền, học viên, khóa học, xếp lịch, điểm danh) | M3 |
| D4 | Bản phát hành vòng lặp 2: F06–F11 (học phí, lương giờ dạy, đánh giá, thông báo, báo cáo, quản trị) | M4 |
| D5 | Tài liệu kiểm thử: kế hoạch, ca kiểm thử, nhật ký lỗi, báo cáo tổng kết kiểm thử | M5 |
| D6 | Dữ liệu vận hành đã chuyển đổi và đối chiếu với tệp nguồn | M6 |
| D7 | Triển khai môi trường vận hành trên máy chủ đám mây, đã cấu hình sao lưu | M6 |
| D8 | Hướng dẫn sử dụng, hướng dẫn quản trị và triển khai, nhân sự đã được đào tạo (biên bản đào tạo) | M6 |
| D9 | Bàn giao mã nguồn, script cơ sở dữ liệu và tài liệu kỹ thuật | M6 |
| D10 | Kết thúc bảo hành, báo cáo tổng kết và bài học kinh nghiệm | M7 |

#### Yêu cầu mức cao (High-level requirements)

- Hệ thống quản lý 11 nhóm chức năng F01–F11 ở mục 1.4 trên một cơ sở dữ liệu thống nhất, không nhập lại cùng một dữ liệu ở hai nơi.
- Trùng lịch phòng học, giáo viên và lịch học viên được phát hiện và chặn ngay khi tạo hoặc dời lớp, buổi học.
- Hóa đơn học phí sinh ra từ học phí khóa học và chính sách ưu đãi; công nợ tồn xem được theo học viên, lớp và cơ sở tại mọi thời điểm.
- Giờ dạy được suy ra từ dữ liệu điểm danh đã ghi nhận, không nhập tay, và kết xuất được để tính lương.
- Phụ huynh và giáo viên được thông báo tự động về nhắc lịch, vắng mặt, học phí đến hạn và kết quả, kèm nhật ký gửi.
- Mỗi vai trò trong 6 vai trò chỉ thấy dữ liệu và màn hình thuộc quyền của mình; mọi thay đổi dữ liệu tài chính và học viên đều truy vết được.
- Giao diện tiếng Việt, nhân viên hiện tại dùng được sau nửa ngày đào tạo.
- Đáp ứng các yêu cầu phi chức năng N01–N08 ở mục 1.5.

#### Mức rủi ro tổng thể (Overall project risk)

Rủi ro tổng thể ở mức **Trung bình**. Công nghệ đã quen thuộc và nghiệp vụ ổn định, nhưng cả ngân sách lẫn ngày vận hành chính thức đều cố định, đội dự án nhỏ tới mức mất một lập trình viên là đường găng bị đẩy lùi, và những người nắm quy tắc nghiệp vụ phía khách hàng chỉ tham gia bán thời gian. Bất định lớn nhất là sự thay đổi chính sách học phí, ưu đãi và hoàn phí — vốn là quyết định quản trị của trung tâm chứ không phải vấn đề kỹ thuật. Rủi ro thứ hai là dịch vụ thông báo của bên thứ ba nằm ngoài tầm kiểm soát của dự án. Kỳ nghỉ Tết Nguyên đán tháng 02/2027 làm mất toàn bộ dự phòng tiến độ sau ngày vận hành chính thức.

| # | Rủi ro chính | Ứng phó |
| --- | --- | --- |
| R1 | Quy tắc học phí, ưu đãi, hoàn phí thay đổi sau khi chốt yêu cầu | Đóng băng quy tắc tại M1 kèm ký duyệt bằng văn bản; thay đổi sau đó đi qua quy trình quản lý thay đổi, dùng quỹ dự phòng 70 triệu đồng |
| R2 | Nhân sự khách hàng không bố trí được thời gian cho workshop, demo và UAT | Thống nhất khung giờ cố định hằng tuần với nhà tài trợ ngay tại khởi động; báo cáo nhà tài trợ trong 2 ngày làm việc nếu bỏ lỡ |
| R3 | Mất hoặc vắng một lập trình viên trong đội 5 người | Làm cặp ở module xếp lịch và học phí; mã nguồn và tài liệu để trên kho dùng chung; thay người trong 2 tuần với phê duyệt của nhà tài trợ |
| R4 | Dịch vụ SMS/email bên thứ ba không ổn định hoặc chi phí phát sinh | Cô lập dịch vụ sau một lớp giao tiếp duy nhất; làm thử nghiệm khả thi trước M2; giữ một nhà cung cấp dự phòng |
| R5 | Dữ liệu Excel nguồn quá bẩn để chuyển đổi | Đánh giá chất lượng dữ liệu tại M1; trung tâm làm sạch tệp trước M5; giới hạn chuyển đổi trong hai kỳ học gần nhất |
| R6 | Bài toán xếp lịch và phát hiện trùng phức tạp hơn ước lượng | Làm F04 sớm nhất trong vòng lặp 1; khống chế thời gian và soát lại tại buổi demo M3 |
| R7 | Vận hành chính thức trượt qua kỳ nghỉ Tết | Triển khai tại M6, trước kỳ nghỉ một tuần; nếu trượt qua kỳ nghỉ thì go-live chậm 3 tuần và phải báo cáo nhà tài trợ ngay |

#### Mục tiêu dự án và tiêu chí thành công (Project objectives and success criteria)

| Khía cạnh | Mục tiêu | Tiêu chí thành công |
| --- | --- | --- |
| Phạm vi | Bàn giao 11 chức năng F01–F11 và 10 sản phẩm D1–D10 | 100% F01–F11 được chấp nhận trong UAT; cả 10 sản phẩm được nhà tài trợ ký duyệt |
| Thời gian | Vận hành chính thức trước 29/01/2027 và kết thúc dự án trước 05/02/2027 | Go-live vào hoặc trước 29/01/2027; không mốc nào hoàn thành trễ quá 1 tuần |
| Chi phí | Hoàn thành trong 700.000.000 VNĐ | Chi phí cuối ≤ 700 triệu đồng; sai lệch chi phí tại mỗi cổng kiểm soát trong khoảng ±5% so với đường cơ sở |
| Chất lượng | Bàn giao hệ thống dùng được cho vận hành hằng ngày | ≥ 95% ca kiểm thử UAT đạt; không còn lỗi mức Nghiêm trọng hoặc Cao tại thời điểm go-live; tối đa 5 lỗi mức Trung bình còn mở, mỗi lỗi có hạn sửa đã thống nhất |
| Sự hài lòng của bên liên quan | Nhân sự trung tâm vận hành được trên hệ thống | ≥ 80% trong 25 người dùng nghiệp vụ được đào tạo và sử dụng thực tế trong tháng đầu; điểm hài lòng trung bình ≥ 4/5 trong khảo sát tổng kết; ≥ 90% số lớp có điểm danh trên hệ thống trong tháng bảo hành |

#### Lịch mốc tóm tắt (Summary milestone schedule)

| Mã | Mốc | Ngày hoàn thành |
| --- | --- | --- |
| M0 | Khởi động dự án, phê duyệt tuyên bố dự án | 14/09/2026 |
| M1 | Phê duyệt và chốt đường cơ sở đặc tả yêu cầu | 02/10/2026 |
| M2 | Phê duyệt đường cơ sở thiết kế (kiến trúc, cơ sở dữ liệu, giao diện) | 23/10/2026 |
| M3 | Nghiệm thu demo vòng lặp 1 (F01–F05) | 20/11/2026 |
| M4 | Nghiệm thu vòng lặp 2 — hoàn thành chức năng (F06–F11) | 25/12/2026 |
| M5 | Hoàn tất kiểm thử hệ thống, đạt điều kiện vào UAT | 15/01/2027 |
| M6 | Ký duyệt UAT, chuyển đổi dữ liệu, vận hành chính thức và bàn giao | 29/01/2027 |
| M7 | Kết thúc bảo hành, tổng kết dự án | 05/02/2027 |

#### Nguồn tài chính đã phê duyệt (Preapproved financial resources)

Tổng kinh phí đã phê duyệt là **700.000.000 VNĐ**, do trung tâm cấp từ ngân sách đầu tư 2026–2027, giải ngân theo 4 đợt gắn với nghiệm thu mốc: 20% tại M0, 25% tại M3, 30% tại M4, 25% tại M6.

| # | Khoản mục | Số tiền (VNĐ) | Tỷ trọng | Căn cứ |
| --- | --- | --- | --- | --- |
| 1 | Nhân sự — 5 người × 5 tháng = 25 người-tháng | 490.000.000 | 70% | 19,6 triệu đồng/người-tháng, đã gồm chi phí gián tiếp |
| 2 | Hạ tầng và bản quyền | 70.000.000 | 10% | Máy chủ vận hành và môi trường kiểm thử 12 tháng, tên miền, SSL, cước dịch vụ SMS/email, công cụ phát triển |
| 3 | Triển khai, chuyển đổi dữ liệu, đào tạo, tài liệu | 70.000.000 | 10% | Công tác tại chỗ ở 3 cơ sở, tài liệu đào tạo, chi phí in ấn |
| 4 | Quỹ dự phòng quản lý | 70.000.000 | 10% | Do giám đốc dự án nắm giữ để xử lý các rủi ro R1–R7 |
| | **Tổng cộng** | **700.000.000** | **100%** | |

#### Danh sách bên liên quan chính (Key stakeholder list)

| Bên liên quan | Vai trò trong dự án |
| --- | --- |
| Giám đốc trung tâm | Nhà tài trợ: cấp kinh phí, phê duyệt tuyên bố dự án, phê duyệt thay đổi phạm vi và nghiệm thu cuối |
| Quản lý đào tạo | Chủ nghiệp vụ khóa học, lớp, xếp lịch, đánh giá; nguồn yêu cầu chính và trưởng nhóm UAT |
| Kế toán | Chủ nghiệp vụ học phí, công nợ và lương theo giờ dạy; tham gia UAT |
| Trưởng bộ phận tư vấn / lễ tân | Chủ nghiệp vụ ghi danh và ghi nhận thanh toán; đại diện người dùng hằng ngày |
| Đại diện giáo viên (tổ trưởng chuyên môn) | Đại diện 35 giáo viên cho các màn hình điểm danh, điểm số và giờ dạy |
| Học viên và phụ huynh | Người dùng cuối của lịch học, kết quả và học phí; người nhận thông báo |
| Quản trị CNTT của trung tâm | Tiếp nhận hệ thống khi bàn giao; vận hành tài khoản, sao lưu và hạ tầng về sau |
| Giám đốc dự án | Lập kế hoạch, thực thi và kiểm soát dự án; đầu mối duy nhất làm việc với nhà tài trợ |
| Đội dự án (3 lập trình viên, 1 kiểm thử) | Phân tích, thiết kế, lập trình, kiểm thử, triển khai và viết tài liệu |
| Nhà cung cấp dịch vụ SMS/email | Nhà cung cấp bên ngoài cho kênh thông báo |
| Nhà cung cấp hạ tầng đám mây | Nhà cung cấp bên ngoài cho môi trường vận hành và kiểm thử |

#### Tiêu chí kết thúc dự án (Project exit criteria)

Dự án được đóng khi thỏa mãn tất cả các điều kiện sau:

1. Toàn bộ sản phẩm D1–D10 được nhà tài trợ chấp nhận bằng văn bản.
2. UAT được ký duyệt với ≥ 95% ca kiểm thử đạt và không còn lỗi mức Nghiêm trọng hoặc Cao.
3. Hệ thống chạy trên môi trường vận hành của trung tâm, sao lưu được kiểm chứng bằng một lần phục hồi thử thành công.
4. Dữ liệu vận hành đã chuyển đổi và đối chiếu với tệp nguồn, các sai lệch được kế toán chấp nhận bằng văn bản.
5. Tối thiểu 80% trong 25 người dùng nghiệp vụ đã được đào tạo, có biên bản đào tạo.
6. Mã nguồn, script cơ sở dữ liệu, hướng dẫn sử dụng và hướng dẫn quản trị đã bàn giao và được xác nhận.
7. Thời hạn bảo hành một tháng kết thúc, không còn lỗi mức Nghiêm trọng hoặc Cao.
8. Báo cáo tổng kết, bài học kinh nghiệm và quyết toán tài chính được phê duyệt, hóa đơn cuối cùng đã thanh toán.

Dự án cũng có thể kết thúc sớm theo quyết định của nhà tài trợ nếu kinh phí bị rút hoặc nhu cầu nghiệp vụ không còn; khi đó các sản phẩm đã hoàn thành được bàn giao và dự án đóng lại kèm báo cáo chấm dứt.

#### Giám đốc dự án được chỉ định, trách nhiệm và mức thẩm quyền

**Giám đốc dự án:** Nguyễn Văn A, chỉ định toàn thời gian trong suốt 5 tháng.

**Trách nhiệm:** lập kế hoạch, thực thi, giám sát và kết thúc dự án; quản lý phạm vi, tiến độ, chi phí, chất lượng, rủi ro và truyền thông; dẫn dắt đội 5 người; là đầu mối duy nhất với nhà tài trợ và nhân sự trung tâm; báo cáo trạng thái hằng tuần.

**Quyết định nhân sự:** được phân công và điều chuyển công việc trong đội 5 người đã duyệt, duyệt nghỉ phép và quản lý hiệu suất hằng ngày. Được đề nghị thay thế thành viên; quyết định tuyển dụng, chấm dứt và các vấn đề hợp đồng lao động thuộc quản lý trực tuyến của nhà thầu và phải thông báo cho nhà tài trợ.

**Quản lý ngân sách và sai lệch:** được cam kết và chi tiêu trong đường cơ sở đã duyệt, gồm từng giao dịch đơn lẻ tới 20.000.000 VNĐ và sử dụng quỹ dự phòng 70.000.000 VNĐ cho các rủi ro R1–R7. Tự quản lý sai lệch chi phí lũy kế tới 5% đường cơ sở; mọi dự báo vượt quá 5%, mọi lần dùng quỹ dự phòng vượt 40.000.000 VNĐ và mọi thay đổi tổng kinh phí phải trình nhà tài trợ phê duyệt.

**Quyết định kỹ thuật:** toàn quyền về kiến trúc, nền tảng công nghệ, thiết kế cơ sở dữ liệu, quy ước lập trình và cách thức triển khai nội bộ, với điều kiện đáp ứng các yêu cầu phi chức năng N01–N08 và các sản phẩm đã thống nhất. Thay đổi ảnh hưởng đến phạm vi người dùng nhìn thấy, tiến độ hoặc chi phí phải qua quy trình quản lý thay đổi và được nhà tài trợ phê duyệt.

**Giải quyết xung đột:** xử lý xung đột trong nội bộ đội dự án và giữa đội dự án với nhân sự vận hành của trung tâm. Xung đột vượt ranh giới tổ chức, làm thay đổi phạm vi đã thống nhất, hoặc chưa giải quyết được sau 5 ngày làm việc thì trình nhà tài trợ; quyết định của nhà tài trợ là quyết định cuối cùng.

#### Tên và thẩm quyền của nhà tài trợ

**Nhà tài trợ:** Đỗ Thị Bích Ngọc, chủ sở hữu kiêm Giám đốc trung tâm đào tạo.

Nhà tài trợ phê chuẩn dự án và bản tuyên bố dự án này, cấp và giải ngân 700 triệu đồng kinh phí, chỉ định giám đốc dự án và bố trí nhân sự trung tâm tham gia. Nhà tài trợ phê duyệt các thay đổi về phạm vi, tiến độ và ngân sách vượt thẩm quyền của giám đốc dự án, ấn định mức sai lệch chấp nhận được, giải quyết xung đột được trình lên và xung đột giữa các bộ phận, nghiệm thu sản phẩm, cho phép vận hành chính thức và đóng dự án, đồng thời bảo trợ dự án trước nhân sự trung tâm và các trưởng cơ sở.

### 2B. Biểu mẫu tuyên bố dự án (PROJECT CHARTER)

<div class="formpage">

<div class="form-title">Project Charter — Tuyên bố dự án</div>

<table class="form">
<tr><td class="label">Project Title:<br>Tên dự án</td><td>Xây dựng và triển khai phần mềm quản lý trung tâm đào tạo — tên sản phẩm <mark>[tên sản phẩm — sẽ quyết định sau]</mark></td><td class="label">Date Prepared:<br>Ngày lập</td><td>02/09/2026</td></tr>
<tr><td class="label">Project Sponsor:<br>Nhà tài trợ</td><td>Đỗ Thị Bích Ngọc — chủ sở hữu kiêm Giám đốc trung tâm</td><td class="label">Project Customer:<br>Khách hàng</td><td>Đỗ Thị Bích Ngọc — trung tâm đào tạo (3 cơ sở, 1.200 học viên, 35 giáo viên)</td></tr>
<tr><td class="label">Project Manager:<br>Giám đốc dự án</td><td colspan="3">Nguyễn Văn A — chỉ định toàn thời gian trong suốt 5 tháng thực hiện</td></tr>
</table>

<table class="form">
<tr><td class="label">Project Purpose:<br>Mục đích dự án</td><td>Trung tâm đang vận hành bằng giấy tờ và bảng tính, tốn khoảng 60 giờ công mỗi tháng để nhập trùng dữ liệu, thường xuyên xếp trùng phòng và giáo viên, và để khoảng 8% học phí thu quá hạn. Dự án loại bỏ tổn thất vận hành đó và cung cấp cho giám đốc một góc nhìn duy nhất, cập nhật về tuyển sinh, doanh thu và năng lực giảng dạy trên cả 3 cơ sở, phục vụ kế hoạch mở cơ sở thứ tư năm 2027.</td></tr>

<tr><td class="label">High-Level Project Description:<br>Mô tả tổng quan</td><td>Phân tích, thiết kế, lập trình, kiểm thử và triển khai ứng dụng web tiếng Việt quản lý toàn bộ chu trình vận hành của trung tâm — khóa học, mở lớp và xếp lịch, học viên và ghi danh, điểm danh, học phí và thanh toán, giáo viên và lương theo giờ dạy, đánh giá, thông báo, báo cáo quản trị — kèm chuyển đổi dữ liệu từ Excel hiện có, đào tạo và bảo hành một tháng. Bàn giao theo lặp: hai vòng lặp xây dựng và một giai đoạn UAT, 5 nhân sự, 5 tháng, 700 triệu đồng.</td></tr>

<tr><td class="label">Project Boundaries:<br>Ranh giới dự án</td><td><strong>Bao gồm:</strong> chức năng F01–F11 cho 3 cơ sở hiện có; chuyển đổi dữ liệu hai kỳ gần nhất; triển khai trên một máy chủ ảo đám mây; đào tạo; tài liệu; bảo hành một tháng.<br><br><strong>Không bao gồm:</strong> ứng dụng di động gốc; dạy học trực tuyến, video, học liệu điện tử; cổng thanh toán hoặc ví điện tử; tích hợp kế toán, thuế, bảo hiểm xã hội; thiết bị điểm danh và mua sắm phần cứng; vận hành cho trung tâm khác; dữ liệu cũ hơn hai kỳ học.<br><br>Dự án kết thúc tại cuộc họp tổng kết sau tháng bảo hành; vận hành và hạ tầng về sau do trung tâm đảm nhiệm.</td></tr>

<tr><td class="label">Key Deliverables:<br>Sản phẩm bàn giao chính</td><td>D1 Đặc tả yêu cầu đã phê duyệt · D2 Đường cơ sở thiết kế (kiến trúc, cơ sở dữ liệu, giao diện) · D3 Bản phát hành vòng lặp 1 (F01–F05) · D4 Bản phát hành vòng lặp 2 (F06–F11) · D5 Tài liệu và báo cáo tổng kết kiểm thử · D6 Dữ liệu vận hành đã chuyển đổi và đối chiếu · D7 Triển khai vận hành kèm sao lưu · D8 Hướng dẫn sử dụng, hướng dẫn quản trị và nhân sự đã đào tạo · D9 Mã nguồn, script cơ sở dữ liệu, tài liệu kỹ thuật · D10 Báo cáo tổng kết và bài học kinh nghiệm</td></tr>

<tr><td class="label">High-Level Requirements:<br>Yêu cầu mức cao</td><td>Một cơ sở dữ liệu thống nhất, không nhập trùng dữ liệu giữa 11 nhóm chức năng · Chặn trùng lịch phòng, giáo viên và học viên ngay khi tạo lớp, buổi học · Hóa đơn học phí sinh từ học phí khóa học và chính sách ưu đãi, công nợ xem được theo học viên, lớp, cơ sở · Giờ dạy suy ra từ dữ liệu điểm danh và kết xuất được để tính lương · Thông báo tự động về nhắc lịch, vắng mặt, học phí đến hạn và kết quả kèm nhật ký gửi · Phân quyền cho 6 vai trò và truy vết mọi thay đổi dữ liệu tài chính, học viên · Giao diện tiếng Việt dùng được sau nửa ngày đào tạo · Yêu cầu phi chức năng N01–N08 (hiệu năng, sức chứa, an toàn, truy vết, sẵn sàng, dễ dùng, tương thích, bảo trì)</td></tr>

<tr><td class="label">Overall Project Risk:<br>Rủi ro tổng thể</td><td><strong>Trung bình.</strong> Công nghệ và nghiệp vụ đã quen thuộc, nhưng ngân sách và ngày go-live đều cố định, kỳ nghỉ Tết tháng 02/2027 làm mất dự phòng tiến độ. Đội 5 người nhỏ tới mức mất một lập trình viên là đường găng bị đẩy lùi; người nắm quy tắc nghiệp vụ phía khách hàng chỉ tham gia bán thời gian. Bất định lớn nhất: chính sách học phí, ưu đãi và hoàn phí thay đổi. Rủi ro R1–R7 đã nhận diện kèm ứng phó và có quỹ dự phòng 70 triệu đồng.</td></tr>
</table>

<div class="page-of">Page 1 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter — Tuyên bố dự án</div>

<table class="form">
<tr><th style="width:14%">&nbsp;</th><th style="width:43%">Project Objectives — Mục tiêu</th><th style="width:43%">Success Criteria — Tiêu chí thành công</th></tr>

<tr><td class="label">Scope:<br>Phạm vi</td><td>Bàn giao 11 chức năng F01–F11 và 10 sản phẩm D1–D10 cho 3 cơ sở.</td><td>100% F01–F11 được chấp nhận trong UAT; cả 10 sản phẩm được nhà tài trợ ký duyệt; không chức năng nào bị hoãn nếu không có yêu cầu thay đổi đã duyệt.</td></tr>

<tr><td class="label">Time:<br>Thời gian</td><td>Vận hành chính thức trước 29/01/2027 và đóng dự án trước 05/02/2027, trong khung 5 tháng kể từ 14/09/2026.</td><td>Go-live vào hoặc trước 29/01/2027; không mốc M1–M7 nào hoàn thành trễ quá 1 tuần so với đường cơ sở.</td></tr>

<tr><td class="label">Cost:<br>Chi phí</td><td>Hoàn thành toàn bộ phạm vi trong 700.000.000 VNĐ đã phê duyệt, gồm phần mềm, triển khai, đào tạo và bảo hành.</td><td>Chi phí cuối ≤ 700.000.000 VNĐ; sai lệch tại mỗi cổng kiểm soát trong ±5% đường cơ sở; báo cáo mức sử dụng quỹ dự phòng hằng tháng.</td></tr>

<tr><td class="label">Other:<br>Khác</td><td><strong>Chất lượng:</strong> hệ thống dùng được cho vận hành hằng ngày ngay từ đầu.<br><br><strong>Sự hài lòng:</strong> nhân sự trung tâm vận hành hằng ngày trên hệ thống thay vì trên bảng tính.</td><td>≥ 95% ca kiểm thử UAT đạt; không còn lỗi Nghiêm trọng/Cao khi go-live; tối đa 5 lỗi Trung bình còn mở, mỗi lỗi có hạn sửa đã thống nhất.<br><br>≥ 80% trong 25 người dùng nghiệp vụ được đào tạo và sử dụng trong tháng đầu; điểm hài lòng trung bình ≥ 4/5; ≥ 90% số lớp có điểm danh trên hệ thống trong tháng bảo hành.</td></tr>
</table>

<table class="form">
<tr><th style="width:72%">Summary Milestones — Mốc chính</th><th style="width:28%">Due Date — Hạn</th></tr>
<tr><td>M0 — Khởi động dự án; phê duyệt tuyên bố dự án và huy động nhân sự</td><td>14/09/2026</td></tr>
<tr><td>M1 — Phê duyệt và chốt đường cơ sở đặc tả yêu cầu</td><td>02/10/2026</td></tr>
<tr><td>M2 — Phê duyệt đường cơ sở thiết kế (kiến trúc, lược đồ CSDL, giao diện)</td><td>23/10/2026</td></tr>
<tr><td>M3 — Nghiệm thu demo vòng lặp 1: F01–F05</td><td>20/11/2026</td></tr>
<tr><td>M4 — Nghiệm thu vòng lặp 2, hoàn thành chức năng: F06–F11</td><td>25/12/2026</td></tr>
<tr><td>M5 — Hoàn tất kiểm thử hệ thống; đạt điều kiện vào UAT</td><td>15/01/2027</td></tr>
<tr><td>M6 — Ký duyệt UAT, chuyển đổi dữ liệu, vận hành chính thức và bàn giao</td><td>29/01/2027</td></tr>
<tr><td>M7 — Kết thúc bảo hành; tổng kết và đóng dự án</td><td>05/02/2027</td></tr>
</table>

<div class="page-of">Page 2 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter — Tuyên bố dự án</div>

<table class="form">
<tr><td class="label">Preapproved Financial Resources:<br>Kinh phí đã phê duyệt</td><td>Tổng <strong>700.000.000 VNĐ</strong> từ ngân sách đầu tư 2026–2027 của trung tâm, giải ngân theo nghiệm thu mốc: 20% tại M0, 25% tại M3, 30% tại M4, 25% tại M6.<br><br>Nhân sự (25 người-tháng) 490.000.000 · Hạ tầng và bản quyền 70.000.000 · Triển khai, chuyển đổi dữ liệu, đào tạo, tài liệu 70.000.000 · Quỹ dự phòng quản lý 70.000.000.<br><br>Không cam kết thêm kinh phí; mọi khoản tăng phải có phê duyệt bằng văn bản của nhà tài trợ.</td></tr>
</table>

<table class="form">
<tr><th style="width:38%">Stakeholder(s) — Bên liên quan</th><th style="width:62%">Role — Vai trò</th></tr>
<tr><td>Đỗ Thị Bích Ngọc — chủ sở hữu kiêm Giám đốc trung tâm</td><td>Nhà tài trợ: cấp kinh phí, phê duyệt tuyên bố dự án, thay đổi phạm vi và nghiệm thu cuối</td></tr>
<tr><td>Quản lý đào tạo</td><td>Chủ nghiệp vụ khóa học, lớp, xếp lịch, đánh giá; nguồn yêu cầu chính và trưởng nhóm UAT</td></tr>
<tr><td>Kế toán</td><td>Chủ nghiệp vụ học phí, công nợ, lương theo giờ dạy; tham gia UAT</td></tr>
<tr><td>Trưởng bộ phận tư vấn / lễ tân</td><td>Chủ nghiệp vụ ghi danh và ghi nhận thanh toán; đại diện người dùng hằng ngày</td></tr>
<tr><td>Tổ trưởng chuyên môn (đại diện giáo viên)</td><td>Đại diện 35 giáo viên cho màn hình điểm danh, điểm số và giờ dạy</td></tr>
<tr><td>Học viên và phụ huynh</td><td>Người dùng cuối của lịch học, kết quả, học phí; người nhận thông báo</td></tr>
<tr><td>Quản trị CNTT của trung tâm</td><td>Tiếp nhận hệ thống khi bàn giao; vận hành tài khoản, sao lưu, hạ tầng về sau</td></tr>
<tr><td>Nguyễn Văn A — Giám đốc dự án</td><td>Lập kế hoạch, thực thi, kiểm soát dự án; đầu mối duy nhất với nhà tài trợ</td></tr>
<tr><td>Đội dự án (3 lập trình viên, 1 kiểm thử)</td><td>Phân tích, thiết kế, lập trình, kiểm thử, triển khai, viết tài liệu</td></tr>
<tr><td>Nhà cung cấp dịch vụ SMS/email</td><td>Nhà cung cấp bên ngoài cho kênh thông báo</td></tr>
<tr><td>Nhà cung cấp hạ tầng đám mây</td><td>Nhà cung cấp bên ngoài cho môi trường vận hành và kiểm thử</td></tr>
</table>

<table class="form">
<tr><td class="label">Project Exit Criteria:<br>Tiêu chí kết thúc</td><td>1. Toàn bộ sản phẩm D1–D10 được nhà tài trợ chấp nhận bằng văn bản. 2. UAT ký duyệt với ≥ 95% ca kiểm thử đạt, không còn lỗi Nghiêm trọng/Cao. 3. Hệ thống chạy trên môi trường vận hành, sao lưu được kiểm chứng bằng phục hồi thử thành công. 4. Dữ liệu đã chuyển đổi và đối chiếu với tệp nguồn, sai lệch được kế toán chấp nhận bằng văn bản. 5. Tối thiểu 80% trong 25 người dùng nghiệp vụ đã được đào tạo, có biên bản. 6. Mã nguồn, script CSDL, hướng dẫn sử dụng và hướng dẫn quản trị đã bàn giao và được xác nhận. 7. Bảo hành một tháng kết thúc, không còn lỗi Nghiêm trọng/Cao. 8. Báo cáo tổng kết, bài học kinh nghiệm và quyết toán được phê duyệt, hóa đơn cuối đã thanh toán.<br><br>Kết thúc sớm theo quyết định của nhà tài trợ (rút kinh phí hoặc mất nhu cầu nghiệp vụ): bàn giao phần đã hoàn thành và đóng dự án kèm báo cáo chấm dứt.</td></tr>
</table>

<table class="form">
<tr><td class="label" colspan="2">Project Manager Authority Level: — Mức thẩm quyền của giám đốc dự án</td></tr>
<tr><td class="label">Staffing Decisions:<br>Quyết định nhân sự</td><td>Phân công và điều chuyển công việc trong đội 5 người đã duyệt, duyệt nghỉ phép, quản lý hiệu suất hằng ngày. Được đề nghị thay thế thành viên kèm thông báo cho nhà tài trợ; quyết định tuyển dụng, chấm dứt và hợp đồng lao động thuộc quản lý trực tuyến của nhà thầu.</td></tr>
<tr><td class="label">Budget Management and Variance:<br>Quản lý ngân sách và sai lệch</td><td>Cam kết và chi tiêu trong đường cơ sở đã duyệt, gồm giao dịch đơn lẻ tới 20.000.000 VNĐ và sử dụng quỹ dự phòng 70.000.000 VNĐ cho rủi ro R1–R7. Tự quản lý sai lệch chi phí lũy kế trong ±5% đường cơ sở. Trình nhà tài trợ mọi dự báo vượt 5%, mọi lần dùng dự phòng vượt 40.000.000 VNĐ và mọi thay đổi tổng kinh phí.</td></tr>
</table>

<div class="page-of">Page 3 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter — Tuyên bố dự án</div>

<table class="form">
<tr><td class="label">Technical Decisions:<br>Quyết định kỹ thuật</td><td>Toàn quyền về kiến trúc, nền tảng công nghệ, thiết kế cơ sở dữ liệu, quy ước lập trình, công cụ và cách thức triển khai nội bộ, với điều kiện đáp ứng yêu cầu phi chức năng N01–N08 và các sản phẩm đã thống nhất. Quyết định nội dung từng vòng lặp trong phạm vi đã duyệt. Mọi quyết định làm thay đổi phạm vi người dùng nhìn thấy, tiến độ hoặc chi phí phải trình nhà tài trợ qua quy trình quản lý thay đổi.</td></tr>

<tr><td class="label">Conflict Resolution:<br>Giải quyết xung đột</td><td>Xử lý xung đột trong nội bộ đội dự án và giữa đội dự án với nhân sự vận hành của trung tâm, kể cả xung đột ưu tiên về thời gian tham gia của nhân sự. Xung đột vượt ranh giới tổ chức, làm thay đổi phạm vi đã thống nhất, hoặc chưa xử lý được sau 5 ngày làm việc thì trình nhà tài trợ; quyết định của nhà tài trợ là cuối cùng. Tranh chấp với nhà cung cấp bên ngoài xử lý theo hợp đồng dịch vụ tương ứng.</td></tr>

<tr><td class="label">Sponsor Authority:<br>Thẩm quyền nhà tài trợ</td><td>Đỗ Thị Bích Ngọc, chủ sở hữu kiêm Giám đốc trung tâm đào tạo, phê chuẩn dự án và bản tuyên bố dự án này, cấp và giải ngân 700 triệu đồng, chỉ định giám đốc dự án, bố trí nhân sự trung tâm tham gia. Phê duyệt thay đổi phạm vi, tiến độ, ngân sách vượt thẩm quyền của giám đốc dự án; ấn định mức sai lệch chấp nhận được; giải quyết xung đột được trình lên và xung đột giữa các bộ phận; nghiệm thu sản phẩm; cho phép vận hành chính thức và đóng dự án; bảo trợ dự án trước nhân sự và các trưởng cơ sở.</td></tr>
</table>

<table class="form">
<tr><td class="label" colspan="2">Approvals: — Phê duyệt</td></tr>
<tr><td style="height:60pt">Project Manager Signature — Chữ ký giám đốc dự án</td><td style="height:60pt">Sponsor or Originator Signature — Chữ ký nhà tài trợ</td></tr>
<tr><td>Project Manager Name — Họ tên: Nguyễn Văn A</td><td>Sponsor or Originator Name — Họ tên: Đỗ Thị Bích Ngọc</td></tr>
<tr><td>Date — Ngày: ______________________</td><td>Date — Ngày: ______________________</td></tr>
</table>

<div class="page-of">Page 4 of 4</div>

</div>
