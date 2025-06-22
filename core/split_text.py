# core/split_text.py

import re

def split_sentences(text, lang):
    text = text.strip()

    if lang == "zh":
        # 改為「段落」為單位切割（兩個以上換行）
        paragraphs = re.split(r'\n{2,}', text)
        return [p.strip() for p in paragraphs if len(p.strip()) > 10]

    elif lang == "en":
        # 英文部分保留句號斷句但做緩衝合併
        sentence_endings = re.compile(r'(\b(?:Mr|Mrs|Dr|Inc|Ltd|Jr|Sr|vs|St|Ave|CA|NY|TX|U\.S|e\.g|i\.e)\.)|(?<=\.)\s+(?=[A-Z])|(?<=[!?])\s+|\n+')
        parts = sentence_endings.split(text)

        # 合併英文句段
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

        # 合併太短句段
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
        return merged

    else:
        return [text]
