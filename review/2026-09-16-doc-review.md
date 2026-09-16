# Review of the shared Google Doc, 16 September 2026

Replies are posted on the reviewer's thread; new findings are separate comments prefixed with their location.

## 1. Thẻ 1, trang bìa: MÔN QUẢN LÝ DỰ ÁN PHẦN MỀM

Thread `AAACG0ldthI`. Reviewer: Vatten: Cho xuống dưới title báo cáo

Đồng ý. Đề xuất thứ tự trang bìa: HỌC VIỆN, KHOA, BÁO CÁO BÀI TẬP LỚN, rồi MÔN QUẢN LÝ DỰ ÁN PHẦN MỀM, rồi bảng GVHD và thành viên, Hà Nội 2026. Chỉ sửa trên Google Doc; file nguồn trong repo không có trang bìa nên không ảnh hưởng.

## 2. Thẻ 1, 1.1.1: đoạn 'The center runs today on paper registers...'

Thread `AAACG0ldthE`. Reviewer: Nguyễn Bá Hùng: viết rõ project scope. Vatten: Thêm tính năng giao tiếp với nội bộ

Đã làm hai việc trong v3.1 (nhánh charter-v3-review, file docs/charter-package.en.md).
(1) Thêm câu phạm vi ngay trong 1.1.1: học viên 6 đến 18 tuổi, học sau giờ học và cuối tuần, không có chương trình mầm non, hệ thống chỉ phục vụ 3 cơ sở hiện có (giả định 1 cập nhật theo).
(2) F09 đổi thành 'Notification and internal communication': thông báo nội bộ từ Academic Manager tới giáo viên và nhân viên, bảng tin theo lớp từ giáo viên tới phụ huynh, tin nhắn giữa phụ huynh và lễ tân, tất cả chung một log. Không tách thành chức năng riêng để khỏi đánh số lại F01 đến F11; số F12 dành cho mobile app.
Câu EN: 'The learners are school-age students, aged 6 to 18, who attend after school and at weekends; the center runs no preschool programme, and the system is scoped to these learners at these three branches.'

## 3. Thẻ 1, tiêu đề 1.1.3 Users and roles

Thread `AAACG0ldtho`. Reviewer: Nguyễn Bá Hùng: thêm nghiệp vụ nặng. Vatten: Tăng số học viên lên

Đã thêm các nghiệp vụ nặng vào bảng vai trò 1.1.3, mỗi nghiệp vụ trỏ về chức năng tương ứng: Academic Manager phân công dạy thay, hoãn buổi, duyệt bảng giờ dạy, xem danh sách ngoại lệ hằng ngày; Accountant khớp chuyển khoản chưa xác định, duyệt đề xuất hoàn tiền, khoá bảng lương tháng; Front-desk xử lý yêu cầu học bù và tái ghi danh; phụ huynh gửi yêu cầu học bù, xác nhận chuyển khoản kèm mã tham chiếu, tái ghi danh, đánh giá cuối khoá. Luồng xử lý ngoại lệ của từng nghiệp vụ đã có ở 1.1.5.
Số học viên giữ 1.200 (giả định 1): tăng số chỉ đổi con số chứ không thêm nghiệp vụ, trong khi business case, A02 và A03 (5.000 hồ sơ) đã tính trên con số này. Nếu nhóm muốn tăng thì đổi giả định 1, A02, A03 và business case cùng lúc.

## 4. Thẻ 1, tiêu đề 1.1.3 Users and roles

Thread `AAACG0ldthg`. Reviewer: Vatten: Thêm các tính năng của giáo viên (báo cáo, tương tác)

Đã mở rộng dòng Teacher: ngoài điểm danh, điểm số và bảng giờ dạy, giáo viên có ghi chú buổi học, báo cáo theo lớp, thông báo và tin nhắn tới phụ huynh (qua F09), xem kết quả đánh giá cuối khoá của lớp mình, tất cả từ mobile app (F12) hoặc web.
Dòng Teacher mới: 'Class roster, attendance, scores and progress comments, session notes and a per-class report, announcements and messages to parents, own teaching-hour sheet, the end-of-course evaluation of their classes, from the mobile app (F12) or the web'.

