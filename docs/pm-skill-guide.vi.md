# Hướng dẫn dùng PM skill

Cách dùng skill `pm` trong Claude Code để tạo, kiểm tra và audit các form trong *A Project Manager's
Book of Forms*, bản thứ 3, cho dự án này. Tài liệu viết cho các bạn trong nhóm đã nắm môn học và cuốn
sách nhưng chưa đọc phần bên trong của skill.

Bản tiếng Anh: [`pm-skill-guide.md`](pm-skill-guide.md). Lệnh, tên file và nhãn in trên form được
giữ nguyên tiếng Anh.

Mọi lệnh dưới đây đã được chạy thử trong repo ngày 1 October 2026 từ thư mục gốc, trừ các lệnh `gdoc` cần thông tin đăng nhập Google của nhóm.

## Mục lục

1. Skill làm gì và không làm gì
2. Chuẩn bị
3. Cách yêu cầu một form
4. Từ yêu cầu đến sản phẩm
5. Ba trạng thái đánh dấu
6. Quy tắc reviewer kiểm tra
7. Audit và trả lời comment trên Google Doc
8. Toàn bộ 66 form
9. Bảng lệnh nhanh
10. Xử lý sự cố
11. Cải tiến skill

## 1. Skill làm gì và không làm gì

Skill nằm ở `.claude/skills/pm/`. Claude Code tự nạp skill khi bạn yêu cầu một form, nhắc số hiệu
form, hoặc yêu cầu audit tài liệu trong `docs/`.

| Skill làm | Skill không làm |
| --- | --- |
| Tìm đúng form trong 66 form theo số hoặc theo tên, và hỏi lại khi một tên khớp nhiều form | Nhớ danh sách trường theo trí nhớ; mọi nhãn lấy từ `references/fields/<form>.json`, được chép từ trang form trống |
| Dựng khung form bằng Markdown với title block, nhãn, tiêu đề trang, header nhóm và các bank đúng như bản in, đúng thứ tự in | Thêm trường, cột hay ghi chú mà form in không có |
| Điền form từ `docs/charter-package.en.md`, `docs/scope-package.en.md` và các form trong `docs/forms/` | Bịa giá trị dự án; giá trị giả định được tô vàng, giá trị chưa biết để trống hoặc `[TBD]` |
| Chạy kiểm tra fidelity và consistency rồi báo kết quả | Âm thầm chọn một bên khi hai tài liệu mâu thuẫn; skill báo mâu thuẫn để nhóm quyết định |
| Xuất form ra `.docx` trông giống sách | Đẩy lên Google Doc của nhóm khi bạn chưa yêu cầu, và không bao giờ đẩy khi không có Doc ID bạn đưa |
| Audit cả gói tài liệu và soạn trả lời comment của reviewer | Sửa file trong lúc audit, trừ khi bạn yêu cầu sửa |

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

Bạn cũng có thể gọi skill trực tiếp bằng slash command:

```text
/pm 2.32                      điền form 2.32 từ tài liệu dự án
/pm risk register             như trên, gọi bằng tên
/pm 4.2 --blank               form trống, không có giá trị dự án
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
  2. đọc form in               extract_form.py --fields, thêm trang PDF với form dạng biểu đồ
  3. thu thập dữ liệu dự án    docs/charter-package.en.md, docs/scope-package.en.md, docs/forms/
  4. dựng khung rồi điền       new_form.py, sau đó sửa Markdown
  5. kiểm tra                  check_fidelity.py, check_consistency.py, tools/check_scope.py, đọc lại
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
python3 .claude/skills/pm/scripts/new_form.py 2.32 --out -        # in form trống ra màn hình
python3 .claude/skills/pm/scripts/new_form.py 2.32                # ghi docs/forms/2-32-risk-register.en.md
python3 .claude/skills/pm/scripts/new_form.py 2.32 --rows 12      # 12 dòng trống cho mỗi bảng register
python3 .claude/skills/pm/scripts/new_form.py 2.32 --force        # ghi đè file đã có
```

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

