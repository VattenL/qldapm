# Hướng dẫn dùng PM skill

Cách dùng skill `pm` trong Claude Code để tạo, kiểm tra và audit các form trong *A Project Manager's
Book of Forms*, bản thứ 3, cho dự án này. Tài liệu viết cho các bạn trong nhóm đã nắm môn học và cuốn
sách nhưng chưa đọc phần bên trong của skill.

Bản tiếng Anh: [`pm-skill-guide.md`](pm-skill-guide.md). Lệnh, tên file và nhãn in trên form được
giữ nguyên tiếng Anh.

Mọi lệnh dưới đây đã được chạy thử trong repo từ thư mục gốc, trừ các lệnh `gdoc` cần thông tin đăng nhập Google của nhóm: các lệnh về form chạy ngày 1 October 2026, các lệnh về quyết định (`--knowledge`, `pm_calc.py`, `form_graph.py`, mục 8) chạy ngày 15 October 2026.

## Mục lục

1. Skill làm gì và không làm gì
2. Chuẩn bị
3. Cách yêu cầu một form
4. Từ yêu cầu đến sản phẩm
5. Ba trạng thái đánh dấu
6. Quy tắc reviewer kiểm tra
7. Audit và trả lời comment trên Google Doc
8. Ra quyết định: hỏi nên làm gì
9. Toàn bộ 66 form
10. Bảng lệnh nhanh
11. Xử lý sự cố
12. Cải tiến skill

## 1. Skill làm gì và không làm gì

Skill nằm ở `.claude/skills/pm/`. Claude Code tự nạp skill khi bạn yêu cầu một form, nhắc số hiệu
form, yêu cầu audit tài liệu trong `docs/`, hoặc hỏi nên làm gì trước một tình huống của dự án (trễ
tiến độ, vượt chi phí, một rủi ro đã xảy ra, một change request).

| Skill làm | Skill không làm |
| --- | --- |
| Tìm đúng form trong 66 form theo số hoặc theo tên, và hỏi lại khi một tên khớp nhiều form | Nhớ danh sách trường theo trí nhớ; mọi nhãn lấy từ `references/fields/<form>.json`, được chép từ trang form trống |
| Dựng khung form bằng Markdown với title block, nhãn, tiêu đề trang, header nhóm và các bank đúng như bản in, đúng thứ tự in | Thêm trường, cột hay ghi chú mà form in không có |
| Điền form từ `docs/charter-package.en.md`, `docs/scope-package.en.md` và các form trong `docs/forms/` | Bịa giá trị dự án; giá trị giả định được tô vàng, giá trị chưa biết để trống hoặc `[TBD]` |
| Chạy kiểm tra fidelity và consistency rồi báo kết quả | Âm thầm chọn một bên khi hai tài liệu mâu thuẫn; skill báo mâu thuẫn để nhóm quyết định |
| Xuất form ra `.docx` trông giống sách | Đẩy lên Google Doc của nhóm khi bạn chưa yêu cầu, và không bao giờ đẩy khi không có Doc ID bạn đưa |
| Audit cả gói tài liệu và soạn trả lời comment của reviewer | Sửa file trong lúc audit, trừ khi bạn yêu cầu sửa |
| Trả lời câu hỏi "nên làm gì" bằng các phương án là kỹ thuật của PMBOK 6 hoặc Book of Forms, kèm đánh đổi sách nêu, rồi tính các con số suy ra và liệt kê các form phải đổi (mục 8) | Cắt estimate cho vừa ngày hay vừa tiền, bịa người chịu trách nhiệm, ngưỡng hay điểm số, hoặc quyết thay sponsor; khi phạm vi, tiến độ, chi phí và chất lượng không thể cùng giữ, nó đưa về change request (3.3) gửi sponsor |

Markdown trong `docs/` là nguồn gốc. File `.docx` và Google Doc đều được dựng từ Markdown.

## 2. Chuẩn bị

| Cần có | Để làm gì | Kiểm tra |
| --- | --- | --- |
| Claude Code, mở tại thư mục gốc repo | Skill gắn với project và script dùng đường dẫn trong repo | Gõ `/` thấy `/pm` |
| Python 3 | Mọi script là Python thuần (đã thử trên 3.9 và 3.14) | `python3 --version` |
| `pdftotext` (poppler) | `extract_form.py` đọc chữ trong sách | `pdftotext -v` |
| `uv` | Chạy `md_to_docx.py`, test và công cụ Google kèm thư viện cần thiết | `uv --version` |
| `A_Project_Managers_Book_of_Forms.pdf` ở thư mục gốc | Căn cứ cho mọi form | `ls A_Project_Managers_Book_of_Forms.pdf` |
| `~/.config/qldapm/client_secret.json` | Chỉ cần khi đọc hoặc ghi Google Doc | xem README, mục Google Doc |

Số trang: skill và script dùng **trang PDF**. Trang PDF = trang in + 11. Khi trích dẫn ghi cả hai, ví
dụ "form 2.32, PDF page 141 (printed page 130)".

## 3. Cách yêu cầu một form

Hỏi bằng tiếng Anh hay tiếng Việt đều được. Nêu số hiệu form là cách nhanh nhất để ra đúng form.

| Bạn muốn | Ví dụ câu lệnh |
| --- | --- |
| Một form đã điền | `Make the 2.32 Risk Register from the risks in the charter. Keep the R numbers; we have not scored probability or impact yet.` |
| Một form đã điền, hỏi bằng tiếng Việt | `Tạo cho nhóm form 1.3 Stakeholder Register từ charter, đúng form trong sách nhé. Nội dung tiếng Anh.` |
| Một form trống | `Give me a blank 4.2 Project Status Report for the team, we'll fill it in every week.` |
| Một form trống, hỏi bằng tiếng Việt | `Cho mình form 2.14 Milestone List để trống, nhóm sẽ tự điền.` |
| Một bản audit | `Audit docs/charter-package.en.md and docs/scope-package.en.md before we push them. Errors and warnings with locations. Don't fix anything.` |
| Một bản audit, hỏi bằng tiếng Việt | `Kiểm tra docs/forms/2-18-project-schedule.en.md so với charter và scope package, liệt kê lỗi và cảnh báo, đừng sửa file.` |
| Một file Word | `Render docs/forms/2-32-risk-register.en.md to .docx for submission.` |
| Một quyết định | `The mobile work is two weeks late against its milestone. What are my options and what do I update?` (mục 8) |
| Một quyết định, hỏi bằng tiếng Việt | `khach hang muon them chuc nang moi thi ghi vao dau?` (mục 8) |

Bạn cũng có thể gọi skill trực tiếp bằng slash command:

```text
/pm 2.32                      điền form 2.32 từ tài liệu dự án
/pm risk register             như trên, gọi bằng tên
/pm 4.2 blank                 form trống, không có giá trị dự án
/pm audit docs/charter-package.en.md docs/scope-package.en.md
```

Mẹo:

- **Ngôn ngữ nội dung.** Sản phẩm viết bằng tiếng Anh kể cả khi bạn hỏi bằng tiếng Việt. Muốn khác thì
  nói rõ.
- **Tên mơ hồ.** "risk" khớp sáu form (2.31, 2.32, 2.33, 2.34, 2.36, 4.5). Skill liệt kê và hỏi lại
  thay vì đoán.
- **Thiếu dữ liệu.** Nếu tài liệu không có giá trị form cần, skill sẽ hỏi bạn hoặc để trống. Hãy trả
  lời câu hỏi; đừng bảo nó "cứ điền đại".
- **Ghi ra đâu.** Form mới được ghi vào `docs/forms/<number>-<slug>.en.md`, ví dụ
  `docs/forms/2-32-risk-register.en.md`. Skill không ghi đè file có sẵn trừ khi được bảo.

## 4. Từ yêu cầu đến sản phẩm

```text
yêu cầu
  1. xác định form             references/forms-index.md, extract_form.py
  2. đọc form in               extract_form.py --fields và --knowledge, thêm trang PDF với form dạng biểu đồ
  3. thu thập dữ liệu dự án    docs/charter-package.en.md, docs/scope-package.en.md, docs/forms/
  4. dựng khung rồi điền       new_form.py, sau đó sửa Markdown
  5. kiểm tra                  check_fidelity.py, check_consistency.py, tools/check_scope.py, form_graph.py --impact, đọc lại
  6. xuất Word (nếu yêu cầu)   md_to_docx.py
  7. đẩy lên Doc (nếu yêu cầu) tools/gdoc*.py, sau khi audit payload
```

Claude chạy các bước này cho bạn. Bạn có thể tự chạy bất kỳ lệnh nào để xem đúng thứ Claude đã thấy.

### Bước 1 và 2: form nào, và form in gì

```bash
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --fields                 # nhãn in trên form, không cần PDF
python3 .claude/skills/pm/scripts/extract_form.py 2.32                          # bảng Document Element và chữ của form trống
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --alignment --tailoring  # thêm mục Alignment và Tailoring Tips
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --prose                  # toàn bộ phần mô tả
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --knowledge              # mỗi trường chứa gì, nguồn, nơi nhận, quyết định; không cần PDF
python3 .claude/skills/pm/scripts/extract_form.py risk                          # liệt kê sáu form khớp, thoát mã 1
```

Kết quả `--fields` của 2.32, rút gọn:

```text
Title block: Project Title | Date Prepared
Page 1 of 1 (PDF page 141)
  table, bank 1: ID | Risk Statement | Owner | Probability | Impact: Scope | ... | Score | Response
  table, bank 2: Revised Probability | Impact: Scope | ... | Responsible Party | Actions | Status | Comments
Notes: ... Bank 2 prints no ID column. ...
```

Đọc dòng Notes: nó ghi những gì danh sách nhãn không thể hiện được (bank, nội dung mẫu không được chép,
nhãn in hai lần).

`--knowledge` in `references/knowledge/<form>.json`: mục đích, rồi từng nhãn in kèm điều sách nói nên
ghi vào đó, các tài liệu form này nhận thông tin từ và cung cấp thông tin cho, các tài liệu nó phải
khớp, các tailoring tip, và những quyết định form này ghi lại. Với 2.32, rút gọn:

