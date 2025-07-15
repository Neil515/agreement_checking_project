let idCounter = 1;
let missedCount = 0;
let clauseStatusMap = {};
let totalCount = 0;
let completedCount = 0;

let riskItems = [];
let analyzedResults = [];

console.log("✅ content.js 已載入，等待使用者啟動分析。");

try {
  console.log("🚀 嘗試插入啟動分析按鈕");
  const startButton = document.createElement("button");
  startButton.id = "ai-risk-start-button";
  startButton.textContent = "🔍 啟動條文風險分析";
  startButton.style.cssText = `
    position: fixed;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    z-index: 2147483647;
    padding: 10px 16px;
    background-color: #0056d2;
    color: white;
    border: none;
    border-radius: 6px 0 0 6px;
    font-size: 14px;
    cursor: pointer;
    box-shadow: -2px 2px 6px rgba(0,0,0,0.2);
  `;
  document.body.appendChild(startButton);

  console.log("✅ 啟動按鈕已插入");

  startButton.addEventListener("click", () => {
    console.log("🟢 使用者按下啟動分析按鈕");
    startButton.remove();
    showSidebarAndAnalyze();
  });
} catch (err) {
  console.error("❌ 插入啟動按鈕時發生錯誤", err);
}

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