## 5. Thẻ 1, 1.1.3, dòng Teacher: 'Class roster, attendance, scores, own teaching-hour sheet'

Thread `AAACG0ldthU`. Reviewer: Nguyễn Bá Hùng: evaluation

Đã thêm đánh giá ở hai chiều. Giáo viên đánh giá tiến bộ học viên (đã có trong F08, nay ghi rõ 'scores and progress comments' ở dòng Teacher). Giáo viên được học viên và phụ huynh đánh giá cuối khoá (F08 mở rộng; kết quả tổng hợp theo lớp và theo giáo viên gửi Academic Manager). F08 đổi tên thành 'Assessment, progress reports, and course evaluation'.

## 6. Thẻ 1, 1.1.3, dòng Student / Parent: 'Own schedule, attendance and score history...'

Thread `AAACG0ldthQ`. Reviewer: Vatten: Thêm đánh giá

Đã thêm 'end-of-course evaluation of the course and the teacher' vào dòng Student / Parent và vào F08: cuối mỗi khoá, học viên và phụ huynh đánh giá khoá học và giáo viên theo thang 5 điểm cố định kèm nhận xét tự do; kết quả tổng hợp theo lớp và theo giáo viên. Làm từ app (F12) hoặc web.

## 7. Thẻ 1, tiêu đề '2: Project Charter'

Thread `AAACG0ldthw`. Reviewer: Vatten: Chỉnh giống y hệt form

Đồng ý, và đây là lỗi lớn nhất của bản Doc hiện tại: mục 2 của Thẻ 1 là charter bản cũ (N01 đến N08, R1 đến R8, 8 exit criteria, PM là 'Ngô Hải Đăng' ở trang 1 nhưng 'Nguyễn Văn A' ở bảng stakeholder, ô Customer ghi bà Ngọc là 'sponsor of the learning center'), mâu thuẫn với Phần 1 và với Thẻ 2.
Đề xuất: xoá toàn bộ mục 2 của Thẻ 1, dùng nội dung Thẻ 2 làm Phần 2, và chỉnh đúng form sách trang 16 đến 19: thanh tiêu đề PROJECT CHARTER, mỗi trang một page break với 'Page N of 4', trang 1 ghép Project Sponsor với Date Prepared và Project Manager với Project Customer, bảng Approvals chỉ 2 cột (Project Manager, Sponsor or Originator), ô chưa chắc chắn tô nền vàng theo yêu cầu 3, ô chưa biết để trống.
Mục 2B của file nguồn charter-package.en.md đã đúng thứ tự trường của form; Doc nên được sinh lại từ file này (tools/gdoc.py import-html) thay vì sửa tay từng ô.

## 8. Thẻ 1, ô Project Sponsor: '- owner and Director of the learning center'

Thread `AAACG0ldth4`. Reviewer: Vatten: Bỏ

Đã bỏ. Trong v3.1 ô Project Sponsor chỉ còn tên: Dr. Nguyễn Mạnh Hùng.
Lưu ý: theo v3.0 ông Hùng là sponsor (cấp vốn, phê duyệt, nghiệm thu), không phải chủ trung tâm; chủ trung tâm là bà Ngọc (customer). Thẻ 2 đang ghi ông Hùng là 'owner and Center Director' ở bảng stakeholder và ô Sponsor Authority, cần sửa cho khớp.

## 9. Thẻ 1, ô Project Customer: '- sponsor of the learning center: 3 branches, 1,200 active students, 35 teachers'

Thread `AAACG0ldth0`. Reviewer: Vatten: Bỏ

Đã bỏ phần mô tả. Ô Project Customer trong v3.1: 'Đỗ Thị Bích Ngọc, owner and Director of the learning center' (giữ vai trò để phân biệt với sponsor; số cơ sở và số học viên đã có ở 1.1.1, không lặp lại). Chữ 'sponsor of the learning center' ở Thẻ 1 là sai: bà Ngọc là customer, sponsor là ông Hùng.

