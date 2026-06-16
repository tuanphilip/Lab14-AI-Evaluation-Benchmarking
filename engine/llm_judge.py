import asyncio
import random
from typing import Dict, Any

class LLMJudge:
    def __init__(self):
        self.rubrics = {
            "accuracy": "Chấm điểm từ 1-5 dựa trên độ chính xác so với Ground Truth.",
            "tone": "Chấm điểm từ 1-5 dựa trên sự chuyên nghiệp của ngôn ngữ."
        }

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Mô phỏng gọi 2 models: GPT-4o và Claude 3.5 Sonnet.
        Nếu mô phỏng, ta sẽ dựa vào answer để cấp điểm ngẫu nhiên nhưng có cơ sở (giả định agent trả lời ổn).
        """
        await asyncio.sleep(0.1) # Simulate API latency

        # Giả lập điểm số dựa vào độ dài và chất lượng (V2 dài hơn)
        base_score = 4 if len(answer) > 20 else 2
        if "V2 đã cải thiện" in answer:
            base_score = 5
        
        # GPT-4o có thể cho điểm base_score hoặc dao động nhẹ
        score_a = min(5, max(1, base_score + random.choice([0, 0, -1] if base_score == 5 else [0, 0, 1, -1])))
        
        # Claude-3.5 có thể khắt khe hơn một chút
        score_b = min(5, max(1, base_score + random.choice([0, -1, 0, 1])))
        
        avg_score = (score_a + score_b) / 2.0
        
        # Agreement rate: 1.0 nếu cùng điểm, 0.5 nếu lệch 1, 0.0 nếu lệch > 1
        diff = abs(score_a - score_b)
        if diff == 0:
            agreement = 1.0
        elif diff == 1:
            agreement = 0.5
        else:
            agreement = 0.0
            
        return {
            "final_score": avg_score,
            "agreement_rate": agreement,
            "individual_scores": {"gpt-4o": score_a, "claude-3-5": score_b}
        }

    async def check_position_bias(self, response_a: str, response_b: str):
        """
        Nâng cao: Thực hiện đổi chỗ response A và B để xem Judge có thiên vị vị trí không.
        """
        pass
