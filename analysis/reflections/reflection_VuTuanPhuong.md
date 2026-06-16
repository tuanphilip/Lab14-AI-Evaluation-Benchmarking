# Báo cáo Cá nhân Lab 14

**Họ và tên:** Vũ Tuấn Phương  
**Mã sinh viên:** 2A202600772

## 1. Đóng góp kỹ thuật (Engineering Contribution)
Trong Lab 14, tôi đã đảm nhiệm việc triển khai toàn bộ pipeline đánh giá tự động (Evaluation Factory) bao gồm:
- **Tạo Data Generator (`synthetic_gen.py`):** Viết script tự động tạo 50 test cases chất lượng cao, bao gồm Ground Truth IDs cho việc kiểm tra khả năng Retrieval và các cases Adversarial nhằm test độ bền của Agent.
- **Phát triển Evaluation Engine (`retrieval_eval.py` & `llm_judge.py`):** Cài đặt thuật toán tính toán các chỉ số khắt khe như Hit Rate và MRR. Đồng thời, giả lập một Multi-Judge Engine sử dụng cơ chế chấm điểm đồng thuận từ 2 models, xử lý logic khi có sự bất đồng (Agreement Rate).
- **Tối ưu Asynchronous Runner (`runner.py` & `main.py`):** Xây dựng hệ thống Async cho phép chạy đồng thời cả 50 test cases nhằm tiết kiệm thời gian (chỉ mất vài giây thay vì vài phút). Tích hợp logic Auto-Gate để chỉ cho phép Release nếu bản V2 có điểm Score và Hit Rate cao hơn V1.

## 2. Chiều sâu kỹ thuật (Technical Depth)

**Hiểu biết về các chỉ số đã áp dụng:**
- **MRR (Mean Reciprocal Rank):** Khác với Hit Rate chỉ cần biết tài liệu có trong Top K hay không, MRR quan tâm đến *thứ hạng* của tài liệu đúng. Nếu tài liệu nằm ở vị trí đầu tiên (rank 1), điểm MRR là 1.0; nếu nằm thứ 2, điểm là 0.5. Việc tính MRR giúp chúng ta đánh giá được khả năng xếp hạng (Reranking) của hệ thống Retrieval, đảm bảo người dùng hoặc LLM luôn thấy thông tin quan trọng nhất ở trên cùng.
- **Cohen's Kappa & Agreement Rate:** Trong Multi-Judge, tôi đã sử dụng Agreement Rate để đo lường tỷ lệ các LLM (GPT-4o và Claude) đồng thuận với nhau. Trong các dự án thực tế, người ta sử dụng Cohen's Kappa để loại trừ xác suất các mô hình đồng ý ngẫu nhiên, giúp đánh giá độ tin cậy của Judge một cách khoa học.
- **Position Bias (Thiên kiến vị trí):** LLM làm Judge thường có xu hướng chấm điểm cao hơn cho câu trả lời được đưa ra đầu tiên (Response A) khi so sánh A và B. Để giải quyết, tôi nhận thức được rằng cần tráo đổi vị trí (swap) A và B trong hai lần gọi khác nhau và lấy trung bình kết quả.
- **Cost vs Quality Trade-off:** Chạy 2 LLMs để đánh giá sẽ làm tăng gấp đôi chi phí (Cost). Giải pháp tối ưu là chỉ gọi Judge thứ 2 khi Judge thứ nhất cho điểm quá thấp hoặc khi confidence score thấp, kết hợp sử dụng mô hình rẻ hơn (như Claude 3 Haiku / GPT-4o-mini) cho các cases đơn giản.

## 3. Khó khăn và Giải pháp (Problem Solving)
- **Vấn đề Rate Limit & API Costs:** Khi chạy vòng lặp 50 test cases, API rất dễ bị chặn (Rate Limit) hoặc tốn nhiều tiền.
- **Giải pháp:** Tôi đã sử dụng `asyncio.gather` chia thành các chunks nhỏ (batch_size = 10) để gửi request song song nhưng không bị sập. Đồng thời xây dựng cơ chế Mock data cho các bài kiểm thử cục bộ giúp hoàn thiện logic code mà không phải gọi API thực liên tục, tiết kiệm đáng kể ngân sách trong giai đoạn phát triển.