## 10. Thẻ 1, ô Project Manager: '- Project Manager, assigned full-time for the 5-month duration'

Thread `AAACG0ldth8`. Reviewer: Vatten: Bỏ v3

Đã bỏ. Ô Project Manager để trống theo quy ước ô trống của yêu cầu 3 (giả định 15: sponsor bổ nhiệm PM tại M0), ở trang 1, ở bảng stakeholder và ở khối chữ ký. Tên 'Ngô Hải Đăng' ở trang 1 và 'Nguyễn Văn A' ở bảng stakeholder của Thẻ 1 đều bỏ.

## 11. Thẻ 1, Project Purpose: 'leaves roughly 8% of tuition uncollected past due date'

Thread `AAACG0ldtiA`. Reviewer: Vatten: Rephrase

Đã viết lại ở cả 2A và form: 'and at any moment about 8% of billed tuition is past its due date, because nobody holds a reliable list of who owes what.' Con số 8% vẫn là giả định (giả định 6) nên giữ nền vàng.

## 12. Thẻ 1, Project Purpose: 'as required by the plan to open a fourth branch in 2027.'

Thread `AAACG0ldtiE`. Reviewer: Vatten: Top von out of scope

Đã tách hai ý: cơ sở thứ tư là lý do kinh doanh (giữ), còn việc mở cơ sở đó nằm ngoài dự án (ghi rõ). Câu EN: '...which the center needs before it opens a fourth branch in 2027; opening that branch is outside this project (section 1.4).' Mục 1.4 đã nói: cơ sở là dữ liệu cấu hình trong F11, nên trung tâm tự tạo cơ sở thứ tư mà không cần sửa phần mềm.

## 13. Thẻ 1, ô Project Boundaries

Thread `AAACG0ldtiI`. Reviewer: Vatten: Càng chi tiết càng tốt. Ko cho mầm non vào học -> Scope

Đã chi tiết hoá cả Included lẫn Excluded.
Included: F01 đến F12 và hành vi ngoại lệ 1.1.5, cho học viên 6 đến 18 tuổi tại 3 cơ sở hiện có; di trú dữ liệu 2 học kỳ gần nhất; triển khai trên 1 máy chủ cloud kèm môi trường staging; mobile app phát hành trên Google Play và App Store; đào tạo; tài liệu; bảo hành 6 tháng từ go-live, tháng đầu trong dự án.
Excluded thêm: chương trình mầm non và học viên dưới 6 tuổi; chức năng nhân viên trên mobile; chế độ offline của app; và các loại trừ ở mức dự án (xem thread 'Excluded').

## 14. Thẻ 1, Project Boundaries: 'one month of warranty'

Thread `AAACG0ldtiY`. Reviewer: Vatten: Bảo hành 1 năm, ít nhất 6 tháng. Trong budget phải để dành một phần để bảo hành

Đã nâng lên 6 tháng từ go-live (5/1/2027 đến 5/7/2027) cho cả web và app, có dòng ngân sách riêng.
Cách bố trí: tháng bảo hành đầu tiên nằm trong dự án (M6 đến M7, lịch không đổi vì thời hạn 5 tháng của đề bài là cố định); tháng 2 đến 6 chạy sau closeout, do bộ phận hỗ trợ của nhà cung cấp thực hiện (khoảng 0,35 FTE), cấp từ dòng 5 'Warranty and support' 35.000.000 VND (5%), bàn giao bằng văn bản tại closeout (exit criterion 7). Bảng thời gian phản hồi theo mức độ áp dụng cho cả 6 tháng; lỗi Critical/High còn mở ở cuối tháng 6 báo sponsor kèm ngày sửa.
Không chọn 12 tháng vì với 700 triệu cố định thì phải cắt thêm từ nhân sự; nếu nhóm muốn 12 tháng thì dòng 5 lên khoảng 70 triệu và dự phòng về 0.

