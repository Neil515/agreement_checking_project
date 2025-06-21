import unittest
import sys
import os

# 加入 core 資料夾的路徑，讓 Python 找到 risk_analyzer.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

from risk_analyzer import analyze_clause

class TestRiskAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            "我們可能會將您的資料提供給第三方進行行銷分析。",
            "使用本服務即表示您同意所有條款內容。",
            "您可以隨時聯繫我們刪除個人資訊。",
            "服務僅適用於年滿十八歲的使用者。",
            "公司保留隨時修改條款之權利，恕不另行通知。"
        ]

    def test_analyze_clause_format(self):
        for clause in self.test_cases:
            with self.subTest(clause=clause):
                result = analyze_clause(clause, lang="zh")
                self.assertIn("clause", result)
                self.assertIn("risk_level", result)
                self.assertIn("reason", result)
                self.assertIn("type", result)
                self.assertIn("highlight", result)

                # 確保 risk_level 僅為二元分類值
                self.assertIn(result["risk_level"], ["須注意", "一般資訊"])
                self.assertIsInstance(result["highlight"], bool)

if __name__ == "__main__":
    unittest.main()
