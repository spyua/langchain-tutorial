#!/usr/bin/env bash
set -euo pipefail

# 讀取 stdin 的 JSON 輸入
payload="$(cat)"

# 取出欄位（沒有就給空字串，避免錯）
event="$(printf '%s' "$payload" | jq -r '.hook_event_name // ""')"
msg="$(printf '%s' "$payload" | jq -r '.message // ""')"
sid="$(printf '%s' "$payload" | jq -r '.session_id // ""')"

# 1) 一定要叫得出聲（WSL→Windows 嗶一聲）
powershell.exe -c "[System.Console]::Beep(1000,200)" >/dev/null 2>&1 || true

# 2) Windows 桌面通知（BurntToast）
powershell.exe -c "Import-Module BurntToast; New-BurntToastNotification -Text 'Claude $event', '$msg', 'Session: $sid'" >/dev/null 2>&1 || true

# 3) （可選）WSL 專用的 Windows toast 替代方案
# wsl-notify-send.exe \"Claude $event\" \"$msg\" >/dev/null 2>&1 || true

# 0 代表成功；對 Notification 事件來說，stdout 不會顯示，只在 --debug 看得到
exit 0