## 15. Thẻ 1, Project Boundaries: 'Excluded'

Thread `AAACG0ldtig`. Reviewer: Vatten: Chưa có về project, mới có product

Đã thêm mục 'Project exclusions' tách khỏi loại trừ sản phẩm, ở 1.4 và ở Boundaries (2A và form): dự án không mua hoặc trả phí thuê cloud, gateway, store quá 12 tháng đầu; không làm sạch file Excel nguồn (trung tâm làm, giả định 11); không tuyển dụng, tái cơ cấu hay quản lý nhân sự trung tâm; không vận hành hệ thống sau bàn giao; không đào tạo phụ huynh ngoài hướng dẫn trong app và tin nhắn onboarding.

## 16. Thẻ 1, Project Boundaries: 'native mobile apps'

Thread `AAACG0ldtiQ`. Reviewer: Vatten: Làm thêm cả mobile app để tương tác -> Tăng cost. Quay lại objective

Đã đưa mobile app vào phạm vi thành F12 'Mobile app for parents and teachers', bám objective 'stakeholder satisfaction' (phụ huynh được thông tin, giáo viên báo cáo ngay tại lớp).
Nội dung: một mã nguồn cross-platform cho Android và iOS, dùng chung API và tài khoản với web. Phụ huynh: lịch, điểm danh, điểm, học phí và hoá đơn, push notification, nhắn tin lễ tân và giáo viên, yêu cầu học bù, xác nhận chuyển khoản, đánh giá cuối khoá, tái ghi danh. Giáo viên: buổi dạy và danh sách lớp, điểm danh khi online, nhập điểm, bảng giờ dạy, thông báo lớp. Chức năng nhân viên vẫn trên web; không chức năng nào chỉ có trên app.
Chi phí: thêm 1 mobile developer bán thời gian 2,5 person-month (sau M2 đến M5), 49 triệu, vẫn trong 700 triệu nhờ cắt lại ngân sách (xem thread Preapproved Financial Resources); nhóm 6 người vẫn trong khung 4 đến 6 của đề bài. Kèm theo: D11 (app phát hành), A12, R12 (store duyệt chậm hoặc framework lỗi), 4 ca ngoại lệ ở 1.1.5, giả định 18 và 19; go-live không phụ thuộc app, app được phép trễ tối đa 2 tuần sau M6.
Business case: push thay phần lớn SMS, tiết kiệm khoảng 32 triệu/năm chi phí vận hành, là lý do payback giữ được ở năm thứ 5 sau khi tính cả chi phí thông báo mà các bản trước bỏ sót.

## 17. Thẻ 1, ô Key Deliverables

Thread `AAACG0ldtik`. Reviewer: Vatten: Chia thành 2 cái: Cho khách hàng và nội bộ

Đã chia. Bảng 1.2 thêm cột 'For': D1 đến D9 và D11 là Customer, D10 là Internal. Thêm bảng 'Internal deliverable' không đánh số: kế hoạch quản lý dự án, lịch và kế hoạch giao tiếp (M1), báo cáo tuần cho sponsor và Giám đốc (từ M0), sổ rủi ro (M1, xem hằng tuần), test plan và test cases (M2, hoàn tất ở M5 trong D5), closeout report (M7, chính là D10).
Ô Key Deliverables trong form: 'For the customer: D1 ... D9, D11. Internal: D10 cùng bộ tài liệu quản lý dự án.'

## 18. Thẻ 1, bảng 1.2, dòng D10

Thread `AAACG0ldtio`. Reviewer: Vatten: Tốt. Của nội bộ

Đã đánh dấu D10 là Internal trong cột 'For' của bảng 1.2, và ghi D10 vào phần Internal của ô Key Deliverables trong form (xem thread Key Deliverables).

## 19. Thẻ 1, ô High-Level Requirements

Thread `AAACG0ldtiw`. Reviewer: Vatten: Viết thành các gạch đầu dòng