```text
Fields, printed label then what goes in it (13):
  - ID [book element: Risk ID]
      A unique identifier for the risk. The blank form prints the column as ID.
  - Risk Statement [book element: Risk statement]
      The risk event or condition. Usually phrased 'EVENT may occur, causing IMPACT' or ...
Sources, information this form receives from (19):
  - 1.2
      Assumption log: reviewed as a source of risks ...; the book does not say which fields are used
Alignment, must agree with: none listed in the book
Tailoring tips: none printed for this form
Decisions recorded here (6):
  - Which response strategy a risk gets now
      Recorded in: Response
```

"The book does not say" nghĩa là sách im lặng và nhóm tự quyết. Khi nhãn trong knowledge khác nhãn trên
form trống (2.32 in `ID` còn bảng element ghi `Risk ID`), form trống thắng; chép nhãn từ `--fields`.

### Bước 3: dữ liệu dự án nằm ở đâu

| Dữ liệu | File và vị trí |
| --- | --- |
| Vấn đề, sản phẩm, người dùng, chức năng F01 to F12, trường hợp ngoại lệ | `docs/charter-package.en.md`, Part 1, 1.1 |
| Sản phẩm bàn giao D1 to D11 | như trên, 1.2 |
| Tiêu chí nghiệm thu A01 to A12 | như trên, 1.3 |
| Loại trừ, ràng buộc, giả định 1 to 19 | như trên, 1.4 đến 1.6 |
| Các phần tử charter: rủi ro R1 to R12, mốc M0 to M7, ngân sách, stakeholder | `docs/charter-package.en.md`, Part 2A |
| Form 1.1 đã điền | `docs/charter-package.en.md`, Part 2B |
| Yêu cầu BR, FR, NFR và RTM (2.7) | `docs/scope-package.en.md`, Part 1 và 1B |
| WBS (2.9) và WBS dictionary (2.10), mã nguồn lực PM, DEV1 to DEV3, QA1, MOB1 | như trên, Part 2 và 3 |
| Lịch dự án (2.18) và change request cho các mốc bị dời (3.3) | `docs/forms/2-18-project-schedule.en.md`, `docs/forms/3-3-change-request.en.md` |

### Bước 4: dựng khung rồi điền

```bash
python3 .claude/skills/pm/scripts/new_form.py 2.32                    # in form trống ra màn hình, không ghi gì
python3 .claude/skills/pm/scripts/new_form.py 2.32 --out <path>       # ghi vào nơi bạn chọn (đường dẫn tạm khi audit)
python3 .claude/skills/pm/scripts/new_form.py 2.32 --docs --rows 12   # docs/forms/2-32-risk-register.en.md, 12 dòng trống
python3 .claude/skills/pm/scripts/new_form.py 2.32 --docs --force     # ghi đè file đã có
python3 .claude/skills/pm/scripts/new_form.py 4.2 --out <thư mục>/ --dated 2026-10-19   # bản có ngày của báo cáo định kỳ, ghi vào một thư mục ngoài docs/
python3 .claude/skills/pm/scripts/risk_actions.py docs/scope-package.en.md          # ô Actions của 2.32 cho từng rủi ro, lấy từ coverage check
```

Chỉ `--docs` (và `--dated` khi không có `--out`) mới ghi vào `docs/`. `Project Title` để trống: chép từ khối tiêu đề của charter khi bạn điền form.

Khung của 2.32 bắt đầu như sau:

```markdown
# 2.32 Risk Register

*Form 2.32, A Project Manager's Book of Forms, 3rd edition, PDF page 141 (printed page 130). The table
prints in two banks, one above the other; row N of the second table continues row N of the first.*

**Project Title:**
**Date Prepared:**

| ID | Risk Statement | Owner | Probability | Impact: Scope | Impact: Quality | Impact: Schedule | Impact: Cost | Score | Response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Form trống chính là khung này, không thêm gì: không tên, ngày, số tiền hay ID.

Mỗi loại form thành Markdown như sau:

| Kind | Dạng Markdown |
| --- | --- |
| `fields` | Bảng `Field \| Content`, nhãn in đậm bên trái, đúng thứ tự in |
| `log` | Một bảng, mỗi cột in là một cột; register rộng (2.32, 2.36, 3.1) thành hai bảng, mỗi bảng một bank in |
| `matrix` | Lưới với nhãn dòng ở cột đầu, giữ chú giải in bên dưới |
| `outline` | Danh sách đánh số lồng nhau (2.9, 2.29), không bao giờ là bảng Code / Element |
| `chart`, `diagram` | Bảng dữ liệu đằng sau hình, kèm một khối Mermaid |
| `narrative` | Các câu mở đầu in sẵn, điền phần trống (6.1) |

Cột nằm dưới một header nhóm in sẵn được viết `Group: Label`, ví dụ `Impact: Scope`. Không viết
`Impact Scope`, không viết `Scope (Impact)`.

### Bước 5: kiểm tra

```bash
python3 .claude/skills/pm/scripts/check_fidelity.py docs/forms/2-32-risk-register.en.md 2.32
python3 .claude/skills/pm/scripts/check_consistency.py docs/forms/2-32-risk-register.en.md \
    docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/2-32-risk-register.en.md
