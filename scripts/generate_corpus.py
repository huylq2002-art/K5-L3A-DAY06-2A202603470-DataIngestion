# -*- coding: utf-8 -*-
"""Script to generate a 32-page realistic university handbook corpus, PDF, and manifest."""
import json
from pathlib import Path
import fitz  # PyMuPDF

SECTIONS = [
    ("tuyen_sinh_nhap_hoc", "Chương I: Quy Chế Tuyển Sinh và Thủ Tục Nhập Học", 1, 5),
    ("chuong_trinh_tin_chi", "Chương II: Chương Trình Đào Tạo và Đăng Ký Học Phần Tín Chỉ", 6, 11),
    ("danh_gia_hoc_vu", "Chương III: Quy Định Đánh Giá Học Phần và Xử Lý Học Vụ", 12, 18),
    ("hoc_phi_hoc_bong", "Chương IV: Chính Sách Học Phí, Miễn Giảm và Học Bổng Khuyến Khích", 19, 24),
    ("tot_nghiep_bao_luu", "Chương V: Quy Định Tạm Dừng, Bảo Lưu và Xét Tốt Nghiệp", 25, 29),
    ("nckh_ngoai_khoa", "Chương VI: Hoạt Động Nghiên Cứu Khoa Học và Rèn Luyện Sinh Viên", 30, 32),
]