Form trống (`--blank`) chính là khung này, không thêm gì: không tên, ngày, số tiền hay ID.

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
| `check_fidelity.py` | Markdown có đủ mọi nhãn in, đúng chính tả, đúng thứ tự in không? | Thiếu nhãn hoặc sai thứ tự. Nhãn không có trên form chỉ được liệt kê, không làm hỏng kiểm tra |
| `check_consistency.py --report <form>` | Form mới có khớp với charter và scope package không? | Bất kỳ lỗi nào do form mới gây ra. Lỗi cũ trong tài liệu nguồn chỉ được đếm, không hiển thị |
| `tools/check_scope.py` | Scope package còn cộng đủ 4,400 giờ và 700,000,000 VND không? | Bất kỳ kiểm tra nào của nó |

Một form sạch in ra, ví dụ:

```text
2.32 Risk Register, 2-32-risk-register.en.md lines 1 to 18
22/22 printed labels present in printed order
```

Sau script, skill đọc các tài liệu mà sách nói form này phải khớp (mục Alignment) và báo mâu thuẫn. Mục
10 giải thích cách đọc một kiểm tra bị lỗi.

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
python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md
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

1. Script trên cả gói: `check_consistency.py` trên mọi file cùng lúc, `check_fidelity.py` trên từng
   form (dùng `--section` với form nằm trong một package), `tools/check_scope.py`.
2. Từng bài học trong `review-lessons.md`, tính lại số liệu suy ra từ giả định.
3. Trình tự: không gì được dùng, nghiệm thu hay ký trước khi nó tồn tại; không ngày nào rơi vào khoảng
   thời gian charter loại trừ.
4. Khối lượng mỗi người mỗi tuần so với phân bổ trong charter (`python3 tools/level.py` cho lịch đã
   cân bằng nguồn lực).
5. Payload đẩy lên, khi có liên quan đến Doc.

Báo cáo theo mẫu `.claude/skills/pm/references/audit-template.md`:

```text
## Errors        E1, E2, ...   mâu thuẫn chứng minh được bằng hai trích dẫn
## Warnings      W1, W2, ...   điểm yếu người chấm có thể bắt
## What passed                 các kiểm tra không phát hiện gì
```

Mỗi phát hiện có vị trí (`file:line` và mục hoặc trang form), trích dẫn bằng chứng, và cách sửa hoặc
quyết định cần đưa ra và ai quyết định.

Lệnh hữu ích khi audit:

```bash
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 .claude/skills/pm/scripts/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:"
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

## 8. Toàn bộ 66 form

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

## 9. Bảng lệnh nhanh

Chạy từ thư mục gốc repo. `S=.claude/skills/pm/scripts` cho dòng lệnh ngắn hơn.

```bash
S=.claude/skills/pm/scripts

# Tra form
python3 $S/extract_form.py 2.32 --fields                 # nhãn in trên form, không cần PDF
python3 $S/extract_form.py 2.32                          # bảng element và chữ form trống từ PDF
python3 $S/extract_form.py 2.32 --alignment --tailoring  # phải khớp với gì, tailoring thế nào
python3 $S/extract_form.py 2.32 --prose                  # toàn bộ phần mô tả
python3 $S/check_fidelity.py --list 2.32                 # nhãn cần có, ở dạng Markdown

# Dựng khung
python3 $S/new_form.py 2.32 --out -                      # in ra màn hình
python3 $S/new_form.py 2.32                              # ghi docs/forms/2-32-risk-register.en.md
python3 $S/new_form.py 2.32 --rows 12 --out /tmp/r.md    # thêm dòng, đường dẫn khác
python3 $S/new_form.py 2.32 --force                      # ghi đè

# Kiểm tra
python3 $S/check_fidelity.py docs/forms/<file>.md <form>
python3 $S/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:"
python3 $S/check_consistency.py docs/forms/<file>.md docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/<file>.md
python3 $S/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 tools/check_scope.py
python3 tools/level.py

# Xuất Word
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md -o <out>.docx

# Payload cho Google Doc (không cần đăng nhập)
python3 tools/scope_tab3.py --out /tmp/tab3.md
python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md

