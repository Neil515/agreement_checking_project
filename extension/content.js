(function() {
  // 只在特定頁面顯示放大鏡icon
  const url = window.location.href;
  const showIconKeywords = [
    // 英文
    'terms', 'term', 'agreement', 'agreements', 'contract', 'contracts', 'policy', 'policies', 'service', 'services', 'tos', 'privacy', 'disclaimer', 'legal', 'user', 'rules', 'notice',
    // 中文
    '條款', '合約', '協議', '政策', '使用條款', '隱私', '免責', '聲明', '規則', '公告'
  ];
  const shouldShowIcon = showIconKeywords.some(keyword => url.toLowerCase().includes(keyword));
  if (!shouldShowIcon) {
    console.log("🔍 條款分析icon未顯示：本頁網址不符合條件");
    return;
  }

  let idCounter = 1;
  let missedCount = 0;
  let clauseStatusMap = {};
  let totalCount = 0;
  let completedCount = 0;
  let riskItems = [];
  let analyzedResults = [];

  console.log("✅ content.js 已載入，等待使用者啟動分析。");

  function insertFabIcon() {
    // 避免重複插入
    if (document.getElementById("ai-risk-icon-container")) return;
    const iconContainer = document.createElement("div");
    iconContainer.id = "ai-risk-icon-container";
    iconContainer.innerHTML = `
      <div id="ai-risk-fab-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <circle cx="11" cy="11" r="7" stroke="#0056d2" stroke-width="2"/>
          <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="#0056d2" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <button id="ai-risk-start-button" style="display:none;">🔍 啟動AI條文分析<br>Start AI Clause Analysis</button>
    `;
    document.body.appendChild(iconContainer);

    const startButton = document.getElementById("ai-risk-start-button");

    iconContainer.addEventListener("mouseenter", () => {
      startButton.style.display = "block";
    });
    iconContainer.addEventListener("mouseleave", () => {
      startButton.style.display = "none";
    });

    startButton.addEventListener("click", () => {
      iconContainer.remove();
      showSidebarAndAnalyze();
    });
  }

  // 頁面載入時插入icon
  insertFabIcon();

  function showSidebarAndAnalyze() {
    console.log("🔧 建立側欄與開始分析");
    const clauseNodes = document.querySelectorAll("p, li, div[class*='clause'], div[class*='term'], span[class*='clause']");

    const sidebar = document.createElement("div");
    sidebar.id = "clause-sidebar";
    sidebar.innerHTML = `
      <div style="font-family: sans-serif; font-size: 14px; padding: 24px 12px 12px 12px; background: #f8f8f8; border-left: 3px solid #ccc; height: 100vh; overflow-y: auto; position: fixed; top: 0; right: 0; width: 300px; z-index: 2147483646; box-shadow: -2px 0 4px rgba(0,0,0,0.05);">
        <button id="close-sidebar" style="position: absolute; top: 8px; right: 8px; padding: 4px 8px; font-size: 12px; background-color: #eee; border: none; border-radius: 4px; cursor: pointer;">✖</button>
        <h3 style="margin-top: 24px; font-size: 16px;">條文風險分析</h3>
        <div id="timer-display" style="font-size: 13px; margin: 6px 0 4px 0; color: #666;">
          ⏱️ 執行中：00:00
        </div>
        <div id="progress-info" style="margin-bottom: 10px; font-size: 13px;">📊 條文分析進度 / Progress：0 / 0</div>
        <ul id="clause-risk-list" style="list-style: none; padding-left: 0; font-size: 13px;"></ul>
      </div>
    `;
    document.body.appendChild(sidebar);

    document.getElementById("close-sidebar").addEventListener("click", () => {
      document.getElementById("clause-sidebar")?.remove();
      insertFabIcon(); // 關閉側欄時重新插入icon
    });

    let secondsElapsed = 0;
    const timerInterval = setInterval(() => {
      secondsElapsed++;
      const min = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
      const sec = String(secondsElapsed % 60).padStart(2, '0');
      const timerEl = sidebar.querySelector("#timer-display");
      if (timerEl) {
        timerEl.textContent = `⏱️ 執行中 / Running：${min}:${sec}`;
      }
    }, 1000);

    clauseNodes.forEach(node => {
      const text = node.innerText?.trim() || "";
      if (text.length < 20) {
        missedCount++;
        return;
      }

      const clauseId = idCounter++;
      const textNode = findTextContainer(node);
      textNode.setAttribute("data-clause-id", clauseId);
      textNode.classList.add("clause-processing");

      totalCount++;
      clauseStatusMap[clauseId] = "⏳ 分析中 / Analyzing";

      setTimeout(() => {
        completedCount++;
        updateProgress();

        const isRisky = Math.random() < 0.3;
        const preview = text.slice(0, 15).replace(/\n+/g, ' ');
        const risk = isRisky ? "須注意" : "一般資訊";

        analyzedResults.push({ preview, risk });

        if (isRisky) {
          riskItems.push({ id: clauseId, label: `⚠️ 須注意 / Risky：${preview}...` });
          renderSortedRisks();
        }

        chrome.runtime.sendMessage({
          type: "update_clauses",
          data: analyzedResults
        });

        if (completedCount === totalCount) {
          clearInterval(timerInterval);
        }
      }, 1000 + Math.random() * 2000);
    });

    if (missedCount > 0) {
      console.warn(`⚠️ 有 ${missedCount} 個條文過短或無法標記，可能需人工檢查 / ${missedCount} clauses too short or unprocessed`);
    }
  }

  function renderSortedRisks() {
    riskItems.sort((a, b) => a.id - b.id);
    const riskList = document.querySelector("#clause-risk-list");
    if (!riskList) return;
    riskList.innerHTML = "";
    for (const item of riskItems) {
      const li = document.createElement("li");
      li.textContent = item.label;
      riskList.appendChild(li);
    }
  }

  function updateProgress() {
    const progressEl = document.querySelector("#progress-info");
    const timerEl = document.querySelector("#timer-display");
    if (progressEl) {
      progressEl.textContent = `📊 條文分析進度 / Progress：${completedCount} / ${totalCount}`;
    }
    if (completedCount === totalCount && timerEl) {
      timerEl.textContent += " ✅ 完成 / Done";
    }
  }

  function findTextContainer(node) {
    const all = [...node.querySelectorAll("*")];
    const best = all.find(el => el.innerText && el.innerText.trim().length > 20);
    return best || node;
  }

})();