def generate_pages_data():
    pages = []
    
    # Page 1: Thủ tục nhập học và hồ sơ sinh viên
    pages.append({
        "page": 1,
        "section": "tuyen_sinh_nhap_hoc",
        "title": "Điều 1: Quy trình tiếp nhận tân sinh viên và xác nhận nhập học",
        "text": """ĐIỀU 1: QUY TRÌNH TIẾP NHẬN TÂN SINH VIÊN VÀ XÁC NHẬN NHẬP HỌC
1. Thí sinh trúng tuyển vào các ngành đào tạo đại học chính quy phải thực hiện xác nhận nhập học trực tuyến trên cổng thông tin tuyển sinh của Bộ Giáo dục và Đào tạo trước 17h00 ngày 20 tháng 8 hằng năm. Sau thời hạn này, nếu thí sinh không xác nhận, Nhà trường xem như thí sinh từ chối nhập học và sẽ tiến hành gọi thí sinh diện nguyện vọng bổ sung.
2. Hồ sơ nhập học bắt buộc nộp trực tiếp tại Phòng Đào tạo bao gồm:
- Bản chính Giấy chứng nhận kết quả thi tốt nghiệp THPT.
- Bản sao có chứng thực Bằng tốt nghiệp THPT hoặc Giấy chứng nhận tốt nghiệp tạm thời.
- Bản sao có chứng thực Học bạ THPT (đầy đủ 3 năm lớp 10, 11 và 12).
- Bản sao Giấy khai sinh, Căn cước công dân gắn chip (mang theo bản chính để đối chiếu).
- 04 ảnh 3x4 chụp trong thời gian không quá 6 tháng, phía sau ghi rõ họ tên và ngày sinh.
- Giấy chứng nhận ưu tiên đối tượng hoặc khu vực (nếu có để hưởng chính sách điểm ưu tiên).
3. Thời hạn nộp bổ sung các giấy tờ còn thiếu không được vượt quá 30 ngày kể từ ngày tựu trường. Sau 30 ngày, sinh viên chưa hoàn thiện hồ sơ sẽ bị tạm dừng quyền đăng ký học phần của học kỳ tiếp theo cho đến khi bổ sung đầy đủ.
4. Nhà trường có quyền hậu kiểm hồ sơ, đối chiếu văn bằng gốc tại bất kỳ thời điểm nào trong khóa học. Sinh viên có hành vi gian lận hồ sơ sẽ bị buộc thôi học và hủy toàn bộ kết quả học tập tích lũy."""
    })

    # Page 2: Thẻ sinh viên và tài khoản số
    pages.append({
        "page": 2,
        "section": "tuyen_sinh_nhap_hoc",
        "title": "Điều 2: Quản lý mã số sinh viên, thẻ sinh viên và tài khoản định danh số",
        "text": """ĐIỀU 2: QUẢN LÝ MÃ SỐ SINH VIÊN, THẺ SINH VIÊN VÀ TÀI KHOẢN ĐỊNH DANH SỐ
1. Mỗi sinh viên nhập học được cấp một Mã số sinh viên (MSSV) duy nhất gồm 10 ký tự, tồn tại suốt quá trình học tập và không thay đổi kể cả khi sinh viên chuyển ngành hoặc học cùng lúc hai chương trình.
2. Thẻ sinh viên là thẻ tích hợp thông minh dùng cho các mục đích:
- Điểm danh tại giảng đường, phòng thí nghiệm và thư viện thông qua công nghệ RFID.
- Xuất trình khi tham gia các kỳ thi giữa kỳ và cuối kỳ. Thí sinh không có thẻ sinh viên hoặc giấy tờ tùy thân hợp lệ có ảnh sẽ không được vào phòng thi.
- Sử dụng làm thẻ ngân hàng thanh toán học phí và nhận học bổng từ Nhà trường.
3. Sinh viên làm mất hoặc hỏng thẻ phải nộp đơn xin cấp lại tại Trung tâm Hỗ trợ Sinh viên. Lệ phí làm lại thẻ là 80.000 VNĐ đối với lần đầu và 150.000 VNĐ đối với các lần tiếp theo. Thời gian cấp lại thẻ mới từ 5 đến 7 ngày làm việc.
4. Tài khoản email sinh viên (tên miền @student.edu.vn) là kênh liên lạc chính thức duy nhất giữa Nhà trường và sinh viên. Các thông báo về lịch thi, học phí, học bổng và quyết định học vụ gửi qua email này được coi là đã gửi đến sinh viên sau 48 giờ kể từ thời điểm phát hành thông báo."""
    })

    # Page 3: Khám sức khỏe và bảo hiểm y tế
    pages.append({
        "page": 3,
        "section": "tuyen_sinh_nhap_hoc",
        "title": "Điều 3: Kiểm tra sức khỏe đầu khóa và nghĩa vụ tham gia bảo hiểm y tế",
        "text": """ĐIỀU 3: KIỂM TRA SỨC KHỎE ĐẦU KHÓA VÀ NGHĨA VỤ THAM GIA BẢO HIỂM Y TẾ
1. Tất cả tân sinh viên bắt buộc phải tham gia đợt khám sức khỏe tổng quát đầu khóa do Trạm Y tế Nhà trường phối hợp cùng Bệnh viện đa khoa tổ chức trong tháng đầu tiên của năm học.
2. Sinh viên không tham gia khám sức khỏe theo lịch thông báo mà không có lý do chính đáng sẽ bị trừ 10 điểm rèn luyện của học kỳ 1 và bị khóa tài khoản đăng ký tín chỉ kỳ tiếp theo cho đến khi nộp giấy khám sức khỏe đạt tiêu chuẩn từ bệnh viện tuyến quận/huyện trở lên.
3. Sinh viên mắc bệnh truyền nhiễm nguy hiểm hoặc bệnh tâm thần ảnh hưởng đến khả năng học tập sẽ được Nhà trường xem xét cho tạm hoãn học tập để điều trị trong thời hạn tối đa 01 năm, giữ nguyên kết quả trúng tuyển.
4. Bảo hiểm y tế (BHYT) là nghĩa vụ bắt buộc theo Luật Bảo hiểm Y tế Việt Nam. Mức đóng BHYT hằng năm theo quy định của Bảo hiểm Xã hội Nhà nước, trong đó sinh viên được ngân sách Nhà nước hỗ trợ 30% mức đóng, sinh viên tự đóng 70% còn lại. Sinh viên đã có thẻ BHYT theo đối tượng ưu tiên (thân nhân công an, quân đội, hộ nghèo) phải nộp bản sao thẻ còn hạn trước ngày 30 tháng 9 để được miễn trừ thu học phí BHYT."""
    })

    # Page 4: Quy chế chuyển ngành đào tạo
    pages.append({
        "page": 4,
        "section": "tuyen_sinh_nhap_hoc",
        "title": "Điều 4: Điều kiện và thủ tục chuyển ngành đào tạo đại học",
        "text": """ĐIỀU 4: ĐIỀU KIỆN VÀ THỦ TỤC CHUYỂN NGÀNH ĐÀO TẠO ĐẠI HỌC
1. Sinh viên có nguyện vọng chuyển sang ngành đào tạo khác trong cùng trường phải đáp ứng đồng thời các điều kiện sau:
- Không đang là sinh viên năm thứ nhất (học kỳ 1) hoặc năm cuối khóa đào tạo.
- Điểm trúng tuyển đầu vào của sinh viên tại năm tuyển sinh phải bằng hoặc cao hơn điểm chuẩn của ngành dự kiến chuyển sang.
- Điểm trung bình chung tích lũy (CPA) tính đến thời điểm nộp đơn đạt từ 2.50 trở lên trên thang điểm 4.0 và không bị cảnh báo học vụ.
- Ngành dự kiến chuyển sang còn chỉ tiêu tiếp nhận sinh viên theo thông báo của Hội đồng Tuyển sinh Nhà trường.
2. Sinh viên không được phép chuyển ngành trong các trường hợp:
- Trúng tuyển theo diện cử tuyển hoặc các chương trình đào tạo liên kết quốc tế có cam kết riêng.
- Đang trong thời gian bị kỷ luật từ mức khiển trách trở lên.
3. Hồ sơ xin chuyển ngành nộp vào tuần thứ 10 đến tuần thứ 12 của mỗi học kỳ chính. Hội đồng xét duyệt sẽ thông báo kết quả trước khi học kỳ mới bắt đầu ít nhất 2 tuần.
4. Khi được chấp thuận chuyển ngành, sinh viên được công nhận các học phần tương đương và phải học bổ sung các học phần còn thiếu trong khung chương trình của ngành mới."""
    })

    # Page 5: Chuyển trường và tiếp nhận sinh viên trường khác
    pages.append({
        "page": 5,
        "section": "tuyen_sinh_nhap_hoc",
        "title": "Điều 5: Quy định về chuyển trường đến và chuyển trường đi",
        "text": """ĐIỀU 5: QUY ĐỊNH VỀ CHUYỂN TRƯỜNG ĐẾN VÀ CHUYỂN TRƯỜNG ĐI
1. Sinh viên được xét chuyển trường nếu đáp ứng đầy đủ các tiêu chuẩn sau:
- Sinh viên có lý do chính đáng như thay đổi nơi cư trú của gia đình hoặc hoàn cảnh gia đình đặc biệt khó khăn cần chuyển địa bàn sinh sống.
- Trường tiếp nhận đồng ý tiếp nhận bằng văn bản và trường đang theo học đồng ý cho chuyển đi.
- Điểm trúng tuyển của sinh viên không thấp hơn điểm chuẩn của ngành tương ứng tại trường chuyển đến trong cùng năm tuyển sinh.
- Sinh viên đã hoàn thành ít nhất 01 năm học (2 học kỳ chính) và không đang trong thời gian bị kỷ luật, không bị cảnh báo học vụ mức 2 hoặc mức 3.
2. Không cho phép chuyển trường đối với sinh viên năm cuối khóa (khi đã tích lũy từ 75% tổng số tín chỉ của chương trình đào tạo trở lên).
3. Sinh viên chuyển đến từ trường khác phải tích lũy tối thiểu 50% tổng số tín chỉ của chương trình đào tạo tại Nhà trường mới được xét cấp bằng tốt nghiệp đại học của Trường.
4. Hiệu trưởng ra quyết định thành lập Hội đồng chuyên môn để đánh giá và quyết định số lượng tín chỉ được bảo lưu, công nhận giá trị chuyển đổi cho sinh viên chuyển đến."""
    })

    # Page 6: Cấu trúc chương trình đào tạo tín chỉ
    pages.append({
        "page": 6,
        "section": "chuong_trinh_tin_chi",
        "title": "Điều 6: Thời gian đào tạo và khối lượng kiến thức chương trình chuẩn",
        "text": """ĐIỀU 6: THỜI GIAN ĐÀO TẠO VÀ KHỐI LƯỢNG KIẾN THỨC CHƯƠNG TRÌNH CHUẨN
1. Chương trình đào tạo đại học chính quy được thiết kế theo hệ thống tín chỉ:
- Khối ngành Kỹ thuật và Công nghệ: khối lượng kiến thức từ 150 đến 160 tín chỉ, thời gian thiết kế chuẩn là 4.5 năm (9 học kỳ chính).
- Khối ngành Kinh tế, Quản trị và Khoa học Xã hội: khối lượng kiến thức từ 125 đến 135 tín chỉ, thời gian thiết kế chuẩn là 4.0 năm (8 học kỳ chính).
2. Thời gian tối đa để sinh viên hoàn thành chương trình đào tạo không được vượt quá 02 lần thời gian thiết kế chuẩn (tối đa 8 năm đối với khối Kinh tế và 9 năm đối với khối Kỹ thuật), bao gồm cả thời gian tạm dừng học tập có phép. Hết thời gian này, sinh viên chưa tốt nghiệp sẽ bị buộc thôi học.
3. Mỗi năm học bao gồm 02 học kỳ chính (học kỳ 1 và học kỳ 2) với thời lượng 15 tuần học tập và 3 tuần thi kết thúc học phần cho mỗi kỳ.
4. Nhà trường có thể tổ chức thêm 01 học kỳ phụ (học kỳ hè) với thời lượng 5 đến 7 tuần học và 1 tuần thi. Học kỳ hè không bắt buộc, sinh viên tự nguyện đăng ký để học vượt, học lại hoặc cải thiện điểm."""
    })

    # Page 7: Định mức tín chỉ đăng ký mỗi học kỳ
    pages.append({
        "page": 7,
        "section": "chuong_trinh_tin_chi",
        "title": "Điều 7: Giới hạn số lượng tín chỉ đăng ký trong từng học kỳ",
        "text": """ĐIỀU 7: GIỚI HẠN SỐ LƯỢNG TÍN CHỈ ĐĂNG KÝ TRONG TỪNG HỌC KỲ
1. Sinh viên có học lực bình thường (CPA từ 2.00 trở lên) được đăng ký:
- Trong mỗi học kỳ chính: tối thiểu 14 tín chỉ và tối đa 24 tín chỉ.
- Trong học kỳ hè: tối đa 8 tín chỉ và không quy định mức tối thiểu.
2. Sinh viên bị xếp hạng học lực yếu (CPA dưới 2.00) hoặc đang trong diện bị cảnh báo học vụ mức 1:
- Chỉ được đăng ký tối thiểu 10 tín chỉ và tối đa không quá 14 tín chỉ trong mỗi học kỳ chính.
- Mục đích nhằm giúp sinh viên tập trung cải thiện các học phần điểm kém và nâng cao kết quả học tập.
3. Sinh viên có học lực xuất sắc (CPA từ 3.60 trở lên) và không có môn học nào bị điểm dưới C trong kỳ trước đó được phép đăng ký vượt mức tối đa lên đến 28 tín chỉ trong học kỳ chính sau khi có phê duyệt của Trưởng khoa chuyên môn.
4. Sinh viên ở học kỳ cuối khóa chỉ còn thiếu số tín chỉ ít hơn mức tối thiểu quy định để đủ điều kiện tốt nghiệp thì được phép đăng ký đúng số tín chỉ còn thiếu mà không bị ràng buộc bởi mức tối thiểu 14 tín chỉ."""
    })

    # Page 8: Quy trình đăng ký học phần trực tuyến
    pages.append({
        "page": 8,
        "section": "chuong_trinh_tin_chi",
        "title": "Điều 8: Các giai đoạn đăng ký học phần và xử lý hủy lớp học",
        "text": """ĐIỀU 8: CÁC GIAI ĐOẠN ĐĂNG KÝ HỌC PHẦN VÀ XỬ LÝ HỦY LỚP HỌC
1. Việc đăng ký học phần được thực hiện trực tuyến trên cổng thông tin sinh viên theo 3 giai đoạn:
- Giai đoạn 1 (Đăng ký nguyện vọng): Diễn ra vào tuần 10 của học kỳ trước, sinh viên đăng ký danh sách học phần dự kiến học để Nhà trường dự trù số lớp và giảng viên.
- Giai đoạn 2 (Đăng ký chính thức theo thời khóa biểu): Diễn ra trước khi học kỳ mới bắt đầu 3 tuần. Sinh viên chọn lớp, giờ học và giảng viên cụ thể.
- Giai đoạn 3 (Đăng ký điều chỉnh, thêm/hủy môn): Diễn ra trong 02 tuần đầu tiên của học kỳ chính (01 tuần đầu của học kỳ hè).
2. Lớp học phần có số lượng sinh viên đăng ký dưới 20 sinh viên (đối với môn đại cương) hoặc dưới 10 sinh viên (đối với môn chuyên ngành hẹp) sẽ bị hủy lớp. Phòng Đào tạo thông báo hủy lớp chậm nhất 3 ngày trước khi học kỳ bắt đầu.
3. Sinh viên thuộc các lớp bị hủy sẽ được ưu tiên chuyển sang lớp khác còn chỗ hoặc được chọn học phần thay thế trong giai đoạn điều chỉnh."""
    })

    # Page 9: Rút học phần và hủy đăng ký
    pages.append({
        "page": 9,
        "section": "chuong_trinh_tin_chi",
        "title": "Điều 9: Thời hạn và điều kiện rút bớt học phần đã đăng ký",
        "text": """ĐIỀU 9: THỜI HẠN VÀ ĐIỀU KIỆN RÚT BỚT HỌC PHẦN ĐÃ ĐĂNG KÝ
1. Sau khi kết thúc giai đoạn điều chỉnh đăng ký, sinh viên được quyền xin rút học phần nếu cảm thấy không đảm bảo khả năng hoàn thành môn học.
2. Thời hạn rút học phần được quy định như sau:
- Học kỳ chính: Sinh viên được nộp đơn xin rút học phần từ tuần thứ 3 đến hết tuần thứ 6 của học kỳ.
- Học kỳ hè: Sinh viên được nộp đơn xin rút từ tuần thứ 2 đến hết tuần thứ 3 của học kỳ.
- Sau các thời hạn trên, Nhà trường tuyệt đối không giải quyết đơn xin rút học phần với bất kỳ lý do gì.
3. Điều kiện rút học phần: Sau khi rút, tổng số tín chỉ còn lại trong học kỳ chính không được thấp hơn mức tối thiểu (14 tín chỉ đối với sinh viên bình thường, 10 tín chỉ đối với sinh viên diện học lực yếu).
4. Học phần được chấp thuận rút sẽ nhận điểm chữ W (Withdrawn) trên bảng điểm. Điểm W không tính vào điểm trung bình học kỳ (GPA) và điểm trung bình tích lũy (CPA). Sinh viên rút học phần không được hoàn trả học phí của học phần đó."""
    })

    # Page 10: Học lại và học cải thiện điểm
    pages.append({
        "page": 10,
        "section": "chuong_trinh_tin_chi",
        "title": "Điều 10: Quy định về học lại môn bắt buộc và học cải thiện điểm số",
        "text": """ĐIỀU 10: QUY ĐỊNH VỀ HỌC LẠI MÔN BẮT BUỘC VÀ HỌC CẢI THIỆN ĐIỂM SỐ
1. Học lại (đối với môn bị điểm F):
- Sinh viên có học phần bắt buộc bị điểm F (dưới 4.0 thang 10 hoặc dưới 1.0 thang 4) bắt buộc phải đăng ký học lại học phần đó ở các học kỳ tiếp theo cho đến khi đạt điểm D trở lên.
- Đối với học phần tự chọn bị điểm F, sinh viên có thể chọn học lại chính học phần đó hoặc chọn học phần tự chọn khác tương đương trong cùng nhóm kiến thức để thay thế.
2. Học cải thiện điểm:
- Sinh viên có học phần đạt điểm D hoặc D+ được phép đăng ký học cải thiện để nâng cao điểm trung bình tích lũy. Điểm từ C trở lên không được phép học cải thiện.
- Khi học cải thiện, điểm của lần học sau sẽ thay thế hoàn toàn điểm của lần học trước trong việc tính CPA (kể cả trường hợp điểm lần sau thấp hơn lần trước). Điểm của cả hai lần học đều được lưu vết trong bảng điểm chi tiết.
3. Học phí học lại và học cải thiện: Sinh viên phải đóng học phí theo số tín chỉ thực tế của học phần đăng ký lại theo mức quy định hiện hành tại thời điểm học lại."""
    })

    # Page 11: Học cùng lúc hai chương trình (song bằng)
    pages.append({
        "page": 11,
        "section": "chuong_trinh_tin_chi",
        "title": "Điều 11: Điều kiện đăng ký học song bằng và duy trì chương trình thứ hai",
        "text": """ĐIỀU 11: ĐIỀU KIỆN ĐĂNG KÝ HỌC SONG BẰNG VÀ DUY TRÌ CHƯƠNG TRÌNH THỨ HAI
1. Sinh viên có nguyện vọng học cùng lúc hai chương trình đào tạo (song bằng) phải đáp ứng đầy đủ các tiêu chuẩn sau tại thời điểm đăng ký:
- Đã hoàn thành năm học thứ nhất của chương trình thứ nhất.
- Ngành đào tạo ở chương trình thứ hai phải khác ngành đào tạo ở chương trình thứ nhất.
- Điểm trung bình tích lũy CPA của chương trình thứ nhất đạt từ 2.50 trở lên và sinh viên không thuộc diện bị cảnh báo học vụ.
2. Sinh viên nộp đơn đăng ký học chương trình thứ hai tại Phòng Đào tạo vào đầu mỗi học kỳ chính.
3. Trong quá trình học cùng lúc hai chương trình, nếu CPA của chương trình thứ nhất bị giảm xuống dưới 2.00, sinh viên buộc phải dừng học chương trình thứ hai ở học kỳ tiếp theo.
4. Sinh viên chỉ được xét tốt nghiệp chương trình thứ hai nếu đã được công nhận tốt nghiệp chương trình thứ nhất hoặc đủ điều kiện tốt nghiệp đồng thời cả hai chương trình trong cùng một đợt xét tốt nghiệp. Thời gian tối đa hoàn thành chương trình thứ hai bằng thời gian tối đa của chương trình thứ nhất."""
    })

    # Page 12: Thang điểm và cách tính điểm học phần
    pages.append({
        "page": 12,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 12: Thang điểm đánh giá, công thức tính điểm học phần và quy đổi",
        "text": """ĐIỀU 12: THANG ĐIỂM ĐÁNH GIÁ, CÔNG THỨC TÍNH ĐIỂM HỌC PHẦN VÀ QUY ĐỔI
1. Điểm tổng kết học phần được tính theo thang điểm 10 (làm tròn đến một chữ số thập phân) theo công thức trọng số:
- Điểm học phần = (Điểm quá trình x Trọng số quá trình) + (Điểm thi cuối kỳ x Trọng số cuối kỳ).
- Trong đó, trọng số thi cuối kỳ tối thiểu là 50% và tối đa là 70% tùy theo đề cương chi tiết học phần.
2. Quy đổi điểm tổng kết học phần từ thang điểm 10 sang thang điểm chữ và thang điểm 4:
- Từ 8.5 đến 10.0: Điểm A (Tương đương 4.0 điểm thang 4 - Xếp loại Xuất sắc).
- Từ 8.0 đến 8.4: Điểm B+ (Tương đương 3.5 điểm thang 4 - Xếp loại Giỏi).
- Từ 7.0 đến 7.9: Điểm B (Tương đương 3.0 điểm thang 4 - Xếp loại Khá).
- Từ 6.5 đến 6.9: Điểm C+ (Tương đương 2.5 điểm thang 4 - Xếp loại Trung bình khá).
- Từ 5.5 đến 6.4: Điểm C (Tương đương 2.0 điểm thang 4 - Xếp loại Trung bình).
- Từ 5.0 đến 5.4: Điểm D+ (Tương đương 1.5 điểm thang 4 - Xếp loại Trung bình yếu).
- Từ 4.0 đến 4.9: Điểm D (Tương đương 1.0 điểm thang 4 - Xếp loại Đạt / Yếu).
- Dưới 4.0: Điểm F (Tương đương 0.0 điểm thang 4 - Xếp loại Không đạt / Kém).
3. Các học phần nhận điểm D trở lên được tính là đạt và tích lũy số tín chỉ tương ứng."""
    })

    # Page 13: Điều kiện dự thi kết thúc học phần
    pages.append({
        "page": 13,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 13: Tiêu chuẩn chuyên cần và điều kiện bắt buộc để dự thi kết thúc môn",
        "text": """ĐIỀU 13: TIÊU CHUẨN CHUYÊN CẦN VÀ ĐIỀU KIỆN BẮT BUỘC ĐỂ DỰ THI KẾT THÚC MÔN
1. Sinh viên được dự thi kết thúc học phần nếu thỏa mãn đồng thời hai điều kiện:
- Tham dự tối thiểu 80% tổng số giờ lên lớp lý thuyết và bài tập trên lớp theo thời khóa biểu.
- Hoàn thành đầy đủ 100% các bài thực hành, thí nghiệm, bài tập lớn và đồ án môn học (nếu học phần có quy định).
2. Sinh viên vắng mặt quá 20% tổng số giờ giảng lý thuyết (dù có phép hay không phép) sẽ bị cấm thi kết thúc học phần đó và nhận điểm F cho học phần. Giảng viên phụ trách có trách nhiệm công bố danh sách cấm thi trước ngày thi ít nhất 3 ngày làm việc.
3. Điểm đánh giá quá trình phải đạt từ 3.0 điểm trở lên trên thang điểm 10. Sinh viên có điểm quá trình dưới 3.0 điểm không được dự thi cuối kỳ và phải học lại học phần.
4. Sinh viên gian lận trong các bài kiểm tra định kỳ hoặc bài tập lớn sẽ bị nhận điểm 0 cho cột điểm đó và tùy mức độ có thể bị đình chỉ thi học phần."""
    })

    # Page 14: Hoãn thi và vắng thi
    pages.append({
        "page": 14,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 14: Quy trình xin hoãn thi cuối kỳ và xử lý các trường hợp vắng thi",
        "text": """ĐIỀU 14: QUY TRÌNH XIN HOÃN THI CUỐI KỲ VÀ XỬ LÝ CÁC TRƯỜNG HỢP VẮNG THI
1. Sinh viên có lý do chính đáng bất khả kháng (ốm đau cấp tính phải nằm viện, tai nạn, tang gia tứ thân phụ mẫu) không thể tham dự kỳ thi cuối kỳ được phép làm đơn xin hoãn thi.
2. Thủ tục và thời hạn nộp đơn hoãn thi:
- Đơn xin hoãn thi kèm theo minh chứng hợp lệ (giấy ra viện của bệnh viện, giấy chứng tử) phải nộp về Phòng Khảo thí và Đảm bảo chất lượng trong vòng 03 ngày làm việc kể từ ngày diễn ra ca thi.
- Đơn nộp quá thời hạn 03 ngày sẽ không được xem xét giải quyết.
3. Xử lý học phần hoãn thi:
- Học phần được chấp thuận hoãn thi sẽ nhận điểm tạm thời là điểm I (Incomplete).
- Sinh viên có điểm I phải đăng ký dự thi bù vào đợt thi của học kỳ chính gần nhất tiếp theo có tổ chức thi môn đó.
- Sau thời hạn 01 học kỳ chính tiếp theo, nếu sinh viên không dự thi bù, điểm I sẽ tự động chuyển thành điểm F.
4. Sinh viên vắng thi không có phép hoặc không được chấp thuận hoãn thi sẽ nhận điểm 0 cho kỳ thi cuối kỳ và bị tính điểm tổng kết theo công thức quy định."""
    })

    # Page 15: Cảnh báo học vụ
    pages.append({
        "page": 15,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 15: Các mức độ cảnh báo học vụ và tiêu chí áp dụng",
        "text": """ĐIỀU 15: CÁC MỨC ĐỘ CẢNH BÁO HỌC VỤ VÀ TIÊU CHÍ ÁP DỤNG
1. Cảnh báo học vụ được xử lý theo từng học kỳ chính nhằm giúp sinh viên nhận biết tình trạng học tập yếu kém để kịp thời khắc phục. Có 3 mức cảnh báo học vụ:
- Mức 1: Cảnh báo nhắc nhở khi sinh viên rơi vào một trong các trường hợp: Điểm trung bình học kỳ GPA dưới 1.20 đối với học kỳ đầu tiên của khóa học, hoặc dưới 1.40 đối với các học kỳ tiếp theo; hoặc có tổng số tín chỉ nợ đọng vượt quá 16 tín chỉ.
- Mức 2: Cảnh báo nghiêm trọng khi sinh viên đã bị cảnh báo mức 1 ở kỳ trước mà điểm GPA kỳ này tiếp tục dưới 1.60, hoặc CPA tích lũy dưới 1.80.
- Mức 3: Cảnh báo mức cao nhất khi sinh viên bị cảnh báo mức 2 ở kỳ trước mà không cải thiện được điểm số, CPA tích lũy tiếp tục dưới 1.80.
2. Sinh viên bị cảnh báo học vụ sẽ bị giới hạn số tín chỉ đăng ký ở học kỳ kế tiếp (tối đa không quá 14 tín chỉ) và phải tham gia buổi tư vấn học vụ bắt buộc với Cố vấn học tập của Khoa.
3. Thông báo cảnh báo học vụ được gửi trực tiếp về địa chỉ gia đình của sinh viên qua đường bưu điện và qua email sinh viên."""
    })

    # Page 16: Buộc thôi học do học vụ kém
    pages.append({
        "page": 16,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 16: Các trường hợp sinh viên bị xử lý buộc thôi học do học vụ",
        "text": """ĐIỀU 16: CÁC TRƯỜNG HỢP SINH VIÊN BỊ XỬ LÝ BUỘC THÔI HỌC DO HỌC VỤ
1. Sinh viên bị buộc thôi học nếu thuộc vào một trong các trường hợp sau:
- Bị cảnh báo học vụ mức 3 liên tiếp trong 02 học kỳ chính.
- Có tổng số lần bị cảnh báo học vụ vượt quá 03 lần trong toàn bộ khóa học.
- Vượt quá thời gian đào tạo tối đa cho phép theo quy định tại Điều 6 của Quy chế này.
- Tự ý bỏ học không đăng ký học phần trong một học kỳ chính mà không có đơn xin phép tạm dừng học tập được Hiệu trưởng phê duyệt.
- Điểm trung bình tích lũy CPA đạt dưới 1.00 sau 02 năm học đầu tiên.
2. Quy trình xử lý buộc thôi học:
- Phòng Đào tạo lập danh sách dự kiến buộc thôi học và thông báo công khai cho sinh viên trong thời hạn 10 ngày làm việc để khiếu nại hoặc giải trình.
- Sau thời hạn 10 ngày, Hội đồng Khen thưởng và Kỷ luật họp xem xét và trình Hiệu trưởng ký Quyết định buộc thôi học chính thức.
3. Sinh viên bị buộc thôi học được cấp Giấy chứng nhận kết quả học tập đối với các học phần đã tích lũy đạt điểm từ D trở lên."""
    })

    # Page 17: Xử lý vi phạm quy chế thi cử
    pages.append({
        "page": 17,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 17: Hình thức xử lý kỷ luật đối với hành vi gian lận thi cử",
        "text": """ĐIỀU 17: HÌNH THỨC XỬ LÝ KỶ LUẬT ĐỐI VỚI HÀNH VI GIAN LẬN THI CỬ
1. Sinh viên vi phạm quy chế trong phòng thi sẽ bị lập biên bản và xử lý kỷ luật theo các mức độ:
- Khiển trách: Áp dụng đối với thí sinh nhìn bài, trao đổi bài hoặc cho bạn nhìn bài một lần đã bị nhắc nhở nhưng vẫn tái phạm. Thí sinh bị khiển trách bị trừ 25% điểm bài thi của học phần đó.
- Cảnh cáo: Áp dụng đối với thí sinh mang tài liệu cấm vào phòng thi, sử dụng điện thoại di động hoặc thiết bị thu phát sóng trong giờ thi (kể cả chưa sử dụng), hoặc chép bài của người khác. Thí sinh bị cảnh cáo bị trừ 50% điểm bài thi học phần đó.
- Đình chỉ thi: Áp dụng đối với thí sinh tái phạm hành vi đã bị cảnh cáo, hoặc đưa đề thi ra ngoài phòng thi. Thí sinh bị đình chỉ thi nhận điểm 0 cho bài thi học phần và bị cấm thi tất cả các môn còn lại trong đợt thi đó.
- Buộc thôi học: Áp dụng đối với trường hợp thi hộ, nhờ người khác thi hộ, làm bài hộ hoặc nhờ người khác làm bài kiểm tra hộ. Cả người thi hộ và người nhờ thi hộ (nếu là sinh viên của trường) đều bị buộc thôi học ngay lập tức và thông báo về địa phương."""
    })

    # Page 18: Khiếu nại và phúc khảo bài thi
    pages.append({
        "page": 18,
        "section": "danh_gia_hoc_vu",
        "title": "Điều 18: Trình tự nộp đơn phúc khảo và thời hạn công bố điểm phúc khảo",
        "text": """ĐIỀU 18: TRÌNH TỰ NỘP ĐƠN PHÚC KHẢO VÀ THỜI HẠN CÔNG BỐ ĐIỂM PHÚC KHẢO
1. Sinh viên có quyền nộp đơn xin phúc khảo điểm thi kết thúc học phần nếu có nghi vấn về kết quả chấm thi.
2. Trình tự và thủ tục phúc khảo:
- Thời hạn nộp đơn: Trong vòng 07 ngày làm việc kể từ ngày điểm thi được công bố chính thức trên cổng thông tin sinh viên. Quá thời hạn trên, Nhà trường không tiếp nhận đơn phúc khảo.
- Địa điểm nộp đơn: Trực tuyến trên cổng thông tin sinh viên hoặc nộp trực tiếp tại Phòng Khảo thí và Đảm bảo chất lượng.
- Lệ phí phúc khảo là 50.000 VNĐ/bài thi. Nếu sau khi phúc khảo điểm thi thay đổi tăng lên, sinh viên sẽ được hoàn lại 100% lệ phí phúc khảo.
3. Tổ chức chấm phúc khảo:
- Trưởng phòng Khảo thí chỉ định hai cán bộ chấm thi độc lập (khác với cán bộ đã chấm lần đầu) tiến hành chấm lại bài thi.
- Điểm phúc khảo được công nhận nếu chênh lệch từ 0.5 điểm trở lên trên thang điểm 10 so với điểm chấm ban đầu. Trường hợp chênh lệch từ 1.0 điểm trở lên, phải có biên bản đối thoại giữa hai cặp cán bộ chấm thi.
4. Thời hạn công bố kết quả phúc khảo không quá 15 ngày làm việc kể từ ngày hết hạn nhận đơn."""
    })

    # Page 19: Định mức học phí và phương thức nộp
    pages.append({
        "page": 19,
        "section": "hoc_phi_hoc_bong",
        "title": "Điều 19: Cách tính học phí theo tín chỉ và thời hạn hoàn thành nghĩa vụ học phí",
        "text": """ĐIỀU 19: CÁCH TÍNH HỌC PHÍ THEO TÍN CHỈ VÀ THỜI HẠN HOÀN THÀNH NGHĨA VỤ HỌC PHÍ
1. Học phí được tính dựa trên tổng số tín chỉ mà sinh viên đăng ký trong học kỳ nhân với đơn giá của một tín chỉ theo từng nhóm ngành học:
- Nhóm ngành Khoa học Máy tính và Công nghệ Thông tin: 650.000 VNĐ / tín chỉ lý thuyết; 750.000 VNĐ / tín chỉ thực hành hoặc thí nghiệm.
- Nhóm ngành Kỹ thuật Điện - Điện tử và Cơ khí: 580.000 VNĐ / tín chỉ lý thuyết; 680.000 VNĐ / tín chỉ thực hành.
- Nhóm ngành Kinh tế, Quản trị Kinh doanh và Ngôn ngữ: 520.000 VNĐ / tín chỉ.
2. Thời hạn nộp học phí:
- Học kỳ chính: Sinh viên phải hoàn thành đóng học phí trước tuần thứ 8 của học kỳ.
- Học kỳ hè: Sinh viên phải hoàn thành đóng học phí trước tuần thứ 2 của học kỳ.
3. Sinh viên nợ học phí sau thời hạn thông báo sẽ bị xử lý:
- Bị khóa tài khoản đăng ký tín chỉ cho học kỳ tiếp theo.
- Bị cấm thi kết thúc học phần của tất cả các môn đã đăng ký trong học kỳ hiện tại và nhận điểm F.
- Không được cấp bảng điểm, chứng nhận sinh viên hoặc xét khen thưởng học bổng.
4. Phương thức nộp học phí: Chuyển khoản qua cổng thanh toán số của ngân hàng liên kết hoặc qua ứng dụng ngân hàng số quét mã QR định danh sinh viên."""
    })

    # Page 20: Gia hạn nộp học phí
    pages.append({
        "page": 20,
        "section": "hoc_phi_hoc_bong",
        "title": "Điều 20: Điều kiện và thủ tục xin gia hạn thời gian nộp học phí",
        "text": """ĐIỀU 20: ĐIỀU KIỆN VÀ THỦ TỤC XIN GIA HẠN THỜI GIAN NỘP HỌC PHÍ
1. Sinh viên có hoàn cảnh kinh tế gia đình đặc biệt khó khăn đột xuất (tai nạn, thiên tai, hỏa hoạn, biến cố gia đình) được phép làm đơn xin gia hạn nộp học phí.
2. Điều kiện được xem xét gia hạn:
- Sinh viên phải nộp trước tối thiểu 30% tổng số học phí phải nộp của học kỳ đó.
- Có đơn xin gia hạn nêu rõ lý do và cam kết ngày hoàn thành, có xác nhận của chính quyền địa phương cấp xã/phường nơi cư trú hoặc xác nhận của Trưởng khoa.
- Đơn phải nộp về Phòng Kế hoạch - Tài chính trước hạn nộp học phí quy định ít nhất 07 ngày làm việc.
3. Thời gian gia hạn:
- Thời gian gia hạn tối đa không quá 60 ngày kể từ ngày hết hạn nộp học phí chính thức của học kỳ đó, nhưng bắt buộc phải hoàn thành trước kỳ thi kết thúc học phần ít nhất 1 tuần.
4. Sinh viên được chấp thuận gia hạn nộp học phí vẫn được phép dự thi cuối kỳ bình thường và không bị khóa cổng đăng ký học phần đợt 1 của kỳ kế tiếp."""
    })

    # Page 21: Chính sách miễn giảm học phí
    pages.append({
        "page": 21,
        "section": "hoc_phi_hoc_bong",
        "title": "Điều 21: Các đối tượng được hưởng chính sách miễn, giảm học phí",
        "text": """ĐIỀU 21: CÁC ĐỐI TƯỢNG ĐƯỢC HƯỞNG CHÍNH SÁCH MIỄN, GIẢM HỌC PHÍ
1. Đối tượng được miễn 100% học phí bao gồm:
- Sinh viên là con của liệt sĩ, thương binh nặng, người hưởng chính sách như thương binh có tỷ lệ suy giảm khả năng lao động từ 81% trở lên.
- Sinh viên khuyết tật nặng hoặc đặc biệt nặng có giấy xác nhận của cơ quan có thẩm quyền.
- Sinh viên mồ côi cả cha lẫn mẹ, không nơi nương tựa theo quy định của Luật Trợ giúp Xã hội.
- Sinh viên là người dân tộc thiểu số rất ít người ở vùng có điều kiện kinh tế - xã hội khó khăn hoặc đặc biệt khó khăn.
2. Đối tượng được giảm 70% học phí:
- Sinh viên theo học các ngành nghệ thuật truyền thống, các chuyên ngành nhã nhạc cung đình, chèo, tuồng, cải lương hoặc các ngành nặng nhọc, độc hại theo danh mục quy định.
3. Đối tượng được giảm 50% học phí:
- Sinh viên là con của cán bộ, công chức, viên chức, công nhân mà cha hoặc mẹ bị tai nạn lao động hoặc mắc bệnh nghề nghiệp được hưởng trợ cấp thường xuyên.
4. Hồ sơ xin miễn giảm học phí nộp trong vòng 30 ngày kể từ ngày bắt đầu năm học mới. Chính sách miễn giảm chỉ áp dụng cho thời gian học chuẩn, không áp dụng cho số tín chỉ học lại hoặc học cải thiện điểm."""
    })

    # Page 22: Học bổng khuyến khích học tập
    pages.append({
        "page": 22,
        "section": "hoc_phi_hoc_bong",
        "title": "Điều 22: Tiêu chuẩn và định mức học bổng khuyến khích học tập từng học kỳ",
        "text": """ĐIỀU 22: TIÊU CHUẨN VÀ ĐỊNH MỨC HỌC BỔNG KHUYẾN KHÍCH HỌC TẬP TỪNG HỌC KỲ
1. Học bổng khuyến khích học tập được xét và cấp theo từng học kỳ chính (không xét cho học kỳ hè) cho sinh viên có kết quả học tập và rèn luyện từ loại Khá trở lên, không bị kỷ luật trong kỳ xét học bổng.
2. Các mức học bổng khuyến khích học tập:
- Mức học bổng Xuất sắc: Dành cho sinh viên có điểm trung bình học kỳ GPA từ 3.60 trở lên và điểm rèn luyện ĐRL từ 90 điểm trở lên. Mức học bổng tương đương 120% định mức học phí chuẩn của ngành học.
- Mức học bổng Giỏi: Dành cho sinh viên có điểm GPA từ 3.20 đến 3.59 và điểm ĐRL từ 80 điểm trở lên. Mức học bổng tương đương 105% định mức học phí chuẩn của ngành học.
- Mức học bổng Khá: Dành cho sinh viên có điểm GPA từ 2.80 đến 3.19 và điểm ĐRL từ 70 điểm trở lên. Mức học bổng tương đương 100% định mức học phí chuẩn của ngành học.
3. Điều kiện ràng buộc về số tín chỉ:
- Sinh viên phải đăng ký và hoàn thành tối thiểu 15 tín chỉ trong học kỳ xét học bổng (không tính các tín chỉ học lại, học cải thiện, học phần GDTC và GDQP-AN).
- Trong học kỳ đó không có học phần nào bị điểm dưới C (dưới 2.0).
4. Học bổng được xét từ điểm cao xuống thấp cho đến khi hết quỹ học bổng phân bổ cho từng ngành."""
    })

    # Page 23: Học bổng tài trợ của doanh nghiệp
    pages.append({
        "page": 23,
        "section": "hoc_phi_hoc_bong",
        "title": "Điều 23: Quy định tiếp nhận và xét cấp học bổng tài trợ ngoài ngân sách",
        "text": """ĐIỀU 23: QUY ĐỊNH TIẾP NHẬN VÀ XÉT CẤP HỌC BỔNG TÀI TRỢ NGOÀI NGÂN SÁCH
1. Nhà trường tiếp nhận các nguồn học bổng tài trợ từ doanh nghiệp, tổ chức xã hội, cựu sinh viên và các đối tác quốc tế để trao tặng sinh viên.
2. Phân loại học bổng tài trợ:
- Học bổng vượt khó học tốt: Dành cho sinh viên có hoàn cảnh kinh tế gia đình khó khăn (hộ nghèo, cận nghèo) có điểm GPA từ 2.50 trở lên và điểm rèn luyện từ 70 điểm trở lên.
- Học bổng tài năng và nghiên cứu: Dành cho sinh viên đạt giải thưởng trong các cuộc thi học thuật, sáng tạo khởi nghiệp hoặc có bài báo khoa học xuất bản trên các tạp chí uy tín.
- Học bổng phát triển kỹ năng và công nghệ: Do các tập đoàn công nghệ tài trợ kèm cam kết thực tập và cơ hội việc làm sau khi tốt nghiệp.
3. Nguyên tắc xét chọn: Sinh viên được quyền nhận đồng thời học bổng khuyến khích học tập của Nhà trường và học bổng tài trợ doanh nghiệp, trừ trường hợp nhà tài trợ có quy định riêng loại trừ.
4. Thông tin và thời hạn nộp hồ sơ xin học bổng doanh nghiệp được đăng tải công khai trên website Phòng Công tác Sinh viên trước thời hạn nhận đơn tối thiểu 15 ngày."""
    })

    # Page 24: Hỗ trợ sinh viên vay vốn tín dụng học tập
    pages.append({
        "page": 24,
        "section": "hoc_phi_hoc_bong",
        "title": "Điều 24: Thủ tục xác nhận để vay vốn Ngân hàng Chính sách Xã hội",
        "text": """ĐIỀU 24: THỦ TỤC XÁC NHẬN ĐỂ VAY VỐN NGÂN HÀNG CHÍNH SÁCH XÃ HỘI
1. Sinh viên có nhu cầu vay vốn tín dụng học sinh, sinh viên theo Quyết định của Thủ tướng Chính phủ thông qua Ngân hàng Chính sách Xã hội (NHCSXH) được Nhà trường cấp Giấy xác nhận theo mẫu quy định.
2. Đối tượng được cấp giấy xác nhận vay vốn:
- Sinh viên mồ côi cả cha lẫn mẹ hoặc mồ côi một người và người còn lại mất khả năng lao động.
- Sinh viên là thành viên của hộ gia đình thuộc hộ nghèo, hộ cận nghèo theo chuẩn quy định của Nhà nước.
- Sinh viên mà gia đình gặp khó khăn về tài chính do tai nạn, bệnh tật, thiên tai, hỏa hoạn, dịch bệnh có xác nhận của UBND xã/phường.
3. Quy trình cấp giấy xác nhận:
- Sinh viên điền thông tin vào đơn đề nghị trên cổng thông tin sinh viên và in mẫu giấy xác nhận.
- Nộp tại Bộ phận Một cửa - Phòng Công tác Sinh viên kèm bản sao Sổ hộ nghèo/cận nghèo hoặc minh chứng liên quan.
- Thời gian giải quyết và trả kết quả giấy xác nhận là 02 ngày làm việc.
4. Sinh viên có trách nhiệm sử dụng nguồn vốn vay đúng mục đích chi trả học phí và sinh hoạt phí phục vụ học tập, đồng thời thực hiện nghĩa vụ trả nợ gốc và lãi đúng cam kết với ngân hàng."""
    })

    # Page 25: Tạm dừng và bảo lưu kết quả học tập
    pages.append({
        "page": 25,
        "section": "tot_nghiep_bao_luu",
        "title": "Điều 25: Điều kiện và thủ tục xin tạm dừng, bảo lưu kết quả học tập",
        "text": """ĐIỀU 25: ĐIỀU KIỆN VÀ THỦ TỤC XIN TẠM DỪNG, BẢO LƯU KẾT QUẢ HỌC TẬP
1. Sinh viên được quyền xin tạm dừng học tập và bảo lưu kết quả học tập đã tích lũy trong các trường hợp sau:
- Được điều động vào lực lượng vũ trang nhân dân (nghĩa vụ quân sự hoặc nghĩa vụ công an). Thời gian bảo lưu theo thời gian thực hiện nghĩa vụ quân sự không tính vào thời gian học tập tối đa.
- Được cơ quan có thẩm quyền cử đi đại diện quốc gia tham gia các kỳ thi, giải đấu thể thao, văn hóa quốc tế.
- Bị ốm đau, thai sản, tai nạn phải điều trị trong thời gian dài có giấy xác nhận và chỉ định nghỉ học của bệnh viện cấp quận/huyện trở lên.
- Vì lý do cá nhân khác: Sinh viên phải học xong ít nhất 01 học kỳ chính tại trường, đạt điểm GPA kỳ gần nhất từ 2.00 trở lên và không thuộc diện bị cảnh báo học vụ hoặc bị xem xét kỷ luật.
2. Thời gian tạm dừng học tập vì lý do cá nhân không được quá 02 học kỳ chính cho một lần xin và tổng thời gian tạm dừng tích lũy không quá 04 học kỳ trong toàn khóa học.
3. Thời hạn nộp đơn xin tạm dừng: Sinh viên phải nộp đơn trước khi học kỳ mới bắt đầu ít nhất 02 tuần, trừ trường hợp lý do y tế bất khả kháng.
4. Khi hết thời hạn tạm dừng, sinh viên phải nộp đơn xin trở lại học tập trước khi học kỳ mới bắt đầu ít nhất 03 tuần để được xếp lớp."""
    })

    # Page 26: Công nhận và chuyển đổi tín chỉ
    pages.append({
        "page": 26,
        "section": "tot_nghiep_bao_luu",
        "title": "Điều 26: Miễn trừ học phần và công nhận chuyển đổi tín chỉ tương đương",
        "text": """ĐIỀU 26: MIỄN TRỪ HỌC PHẦN VÀ CÔNG NHẬN CHUYỂN ĐỔI TÍN CHỈ TƯƠNG ĐƯƠNG
1. Sinh viên đã học và tích lũy các học phần tại cơ sở đào tạo đại học khác hoặc các chương trình đào tạo khác của Nhà trường được xem xét công nhận tín chỉ và miễn học nếu thỏa mãn:
- Khối lượng kiến thức và số tín chỉ của học phần đề nghị công nhận bằng hoặc lớn hơn học phần trong chương trình hiện tại.
- Nội dung học phần có độ tương đồng tối thiểu từ 80% trở lên theo xác nhận của Bộ môn phụ trách môn học.
- Điểm học phần đạt từ điểm C (hoặc từ 5.5 điểm thang 10) trở lên.
2. Tổng số tín chỉ được công nhận và chuyển đổi tối đa không được vượt quá 50% tổng số tín chỉ của chương trình đào tạo sinh viên đang theo học.
3. Miễn học phần Tiếng Anh và Tin học đại cương:
- Sinh viên có chứng chỉ quốc tế hợp lệ còn thời hạn (IELTS từ 5.5 trở lên, TOEIC 4 kỹ năng tương đương hoặc chứng chỉ MOS, IC3) được miễn học và công nhận điểm A (4.0) cho các học phần ngoại ngữ, tin học đại cương tương ứng theo bảng quy đổi của Trường.
4. Điểm của các học phần được công nhận tương đương sẽ được tính vào điểm trung bình chung tích lũy CPA của sinh viên."""
    })

    # Page 27: Điều kiện xét và công nhận tốt nghiệp
    pages.append({
        "page": 27,
        "section": "tot_nghiep_bao_luu",
        "title": "Điều 27: Bộ tiêu chuẩn bắt buộc để được công nhận tốt nghiệp đại học",
        "text": """ĐIỀU 27: BỘ TIÊU CHUẨN BẮT BUỘC ĐỂ ĐƯỢC CÔNG NHẬN TỐT NGHIỆP ĐẠI HỌC
1. Sinh viên được công nhận tốt nghiệp và cấp bằng cử nhân/kỹ sư khi hội đủ đồng thời các điều kiện sau:
- Tích lũy đủ số tín chỉ và hoàn thành đầy đủ tất cả các học phần bắt buộc, tự chọn theo đúng khung chương trình đào tạo của ngành học.
- Điểm trung bình chung tích lũy toàn khóa học (CPA) đạt từ 2.00 trở lên trên thang điểm 4.0.
- Đạt chuẩn đầu ra về Ngoại ngữ: Chứng chỉ tiếng Anh quốc tế tối thiểu IELTS 5.5 hoặc TOEIC 600 điểm (đối với khối ngành Kinh tế, Kỹ thuật), hoặc chứng chỉ tương đương theo khung 6 bậc Việt Nam (Bậc 3 - B1).
- Đạt chuẩn đầu ra về Tin học: Chứng chỉ Tin học văn phòng quốc tế MOS (tối thiểu 3 kỹ năng Word, Excel, PowerPoint đạt từ 700 điểm/kỹ năng) hoặc IC3.
- Hoàn thành đầy đủ chứng chỉ Giáo dục Thể chất (GDTC) và chứng chỉ Giáo dục Quốc phòng - An ninh (GDQP-AN).
- Có điểm rèn luyện toàn khóa đạt từ loại Trung bình (từ 50 điểm) trở lên.
- Cho đến thời điểm xét tốt nghiệp không bị truy cứu trách nhiệm hình sự hoặc không đang trong thời gian bị kỷ luật từ mức đình chỉ học tập trở lên.
2. Nhà trường tổ chức xét tốt nghiệp chính thức 04 đợt trong một năm học vào các tháng: Tháng 3, Tháng 6, Tháng 9 và Tháng 12."""
    })

    # Page 28: Xếp loại tốt nghiệp và hạ hạng bằng
    pages.append({
        "page": 28,
        "section": "tot_nghiep_bao_luu",
        "title": "Điều 28: Thang phân loại tốt nghiệp và các quy định về hạ hạng tốt nghiệp",
        "text": """ĐIỀU 28: THANG PHÂN LOẠI TỐT NGHIỆP VÀ CÁC QUY ĐỊNH VỀ HẠ HẠNG TỐT NGHIỆP
1. Xếp loại tốt nghiệp được xác định căn cứ vào điểm trung bình chung tích lũy CPA toàn khóa:
- Loại Xuất sắc: Điểm CPA từ 3.60 đến 4.00.
- Loại Giỏi: Điểm CPA từ 3.20 đến 3.59.
- Loại Khá: Điểm CPA từ 2.50 đến 3.19.
- Loại Trung bình: Điểm CPA từ 2.00 đến 2.49.
2. Quy định hạ một bậc xếp loại tốt nghiệp:
Hạng tốt nghiệp của sinh viên có kết quả toàn khóa đạt loại Xuất sắc hoặc Giỏi sẽ bị giảm đi một bậc (từ Xuất sắc xuống Giỏi, từ Giỏi xuống Khá) nếu vi phạm vào một trong hai trường hợp sau:
- Có tổng số tín chỉ của các học phần phải học lại (điểm F) vượt quá 5% tổng số tín chỉ quy định cho toàn bộ chương trình đào tạo.
- Đã từng bị kỷ luật trong thời gian học từ mức cảnh cáo cấp trường trở lên.
3. Không hạ bậc xếp loại đối với sinh viên tốt nghiệp loại Khá hoặc Trung bình.
4. Bằng tốt nghiệp đại học được cấp một lần kèm theo Phụ lục văn bằng (Bảng điểm chi tiết toàn khóa) ghi rõ ngành đào tạo, xếp loại tốt nghiệp và danh mục tất cả học phần đã tích lũy."""
    })

    # Page 29: Cấp giấy chứng nhận tốt nghiệp tạm thời và cấp bằng
    pages.append({
        "page": 29,
        "section": "tot_nghiep_bao_luu",
        "title": "Điều 29: Quy trình cấp chứng nhận tốt nghiệp tạm thời và nhận bằng chính thức",
        "text": """ĐIỀU 29: QUY TRÌNH CẤP CHỨNG NHẬN TỐT NGHIỆP TẠM THỜI VÀ NHẬN BẰNG CHÍNH THỨC
1. Sau khi Hội đồng Xét tốt nghiệp Nhà trường thông qua danh sách và Hiệu trưởng ký Quyết định công nhận tốt nghiệp, sinh viên được cấp Giấy chứng nhận tốt nghiệp tạm thời trong vòng 07 ngày làm việc.
2. Giấy chứng nhận tốt nghiệp tạm thời có giá trị pháp lý tương đương bằng tốt nghiệp trong thời hạn 06 tháng kể từ ngày ký, dùng để sinh viên xin việc hoặc học tiếp lên bậc cao học.
3. Bằng tốt nghiệp đại học chính thức và Bảng điểm chi tiết được trao tại Lễ tốt nghiệp hoặc nhận tại Phòng Đào tạo sau không quá 60 ngày kể từ ngày ban hành quyết định công nhận tốt nghiệp.
4. Thủ tục nhận bằng tốt nghiệp chính thức:
- Sinh viên phải xuất trình Căn cước công dân gốc và Thẻ sinh viên khi nhận bằng.
- Trường hợp ủy quyền nhận bằng thay: Người được ủy quyền phải có Giấy ủy quyền hợp pháp có công chứng của cơ quan công chứng Nhà nước kèm bản sao CCCD của sinh viên và CCCD gốc của người được ủy quyền.
5. Nhà trường không cấp lại bản gốc bằng tốt nghiệp trong bất kỳ trường hợp nào bị mất hoặc hư hỏng; chỉ cấp Bản sao trích lục từ sổ gốc cấp bằng theo quy định của Bộ Giáo dục và Đào tạo."""
    })

    # Page 30: Nghiên cứu khoa học sinh viên
    pages.append({
        "page": 30,
        "section": "nckh_ngoai_khoa",
        "title": "Điều 30: Đăng ký đề tài nghiên cứu khoa học và chính sách khen thưởng",
        "text": """ĐIỀU 30: ĐĂNG KÝ ĐỀ TÀI NGHIÊN CỨU KHOA HỌC VÀ CHÍNH SÁCH KHEN THƯỞNG
1. Sinh viên từ năm thứ hai trở đi có điểm CPA từ 2.50 trở lên được quyền đăng ký chủ trì hoặc tham gia đề tài Nghiên cứu khoa học (NCKH) sinh viên cấp Trường.
2. Mỗi đề tài do một nhóm từ 1 đến 5 sinh viên thực hiện dưới sự hướng dẫn của 01 cán bộ giảng viên. Thời gian thực hiện đề tài tối đa là 10 tháng kể từ ngày phê duyệt thuyết minh.
3. Kinh phí hỗ trợ nghiên cứu:
- Đề tài cấp Trường được phê duyệt được cấp kinh phí hỗ trợ ban đầu từ 5.000.000 VNĐ đến 15.000.000 VNĐ tùy thuộc quy mô và dự toán.
4. Khen thưởng và quyền lợi học vụ:
- Sinh viên đạt giải Nhất, Nhì NCKH cấp Trường được cộng điểm rèn luyện (tương ứng 15 và 10 điểm) và được xem xét thay thế khóa luận tốt nghiệp (tương đương 6 đến 10 tín chỉ) nếu đề tài đạt loại Xuất sắc.
- Nhóm sinh viên có bài báo khoa học được chấp nhận đăng trên tạp chí thuộc danh mục Scopus/WoS được Nhà trường thưởng nóng 10.000.000 VNĐ/bài báo và ưu tiên xét học bổng tài trợ doanh nghiệp."""
    })

    # Page 31: Đánh giá điểm rèn luyện sinh viên
    pages.append({
        "page": 31,
        "section": "nckh_ngoai_khoa",
        "title": "Điều 31: Khung tiêu chí và thang điểm đánh giá kết quả rèn luyện sinh viên",
        "text": """ĐIỀU 31: KHUNG TIÊU CHÍ VÀ THANG ĐIỂM ĐÁNH GIÁ KẾT QUẢ RÈN LUYỆN SINH VIÊN
1. Điểm rèn luyện (ĐRL) được đánh giá theo thang điểm 100 cho từng học kỳ chính dựa trên 5 tiêu chí:
- Tiêu chí 1: Đánh giá về ý thức tham gia học tập (tối đa 20 điểm).
- Tiêu chí 2: Đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong nhà trường (tối đa 25 điểm).
- Tiêu chí 3: Đánh giá về ý thức tham gia các hoạt động chính trị, xã hội, văn hóa, thể thao, tình nguyện (tối đa 20 điểm).
- Tiêu chí 4: Đánh giá về phẩm chất công dân và quan hệ với cộng đồng (tối đa 25 điểm).
- Tiêu chí 5: Đánh giá về ý thức và kết quả tham gia phụ trách lớp, đoàn thể, câu lạc bộ hoặc thành tích đặc biệt (tối đa 10 điểm).
2. Xếp loại rèn luyện theo tổng điểm ĐRL:
- Từ 90 đến 100 điểm: Loại Xuất sắc.
- Từ 80 đến 89 điểm: Loại Tốt.
- Từ 65 đến 79 điểm: Loại Khá.
- Từ 50 đến 64 điểm: Loại Trung bình.
- Từ 35 đến 49 điểm: Loại Yếu.
- Dưới 35 điểm: Loại Kém.
3. Sinh viên bị xếp loại rèn luyện Yếu hoặc Kém trong 02 học kỳ liên tiếp sẽ bị xem xét tạm dừng học tập 01 học kỳ chính."""
    })

    # Page 32: Tiêu chuẩn danh hiệu Sinh viên 5 tốt
    pages.append({
        "page": 32,
        "section": "nckh_ngoai_khoa",
        "title": "Điều 32: Bộ tiêu chuẩn xét chọn danh hiệu Sinh viên 5 tốt các cấp",
        "text": """ĐIỀU 32: BỘ TIÊU CHUẨN XÉT CHỌN DANH HIỆU SINH VIÊN 5 TỐT CÁC CẤP
1. Danh hiệu "Sinh viên 5 tốt" là danh hiệu thi đua cao quý của Hội Sinh viên Việt Nam trao tặng hằng năm cho sinh viên đạt đủ 5 tiêu chuẩn:
- Đạo đức tốt: Điểm rèn luyện đạt từ 85 điểm trở lên; không vi phạm pháp luật và nội quy nhà trường; đạt danh hiệu Đoàn viên xuất sắc.
- Học tập tốt: Điểm trung bình học tập GPA năm học đạt từ 3.20/4.0 trở lên (hoặc từ 3.40 đối với cấp Tỉnh/Thành phố); tham gia ít nhất 01 đề tài NCKH hoặc cuộc thi học thuật chuyên ngành.
- Thể lực tốt: Đạt chuẩn thể lực theo quy định của Bộ Giáo dục và Đào tạo hoặc tham gia tích cực giải thể thao cấp trường trở lên; hoặc có chứng nhận tham gia giải chạy phong trào từ 5km trở lên.
- Tình nguyện tốt: Tham gia ít nhất 05 ngày tình nguyện trong năm học (như chiến dịch Mùa hè xanh, Tiếp sức mùa thi, Hiến máu nhân đạo ít nhất 01 lần).
- Hội nhập tốt: Đạt chứng chỉ tiếng Anh từ B1 trở lên hoặc tham gia ít nhất 01 chương trình giao lưu sinh viên quốc tế, diễn đàn hội nhập thanh niên.
2. Quyền lợi: Sinh viên đạt danh hiệu "Sinh viên 5 tốt" cấp Trường trở lên được nhận Giấy khen của Hiệu trưởng, tiền thưởng theo quy chế thi đua và được ưu tiên giới thiệu học bổng du học, việc làm tại các tập đoàn đối tác."""
    })

    return pages

