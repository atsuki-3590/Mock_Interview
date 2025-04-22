// src/main.js または src/index.js

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'  // ← 拡張子.jsxを明示（拡張子なしでも動くことは多い）
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
