# Giải thích gói phạm vi cho người không chuyên

Bản diễn giải của `docs/scope-package.en.md` theo mức dễ nhất, kiểu giải thích cho trẻ con.
Đây không phải bài nộp. Bài nộp vẫn là file tiếng Anh. File này chỉ để người ngoài ngành đọc
hiểu nhóm đang làm gì, hoặc để chính nhóm dùng khi phải trình bày miệng.

Số liệu trong bài lấy từ file thật ngày 23 tháng 9 năm 2026, không phải nhớ: 57 dòng yêu cầu,
78 gói công việc, 24 control account, 4.400 giờ, 700.000.000 VND, 28 phép kiểm tra đều đạt.
Muốn kiểm lại thì chạy `python tools/check_scope.py`.

---

## Cái file đó là gì

Hãy tưởng tượng sắp xây **một cái nhà cho búp bê thật to**. To lắm. Không phải làm một mình
trong một buổi chiều được.

File đó là **tờ giấy ghi kế hoạch xây nhà**.

Nó có ba phần, giống ba tờ giấy dán cạnh nhau trên tường.

---

## Tờ thứ nhất: ai muốn gì

Trước khi xây thì phải hỏi mọi người xem họ muốn cái gì.

- Mẹ muốn nhà có **cửa sổ**.
- Em muốn có **cầu trượt**.
- Bà muốn **cửa phải đóng được**, kẻo mèo chui vào.

Tờ giấy này ghi lại **57 điều ước** như vậy. Mỗi điều ước đều ghi rõ ba thứ:

| Ghi cái gì | Để làm gì |
| --- | --- |
| Ai ước cái đó | Sau này có gì còn biết hỏi ai |
| Chỗ nào trong nhà sẽ làm ra nó | Để không có điều ước nào bị bỏ quên |
| Làm sao biết là đã làm xong đúng | Để lúc xong không cãi nhau |

Chỗ cuối cùng quan trọng nhất. Nếu chỉ ghi "nhà phải đẹp" thì lúc xây xong sẽ cãi nhau ngay,
vì ai cũng nghĩ đẹp là một kiểu khác nhau. Nên phải ghi kiểu **đếm được**: cửa sổ phải mở ra
được, cầu trượt phải trượt được.

---

## Tờ thứ hai: chia việc ra

Xây cả cái nhà thì to quá, nghĩ thôi đã thấy sợ. Nên phải **bẻ nhỏ nó ra**.

Giống như xếp hình Lego. Không ai xếp một cục khổng lồ. Làm từng mảnh nhỏ, rồi ghép lại.

```
Cả cái nhà
├── Làm cái móng
├── Làm bức tường
│   ├── Tường bên trái
│   └── Tường bên phải
└── Làm cái mái
```

Cứ bẻ nhỏ mãi, cuối cùng ra **78 việc nhỏ**. Mỗi việc nhỏ **một người làm** thôi, để không ai
đổ lỗi cho ai.

Có một quy tắc hay ở đây. Việc nhỏ không được **quá to** mà cũng không được **quá bé**.

- Quá to thì làm cả tháng không biết xong chưa.
- Quá bé thì ghi giấy còn mất công hơn là làm.

---

## Tờ thứ ba: tấm thẻ cho mỗi việc

Mỗi việc nhỏ trong 78 việc kia đều có **một tấm thẻ riêng**, tức là 78 tấm thẻ.

Trên mỗi tấm thẻ ghi:

- Việc này là gì
- Ai làm
- Làm trong bao lâu
- Tốn bao nhiêu tiền
- Làm sao biết là xong rồi

Giống tấm thẻ dán trên hộp đồ chơi. Nhìn vào là biết trong hộp có gì, không cần mở ra.

---

## Chỗ hay nhất

Tất cả các con số **cộng lại phải vừa khít**.

| Cộng cái gì | Phải ra đúng |
| --- | --- |
| Tiền của cả 78 tấm thẻ | 700.000.000 VND |
| Số giờ làm của cả 78 tấm thẻ | 4.400 giờ |

Không thừa một đồng, không thiếu một đồng.

Mà 78 tấm thẻ thì nhiều quá, cộng bằng tay kiểu gì cũng sai. Nên nhóm làm **một cái máy cộng
tự động**. Nó cộng hết, rồi nói đúng rồi hay sai rồi. Bây giờ nó đang nói đúng rồi, cả **28
phép kiểm tra** đều qua.

---

## Vì sao phải làm tất cả cái này

Vì nếu không có tờ giấy này, thì lúc xây được nửa cái nhà sẽ có người hỏi:

> Ơ, hết tiền rồi à? Mà cái mái đâu? Ai là người phải làm cái mái nhỉ?

Lúc đó thì muộn rồi.

---

## Đối chiếu sang từ chuyên môn

Bảng này để người trong nhóm bắc cầu từ cách nói trên sang đúng tên gọi trong bài nộp.

| Trong bài này gọi là | Tên thật trong `scope-package.en.md` | Nguồn |
| --- | --- | --- |
| Tờ ai muốn gì | Requirements Traceability Matrix | Form 2.7 |
| Tờ chia việc | Work Breakdown Structure | Form 2.9 |
| Tấm thẻ mỗi việc | WBS Dictionary | Form 2.10 |
| Việc nhỏ | Work package | 78 cái |
| Nhóm việc | Control account | 24 cái |
| Quy tắc không quá to không quá bé | Quy tắc 8/80 giờ | PMBOK |
| Máy cộng tự động | `tools/check_scope.py` | 28 phép kiểm tra |
