import React, { useState } from 'react';
import liturgicalData from './data/bible_data.json';
import quotesData from './data/daily_quotes.json';
import './App.css';

function App() {
  const [showQuote, setShowQuote] = useState(false);
  
  // Lấy ngày hiện tại định dạng YYYY-MM-DD để khớp với file JSON
  const today = new Date().toLocaleDateString('en-CA'); 

  // Tìm dữ liệu tương ứng với ngày hôm nay
  const lit = liturgicalData.find(item => item.date === today);
  const quo = quotesData.find(item => item.date === today);

  // Định dạng ngày hiển thị kiểu tiếng Việt
  const todayVN = new Date().toLocaleDateString('vi-VN', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });

  return (
    <div className="app-container">
      <div className="glass-card">
        <p className="today-text">{todayVN}</p>
        
        {lit ? (
          <div className="lit-info">
            <h1 className="feast-name">{lit.name}</h1>
            <div className="badges">
              <span className="badge-type">{lit.feast_type}</span>
              <span className={`badge-color ${lit.liturgical_color}`}>
                Áo lễ: {lit.liturgical_color}
              </span>
            </div>
          </div>
        ) : (
          <p className="loading">Đang tải thông tin Phụng vụ...</p>
        )}

        <div className="quote-section">
          {!showQuote ? (
            <button className="btn-main" onClick={() => setShowQuote(true)}>
              Nhận Lời Chúa & Tâm Tình
            </button>
          ) : (
            <div className="quote-detail fade-in">
              <p className="content">"{quo?.content || "Hãy luôn tin tưởng vào sự dẫn dắt của Chúa."}"</p>
              <p className="verse">({quo?.verse || "Lời Chúa"})</p>
              {quo?.explanation && (
                <div className="explanation">
                  <p>{quo.explanation}</p>
                </div>
              )}
              <button className="btn-sub" onClick={() => setShowQuote(false)}>Đóng</button>
            </div>
          )}
        </div>
        
        <footer className="footer">
          <p>© 2026 Daily Bible - {lit?.name || "Lời Chúa Mỗi Ngày"}</p>
        </footer>
      </div>
    </div>
  );
}

export default App;