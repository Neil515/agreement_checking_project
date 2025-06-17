# core/split_text.py

import re

def split_sentences(text, lang):
    # 移除前後空白與多行縮排
    text = text.strip()
    
    if lang == "zh":
        # 中文依據 。！？ 分句
        sentences = re.split(r'(?<=[。！？])\s*', text)
    elif lang == "en":
        # 英文依據 .!? 和換行分句
        sentences = re.split(r'(?<=[.!?])\s*|\n+', text)
    else:
        # 若語言不明，就整段回傳
        return [text]
    
    # 清理：去除空句與過短句（1~2 字）
    return [s.strip() for s in sentences if len(s.strip()) > 2]