python3 tools/check_scope.py         # chỉ khi scope package hoặc thứ nó cộng dồn lên bị thay đổi
```

| Kiểm tra | Trả lời câu hỏi | Báo lỗi (exit 1) khi |
| --- | --- | --- |
| `check_fidelity.py` | Markdown có đủ mọi nhãn in, đúng chính tả, đúng thứ tự in không? | Thiếu nhãn hoặc sai thứ tự. Nhãn không có trên form chỉ được liệt kê, không làm hỏng kiểm tra. `--flattened` chấp nhận RTM và WBS dictionary của scope package, nơi tiêu đề nhóm in được viết thành nhãn con hoặc thành nhóm cộng nhãn con, và liệt kê chúng; `--ignore-tables` bỏ qua bảng nằm trong ô văn bản tự do; `--page N` kiểm một trang in của form mà tài liệu viết tách ra |
| `check_consistency.py --report <form>` | Form mới có khớp với charter và scope package không? | Bất kỳ lỗi nào do form mới gây ra. Lỗi cũ trong tài liệu nguồn chỉ được đếm, không hiển thị (`--show-context` liệt kê chúng kèm đề mục chứa chúng; `--group` in một dòng cho mỗi loại kiểm tra, trừ mỗi `form-note` giữ một dòng riêng kèm đoạn trích; `--today YYYY-MM-DD` so mỗi Date Prepared với ngày đó; hai từ `charter` và `scope` thay cho hai file package) |
| `tools/check_scope.py` | Scope package còn cộng đủ 4,400 giờ và 700,000,000 VND không? | Bất kỳ kiểm tra nào của nó |

Một form sạch in ra, ví dụ:

```text
2.32 Risk Register, 2-32-risk-register.en.md lines 1 to 18
22/22 printed labels present in printed order
```

Sau script, skill liệt kê các tài liệu mà sách nói form này phải khớp và báo mâu thuẫn:

```bash
python3 .claude/skills/pm/scripts/form_graph.py 2.32                      # nguồn, nơi nhận, form phải khớp
python3 .claude/skills/pm/scripts/form_graph.py --impact 2.9 2.10 --depth 1   # tài liệu cần xem lại khi nhiều form đổi cùng lúc
```

`--impact` đánh dấu mỗi tài liệu đã có trong `docs/` hay chưa, đếm số file (2.9 và 2.10 chung một file) và báo "Nothing to compare" khi không có tài liệu nào, nên skill chỉ đọc những gì đang tồn tại.
Một liên kết được tính khi một trong hai form khai báo nó, và nhãn cho biết bên nào khai báo. Mục 11 giải
thích cách đọc một kiểm tra bị lỗi.

### Bước 6: file Word

```bash
uv run --with python-docx .claude/skills/pm/scripts/md_to_docx.py docs/forms/2-32-risk-register.en.md
uv run --with python-docx .claude/skills/pm/scripts/md_to_docx.py docs/forms/2-32-risk-register.en.md -o /tmp/risk.docx
```

File `.docx` có thanh tiêu đề tối màu như sách, bảng có viền, các cặp trường đặt cạnh nhau như form in,
và chân trang "Page N of M". Khối Mermaid bị bỏ qua; bảng phía trên đã chứa số liệu. Chỉ xuất Word khi
tài liệu dùng để nộp hoặc in.

### Bước 7: Google Doc của nhóm

Doc là bản sao của Markdown. Sửa Markdown rồi dựng lại Doc; không bao giờ sửa tay trên Doc.

- Chỉ khi được yêu cầu, và chỉ với Doc ID truyền qua dòng lệnh (ID nằm trong `README.md`, mục Google
  Doc). Không ai ghi ID vào file.
- Cài đặt một lần cho mỗi máy: `README.md`, mục Google Doc.
- Doc có nhiều tab, mỗi tab có generator riêng. Dùng đúng cái tương ứng:

| Phần của Doc | Payload dựng bởi | Ghi bởi |
| --- | --- | --- |
| Tab scope baseline | `python3 tools/scope_tab3.py --out <scratch>/tab3.md` | `tools/gdoc_tab3.py`, `tools/gdoc_scope_sync.py` |
| Tab lịch (2.18, 3.3) | `gdoc_schedule_tab.build()` | `tools/gdoc_schedule_tab.py` |
| Cả tài liệu, chỉ một tab | `tools/gdoc.py` | `gdoc.py import-html` (Doc mới) |

- **Không bao giờ chạy `gdoc.py replace` trên Doc của nhóm.** Lệnh này import lại toàn bộ file và gộp
  Doc nhiều tab thành một tab.
- Dựng và kiểm tra payload trước khi đẩy, vì thứ lên Doc là thứ generator sinh ra. Các lệnh này không
  cần đăng nhập:

```bash
python3 tools/scope_tab3.py --out /tmp/tab3.md
PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md
python3 .claude/skills/pm/scripts/check_consistency.py /tmp/tab3.md
```

## 5. Ba trạng thái đánh dấu

Mỗi giá trị trong form ở một trong ba trạng thái, và Markdown cho thấy trạng thái nào.

| Trạng thái | Cách viết | Ví dụ |
| --- | --- | --- |
| Đã biết: từ tài liệu dự án hoặc từ bạn | Chữ thường | `700,000,000 VND` |
| Giả định, suy ra hoặc chưa xác nhận | `<mark>...</mark>`, ghi lý do ngay trong ô nếu vừa | `courses of <mark>24 to 48 sessions</mark>` (charter 1.1.1) |
| Chưa biết và không suy ra được | Ô trống, hoặc `[TBD]` khi ô trống trông như bị bỏ sót | `[TBD]` |

Vì sao:

- Đề bài yêu cầu điền form và để trống hoặc tô vàng ô chưa biết. `<mark>` trở thành tô vàng trong
  Google Doc.
- `CLAUDE.md` cấm giá trị đoán mò. Form giấu giá trị đoán làm nhóm tốn một buổi họp để gỡ; form đánh
  dấu rõ giá trị đoán thì xác nhận được trong một lượt đọc.
- `<mark>` là HTML duy nhất được phép. Nó đánh dấu nội dung, không bao giờ đánh dấu nhãn hay tiêu đề.

Ô trống là một trạng thái thật, không phải lỗi: tên project manager trong charter được để trống có chủ
ý, vì sponsor bổ nhiệm PM tại M0 (assumption 15).

## 6. Quy tắc reviewer kiểm tra

Các quy tắc này đến từ hai vòng review trên Doc của nhóm (60 phát hiện). Kiểm tra consistency bắt được
các dòng ghi "script".

| Quy tắc | Viết | Không viết | Bắt bởi |
| --- | --- | --- | --- |
| Một kiểu ngày cho cả tài liệu | `2 September 2026` | `02 September 2026`, `2 Sep 2026`, `2026-09-02` | script |
| Chỉ có thứ trong tuần khi cả bảng đều có | `Mon 14 September 2026` ở mọi dòng | trộn ngày có thứ và không có thứ | script (cảnh báo) |
| Dòng ngân sách 28,000,000 VND là contingency reserve | contingency reserve | `management reserve`, là quỹ của sponsor nằm ngoài baseline; dự án này không có quỹ đó | script |
| Sponsor và customer là hai người | Dr. Nguyễn Mạnh Hùng đi với từ sponsor; Đỗ Thị Bích Ngọc đi với từ customer hoặc Director | "sponsor" cạnh tên customer, hoặc "owner" cạnh tên sponsor | script |
| Không xuống dòng trong ô | `(1) ... (2) ... (3) ...` trên một dòng | `<br>`, vì nó hiện nguyên văn trên Doc | script |
| Chỉ dùng `<mark>` làm HTML | `<mark>` | thẻ hay HTML entity khác | script |
| Không thêm gì vào trong form in | giải thích đặt ở đoạn in nghiêng phía trên form | ghi chú dưới bảng, chữ dưới Approvals, tiêu đề thừa | một phần (cảnh báo) |
| Nhãn title block đúng như in | `**Project Title:**`, `**Date Prepared:**` (hoặc `**Date:**` nếu form in vậy) | `**Project:**`, `**Date prepared:**`, `**Source:**` | fidelity |
| Không thêm cột form không in | 1.3 bắt đầu bằng Name | thêm cột ID vào 1.3, 1.4, 2.14, 6.4 hoặc bank 2 của 2.32, 2.36, 3.1 | fidelity |
| Khoảng ID khớp với phần tử cuối hiện tại | `R1 to R12`, `F01 to F12` | `R1 to R10` khi đã có R12 | script (cảnh báo) |
| Một ID, một nội dung | NFR02 viết giống nhau ở mọi nơi | một ID mang hai nghĩa | script (cảnh báo) |
| `A` nghĩa là tiêu chí nghiệm thu | `A01`, `assumption 18` | `A18` cho một giả định | đọc |
| Tổng phải khớp | các dòng cộng đúng bằng dòng Total | tổng gõ tay | script |
| Văn bản chép thì chép nguyên | câu rủi ro của charter, đúng từng chữ | viết lại theo ý | đọc |
| Không em dash, không emoji | dấu phẩy, chấm phẩy, hai chấm hoặc dấu chấm | em dash, en dash, emoji | script |
| Ghi cả hai số trang | PDF page 141 (printed page 130) | "page 130" | đọc |

Danh sách đầy đủ, kèm các thread review đứng sau mỗi quy tắc, nằm ở
`.claude/skills/pm/references/review-lessons.md`.

## 7. Audit và trả lời comment trên Google Doc

### Audit

Yêu cầu audit khi tài liệu sắp được đẩy lên Doc, hoặc trước hạn chấm điểm. Skill đóng vai reviewer và
không sửa file trừ khi bạn yêu cầu.

Thứ tự skill chạy:

1. Script trên cả gói: `check_consistency.py --audit` trên mọi file cùng lúc (`--audit` còn báo cột toàn
   một giá trị dù văn bản phía trên đã giải thích), `check_fidelity.py` trên từng form (dùng `--section` với
   form nằm trong một package, `--flattened` cho RTM), `check_schedule.py` cho 2.18 (còn so tên mốc với charter;
   `--explained hours` báo chênh lệch giờ mà một 3.3 đang chờ giải thích thành warning; một 3.3 đang chờ không bao giờ giải thích
   được lỗi thứ tự, nên `--explained sequence=LÝ DO` và `break=LÝ DO` phải kèm lý do trích từ tài liệu), `tools/check_scope.py`.
   Thêm `--report <file>` khi chỉ một file là sản phẩm bàn giao. Mỗi lần quét bắt buộc trong `audit-template.md` đều được báo cáo, hoặc là một phát hiện hoặc là một dòng dưới "Scans that found nothing": định dạng ngày, `<br>`, sponsor và khách hàng bị gộp, cách gọi reserve, RTM có Priority chỉ một giá trị (luôn là cảnh báo dù có câu giải thích), cùng một ID giữa Part 1 và 1B.
2. Từng bài học trong `review-lessons.md`, tính lại số liệu suy ra từ giả định.
3. Trình tự: không gì được dùng, nghiệm thu hay ký trước khi nó tồn tại; không ngày nào rơi vào khoảng
   thời gian charter loại trừ. `check_schedule.py` bắt việc kiểm tra đặt trước đối tượng của nó, đóng dự án trước
   tháng bảo hành hoặc mốc của nó, go-live trước UAT, kiểm thử trước khi build, review trước công việc của package khác, con số trong tên việc hay trong câu của dictionary so với khoảng thời gian của nó,
   và việc nằm trong kỳ nghỉ (là lỗi khi charter nói kỳ nghỉ không chịu thêm độ trễ nào); phần còn lại đọc tay theo công thức trong `audit-template.md` (Used before it exists).
4. Khối lượng mỗi người mỗi tuần so với phân bổ trong charter (`load_check.py docs/scope-package.en.md --limit
   MOB1=<giờ> --leaves MOB1=YYYY-MM-DD`, thêm `--charter`, `--holiday`, `--daily-limit`; `--schedule <file 2.18>` rải giờ theo các dòng của lịch đã cân bằng nguồn lực;
   `--explained overload=LÝ DO` biến quá tải thành cảnh báo nêu tài liệu giải thích; kết quả dùng mặc định 40 giờ có ghi "limit assumed", và khi charter không nêu số giờ mỗi tuần
   của người bán thời gian, mặc định che mất quá tải, nên hỏi sponsor; `python3 tools/level.py` cho lịch đã cân bằng nguồn lực).
5. Form được sinh tự động hoặc payload đẩy lên, khi có liên quan đến Doc (`references/push-audit.md`).

Báo cáo theo mẫu `.claude/skills/pm/references/audit-template.md`:

```text
## Errors        E1, E2, ...   mâu thuẫn chứng minh được bằng hai trích dẫn
## Warnings      W1, W2, ...   điểm yếu người chấm có thể bắt
## Scans that found nothing    mỗi lần quét không có kết quả, để người đọc biết nó đã chạy
## What passed                 các kiểm tra khác không phát hiện gì
```

Mỗi phát hiện có vị trí (`file:line` và mục hoặc trang form), trích dẫn bằng chứng, và cách sửa hoặc
quyết định cần đưa ra và ai quyết định.

Lệnh hữu ích khi audit:

```bash
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 .claude/skills/pm/scripts/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:" --flattened
python3 .claude/skills/pm/scripts/load_check.py docs/scope-package.en.md --limit MOB1=20 --leaves MOB1=2026-12-18
python3 tools/check_scope.py
python3 tools/level.py
```

### Trả lời comment trên Doc

Ví dụ hỏi `Trả lời các comment còn mở trên Doc của nhóm` và đưa Doc ID. Skill liệt kê các thread cùng
đoạn văn mỗi thread gắn vào, soạn câu trả lời, và cho bạn xem trước những gì sẽ đăng trước khi đăng.

```bash
gdoc() { uv run --with google-api-python-client,google-auth-oauthlib,markdown tools/gdoc.py "$@"; }
gdoc comments --doc DOC_ID                                         # các thread và đoạn văn được gắn
gdoc post --doc DOC_ID --review review/<date>-doc-review.json --dry-run
gdoc post --doc DOC_ID --review review/<date>-doc-review.json
```

Cách viết câu trả lời (`review-lessons.md` mục 11):

1. Đồng ý hay không ngay ở từ đầu tiên ("Đồng ý", "Đã bỏ", "Đã thêm").
2. Nói rõ đã đổi gì và ở đâu: mục, ô, phiên bản.
3. Trích câu mới bằng tiếng Anh khi tài liệu gốc là tiếng Anh.
4. Liệt kê các chỗ khác bị sửa theo.
5. Khi yêu cầu xung đột với ràng buộc cố định (ngân sách, thời gian), nêu ràng buộc đó và cái giá của
   việc đánh đổi, để nhóm quyết định.
6. Trả lời bằng ngôn ngữ của reviewer.

`post` là idempotent: câu trả lời có dòng đầu đã có trên Doc sẽ được bỏ qua.

## 8. Ra quyết định: hỏi nên làm gì

Form ghi lại quyết định; form không đưa ra quyết định. Khi bạn hỏi nên làm gì ("trễ hai tuần rồi", "R5
xảy ra rồi", "khách hàng muốn thêm chức năng mới", "điền form nào đây?"), skill đi theo đường quyết định
và kết thúc ở các form ghi lại quyết định đó.

```text
tình huống
  1. định tuyến                references/decisions.md (40 dòng định tuyến, 43 quyết định), references/pmbok-<area>.md
  2. tính các số suy ra        scripts/pm_calc.py
  3. liệt kê thứ khác phải đổi scripts/form_graph.py --impact
  4. trình bày                 định dạng khuyến nghị ở mục 5 của decisions.md
  5. ghi lại (sau khi bạn đồng ý) 3.2 Decision Log; 3.3 Change Request rồi 3.4 Change Log khi baseline đổi