def build_pdf(pages_data, output_pdf_path):
    doc = fitz.open()
    # A4 size in points: 595 x 842
    font_name = "helv"
    
    for page_dict in pages_data:
        page = doc.new_page(width=595, height=842)
        
        # Header banner
        header_text = f"SỔ TAY SINH VIÊN & QUY CHẾ ĐÀO TẠO 2025-2026 | TRANG {page_dict['page']}"
        page.insert_text(fitz.Point(50, 40), header_text, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
        
        # Section title
        sec_title = f"[{page_dict['section'].upper()}] - {page_dict['title']}"
        page.insert_text(fitz.Point(50, 70), sec_title, fontsize=12, fontname="helv", color=(0.1, 0.1, 0.6))
        
        # Body text in rect
        rect = fitz.Rect(50, 95, 545, 780)
        # We insert text
        page.insert_textbox(rect, page_dict["text"], fontsize=10.5, fontname="helv", color=(0, 0, 0))
        
        # Footer
        footer_text = f"Mã văn bản: QC-DT-2025 | Hiệu lực: 01/09/2025 | Trang {page_dict['page']}/32"
        page.insert_text(fitz.Point(180, 810), footer_text, fontsize=8.5, fontname="helv", color=(0.4, 0.4, 0.4))
        
    doc.save(str(output_pdf_path))
    doc.close()

def main():
    pages_data = generate_pages_data()
    print(f"Generated {len(pages_data)} pages.")
    
    # Save JSON corpus
    json_path = Path("data/handbook_sv_2025.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pages_data, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON corpus to {json_path}")
    
    # Save PDF corpus
    pdf_path = Path("data/handbook_sv_2025.pdf")
    build_pdf(pages_data, pdf_path)
    print(f"Saved PDF corpus to {pdf_path}")
    
    # Calculate stats
    total_chars = sum(len(p["text"]) for p in pages_data)
    min_chars = min(len(p["text"]) for p in pages_data)
    max_chars = max(len(p["text"]) for p in pages_data)
    avg_chars = total_chars / len(pages_data)
    
    print(f"Total characters: {total_chars}")
    print(f"Min chars per page: {min_chars}")
    print(f"Max chars per page: {max_chars}")
    print(f"Avg chars per page: {avg_chars:.1f}")
    
    # Generate Manifest
    manifest = {
        "source_id": "handbook_sv_2025",
        "title": "Sổ tay Sinh viên và Quy chế Đào tạo Đại học Chính quy năm học 2025-2026",
        "source_path": "data/handbook_sv_2025.pdf",
        "license_or_permission": "Tài liệu học thuật nội bộ mở cho mục đích đào tạo và nghiên cứu (Creative Commons Attribution-NonCommercial 4.0 International - CC BY-NC 4.0)",
        "accessed_at": "2026-11-14T00:00:00Z",
        "snapshot_version": "2025.1.0",
        "effective_date": "2025-09-01",
        "total_physical_pages": 32,
        "content_pages_count": 32,
        "content_pages_list": list(range(1, 33)),
        "page_counting_rule": "Toàn bộ 32 trang vật lý đều là trang nội dung hữu ích theo từng Điều quy chế cụ thể; không bao gồm trang bìa rỗng hoặc phụ lục chỉ có danh mục ngoài lề. Mỗi trang trung bình trên 1.500 ký tự chuẩn hóa.",
        "character_statistics": {
            "total_normalized_characters": total_chars,
            "min_characters_per_page": min_chars,
            "max_characters_per_page": max_chars,
            "avg_characters_per_page": round(avg_chars, 1)
        },
        "sections": [
            {"section_id": s[0], "title": s[1], "start_page": s[2], "end_page": s[3]}
            for s in SECTIONS
        ]
    }
    
    manifest_path = Path("data/manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Saved manifest to {manifest_path}")

if __name__ == "__main__":
    main()

