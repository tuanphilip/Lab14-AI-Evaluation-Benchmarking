import asyncio
import time
from typing import List, Dict

class BenchmarkRunner:
    def __init__(self, agent, evaluator, judge):
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge

    async def run_single_test(self, test_case: Dict) -> Dict:
        start_time = time.perf_counter()
        
        # 1. Gọi Agent
        response = await self.agent.query(test_case["question"])
        latency = time.perf_counter() - start_time
        
        # 2. Chạy Retrieval metrics (RAGAS giả lập)
        expected_ids = test_case.get("expected_retrieval_ids", [])
        retrieved_ids = response.get("retrieved_ids", [])
        
        ragas_scores = await self.evaluator.score(expected_ids, retrieved_ids)
        # Giả lập thêm faithfulness và relevancy cho đầy đủ
        ragas_scores["faithfulness"] = 0.9 if ragas_scores["hit_rate"] > 0 else 0.4
        ragas_scores["relevancy"] = 0.85 if ragas_scores["mrr"] > 0 else 0.3
        
        # 3. Chạy Multi-Judge
        judge_result = await self.judge.evaluate_multi_judge(
            test_case["question"], 
            response["answer"], 
            test_case["expected_answer"]
        )
        
        return {
            "test_case": test_case["question"],
            "agent_response": response["answer"],
            "latency": latency,
            "ragas": {"retrieval": {"hit_rate": ragas_scores["hit_rate"], "mrr": ragas_scores["mrr"]}, "faithfulness": ragas_scores["faithfulness"], "relevancy": ragas_scores["relevancy"]},
            "judge": judge_result,
            "status": "fail" if judge_result["final_score"] < 3 else "pass",
            "cost_simulated": 0.0015  # giả lập cost 0.0015$ / query
        }

    async def run_all(self, dataset: List[Dict], batch_size: int = 10) -> List[Dict]:
        """
        Chạy song song bằng asyncio.gather với giới hạn batch_size.
        """
        results = []
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i + batch_size]
            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
        return results
