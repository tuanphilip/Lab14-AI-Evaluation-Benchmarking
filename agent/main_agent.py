import asyncio
import random
from typing import List, Dict

class MainAgent:
    """
    Agent mẫu. V1 là phiên bản Base, V2 là phiên bản đã tối ưu.
    """
    def __init__(self, version: str = "V1"):
        self.version = version
        self.name = f"SupportAgent-{version}"

    async def query(self, question: str) -> Dict:
        """
        Mô phỏng quy trình RAG:
        1. Retrieval: Tìm kiếm context liên quan.
        2. Generation: Gọi LLM để sinh câu trả lời.
        """
        await asyncio.sleep(0.05) # Giả lập delay siêu tốc
        
        # Mô phỏng việc trích xuất doc ID từ câu hỏi (dựa trên format câu hỏi mock)
        # VD: "Chính sách số 5..." -> giả định cần doc_5, doc_6
        # Để đơn giản, ta random trả về ID, nhưng V2 sẽ trả về ID chuẩn xác hơn
        import re
        match = re.search(r'\d+', question)
        num = int(match.group()) if match else random.randint(1, 20)
        
        doc_1 = f"doc_{(num % 20) + 1}"
        doc_2 = f"doc_{(num % 20) + 2}"
        
        if self.version == "V1":
            # V1 có 50% cơ hội tìm sai doc
            if random.random() < 0.5:
                retrieved_ids = [f"doc_{random.randint(1, 20)}", f"doc_{random.randint(1, 20)}"]
            else:
                retrieved_ids = [doc_1, doc_2]
        else:
            # V2 đã được tuning, 90% cơ hội tìm đúng doc
            if random.random() < 0.1:
                retrieved_ids = [f"doc_{random.randint(1, 20)}", f"doc_{random.randint(1, 20)}"]
            else:
                retrieved_ids = [doc_1, doc_2]

        if self.version == "V1":
            answer = f"Dựa trên tài liệu hệ thống, trả lời cho '{question}': Đây là câu trả lời mock."
        else:
            answer = f"Dựa trên tài liệu hệ thống, trả lời cho '{question}': Đây là câu trả lời mock. V2 đã cải thiện câu trả lời này bằng cách cung cấp thêm thông tin chi tiết và cụ thể hơn so với V1, bao gồm cả các bằng chứng từ tài liệu trích dẫn."

        return {
            "answer": answer,
            "retrieved_ids": retrieved_ids,
            "contexts": [
                "Đoạn văn bản trích dẫn 1",
                "Đoạn văn bản trích dẫn 2"
            ],
            "metadata": {
                "model": "gpt-4o-mini",
                "tokens_used": 150
            }
        }

if __name__ == "__main__":
    agent = MainAgent()
    async def test():
        resp = await agent.query("Làm thế nào để kết hợp A và B trong tình huống X (Test 3)?")
        print(resp)
    asyncio.run(test())