```

### Câu lệnh ví dụ

| Tình huống | Câu lệnh ví dụ | Nhận lại gì |
| --- | --- | --- |
| Trễ tiến độ | `The mobile application work (WBS 1.5.4, due for M5) is two weeks late. What are my options, which are allowed, and what do I update? I do not want an answer that just says the estimate was wrong.` | Crashing và fast tracking (PMBOK 6 section 6.5.2.6) kèm đánh đổi, phần 2.18 đã dùng rồi, giới hạn dự phòng và quyền hạn lấy từ charter, change request gửi sponsor, các form phải cập nhật |
| Tình trạng earned value | `BAC 700,000,000; PV 280,000,000; EV 252,000,000; AC 294,000,000 VND. Give me the status, a forecast at completion and what goes in form 4.4.` | CV, SV, CPI, SPI, ba EAC và TCPI từ `pm_calc.py evm`, cách gọi tình trạng của PMBOK 6 Table 7-1, các trường của 4.4, ngưỡng leo thang 5% |
| Rủi ro đã xảy ra | `R5 has happened: the notification gateway is unstable and the price went up. What do we do, and what do I write in the register and the decision log? I do not know who owns it.` | Các chiến lược của 11.5, contingency reserve trong giới hạn của charter, nội dung đề xuất cho 2.32 và 3.2, để trống người phụ trách và điểm số |
| Dùng form nào | `khach hang muon them chuc nang moi thi ghi vao dau?` | 3.3 rồi 3.4, sponsor quyết định, 2.7 và scope baseline 2.8 đến 2.10 chỉ đổi sau khi duyệt, trả lời bằng tiếng Việt |
| Ghi ở đâu | `Where do I write down why we chose a second provider?` | 3.2 Decision Log, cột Comments ghi các phương án và lý do |

Các câu hỏi trên hỏi bằng tiếng Việt cũng được; câu trả lời theo ngôn ngữ bạn hỏi.

### Câu trả lời gồm những gì

Định dạng khuyến nghị (`decisions.md` mục 5) có tám phần: tình huống kèm tài liệu và mục mà mỗi dữ kiện
đến từ đó; kiểm tra ràng buộc (cái nào trong phạm vi, tiến độ, chi phí, chất lượng, nguồn lực và rủi ro
đang chặt, phương án chạm baseline nào, quyền hạn của PM có đủ không); bảng phương án (kỹ thuật kèm trích
dẫn, đánh đổi sách nêu hoặc "not stated in the book", ảnh hưởng đến baseline); một khuyến nghị; kết quả
máy tính; nhóm phải quyết định gì và ai quyết; các form cần cập nhật kèm trường in; và trích dẫn có cả hai
số trang. Những dữ kiện như giới hạn dự phòng 20,000,000 VND, ngưỡng sai lệch 5% hay ngày của một mốc
được đọc từ charter và các package mỗi lần; danh mục quyết định không lưu chúng. Nó giữ một danh sách các giới
hạn quyền hạn cần đọc (mỗi giao dịch, mỗi lần dùng dự phòng, phần trăm vượt dự báo và cơ sở tính, thay đổi vốn,
loại dự phòng và rủi ro nào được rút) mà các quyết định về trễ tiến độ, sai lệch, dự báo và dự phòng đều trỏ tới.
Câu hỏi như "tôi viết gì" hay "báo gì cho sponsor" được trả lời bằng bản nháp ngay trong câu trả lời, không tạo file.

### Các quy tắc skill giữ

Đây là quy tắc của nhóm, được nhắc lại trong `SKILL.md` và `decisions.md`.

- Mọi cách xử lý là một kỹ thuật PMBOK 6 hoặc Book of Forms có nêu tên, kèm đánh đổi sách nêu. Nếu sách
  không nêu, câu trả lời ghi "not stated in the book" và đánh dấu đó là phán đoán.
- Không bao giờ cắt estimate cho vừa ngày hay vừa tiền.
- Khi phạm vi, tiến độ, chi phí và chất lượng không thể cùng giữ, đường đi là change request (3.3) gửi
  sponsor.
- Contingency reserve (nằm trong cost baseline, dành cho rủi ro đã nhận diện) khác management reserve
  (nằm ngoài). Khi charter gọi reserve khác với dòng ngân sách, câu trả lời nêu cả hai cách gọi như một lỗi nguồn để sponsor quyết định.
- Câu hỏi hẹp (một con số trạng thái, dùng form nào) nhận câu trả lời ngắn kèm ba form cần viết trước; định dạng bảy phần đầy đủ dành cho quyết định làm dịch chuyển baseline hoặc đòi phương án.
- Không bịa người chịu trách nhiệm, ngưỡng, điểm số, đơn giá hay ngày; hỏi lại hoặc để trống.
- Không ghi gì vào `docs/` nếu bạn chưa yêu cầu.

### pm_calc.py: các con số

Python thuần, không cần gói nào. Mỗi kết quả in kèm trang sách in công thức đó, cả trang PDF và trang in.
`--json` cho đầu ra đọc bằng máy.

| Lệnh con | Tính | Sách in ở đâu |
| --- | --- | --- |
| `evm` | CV, SV, CPI, SPI, phần trăm kế hoạch, đạt được và đã chi, ba EAC, ETC, VAC, TCPI (TCPI hướng tới EAC theo CPI hiện tại bằng đúng CPI và hướng tới EAC theo tỷ lệ ngân sách bằng 1, nên hai dòng đó không kèm lời của Table 7-1); `--threshold` và `--base` thêm mức vượt dưới dạng phần trăm của BAC, PV, EV hoặc AC cùng số tiền của ngưỡng và đánh dấu trong hay ngoài ngưỡng; chỉ `--bac` với `--threshold` thì in số tiền | PMBOK 6 section 7.4.2.2 và Table 7-1; Book of Forms 4.4. Phần trăm là công cụ tính ngoài sách: không sách nào in phần trăm sai lệch |
| `pert` | Trung bình beta và tam giác của ba estimate | Book of Forms 2.17, 2.21; PMBOK 6 section 6.4.2.4, 7.2.2.5 |
| `effort-to-duration` | Thời lượng từ công sức, số lượng, phần trăm sẵn sàng và hệ số năng suất | Book of Forms 2.17, Table 2.16 |
| `analogous` | Estimate từ giá trị trước và tỉ lệ kích thước | Book of Forms 2.17, 2.21 |
| `bottom-up` | Chi phí bằng giờ x đơn giá cộng vật tư và các phần còn lại | Book of Forms 2.21, Table 2.20 |
| `risk-score` | High, Medium hoặc Low từ xác suất và tác động; `--matrix` in lưới 2.35 | Book of Forms 2.34 Table 2.31, 2.35; PMBOK 6 Figure 11-5 |
| `emv` | Giá trị tiền tệ kỳ vọng và cây quyết định với `--option` | PMBOK 6 section 11.4.2.5, Figure 11-15 |
| `weighted-score` | Điểm theo tiêu chí có trọng số và phương án thắng | Book of Forms 2.39, Table 2.35 |
| `earned-schedule` | SV(t) = ES - AT, SPI(t) = ES / AT | PMBOK 6, Trends and Emerging Practices in Project Cost Management, printed page 233 (PDF page 272) |
| `crash` | Các phương án crashing xếp theo chi phí thêm cho mỗi ngày rút được, và những phương án rẻ nhất đạt `--needed` ngày; chỉ việc trên đường găng, với thời lượng và chi phí crash do nhóm đưa ra | PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254) định nghĩa crashing là chi phí gia tăng thấp nhất và không in công thức; được ghi là công cụ tính ngoài sách |
| `cpm` | Ngày sớm và muộn, float tổng và float tự do, đường găng, `--deadline` (số ngày làm việc từ ngày 1, hoặc một ngày kèm `--start`), kịch bản `--slip`; `--start` và `--holiday` đổi ngày làm việc thành ngày lịch và cho biết độ trễ có vượt qua kỳ nghỉ không | PMBOK 6 section 6.5.2.2 và Figure 6-16 mô tả các lượt tính và không in công thức; được ghi là công cụ tính ngoài sách |
| `velocity` | Velocity mỗi iteration, trung bình, số iteration còn lại | Agile Practice Guide section 5.4.1, printed page 64 (PDF page 874); trung bình và dự báo là công cụ tính ngoài sách |
| `cd3` | Xếp hạng theo chi phí trì hoãn chia cho thời lượng | Agile Practice Guide Table 5-1, printed page 59 (PDF page 869); Guide chỉ in lời, không in đơn vị |
| `payback` | Kỳ đầu tiên mà lợi ích ròng tích lũy đạt vốn đầu tư | PMBOK 6 nêu payback và không in công thức; được ghi là công cụ tính ngoài sách |
| `comms-channels` | n(n-1)/2 | Cả hai sách đều không in; được ghi là công cụ tính ngoài sách |
| `reserve` | Dự phòng rủi ro còn lại so với giá trị kỳ vọng của các rủi ro còn mở | PMBOK 6 section 11.7.2.1, printed page 456 (PDF page 495) nêu phép so sánh và không in công thức; được ghi là công cụ tính ngoài sách |
| `funding` | Vốn đã giải ngân theo từng đợt so với chi phí đến nay | PMBOK 6 section 7.3.3.2, printed page 256 (PDF page 295), và Figure 7-9; được ghi là công cụ tính ngoài sách |
| `response-effectiveness` | (thay đổi mức tác động) / (chi phí thực hiện) của từng biện pháp | PMBOK 6 section 11.5.2.8, printed page 446 (PDF page 485) |

```bash
python3 .claude/skills/pm/scripts/pm_calc.py evm --bac 700000000 --pv 280000000 --ev 252000000 --ac 294000000
```

```text
Variances and indexes (no assumption beyond the inputs)
  CV                                 -42000000  (over planned cost)  [1]
  SV                                 -28000000  (behind schedule)  [1]
  CPI                                0.8571  (over planned cost)  [2]
  SPI                                0.9  (behind schedule)  [2]