Trên Google Doc: dùng bullet thật trong ô. Trong file nguồn Markdown, ô bảng không chứa được danh sách, nên ô này viết thành 10 mục đánh số (1) đến (10) trong v3.1; mục 2A tương ứng đã là bullet.
Thêm 2 mục so với bản cũ: (8) phụ huynh và giáo viên dùng app Android/iOS trên cùng API, không chức năng nào chỉ có trên app; (9) hành vi ngoại lệ 1.1.5 được giao và kiểm thử ngang với các chức năng.

## 20. Thẻ 1, ô Overall Project Risk

Thread `AAACG0ldti0`. Reviewer: Vatten: Cần thêm. Rủi ro về product và project. Rủi ro đầu tiên là không đáp ứng objective

Đã làm cả ba ý. Sổ rủi ro có cột Type (Product hoặc Project). R1 mới: 'hệ thống giao không đạt A01 đến A12 nên trung tâm không vận hành được, mục tiêu không đạt'; ứng phó: chốt bộ test UAT với business owner tại M5 và đo chấp nhận trên bộ đó, pilot F01 đến F06 ở 1 cơ sở trước M6, gate go-live bằng A01, nếu UAT trượt thì đưa 3 phương án cho sponsor trong 2 ngày làm việc. R2 đến R11 là R1 đến R10 cũ; R12 mới là rủi ro store duyệt chậm hoặc framework cross-platform lỗi. Đoạn mở đầu nói rõ cách phân loại.

## 21. Thẻ 1, ô Overall Project Risk: 'Medium. Technology and domain are well understood...'

Thread `AAACG0ldtjM`. Reviewer: Vatten: Nhân sự so với budget chưa hợp lý. Không cho PM thêm tiền để cover rủi ro

Hai sửa đổi.
(1) Dự phòng: đổi 'management reserve do PM giữ' thành 'contingency reserve' 28.000.000 VND (4%) nằm trong cost baseline; PM chỉ được rút cho các rủi ro đã nhận diện R1 đến R12 qua change control, báo cáo hằng tháng, rút quá 20 triệu phải xin sponsor. Đúng phân biệt của PMBOK: management reserve thuộc về sponsor và nằm ngoài 700 triệu, ở đây không có.
(2) Nhân sự: giữ đơn giá 19,6 triệu/person-month nhưng nêu cơ sở ở giả định 17 (PM/BA 26 triệu, developer 19 triệu, QA 15 triệu, fully loaded, không tính lợi nhuận nhà cung cấp) để kiểm tra được; 25 + 2,5 person-month = 539 triệu (77%). Nếu nhóm thấy đơn giá thấp so với thị trường thì con số bị 700 triệu cố định ràng buộc: hoặc giảm FTE, hoặc giảm phạm vi; cần quyết định chung.

## 22. Thẻ 1, Success Criteria ô Scope: '100%'

Thread `AAACG0ldtjY`. Reviewer: Vatten: Cao quá. 99 thôi, 1 còn lại là lỗi không ảnh hưởng đến vận hành hệ thống. Nguyễn Bá Hùng: focus vào key deliverable

Đã hạ và đổi cách đo. Tiêu chí Scope: 'All twelve functions accepted in UAT against the test set agreed at M5, with at least 99% of test cases passed and the remainder being defects that do not affect operation; all eleven deliverables signed off'. A01, ô Other, exit criterion 2 và đường xử lý khi UAT trượt đổi từ 95% lên 99% cho khớp. Nhấn vào key deliverable như Hùng nói: điều kiện chính là D1 đến D11 được ký, không phải con số chức năng.

## 23. Thẻ 1, Success Criteria ô Scope: 'UAT'

Thread `AAACG0ldtjo`. Reviewer: Vatten: Cái 100% đang trao hết quyền cho khách hàng

Đúng, nên v3.1 đưa vào ô Scope của form: chấp nhận được đo trên bộ test UAT đã thống nhất và ký tại M5, và 'acceptance cannot be withheld for scope outside the baseline' (câu này đã có ở 2A Project approval requirements, nay đưa lên form). Khách hàng ký bộ test trước, không được từ chối bằng yêu cầu ngoài baseline.

