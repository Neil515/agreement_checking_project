(function() {
  // 條款淺藍色背景色
  const clauseBlueBg = '#e3f0ff';
  
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
  let isAnalysisComplete = false;
  let selectedMode = 'fast';
  let timerInterval = null;

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

	// 將 analyzeClausesWithAPI 改為逐條送出
	async function analyzeClausesWithAPI(clauses, lang = 'auto', mode = 'fast') {
	  // 並行分析所有條文
	  const results = await Promise.all(
		clauses.map(clause =>
		  fetch('http://localhost:5000/analyze', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ text: clause, lang, mode })
		  })
		  .then(res => res.ok ? res.json() : {})
		  .then(data => data || {})
		  .catch(() => ({}))
		)
	  );
	  return results;
	}

  function showSidebarAndAnalyze() {
    console.log("🔧 建立側欄與開始分析");
    const sidebar = document.createElement("div");
    sidebar.id = "clause-sidebar";
    sidebar.innerHTML = `
      <div style="font-family: sans-serif; font-size: 14px; padding: 24px 12px 12px 12px; background: #f8f8f8; border-left: 3px solid #ccc; height: 100vh; overflow-y: auto; position: fixed; top: 0; right: 0; width: 320px; z-index: 2147483646; box-shadow: -2px 0 4px rgba(0,0,0,0.05);">
        <button id="close-sidebar" style="position: absolute; top: 8px; right: 8px; padding: 4px 8px; font-size: 12px; background-color: #eee; border: none; border-radius: 4px; cursor: pointer;">✖</button>
        <h3 style="margin-top: 24px; font-size: 16px;">條文風險分析</h3>
        <!-- 分析模式選擇 -->
        <div style="margin: 12px 0; padding: 8px; background: #fff; border-radius: 4px; border: 1px solid #ddd;">
          <label style="font-weight: bold; display: block; margin-bottom: 8px;">分析模式 / Analysis Mode:</label>
          <div style="display: flex; flex-direction: column; gap: 6px;">
            <label style="display: flex; align-items: center; cursor: pointer;">
              <input type="radio" name="analysis-mode" value="fast" checked style="margin-right: 6px;">
              <span style="font-size: 13px;">🚀 快速分析 (Fast) - 較快完成</span>
            </label>
            <label style="display: flex; align-items: center; cursor: pointer;">
              <input type="radio" name="analysis-mode" value="accurate" style="margin-right: 6px;">
              <span style="font-size: 13px;">🎯 精準分析 (Accurate) - 較慢但更準確</span>
            </label>
          </div>
        </div>
        <div id="analyze-btn-container" style="text-align:center; margin-bottom:10px;">
          <button id="analyze-btn" style="padding:8px 16px; font-size:14px; background:${clauseBlueBg}; color:#0056d2; border:none; border-radius:4px; cursor:pointer;">開始分析 <span style="margin-left:8px;">👈</span></button>
        </div>
        <div id="timer-display" style="font-size: 13px; margin: 6px 0 4px 0; color: #666;">
          ⏱️ 執行中：00:00
        </div>
        <div id="progress-info" style="margin-bottom: 10px; font-size: 13px;">📊 條文分析進度 / Progress：0 / 0</div>
        <div id="completion-notice" style="margin: 8px 0; padding: 8px; background: #e8f5e8; border-radius: 4px; border: 1px solid #4caf50; display: none;">
          ✅ 分析完成！你有 <span id="risk-count">0</span> 個須注意條款
        </div>
        <ul id="clause-risk-list" style="list-style: none; padding-left: 0; font-size: 13px;"></ul>
      </div>
    `;
    document.body.appendChild(sidebar);

    // 條款內容陣列
    const clauseNodes = document.querySelectorAll(
      "p, li, div, section, article, blockquote, span, h2, h3, h4, h5, h6"
    );
    const filteredNodes = Array.from(clauseNodes).filter(node => {
      const text = node.innerText?.trim() || "";
      if (node.hasAttribute("data-clause-id")) return false;
      return text.length > 0;
    });
    const clauseTexts = filteredNodes.map(node => node.innerText?.trim() || "");
    totalCount = filteredNodes.length;
    completedCount = 0;
    isAnalysisComplete = false;
    updateProgress();

    // 監聽模式選擇變更
    const modeInputs = sidebar.querySelectorAll('input[name="analysis-mode"]');
    modeInputs.forEach(input => {
      input.addEventListener('change', (e) => {
        selectedMode = e.target.value;
        // 切換模式時重置所有狀態
        resetAllStates();
        updateProgress();
        sidebar.querySelector('#timer-display').textContent = `⏱️ 執行中 / Running：00:00`;
        sidebar.querySelector('#completion-notice').style.display = 'none';
        renderSortedRisks();
        // 明確提示需點擊按鈕開始分析
        sidebar.querySelector('#analyze-btn').disabled = false;
        sidebar.querySelector('#analyze-btn').textContent = '開始分析';
      });
    });

    const analyzeBtn = sidebar.querySelector('#analyze-btn');
    const analyzeBtnContainer = sidebar.querySelector('#analyze-btn-container');
    const completionNotice = sidebar.querySelector('#completion-notice');
    const riskCount = sidebar.querySelector('#risk-count');
    const timerEl = sidebar.querySelector('#timer-display');

    function resetClauseHighlight() {
      document.querySelectorAll('.clause-processing').forEach(node => {
        node.classList.remove('clause-processing');
        node.style.background = '';
        node.removeAttribute('data-clause-id');
      });
    }

    function resetAllStates() {
      resetClauseHighlight();
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
      isAnalysisComplete = false;
      completedCount = 0;
      totalCount = filteredNodes.length;
      riskItems = [];
      analyzedResults = [];
      clauseStatusMap = {};
      sidebar.querySelector('#completion-notice').style.display = 'none';
      sidebar.querySelector('#risk-count').textContent = '0';
      sidebar.querySelector('#timer-display').textContent = `⏱️ 執行中 / Running：00:00`;
      renderSortedRisks();
    }

    function startAnalysis() {
      resetAllStates();
      if (totalCount === 0) {
        sidebar.querySelector('#completion-notice').style.display = 'none';
        sidebar.querySelector('#timer-display').textContent = `⏱️ 無可分析條款 / No clauses`;
        return;
      }
      let secondsElapsed = 0;
      timerEl.textContent = `⏱️ 執行中 / Running：00:00`;
      completionNotice.style.display = 'none';
      analyzeBtn.disabled = true;
      timerInterval = setInterval(() => {
        if (!isAnalysisComplete) {
          secondsElapsed++;
          const min = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
          const sec = String(secondsElapsed % 60).padStart(2, '0');
          timerEl.textContent = `⏱️ 執行中 / Running：${min}:${sec}`;
        }
      }, 1000);
      analyzeClausesWithAPI(clauseTexts, 'auto', selectedMode).then(results => {
	  console.log('clauseTexts.length:', clauseTexts.length, 'results.length:', results.length);
        riskItems = [];
        analyzedResults = [];
		results.forEach((result, idx) => {
		  const node = filteredNodes[idx];
		  if (!node) return; // 防呆，避免 undefined
		  const clauseId = idCounter++;
		  node.setAttribute("data-clause-id", clauseId);
		  node.classList.add("clause-processing");
		// 不要再加 node.style.background = clauseBlueBg;
		  clauseStatusMap[clauseId] = "⏳ 分析中 / Analyzing";
		  completedCount++;
		  updateProgress();
		  const preview = result.text ? result.text.slice(0, 15).replace(/\n+/g, ' ') : '';
		  const risk = result.risk_type === "須注意" ? "須注意" : "一般資訊";
		  analyzedResults.push({ preview, risk });
		  if (risk === "須注意") {
			riskItems.push({ id: clauseId, label: `⚠️ 須注意 / Risky：${preview}...` });
			renderSortedRisks();
		  }
		  // chrome.runtime.sendMessage({ ... }); // 可註解掉，除非你有 background script
		});
        isAnalysisComplete = true;
        updateProgress();
        if (timerInterval) {
          clearInterval(timerInterval);
          timerInterval = null;
        }
        // 僅在條款數>0且進度100%時顯示分析完成訊息
        if (totalCount > 0 && completedCount === totalCount) {
          riskCount.textContent = riskItems.length;
          completionNotice.style.display = 'block';
        } else {
          completionNotice.style.display = 'none';
        }
        analyzeBtn.disabled = false;
      });
    }

    analyzeBtn.addEventListener('click', startAnalysis);

    document.getElementById("close-sidebar").addEventListener("click", () => {
      document.getElementById("clause-sidebar")?.remove();
      resetClauseHighlight();
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
      isAnalysisComplete = false;
      completedCount = 0;
      totalCount = 0;
      riskItems = [];
      analyzedResults = [];
      clauseStatusMap = {};
      insertFabIcon();
    });
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
		// 只顯示一次「完成 / Done」
		if (!timerEl.textContent.includes("✅ 完成 / Done")) {
		  timerEl.textContent += " ✅ 完成 / Done";
		}
	  }
	} // <--- 這裡要有 function 的結尾大括號

	})(); // <--- 這才是 IIFE 的結尾 