EAC at the present CPI
  EAC                                816666666.6667  [6]
      formula: EAC = BAC / CPI
      assumption: The cumulative CPI to date continues for all remaining work.
Sources
  [1] PMBOK 6 section 7.4.2.2, printed page 262 (PDF page 301); PMBOK 6 Table 7-1, printed page 267 (PDF page 306); ...
```

Công cụ sẽ không làm gì:

- Chỗ hai cuốn sách không in công thức, nó ghi "not stated in the book": độ lệch chuẩn của beta, thời
  gian hoàn vốn, phần trăm sai lệch. Nó không tự thêm công thức.
- Nó từ chối đầu vào mà công thức không nhận được (BAC bằng không, xác suất âm, `nan`) và nói rõ vì sao;
  AC hoặc PV bằng không thì không có CPI hay SPI và đầu ra nói như vậy. Nó không thay bằng một giá trị khác.
- Nó in tối đa bốn chữ số thập phân, không làm tròn. Không cuốn sách nào nêu quy tắc làm tròn; chỉ số được
  báo như công cụ in (CPI 0.8621 không được ghi thành 0.86 cho đẹp), kèm các từ của Table 7-1, tiền theo
  đồng nguyên, so với ngưỡng bằng giá trị chưa làm tròn. Phần trăm vượt chi là công cụ tính ngoài sách, kèm cơ sở tính.
- Phần văn xuôi của form 2.17 nói người giỏi thì nhanh hơn, còn công thức in lại chia cho hệ số. Công cụ
  theo công thức in và ví dụ in (150 giờ công, 2 người, 75 phần trăm, hệ số 0.8 ra 125 giờ) và in một ghi
  chú về chỗ không khớp này. Hãy báo nhóm bạn dùng cách đọc nào.
- Table 2.31 in 80 phần trăm ở hai dải xác suất; công cụ từ chối `80%` trơn và hỏi từ chỉ mức.

### form_graph.py: còn gì khác phải đổi

66 form dưới dạng đồ thị, dựng từ các danh sách `receives_from`, `provides_to` và `alignment` trong
`references/knowledge/`.

| Lệnh | In ra |
| --- | --- |
| `form_graph.py 3.3` | Nguồn, nơi nhận và form phải khớp của một form, cái gì chảy qua, và bên nào khai báo từng liên kết |
| `form_graph.py --impact 2.9 2.10 --depth 1` | Tài liệu cần xem lại khi một hay nhiều form đổi, xếp theo khoảng cách, mỗi dòng ghi đã có trong docs/ hay chưa (hoặc là mục thay thế: charter giữ nội dung của 1.2, 1.3, 2.6, 2.14 và 2.32, đếm riêng), kèm số file và một dòng nói form đang đổi nhận từ đâu; câu trả lời nêu đủ mọi form được liệt kê, không bỏ, không thêm; `--category` giới hạn 3.3 vào một số nhóm Impacts of Change; không có `--depth` thì đi theo liên kết đến hết |
| `form_graph.py --order [--group Planning]` | Thứ tự tạo form theo trình tự quy trình PMBOK (9.1 và 9.2 xếp trước 6.4 vì chúng tạo đầu vào của 6.4); các form thuộc nhóm Executing, Monitoring and Controlling và Closing được liệt kê riêng, mỗi form gắn nhãn bước của bản đầu và lúc nó hoàn tất; liên kết từ quy trình sau về quy trình trước là đầu vào để sửa lại, và các cạnh bị cắt được in ra; 2.27, 2.39 và 4.8, mà sách chỉ nói là khớp với một kế hoạch, cùng 4.3, 4.4, 4.6 và 4.7 nhận các kế hoạch và baseline mà chúng đo làm điều kiện tiên quyết, gắn nhãn là ánh xạ của skill |
| `form_graph.py --check` | Liên kết một form khai báo mà form kia không khai báo |
| `form_graph.py --markdown [--out F]` | In ra bản đồ form; `--out` ghi vào file (bản đã commit là `references/form-graph.md`, và một test báo lỗi khi bản đó cũ) |

```text
$ python3 .claude/skills/pm/scripts/form_graph.py --impact 3.3 --depth 1 --category Cost
Recheck when 3.3 Change Request changes (6 documents, within 1 edge):
  1  2.2 Change Management Plan  [not in docs]  (3.3 provides to it)
  1  2.20 Cost Estimates  [not in docs]  (3.3 Impacts of Change: Cost; skill mapping, not book text)
  1  2.21 Cost Estimating Worksheet  [not in docs]  (3.3 Impacts of Change: Cost; skill mapping, not book text)
  1  2.22 Cost Baseline  [not in docs]  (3.3 Impacts of Change: Cost; skill mapping, not book text)
  1  3.4 Change Log  [not in docs]  (3.3 provides to it)
  1  Change control board (external)  [external, no form]  (3.3 provides to it)