## 24. Thẻ 1, ô Preapproved Financial Resources

Thread `AAACG0ldtj8`. Reviewer: Vatten: Còn thiếu các chi phí khác như cơ sở vật chất...

Đã thêm dòng 'Facilities, equipment, travel' 14 triệu (chỗ làm việc, laptop, 2 điện thoại test Android và iOS, đi lại 3 cơ sở) và dòng 'Warranty and support' 35 triệu.
Bảng mới 6 dòng, tổng đúng 700 triệu: nhân sự 539 (77%); hạ tầng, giấy phép, tài khoản store 42 (6%); cơ sở vật chất 14 (2%); triển khai, di trú, đào tạo, tài liệu 42 (6%); bảo hành tháng 2 đến 6 là 35 (5%); dự phòng 28 (4%). Mỗi dòng có cột cơ sở tính, tô vàng vì là giả định.

## 25. Thẻ 1, Preapproved Financial Resources: 'Infrastructure and licenses, 70,000,000.'

Thread `AAACG0ldtj4`. Reviewer: Vatten: Phải chứng minh về sau

Đã tách dòng hạ tầng thành hạng mục có đơn giá (giả định, tô vàng): cloud và staging 12 tháng 24 triệu; domain và SSL 2 triệu; tín dụng gateway cho dev/test 4 triệu; công cụ phát triển 8,7 triệu; Apple Developer 2,6 triệu/năm và Google Play 0,7 triệu một lần; push service gói miễn phí; tổng 42 triệu, ghi rõ 'ước tính lại tại M1'. Chi phí SMS vận hành do trung tâm trả (giả định 12) nên không nằm ở đây mà nằm trong business case.

## 26. Thẻ 1, Preapproved Financial Resources: 'Total 700,000,000 VND from the center's 2026 to 2027 capital budget, released against milestone acceptance...'

Thread `AAACG0ldtj0`. Reviewer: Vatten: Chia tiền sai (maybe)

Đã cắt lại toàn bộ (xem thread Preapproved Financial Resources) và thêm ràng buộc cho các đợt giải ngân 20/25/30/25: mỗi đợt được xuất hoá đơn dựa trên biên bản nghiệm thu của mốc tương ứng (2A, Project approval requirements); phần chia là cơ sở cấp vốn, ước tính lại tại M1. Nếu 'sai' là ý 77% cho nhân sự thì con số ra từ 27,5 person-month nhân đơn giá ở giả định 17; muốn khác thì đổi giả định.

## New 1. Thẻ 1, mục 2: Project Charter

Quoted: PROJECT CHARTER, page 1 of 4

Mục 2 của Thẻ 1 là charter bản cũ và mâu thuẫn với Phần 1 và với Thẻ 2: tham chiếu N01 đến N08 trong khi Phần 1 dùng A01 đến A11; R1 đến R8 trong khi Thẻ 2 dùng R1 đến R10; 8 exit criteria so với 10; PM là 'Ngô Hải Đăng' ở trang 1 nhưng 'Nguyễn Văn A' ở bảng stakeholder; ô Customer ghi bà Ngọc là 'sponsor of the learning center'. Đề xuất xoá toàn bộ mục 2 của Thẻ 1 và dùng Thẻ 2 làm Phần 2.

## New 2. Toàn tài liệu: thiếu Phần 3 Prompt Log

Quoted: BÁO CÁO BÀI TẬP LỚN

Thiếu Phần 3 Prompt Log, tức yêu cầu 4 của đề bài (liệt kê mọi phiên bản prompt, chất lượng từng bản, lý do phải sửa). File nguồn charter-package.en.md v3.1 có sẵn V1 đến V12; cần chép vào Doc, nếu không yêu cầu 4 được 0 điểm.

## New 3. Thẻ 2, ô Project Purpose và Overall Project Risk: tham chiếu treo

Quoted: Quantified business case in section 2A

