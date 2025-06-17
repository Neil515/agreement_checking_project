import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.split_text import split_sentences

test_cases = [
    {
        "lang": "zh",
        "text": """
本平台僅提供資訊服務。您不得將本服務用於非法用途！若您不同意條款，請勿繼續使用？
請立即通知我們。
        """,
        "expected": [
            "本平台僅提供資訊服務。",
            "您不得將本服務用於非法用途！",
            "若您不同意條款，請勿繼續使用？",
            "請立即通知我們。"
        ]
    },
    {
        "lang": "en",
        "text": """
You agree to our terms of service.
Do not misuse the platform!
If you disagree, stop using it?
        """,
        "expected": [
            "You agree to our terms of service.",
            "Do not misuse the platform!",
            "If you disagree, stop using it?"
        ]
    },
    {
        "lang": "zh",
        "text": """
同意即表示您已閱讀、理解並接受本協議。
未經授權，不得轉載、改作、散布。
        """,
        "expected": [
            "同意即表示您已閱讀、理解並接受本協議。",
            "未經授權，不得轉載、改作、散布。"
        ]
    },
    {
        "lang": "en",
        "text": """
We collect your data. Please read carefully!
This is your responsibility.
        """,
        "expected": [
            "We collect your data.",
            "Please read carefully!",
            "This is your responsibility."
        ]
    }
]

def run_tests():
    for idx, case in enumerate(test_cases):
        result = split_sentences(case["text"], case["lang"])
        expected = case["expected"]
        if result == expected:
            print(f"✅ Test {idx + 1} passed.")
        else:
            print(f"❌ Test {idx + 1} failed.")
            print("Expected:")
            print(expected)
            print("Got:")
            print(result)
            print("")

if __name__ == "__main__":
    run_tests()