0 of 5 forms exist in docs/, in 0 files.
Nothing to compare: none of these 5 forms exists in docs/. Say so, list them as forms to create or update later, and do not paste the rows as if they were documents to recheck.
Changed form lives in: forms/3-3-change-request.en.md (3.3)
```

Without `--category`, 3.3 also lists the forms of the other categories (Scope, Quality, Requirements,
Schedule, Stakeholder Impact, Project Documents, and resources and risk), and the forms whose results may become
a 3.3 (2.18, 2.32, 2.40, 3.6, 4.3, 4.4, 4.6) point back to it. Those rows are tagged `skill mapping, not book text`: the
book lists the categories on 3.3 (Book of Forms form 3.3, PDF pages 181 to 182 (printed pages 170 to 171)),
and the mapping from a category to the forms of the matching knowledge area is the skill's.

Đọc kết quả cẩn thận:

- Scope baseline là hợp thể duy nhất: 2.8, 2.9 và 2.10 gộp lại (Book of Forms form 2.9, PDF page 60
  (printed page 49)). Form nhận từ hoặc phải khớp với scope baseline được liệt kê theo cả ba. Schedule
  baseline và project budget là tên bên ngoài vì sách không gọi tên form nào cho chúng.
- Sách thường chỉ nói form này cung cấp cho form kia, không nói trường nào chảy qua. Dòng chữ trên mỗi
  liên kết ghi đúng điều đó; đừng suy thành ánh xạ trường.
- `--check` báo 340 liên kết một chiều (117 `provides_to`, 68 `receives_from`, 155 alignment). Phần lớn là
  một form liệt kê nơi nhận mà nơi nhận không liệt kê lại. Đó là sách im lặng ở một phía, hoặc khoảng
  trống trong các file knowledge, không phải lỗi của dự án.
- `--order` cắt mọi liên kết đi từ form của quy trình PMBOK 6 sau về form của quy trình trước (nhóm quy
  trình, rồi chương và mục, rồi số form), nên 1.3 đứng trước 2.4 và 2.16 trước 2.18. Risk register 2.32,
  risk report 2.33, issue log 3.1 và decision log 3.2 được tạo từ đầu dự án (Book of Forms form 2.32, PDF
  page 140 (printed page 129); 2.33, PDF page 142 (printed page 131); 3.1, PDF page 176 (printed page 165);
  3.2, PDF page 179 (printed page 168)), nên các liên kết đến chúng là đầu vào để sửa lại. Thứ tự này là
  cách đọc của skill trên các liên kết đã ghi, không phải của sách.

### Giới hạn

- Danh mục quyết định và các ghi chú PMBOK được viết từ hai cuốn sách và kiểm hai lượt. Số trang PMBOK
  trong các mục quyết định đã được đối chiếu với PDF. Những nhận định dựa vào Book of Forms chỉ được kiểm
  độ lệch trang, trừ các liên kết của form 2.10, 2.32 và 3.3 và công thức của form 2.16, 2.17, 2.21,
  2.34, 2.35, 2.39, 4.3 và 4.4 đã được đọc trên trang. Hãy coi trích dẫn là con trỏ và mở trang ra trước
  khi trích cho reviewer.
- Danh mục gộp khoảng 100 quyết định theo từng lĩnh vực thành 43 mục xuyên lĩnh vực. Tình huống không khớp
  dòng nào được trả lời từ mục gần nhất, và câu trả lời nói rõ điều đó.
- Skill chỉ khuyến nghị. Sponsor quyết định những gì vượt quyền hạn của project manager, và charter không
  nêu change control board.

## 9. Toàn bộ 66 form

Kind quyết định dạng Markdown (mục 4). Cột "Trong repo" chỉ nơi đã có bản điền sẵn. Tên form giữ
nguyên như in trong sách.

| Form | Name | Kind | Dữ liệu dự án cần có | Trong repo |
| --- | --- | --- | --- | --- |
| 1.1 | Project Charter | fields | Mục đích, mô tả, phạm vi, sản phẩm bàn giao, yêu cầu, rủi ro tổng thể, mục tiêu và tiêu chí thành công, các mốc, ngân sách được duyệt, stakeholder, tiêu chí kết thúc, quyền hạn PM, sponsor | charter Part 2B |
| 1.2 | Assumption Log | log | Giả định 1 to 19 và các ràng buộc, kèm phân loại, người chịu trách nhiệm, hạn, hành động, trạng thái | |
| 1.3 | Stakeholder Register | log | Tên, vị trí hoặc vai trò, liên hệ, yêu cầu, kỳ vọng, phân loại của từng stakeholder | |
| 1.4 | Stakeholder Analysis | log | Từng stakeholder hoặc vai trò với mức quan tâm, ảnh hưởng và thái độ | |
| 2.1 | Project Management Plan | fields | Các giai đoạn vòng đời, hoạt động và sản phẩm, review giai đoạn với tiêu chí vào và ra, cách phát triển từng sản phẩm, các kế hoạch con, ngưỡng sai lệch, quản lý baseline | |
| 2.2 | Change Management Plan | fields | Cách quản lý thay đổi, thế nào là thay đổi lịch, ngân sách, phạm vi hay tài liệu, change control board, quy trình xử lý change request | |
| 2.3 | Project Roadmap | chart | Các giai đoạn với ngày bắt đầu và kết thúc, các mốc lớn | |
| 2.4 | Scope Management Plan | fields | Cách dựng và duy trì WBS và dictionary, nghiệm thu sản phẩm, gắn phạm vi với yêu cầu | |
| 2.5 | Requirements Management Plan | fields | Cách thu thập, phân tích, phân loại, ưu tiên, truy vết, theo dõi, báo cáo, xác nhận yêu cầu và quản lý cấu hình | |
| 2.6 | Requirements Documentation | log | Yêu cầu kèm stakeholder, phân loại, ưu tiên, tiêu chí nghiệm thu, kiểm thử, giai đoạn hoặc bản phát hành | |
| 2.7 | Requirements Traceability Matrix | matrix | ID yêu cầu, nội dung, nguồn, ưu tiên, phân loại; mục tiêu kinh doanh, sản phẩm, verification, validation; yêu cầu kinh doanh đối chiếu yêu cầu kỹ thuật ở trang 2 | scope Part 1, 1B |
| 2.8 | Project Scope Statement | fields | Mô tả phạm vi, sản phẩm bàn giao, tiêu chí nghiệm thu, loại trừ, ràng buộc, giả định | charter Part 1 |
| 2.9 | Work Breakdown Structure | outline | Sản phẩm, control account và work package có mã, theo thứ tự công việc | scope Part 2 |
| 2.10 | WBS Dictionary | fields | Mỗi work package: mô tả, giả định, mốc và hạn, hoạt động với nguồn lực, giờ, đơn giá, vật tư, chi phí, tiêu chí chất lượng và nghiệm thu | scope Part 3 |
| 2.11 | Schedule Management Plan | fields | Phương pháp, công cụ, độ chính xác, đơn vị, ngưỡng sai lệch, báo cáo, quy tắc cập nhật | |
| 2.12 | Activity List | log | Hoạt động của từng work package với ID và mô tả công việc | |
| 2.13 | Activity Attributes | fields | Một hoạt động: hoạt động trước và sau với kiểu quan hệ và lead hoặc lag, nguồn lực, kỹ năng, loại công sức, địa điểm, ngày bắt buộc, giả định | |
| 2.14 | Milestone List | log | Các mốc M0 to M7 với mô tả và loại | |
| 2.15 | Network Diagram | diagram | Hoạt động với hoạt động trước, kiểu quan hệ (FS, SS, FF, SF), lead hoặc lag | |
| 2.16 | Duration Estimates | log | Mỗi hoạt động: số giờ công, ước lượng thời gian | |
| 2.17 | Duration Estimating Worksheet | log | Đầu vào ước lượng parametric, analogous và three-point cho từng hoạt động | |
| 2.18 | Project Schedule | chart | Hoạt động với ID, mã WBS, tên, ngày bắt đầu, ngày kết thúc; các mốc | `docs/forms/2-18-project-schedule.en.md` |
| 2.19 | Cost Management Plan | fields | Đơn vị, độ chi tiết, độ chính xác, ngưỡng kiểm soát, quy tắc đo hiệu suất, báo cáo | |
| 2.20 | Cost Estimates (in là Activity Cost Estimates) | log | Mỗi WBS ID: nguồn lực, chi phí nhân công và vật chất, dự phòng, ước lượng, phương pháp, cơ sở, khoảng, độ tin cậy | |
| 2.21 | Cost Estimating Worksheet | log | Đầu vào chi phí parametric, analogous, three-point và bottom-up | |
| 2.22 | Cost Baseline | chart | Giá trị kế hoạch cộng dồn theo kỳ, từ lịch và ước lượng chi phí | |
| 2.23 | Quality Management Plan | fields | Tiêu chuẩn, mục tiêu kèm thước đo, vai trò chất lượng, sản phẩm và quy trình được review, cách làm QA và QC | |
| 2.24 | Quality Metrics | log | Hạng mục, thước đo, cách đo (từ A01 to A12 và các NFR) | |
| 2.25 | Responsibility Assignment Matrix | matrix | Work package đối chiếu người (PM, DEV1 to DEV3, QA1, MOB1) với R, A, C, I | |
| 2.26 | Resource Management Plan | fields | Vai trò với số lượng, kỹ năng, thời điểm nhận và trả người; trách nhiệm và quyền hạn; cơ cấu; đào tạo; khen thưởng; nguồn lực vật chất | |
| 2.27 | Team Charter | fields | Giá trị chung, quy tắc họp, giao tiếp, ra quyết định và giải quyết xung đột, chữ ký thành viên | |
| 2.28 | Resource Requirements | log | Mỗi ID: nguồn lực, số lượng, giả định | |
| 2.29 | Resource Breakdown Structure | outline | Nguồn lực theo nhóm: người, thiết bị, vật tư, đồ dùng | |
| 2.30 | Communications Management Plan | fields | Mỗi stakeholder: thông tin, phương thức, thời điểm, người gửi; giả định, ràng buộc, bảng thuật ngữ | |
| 2.31 | Risk Management Plan | fields | Chiến lược, phương pháp, vai trò, nhóm rủi ro, ngân sách rủi ro, quy tắc dùng dự phòng, mức chấp nhận rủi ro, định nghĩa xác suất và tác động | |
| 2.32 | Risk Register | log | Rủi ro R1 to R12 với owner, xác suất, tác động lên scope, quality, schedule và cost, điểm, phản ứng, các giá trị sau phản ứng | |
| 2.33 | Risk Report | fields | Tóm tắt, tình trạng và động lực rủi ro tổng thể, số rủi ro theo xác suất và tác động, các chỉ số | |
| 2.34 | Probability and Impact Assessment (in là Probability and Impact Risk Rating) | matrix | Định nghĩa Very High đến Very Low cho từng mục tiêu và cho xác suất, ngưỡng xếp hạng | |
| 2.35 | Probability and Impact Matrix | matrix | Ô xác suất và tác động nào nhóm coi là cao, trung bình, thấp | |
| 2.36 | Risk Data Sheet | log | Một rủi ro chi tiết: nguyên nhân, điểm, phản ứng, rủi ro thứ cấp và còn lại, kế hoạch dự phòng, tiền, thời gian, phương án lùi | |
| 2.37 | Procurement Management Plan | fields | Gắn mua sắm với phạm vi, lịch và rủi ro, thời điểm mua sắm, chỉ số, vai trò, giả định, luật áp dụng và tiền tệ, ước lượng độc lập | |
| 2.38 | Procurement Strategy | fields | Hình thức giao, loại hợp đồng, tiêu chí thưởng, vòng đời mua sắm | |
| 2.39 | Source Selection Criteria | log | Tiêu chí với trọng số và điểm cho từng ứng viên | |
| 2.40 | Stakeholder Engagement Plan | fields | Mức tham gia hiện tại và mong muốn của từng stakeholder, thay đổi sắp tới, quan hệ, cách tiếp cận | |
| 3.1 | Issue Log | log | Vấn đề với loại, mô tả, ưu tiên, tác động, người chịu trách nhiệm, trạng thái, ngày và cách giải quyết | |
| 3.2 | Decision Log | log | Quyết định với phân loại, người chịu trách nhiệm, ngày | |
| 3.3 | Change Request | fields | Người yêu cầu, phân loại, mô tả, lý do, tác động lên scope, quality, requirements, cost, schedule và stakeholder, kết quả xử lý | `docs/forms/3-3-change-request.en.md` |
| 3.4 | Change Log | log | Thay đổi với phân loại, người yêu cầu, ngày nộp, trạng thái, kết quả xử lý | |
| 3.5 | Lessons Learned Register | log | Bài học với phân loại, tác nhân, người chịu trách nhiệm | |
| 3.6 | Quality Audit | fields | Người audit, ngày audit, khu vực audit, thực hành tốt, điểm cần cải thiện, lỗi và hành động | |
| 3.7 | Team Performance Assessment | fields | Đánh giá và nhận xét về hiệu suất kỹ thuật và năng lực giao tiếp | |
| 4.1 | Team Member Status Report | fields | Hoạt động kế hoạch, đã làm và chưa làm của một người, chi phí, sai lệch, kỳ tới | |
| 4.2 | Project Status Report | fields | Kết quả trong kỳ, sai lệch và tác động lên mốc và ngân sách, kỳ tới, rủi ro, vấn đề, thay đổi | |
| 4.3 | Variance Analysis | fields | Kế hoạch so với thực tế cho lịch, chi phí và chất lượng, nguyên nhân gốc, phản ứng | |
| 4.4 | Earned Value Analysis (in là Earned Value Analysis Report) | fields | BAC, PV, EV, AC theo kỳ; SV, CV, SPI, CPI; nguyên nhân gốc và tác động | |
| 4.5 | Risk Audit | fields | Sự kiện rủi ro và phản ứng đã xảy ra, quy trình rủi ro có được tuân thủ không | |
| 4.6 | Contractor Status Report | fields | Hiệu suất scope, quality, schedule và cost của nhà thầu, dự báo, khiếu nại, rủi ro | |
| 4.7 | Procurement Audit | fields | Hiệu suất nhà cung cấp, quy trình mua sắm có được tuân thủ không | |
| 4.8 | Contract Closeout Report (in là Contract Closeout) | fields | Hiệu suất nhà cung cấp, thay đổi và tranh chấp hợp đồng, ngày hoàn thành và ngày thanh toán cuối | |
| 4.9 | Product Acceptance Form (in là Formal Acceptance Form) | log | Yêu cầu với tiêu chí nghiệm thu, cách xác nhận, trạng thái, ký duyệt | |
| 5.1 | Lessons Learned Summary | fields | Điều làm tốt và điều cần cải thiện theo từng lĩnh vực, khi kết thúc dự án | |
| 5.2 | Project or Phase Closeout (in là Project Closeout) | fields | Mục tiêu so với kết quả cho scope, quality, time, cost; lợi ích; nhu cầu kinh doanh; rủi ro và vấn đề | |
| 6.1 | Product Vision | narrative | Sản phẩm cho ai, nhu cầu, cách đáp ứng, vì sao khách hàng mua | |
| 6.2 | Product Backlog | log | Hạng mục với tóm tắt, ưu tiên, story, trạng thái | |
| 6.3 | Release Plan | chart | Mục tiêu phát hành, sprint đối chiếu team | |
| 6.4 | Retrospective | log | Start, stop, keep, more, less | |

Khoảng trang của từng form nằm trong `.claude/skills/pm/references/forms-index.md`. Nhãn in chính xác
của một form: `python3 .claude/skills/pm/scripts/check_fidelity.py --list <form>`.

## 10. Bảng lệnh nhanh

Chạy từ thư mục gốc repo. `S=.claude/skills/pm/scripts` cho dòng lệnh ngắn hơn.

```bash
S=.claude/skills/pm/scripts