Form đang tham chiếu 'section 2A' (business case), 'Risks R1 to R10' và 'section 1.3', nhưng Doc không có mục 2A (14 charter elements của Table 1.1 trong sách). Hoặc chép 2A từ file nguồn vào trước form (business case, sổ rủi ro, project approval requirements, đường xử lý khi UAT trượt), hoặc bỏ các tham chiếu.

## New 4. Thẻ 2, bảng Stakeholder(s) và ô Sponsor Authority

Quoted: Dr. Nguyễn Mạnh Hùng, owner and Center Director

Thẻ 2 gộp lại sponsor và customer: bảng stakeholder ghi ông Hùng là 'owner and Center Director | Customer' và bỏ dòng bà Ngọc; ô Sponsor Authority gọi ông Hùng là 'owner and Director of the learning center'. Mâu thuẫn với ô Project Sponsor và Project Customer ở trang 1 và với giả định 16 của v3.0 (sponsor và customer là hai người khác nhau), mà giả định 16 cũng chưa có trong mục 1.6 của Doc. Đề xuất: 2 dòng stakeholder riêng (sponsor: cấp vốn, phê duyệt, nghiệm thu; customer: chủ nhu cầu, cam kết nhân sự và dữ liệu, đưa hệ thống vào vận hành), sửa Sponsor Authority, thêm giả định 16.

## New 5. Thẻ 2, khối Approvals

Quoted: Sponsor | Project Manager | Customer

Form sách chỉ có 2 chữ ký: Project Manager và Sponsor or Originator, mỗi bên có Signature, Name, Date. Doc đang có 3 cột kể cả Customer, và ghi tên ông Hùng dưới cột Customer trong khi ông là Sponsor. Đề xuất về 2 cột đúng form, tên ông Hùng ở cột Sponsor or Originator, ô PM và các ô ngày để trống.

## New 6. Toàn tài liệu: quy ước nền vàng và ô trống (yêu cầu 3)

Quoted: Project Manager

Yêu cầu 3 của đề bài: ô chưa chắc đúng thì tô nền vàng, ô không biết thì để trống. File nguồn v3.1 đánh dấu 87 chỗ giả định. Cần rà lại trên Doc xem các ô tương ứng đã tô nền vàng chưa (1.200 học viên / 35 giáo viên / 3 cơ sở, 60 giờ, 8%, các ngày mốc, đơn giá, tên sponsor và customer, tên sản phẩm) và ô Project Manager, chữ ký, ngày ký để trống có chủ ý, kèm một câu giải thích quy ước ở đầu tài liệu như file nguồn.

## New 7. Thẻ 1 và Thẻ 2: định dạng ngày

Quoted: 02 September 2026

Ngày ghi không thống nhất: '02 September 2026' và '05 Jan 2027' ở Thẻ 1, '2 September 2026' và '5 Jan 2027' ở Thẻ 2. Đề xuất bỏ số 0 đầu như file nguồn v3.x.

## New 8. Trang bìa và ô Project Customer: tên khách hàng

Quoted: ĐỖ THỊ BÍCH NGỌC

Câu hỏi cho nhóm: customer giả định đang mang tên thật của giảng viên hướng dẫn (trang bìa). Nếu là chủ ý thì giữ; nếu không, nên đổi sang tên hư cấu để người chấm không hiểu nhầm. Ưu tiên thấp.

## New 9. Thẻ 1, mục 1.6 Project Assumptions: thiếu giả định 16 đến 19

Quoted: 15 | The commercial product name and the project manager's name are not yet decided.

Doc dừng ở giả định 15; v3.1 có 16 đến 19: (16) sponsor và customer là hai người khác nhau; (17) cơ sở đơn giá nhân sự 19,6 triệu/person-month; (18) mobile app: 80% phụ huynh có smartphone, cross-platform, 2,5 person-month, store duyệt tối đa 1 tuần, 70% kích hoạt trong học kỳ đầu; (19) SMS 800 VND, 4 tin/học viên/tháng, hosting sau năm 1 khoảng 27,6 triệu. Cần bổ sung khi chép nội dung mới vào Doc.
