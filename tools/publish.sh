#!/bin/bash
# 새로 조립된 회차를 내보내고 GitHub Pages에 올린다. 사용: bash tools/publish.sh
cd "$(dirname "$0")/.."
python3 tools/export.py
git add -A
git diff --cached --quiet && { echo "바뀐 것 없음"; exit 0; }
git commit -q -m "update: 웹툰 회차 갱신 $(date +%F_%H:%M)"
git push -q origin main && echo "올림"
