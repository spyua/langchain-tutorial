# 專案概述

## 專案目的
這是一個全面的 LangChain 教育網站，使用混合架構：
- **VitePress**: 靜態文檔網站，部署到 GitHub Pages
- **Streamlit**: 互動示例，提供實作體驗

## 技術堆疊
- **前端文檔**: VitePress (Node.js/Vite)
- **互動示例**: Streamlit (Python)
- **部署**: GitHub Pages (VitePress), 本地運行 (Streamlit)
- **內容語言**: 繁體中文

## 專案結構
```
/
├── docs/                         # VitePress 文檔網站
│   ├── .vitepress/              # VitePress 配置
│   ├── tutorials/               # 教學文檔
│   ├── examples/                # 實例文檔  
│   └── demos/                   # 示例文檔
├── streamlit-demos/             # Streamlit 應用
└── 其他配置文件
```

## 主要特色
- 混合架構：靜態文檔 + 互動示例
- 全繁體中文內容
- 實作導向的教學設計
- GitHub Pages 自動部署