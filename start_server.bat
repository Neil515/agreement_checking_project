@echo off
cd /d C:\GitHubProjects\agreement_checking_project
echo 啟動本地伺服器中...（請勿關閉此視窗）
python -m http.server 8000
pause
