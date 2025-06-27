import json
import shutil

# 預設檔案路徑
SOURCE_FILE = "data/risk_examples_mapped.json"
TARGET_FILE = "data/risk_examples.json"
BACKUP_FILE = "data/risk_examples_backup.json"

# 備份原始檔
shutil.copyfile(TARGET_FILE, BACKUP_FILE)

# 讀取標準化後資料
with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    mapped_data = json.load(f)

# 覆寫原始檔案
with open(TARGET_FILE, "w", encoding="utf-8") as f:
    json.dump(mapped_data, f, ensure_ascii=False, indent=2)

print(f"✅ 已使用 {SOURCE_FILE} 更新 {TARGET_FILE}，原始檔已備份為 {BACKUP_FILE}")
