# core/split_text.py

import re

def split_sentences(text, lang):
    text = text.strip()

    if lang == "zh":
        # 中文依據 。！？ 分句
        sentences = re.split(r'(?<=[。！？])\s*', text)
    elif lang == "en":
        # 改進英文分句：避免切在網址、括號中、小數點、數字後
        # 改用更安全的判斷方式（避免使用變長 lookbehind）
        sentence_endings = re.compile(r'(\b(?:Mr|Mrs|Dr|Inc|Ltd|Jr|Sr|vs|St|Ave|CA|NY|TX|U\.S|e\.g|i\.e)\.)|(?<=\.)\s+(?=[A-Z])|(?<=[!?])\s+|\n+')
        parts = sentence_endings.split(text)

        # 合併句段
        sentences = []
        buffer = ""
        for part in parts:
            if not part:
                continue
            part = part.strip()
            if buffer:
                buffer += " " + part
            else:
                buffer = part
            if re.match(r'.*[.!?]$', part):
                sentences.append(buffer.strip())
                buffer = ""
        if buffer:
            sentences.append(buffer.strip())

        # 合併太短句段（如地址）
        merged = []
        buffer = ""
        for s in sentences:
            if len(s) < 20:
                buffer += " " + s
            else:
                if buffer:
                    merged.append((buffer + " " + s).strip())
                    buffer = ""
                else:
                    merged.append(s)
        if buffer:
            merged.append(buffer.strip())
        sentences = merged
    else:
        return [text]

    return [s.strip() for s in sentences if len(s.strip()) > 2]
