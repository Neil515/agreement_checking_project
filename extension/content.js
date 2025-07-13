// content.js - 清爽 + 明確進度版（只顯示進度與須注意條文）

const clauseNodes = document.querySelectorAll("p, li, div[class*='clause'], div[class*='term'], span[class*='clause']");

let idCounter = 1;
let missedCount = 0;
let clauseStatusMap = {};
let totalCount = 0;
let completedCount = 0;

// 建立側欄 UI（進度條 + 僅顯示須注意條文）
const sidebar = document.createElement("div");
sidebar.id = "clause-sidebar";
sidebar.innerHTML = `
  <div style="font-family: sans-serif; font-size: 14px; padding: 24px 12px 12px 12px; background: #f8f8f8; border-left: 3px solid #ccc; height: 100vh; overflow-y: auto; position: fixed; top: 0; right: 0; width: 280px; z-index: 9999; box-shadow: -2px 0 4px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; font-size: 16px;">條文風險分析</h3>
    <div id="timer-display" style="font-size: 13px; margin: 6px 0 4px 0; color: #666;">
      ⏱️ 執行中：00:00
    </div>
    <div id="progress-info" style="margin-bottom: 10px; font-size: 13px;">📊 條文分析進度 / Progress：0 / 0</div>
    <ul id="clause-risk-list" style="list-style: none; padding-left: 0; font-size: 13px;"></ul>
  </div>
`;
document.body.appendChild(sidebar);
const timerEl = document.getElementById("timer-display");
const progressEl = document.getElementById("progress-info");
const riskList = document.getElementById("clause-risk-list");

// 啟動碼表計時器
let secondsElapsed = 0;
const timerInterval = setInterval(() => {
  secondsElapsed++;
  const min = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
  const sec = String(secondsElapsed % 60).padStart(2, '0');
  timerEl.textContent = `⏱️ 執行中 / Running：${min}:${sec}`;
}, 1000);

function updateProgress() {
  progressEl.textContent = `📊 條文分析進度 / Progress：${completedCount} / ${totalCount}`;
  if (completedCount === totalCount) {
    clearInterval(timerInterval);
    timerEl.textContent += " ✅ 完成 / Done";
  }
}

let riskItems = [];

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
    if (isRisky) {
      const preview = text.slice(0, 15).replace(/\n+/g, ' ');
      riskItems.push({ id: clauseId, label: `⚠️ 須注意 / Risky：${preview}...` });
      renderSortedRisks();
    }
  }, 1000 + Math.random() * 2000);

  console.log(`📄 條文 ${clauseId}: ${text.slice(0, 80)}...`);
});

function renderSortedRisks() {
  riskItems.sort((a, b) => a.id - b.id);
  riskList.innerHTML = "";
  for (const item of riskItems) {
    const li = document.createElement("li");
    li.textContent = item.label;
    riskList.appendChild(li);
  }
}

function findTextContainer(node) {
  const all = [...node.querySelectorAll("*")];
  const best = all.find(el => el.innerText && el.innerText.trim().length > 20);
  return best || node;
}

if (missedCount > 0) {
  console.warn(`⚠️ 有 ${missedCount} 個條文過短或無法標記，可能需人工檢查 / ${missedCount} clauses too short or unprocessed`);
}

console.log("content.js 已成功載入！");
