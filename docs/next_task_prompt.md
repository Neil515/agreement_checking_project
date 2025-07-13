## 🔧 明日(7/15)首要工作：Chrome Extension 正式版第一步（模組化 sidebar 架構）

### 🔎 問題背景：

目前 content.js 屬於 MVP 快速整合版本，將 sidebar 的 HTML、邏輯與樣式全部硬寫在 content script 中（透過 innerHTML 建立側欄畫面），雖然運作正常，但缺乏正式 Chrome Extension 架構的可維護性與擴充性。

### 🚀 明日目標：開始將 Chrome Extension 架構模組化，邁向正式版本

---

### ✅ 你要完成的任務內容：

#### 1. 拆出獨立的 `sidebar.html`

* 將目前 content.js 中的 HTML 區塊抽出成一個實體檔案 `sidebar.html`
* 用來註冊在 manifest.json 的 `sidebar_action`（類似 popup，但可固定在畫面右側）

#### 2. 新增 `sidebar.js`

* 原本 sidebar 的更新邏輯（顯示進度、顯示風險條文）要轉移至 `sidebar.js`
* 預留與 content.js 溝通用的 message listener（未來可擴充）

#### 3. 抽離樣式至 `style.css`

* 將 inline style 的 CSS 規則全部集中管理，提升外觀一致性與維護方便性
* 與 `sidebar.html` 連結

#### 4. 修改 `manifest.json`

* 加入 `sidebar_action` 欄位，指定 `sidebar.html` 作為側欄頁面
* 並保留 content script 欄位供 content.js 操作網頁條文

---

### 📌 你將得到什麼結果？

* 擁有更正式的 Extension 架構
* 側欄視圖不再由 JS 動態產生，而是獨立的 HTML + CSS + JS 檔案
* 後續更容易連接背景任務、儲存分析結果、雙向溝通

---

### 💡 延伸注意事項（供日後實作）

* 待與 content.js 完整溝通，可使用 `chrome.runtime.sendMessage()` 或 `chrome.storage`
* 側欄樣式也可日後考慮使用 tailwind 風格或 dark mode

---

是否要由我先幫你草擬 `sidebar.html` / `sidebar.js` / `style.css` 的最小可用版本？