# Test
uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts
python3 -m unittest discover -s .claude/skills/pm/scripts    # không cần uv, nhưng cần đã cài python-docx
python3 -m unittest tools.test_check_scope
```

Mã thoát: `0` sạch, `1` có phát hiện gây lỗi, `2` dùng sai lệnh (ví dụ thiếu file).

## 10. Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách sửa |
| --- | --- | --- |
| `uv: command not found` | Chưa cài uv | `brew install uv`, hoặc `curl -LsSf https://astral.sh/uv/install.sh \| sh`. Không có uv: `python3 -m venv .venv && .venv/bin/pip install python-docx pytest`, rồi dùng `.venv/bin/python` (`.venv/` đã nằm trong gitignore) |
| `FileNotFoundError: ... 'pdftotext'` | Chưa cài poppler | macOS `brew install poppler`; Ubuntu hoặc WSL `sudo apt install poppler-utils`. Trong lúc chờ, `--fields` vẫn chạy được |
| `A_Project_Managers_Book_of_Forms.pdf not found ...; pass --pdf` | Chạy ngoài repo, hoặc thiếu PDF | `cd` về thư mục gốc repo, hoặc thêm `--pdf <path>` |
| `several forms match 'risk'` | Tên khớp nhiều form | Dùng số hiệu, ví dụ `2.32` |
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

- Error làm lần chạy thất bại; warning thì không. Mọi cảnh báo `range` phải được sửa hoặc giải thích, vì
  đây là kiểm tra đã bắt được `R1 to R10`.
- Với `--report`, các phát hiện đã có sẵn trong charter hoặc scope package chỉ được đếm ở cuối, không
  hiển thị. Tài liệu nguồn vẫn còn một số lỗi (ví dụ ngày viết tắt trong charter); đó là việc riêng,
  không phải lý do form của bạn bị lỗi.
- Phát hiện của script là manh mối. Mở dòng đó ra đọc trước khi sửa.

## 11. Cải tiến skill

### Cấu trúc

| Đường dẫn | Sửa gì ở đây |
| --- | --- |
| `.claude/skills/pm/SKILL.md` | Quy trình Claude làm theo |
| `references/review-lessons.md` | Những gì reviewer bắt, và cách kiểm tra |
| `references/house-style.md` | Quy tắc đánh dấu, ngày, bảng "Never write", nơi chứa dữ liệu dự án |
| `references/rendering.md` | Mỗi loại form thành Markdown thế nào |
| `references/forms-index.md` | 66 form, trang, loại, tiêu đề in |
| `references/fields/<form>.json` | Nhãn in của từng form; sửa ở đây nếu một nhãn sai |
| `references/audit-template.md` | Mẫu báo cáo audit |
| `scripts/*.py`, `scripts/test_*.py`, `scripts/fixtures/` | Script, test và dữ liệu test |
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

Kết quả hiện tại: `142 passed`. Chạy lại sau mọi thay đổi trong `.claude/skills/pm/`.

### Chạy eval

`evals/evals.json` có năm câu lệnh kèm assertion: audit charter và scope package, form 1.3 Stakeholder
Register từ câu hỏi tiếng Việt, form 2.32 Risk Register, audit giữ riêng cho lịch 2.18, và form 4.2
trống. Để chạy, hỏi Claude Code:

```text
Use the skill-creator skill to run the pm evals in .claude/skills/pm/evals/evals.json
and write the results to .claude/skills/pm-workspace/iteration-<N>/.
```

Các lần chạy trước nằm ở `.claude/skills/pm-workspace/iteration-1/` và `iteration-2/`: mỗi eval một
thư mục chứa output, và `benchmark.md` với tỉ lệ đạt so với phiên bản skill trước. Khi thêm eval, ghi
đủ `id`, `eval_name`, `prompt`, `expected_output`, `files` và `assertions`, và viết mỗi assertion sao
cho người khác kiểm được chỉ từ output.

### Trước khi commit

- Test chạy qua.
- Không em dash, en dash hay emoji (`CLAUDE.md`).
- Không ghi AI vào commit message.
- Không ghi Doc ID hay giá trị hardcode nào vào file.