# Tra form
python3 $S/extract_form.py 2.32 --fields                 # nhãn in trên form, không cần PDF
python3 $S/extract_form.py 2.32                          # bảng element và chữ form trống từ PDF
python3 $S/extract_form.py 2.32 --alignment --tailoring  # phải khớp với gì, tailoring thế nào
python3 $S/extract_form.py 2.32 --prose                  # toàn bộ phần mô tả
python3 $S/extract_form.py 2.32 --knowledge              # hướng dẫn từng trường, nguồn, nơi nhận, quyết định; không cần PDF
python3 $S/check_fidelity.py --list 2.32                 # nhãn cần có, ở dạng Markdown

# Quyết định
python3 $S/pm_calc.py evm --bac <BAC> --pv <PV> --ev <EV> --ac <AC>      # thêm --json cho đầu ra máy đọc
python3 $S/pm_calc.py pert --o 20 --m 25 --p 36
python3 $S/pm_calc.py risk-score --probability high --impact very-high
python3 $S/pm_calc.py evm --bac 700 --pv 280 --ev 252 --ac 294 --threshold 5 --base bac pv   # phần trăm vượt, trong hay ngoài ngưỡng
python3 $S/pm_calc.py cpm --activity A=5 --activity B=3 --link A,B --slip A=4 --start 2027-01-25 --holiday 2027-02-06:2027-02-14
python3 $S/pm_calc.py reserve --contingency 28 --used 5 --risk R5=0.3:12
python3 $S/pm_calc.py evm --bac 700 --threshold 5                        # số tiền ứng với một ngưỡng phần trăm
python3 $S/pm_calc.py crash --option A 10 7 30 --option B 8 6 12 --needed 4   # phương án crashing theo chi phí thêm mỗi ngày rút được
python3 $S/pm_calc.py cpm --activity A=5 --activity B=3 --link A,B --start 2027-01-25 --deadline 2027-02-05   # deadline là ngày thì cần --start
python3 $S/pm_calc.py --help                                             # cả mười tám lệnh con
python3 $S/form_graph.py 3.3                             # nguồn, nơi nhận, form phải khớp
python3 $S/form_graph.py --impact 2.9 --depth 1          # cần xem lại gì khi 2.9 đổi
python3 $S/form_graph.py --order --group Planning        # thứ tự tạo form từ các liên kết đã ghi
python3 $S/form_graph.py --check                         # liên kết một chiều trong các file knowledge
python3 $S/form_graph.py --markdown --out .claude/skills/pm/references/form-graph.md   # sinh lại bản đã commit

# Dựng khung
python3 $S/new_form.py 2.32                              # in ra màn hình, không ghi gì
python3 $S/new_form.py 2.32 --docs                       # ghi docs/forms/2-32-risk-register.en.md
python3 $S/new_form.py 2.32 --rows 12 --out /tmp/r.md    # thêm dòng, đường dẫn khác
python3 $S/new_form.py 2.32 --docs --force               # ghi đè
python3 $S/new_form.py 4.2 --out /tmp/reports/ --dated 2026-10-19   # bản có ngày trong một thư mục, không bao giờ vào docs/
python3 $S/risk_actions.py docs/scope-package.en.md      # ô Actions của 2.32 cho từng rủi ro

# Kiểm tra
python3 $S/check_fidelity.py docs/forms/<file>.md <form>
python3 $S/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:" --flattened
python3 $S/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1B" --page 2 --flattened
python3 $S/check_pages.py <reply>.md                     # mọi số trang đều có số trang in hoặc PDF đi kèm (tiếng Anh hoặc tiếng Việt); mục không kèm trang bị cảnh báo
python3 $S/load_check.py docs/scope-package.en.md --limit MOB1=20 --leaves MOB1=2026-12-18
python3 $S/load_check.py docs/scope-package.en.md --charter docs/charter-package.en.md --daily-limit 8
python3 $S/load_check.py docs/scope-package.en.md --schedule docs/forms/2-18-project-schedule.en.md --limit MOB1=20   # các dòng của 2.18 đã cân bằng
python3 $S/check_consistency.py docs/forms/<file>.md docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/<file>.md
python3 $S/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 $S/check_consistency.py charter scope --group --today 2026-10-15   # một dòng cho mỗi loại; Date Prepared so với một ngày
python3 tools/check_scope.py
python3 tools/level.py

# Xuất Word
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md -o <out>.docx

# Payload cho Google Doc (không cần đăng nhập)
python3 tools/scope_tab3.py --out /tmp/tab3.md
PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md

# Test
uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts
python3 -m unittest discover -s .claude/skills/pm/scripts    # không cần uv, nhưng cần đã cài python-docx
python3 -m unittest tools.test_check_scope
```

Mã thoát: `0` sạch, `1` có phát hiện gây lỗi, `2` dùng sai lệnh (ví dụ thiếu file).

## 11. Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách sửa |
| --- | --- | --- |
| `uv: command not found` | Chưa cài uv | `brew install uv`, hoặc `curl -LsSf https://astral.sh/uv/install.sh \| sh`. Không có uv: `python3 -m venv .venv && .venv/bin/pip install python-docx pytest`, rồi dùng `.venv/bin/python` (`.venv/` đã nằm trong gitignore) |
| `FileNotFoundError: ... 'pdftotext'` | Chưa cài poppler | macOS `brew install poppler`; Ubuntu hoặc WSL `sudo apt install poppler-utils`. Trong lúc chờ, `--fields` vẫn chạy được |
| `A_Project_Managers_Book_of_Forms.pdf not found ...; pass --pdf` | Chạy ngoài repo, hoặc thiếu PDF | `cd` về thư mục gốc repo, hoặc thêm `--pdf <path>` |
| `several forms match 'risk'` | Tên khớp nhiều form | Dùng số hiệu, ví dụ `2.32` |
| `unknown form or document: 9.9` (thoát mã 2) từ `form_graph.py` | Đối số không phải số hiệu form cũng không phải tên có trong đồ thị | Dùng số ở mục 9, hoặc tên bên ngoài đúng như sách viết, ví dụ `"Scope baseline"` |
| `form_graph.py --impact 2.9` in ra khoảng một trăm tài liệu | Không có `--depth` thì nó đi theo mọi liên kết xuống hết, mà đồ thị rất dày | Thêm `--depth 1` hoặc `--depth 2` |
| `pm_calc.py` thoát mã 2 kèm `error:` | Công thức không nhận được đầu vào: BAC bằng không, xác suất ngoài 0 đến 100%, `80%` trơn ở Table 2.31, `nan` | Đọc thông báo; nó nêu đầu vào nào và vì sao. Đưa số còn thiếu hoặc từ chỉ mức |
| Một con số hiện `not stated in the book` | Hai cuốn sách không in công thức cho nó (độ lệch chuẩn beta, phần trăm sai lệch; hoàn vốn và các lượt tính đường găng là công cụ tính ngoài sách) | Thống nhất cách tính với nhóm và ghi vào 3.2; đừng trích sách cho nó |
| `no knowledge file for form ...` từ `extract_form.py --knowledge` | Số hiệu sai hoặc thiếu file | Dùng `references/knowledge/<number>.json`; cả 66 form đều có |
| `... exists; pass --force to overwrite it` | `new_form.py` không ghi đè | `--out <đường dẫn khác>`, hoặc `--force` nếu đúng ý |
| `tools/gdoc_edit.py not found; run this from inside the repo` | Chạy `md_to_docx.py` ngoài repo | Chạy từ thư mục gốc repo |
| Skill không chạy | Claude Code mở ngoài repo, hoặc yêu cầu không giống việc PM | Mở Claude Code tại thư mục gốc repo, gõ `/pm <form>` |

### Đọc một kiểm tra fidelity bị lỗi

`check_fidelity.py` chạy trên `.claude/skills/pm/scripts/fixtures/fidelity/broken-2-32.md`, một lần
làm thật trước đây, rút gọn:

