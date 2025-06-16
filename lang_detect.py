from langdetect import detect

def detect_language(text):
    """
    偵測輸入文字是中文（zh）或英文（en）為主。
    若偵測失敗，會補強以中文字元比例進行推測。
    """
    try:
        lang = detect(text)
        if lang.startswith('zh'):
            return 'zh'
        elif lang.startswith('en'):
            return 'en'
    except:
        pass

    # 簡易補強：若中文字元比例超過 20%，視為中文
    zh_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    if zh_count / max(len(text), 1) > 0.2:
        return 'zh'

    return 'unknown'

# 測試用
if __name__ == '__main__':
    print(detect_language("本服務僅限註冊會員使用。"))  # 預期：zh
    print(detect_language("You must accept all terms."))  # 預期：en
    print(detect_language("12345"))  # 預期：unknown
