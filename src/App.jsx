import React, { useState } from 'react';
import liturgicalData from './data/bible_data.json';
import quotesData from './data/daily_quotes.json';
import './App.css';

function App() {
  // State điều khiển việc hiển thị Lời Chúa (Mặc định là FALSE = không hiện)
  const [showQuote, setShowQuote] = useState(false);
  
  // 1. TRUY XUẤT DỮ LIỆU: Tìm thông tin theo ngày hiện tại
  const today = new Date().toLocaleDateString('en-CA'); 
  const lit = liturgicalData.find(item => item.date === today);
  const quo = quotesData.find(item => item.date === today);

  // 2. ĐỊNH DẠNG NGÀY THÁNG: Hiển thị tiếng Việt
  const d = new Date();
  const days = ['Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];
  const dayName = days[d.getDay()];
  const dateStr = d.toLocaleDateString('en-GB'); 
  const todayFormatted = `${dayName}, ngày ${dateStr}`;

  return (
    <div className="app-container">
      {/* Bố cục mới: Không dùng mobile-wrapper bọc ngoài nữa. 
         Glass Card sẽ dãn nở tự do theo chiều dọc của ĐT.
      */}
      <div className="glass-card">
        
        {/* === PHẦN 1: THÔNG TIN PHỤNG VỤ (LUÔN HIỂN THỊ) === */}
        <div className="welcome-screen">
          {/* Ô 1: Pallet Ngày tháng */}
          <div className="info-box date-box">
            <p className="classic-date">{todayFormatted.toUpperCase()}</p>
          </div>
          
          {/* Ô 2: Pallet Tên Lễ (Tự dãn cao theo chữ, không dính dòng) */}
          <div className="info-box feast-box">
            {lit ? (
              <h1 className="feast-name">{lit.name}</h1>
            ) : (
              <p className="loading">Đang tải dữ liệu...</p>
            )}
          </div>

          {/* THANH NGANG TRANG TRÍ: Tự động bám sát dưới Tên Lễ */}
          <div className="ornament-wrapper">
            <div className="ornament-line"></div>
            <span className="cross-icon">†</span>
            <div className="ornament-line"></div>
          </div>

          {/* Ô 3: Pallet Thông tin phụ (Loại lễ | Màu áo) */}
          <div className="info-box sub-info-box">
            <div className="sub-info-row">
              <span>{lit?.feast_type || "Lễ Thường"}</span>
              <span className="separator">|</span>
              <span>ÁO LỄ: {lit?.liturgical_color || "Xanh"}</span>
            </div>
          </div>
        </div>

        {/* === PHẦN 2: CHI TIẾT LỜI CHÚA (CHỈ HIỆN KHI ẤN NÚT) === */}
        {/* Nhờ dùng Flexbox mẹ, khi cái hộp này hiện ra, nó sẽ 
           tự động dùng lực "đẩy" nút bấm xuống dưới cùng 
        */}
        {showQuote && (
          <div className="quote-section-wrapper fade-in-gentle">
            <div className="quote-detail-box">
              {/* Câu Lời Chúa */}
              <p className="quote-content">"{quo?.content}"</p>
              {/* Nguồn đoạn Kinh Thánh */}
              <p className="quote-verse">({quo?.verse})</p>
              
              {/* PHẦN GIẢI THÍCH: Chỉ hiện ra nếu có dữ liệu */}
              {quo?.explanation && (
                <div className="explanation-section">
                  <div className="small-divider"></div>
                  <p className="explanation-text">{quo.explanation}</p>
                </div>
              )}
              
              {/* Link để đóng lại nếu muốn */}
              <span className="btn-close-link" onClick={() => setShowQuote(false)}>
                ❖ Gấp lại ❖
              </span>
            </div>
          </div>
        )}

        {/* === PHẦN 3: VÙNG NÚT BẤM (CỐ ĐỊNH Ở ĐÁY) === */}
        {/* Khi hiện Lời Chúa, nút bấm này sẽ mờ đi để nhường 
           chỗ cho phần Giải thích.
        */}
        <div className={`button-area ${showQuote ? 'button-area-fade-out' : ''}`}>
          {!showQuote ? (
            <button className="classic-btn" onClick={() => setShowQuote(true)}>
              Nhận lời Chúa hôm nay
            </button>
          ) : (
            /* Khi đang hiện Lời Chúa, ta hiện một nút bấm mờ để dự phòng */
            <button className="classic-btn btn-faded">
              Mời bạn suy niệm...
            </button>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;