```text
2.32 Risk Register, broken-2-32.md lines 1 to 37
12/22 printed labels present in printed order
missing (9):
  page 1, table, bank 1: Impact: Scope (written as 'Impact Scope' on line 9)
  page 1, table, bank 2: Status
out of printed order (1):
  page 1, table, bank 1: Probability (line 9)
unprinted labels (9), reported only:
  line 5: Source
  line 9: Impact Scope (printed as 'Impact: Scope')
```

- **missing**: thiếu một nhãn in. Có "written as" nghĩa là nhãn có nhưng sai chính tả; đổi tên lại.
  Không có gợi ý nghĩa là không có; thêm vào đúng vị trí in.
- **out of printed order**: có nhưng sai vị trí; chuyển chỗ.
- **unprinted labels**: thứ form không in, như `**Source:**`. Xóa đi, hoặc ghi rõ là tailoring trong
  đoạn in nghiêng phía trên form. Mục này không làm hỏng kiểm tra.

### Đọc một kiểm tra consistency bị lỗi

Mỗi dòng có dạng `LEVEL file:line [check] message`. Ví dụ thật:

```text
WARNING docs/forms/3-3-change-request.en.md:34 [date-style] this table column mixes date styles: plain 1 (first line 34), weekday 2 (first line 34)
0 error(s), 1 warning(s) in 3 file(s); reporting on docs/forms/3-3-change-request.en.md, 24 finding(s) already in the context files not shown
```

| Tên kiểm tra | Ý nghĩa |
| --- | --- |
| `date`, `date-style` | Ngày không theo kiểu `2 September 2026`, hoặc trộn kiểu trong một cột |
| `range` | Một khoảng như `R1 to R10` dừng trước phần tử cuối hiện tại |
| `role-merge` | Lẫn từ ngữ của sponsor và customer |
| `term` | Một từ trong bảng "Never write" của `house-style.md` |
| `html`, `em-dash`, `emoji` | Markup hoặc ký tự không sống sót khi lên Doc hoặc vi phạm quy tắc |
| `mark-on-label` | Tô vàng nhãn hoặc tiêu đề |
| `total` | Dòng Total không bằng tổng các dòng |
| `uniform-column` | Mọi dòng cùng một giá trị, nên cột không mang thông tin |
| `id-conflict` | Một ID có hai nội dung khác nhau |
| `section-ref` | Tham chiếu tới mục không có trong tài liệu nộp |
| `approvals` | Khối chữ ký không giống bản in |
| `form-note` | Có chữ bên trong form in mà form không in |
| `note-length` | Một đoạn in nghiêng phía trên form (các dòng xuống hàng tính là một đoạn) dài quá khoảng 150 từ |
| `date-prepared` | Với `--today`: Date Prepared sau ngày đó (lỗi) hoặc trước ngày đó (cảnh báo, xác nhận nội dung được kiểm lần cuối vào ngày ấy) |
| `stale-m0` | Việc bổ nhiệm project manager gắn với M0 hoặc một ngày trước đó, trong tài liệu lập sau M0 |
| `table-rule` | Dòng `---` nằm ngay dưới một dòng bảng, bị bộ sinh Doc biến thành một ô thừa |

- Error làm lần chạy thất bại; warning thì không. Mọi cảnh báo `range` phải được sửa hoặc giải thích, vì
  đây là kiểm tra đã bắt được `R1 to R10`.
- Với `--report`, các phát hiện đã có sẵn trong charter hoặc scope package chỉ được đếm ở cuối, không
  hiển thị. Tài liệu nguồn vẫn còn một số lỗi (ví dụ ngày viết tắt trong charter); đó là việc riêng,
  không phải lý do form của bạn bị lỗi.
- Phát hiện của script là manh mối. Mở dòng đó ra đọc trước khi sửa.

## 12. Cải tiến skill

### Cấu trúc

| Đường dẫn | Sửa gì ở đây |
| --- | --- |
| `.claude/skills/pm/SKILL.md` | Quy trình làm form và đường quyết định Claude làm theo (giữ dưới 450 dòng) |
| `references/decisions.md` | Danh mục quyết định: bảng định tuyến, 43 quyết định, đường kiểm soát thay đổi, định dạng khuyến nghị |
| `references/pmbok-<area>.md` | Một ghi chú PMBOK 6 cho mỗi lĩnh vực kiến thức, và `pmbok-agile.md`; bảng form đến ghi chú nằm trong `SKILL.md` |
| `references/knowledge/<form>.json` | Mỗi trường chứa gì, nguồn, nơi nhận, alignment, quyết định; đọc qua `extract_form.py --knowledge`. `form_graph.py` dựng từ đây |
| `references/book-structure.md`, `references/form-graph.md` | Cách sách được tổ chức; bản đồ form sinh tự động (sinh lại bằng `form_graph.py --markdown --out references/form-graph.md`) |
| `references/review-lessons.md` | Những gì reviewer bắt, và cách kiểm tra |
| `references/house-style.md` | Quy tắc đánh dấu, ngày, bảng "Never write", nơi chứa dữ liệu dự án |
| `references/rendering.md` | Mỗi loại form thành Markdown thế nào |
| `references/forms-index.md` | 66 form, trang, loại, tiêu đề in |
| `references/fields/<form>.json` | Nhãn in của từng form; sửa ở đây nếu một nhãn sai |
| `references/audit-template.md`, `references/push-audit.md` | Mẫu báo cáo audit; audit form được sinh tự động (sinh lại vào bản sao tạm) và payload đẩy lên Doc |
| `references/book-counts.json` | Số dòng sách in trong một bảng có tên, cho kiểm tra `count` của `check_consistency.py` |
| `scripts/*.py`, `scripts/test_*.py`, `scripts/fixtures/` | Script, test và dữ liệu test, gồm `pm_calc.py`, `form_graph.py`, `check_schedule.py`, `load_check.py`, `check_pages.py` và `risk_actions.py` |
| `evals/evals.json` | Câu lệnh test kèm assertion chấm được |

### Thêm một bài học review

Khi reviewer bắt một lỗi mới trên Doc:

1. Thêm vào mục phù hợp của `references/review-lessons.md` (1 người và vai trò, 2 ID và khoảng, 3 số
   liệu, 4 phạm vi, 5 tiền, 6 tiêu chí thành công, 7 bố cục, 8 markup, 9 ngày, 10 tính đầy đủ, 11 trả
   lời). Ghi sai ở đâu, vì sao reviewer quan tâm, cách kiểm tra, và trích ID thread hoặc audit.
2. Một từ bị cấm: thêm một dòng vào bảng "Never write | Write instead | Why" trong
   `references/house-style.md`. Kiểm tra consistency đọc bảng này, không cần sửa code.
3. Một quy tắc kiểm tra được bằng máy: thêm kiểm tra vào `scripts/check_consistency.py`, đánh dấu bài
   học **[script]**, và thêm fixture trong `scripts/fixtures/consistency/`: `fnNN-*.md` phải bị bắt,
   `fpNN-*.md` không được bị bắt. Đăng ký chúng trong `scripts/test_check_consistency.py`.
4. Một nhãn in bị sai: sửa `references/fields/<form>.json` sau khi xem trang form trống (`Read` trang
   PDF, hoặc `pdftotext -layout -f N -l N A_Project_Managers_Book_of_Forms.pdf -`).

### Chạy test

```bash
uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts
```

Kết quả hiện tại: `481 passed` cùng các subtest. `test_pm_skill.py` còn kiểm `SKILL.md` giữ dưới 450 dòng, phần description vừa 1,024 ký tự, và các eval đúng cấu trúc; `test_pm_calc.py` dựng lại các ví dụ có tính toán mà sách in. Chạy lại sau mọi thay đổi trong `.claude/skills/pm/`.

### Chạy eval

`evals/evals.json` có chín câu lệnh kèm assertion: audit charter và scope package, form 1.3 Stakeholder
Register từ câu hỏi tiếng Việt, form 2.32 Risk Register, audit giữ riêng cho lịch 2.18, form 4.2 trống,
và bốn câu hỏi quyết định (trễ tiến độ phần mobile, tình trạng earned value với số liệu cho sẵn, xử lý
R5, và câu hỏi tiếng Việt về nơi ghi một chức năng mới). Để chạy, hỏi Claude Code:

```text
Use the skill-creator skill to run the pm evals in .claude/skills/pm/evals/evals.json
and write the results to .claude/skills/pm-workspace/iteration-<N>/.
```

Các lần chạy trước nằm ở `.claude/skills/pm-workspace/iteration-1/` và `iteration-2/`: mỗi eval một
thư mục chứa output, và `benchmark.md` với tỉ lệ đạt so với phiên bản skill trước. Khi thêm eval, ghi
đủ `id`, `eval_name`, `prompt`, `expected_output`, `files` và `assertions`, và viết mỗi assertion sao
cho người khác kiểm được chỉ từ output.

### Thêm hoặc sửa tri thức về quyết định

- Một dữ kiện PMBOK hay Book of Forms trong một quyết định: sửa `references/pmbok-<area>.md` tương ứng và
  `references/decisions.md`, ghi trang theo cả hai cách đánh số, rồi mở trang ra kiểm.
- Liên kết hay hướng dẫn trường của một form: sửa `references/knowledge/<form>.json`. Chạy
  `form_graph.py --check` xem phía kia có liệt kê liên kết không, và `form_graph.py --markdown --out references/form-graph.md` để sinh lại
  (không có `--out` thì chỉ in ra, và một test báo lỗi khi bản đã commit cũ).
- Một công thức: sửa `scripts/pm_calc.py` khi một cuốn sách in công thức đó, và thêm test với ví dụ có tính
  toán của sách. Phép tính mà sách chỉ nêu hoặc vẽ (hoàn vốn, các lượt tính đường găng) có thể thêm như công
  cụ tính ngoài sách, ghi rõ như vậy trong đầu ra và docstring. Nếu không, công cụ phải ghi "not stated in
  the book".

### Trước khi commit

- Test chạy qua.
- Không em dash, en dash hay emoji (`CLAUDE.md`).
- Không ghi AI vào commit message.
- Không ghi Doc ID hay giá trị hardcode nào vào file.
