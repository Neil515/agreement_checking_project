import re
from bs4 import BeautifulSoup

def clean_text(raw_text):
    """
    接收原始條款文字（可能來自 HTML 或 PDF 轉換），清除雜訊與格式。
    包含：
      - 去除 HTML 標籤
      - 移除多餘空白與換行
      - 移除特殊符號或控制字元
    回傳乾淨、可斷句的純文字。
    """
    # 若是 HTML 格式，移除所有標籤
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator=" ")

    # 移除控制字元與特殊符號（如 Unicode 換頁、全形空格等）
    text = re.sub(r"[\u3000\r\f\x0b\x0c]+", " ", text)

    # 移除重複空白（多空格、連續換行等）
    text = re.sub(r"\s+", " ", text)

    # 移除開頭結尾空白
    return text.strip()

# 測試用
if __name__ == '__main__':
    sample_html = """
    <html><body><h1>使用條款</h1><p>您必須同意所有規定。</p><p>否則不得使用本服務。</p></body></html>
    """
    clean = clean_text(sample_html)
    print(clean)  # 預期輸出：使用條款 您必須同意所有規定。 否則不得使用本服務。
