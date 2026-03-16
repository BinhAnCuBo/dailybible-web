import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine
import urllib.parse
import time

# 1. Kết nối Database
DB_USER, DB_PASS, DB_HOST, DB_NAME = "root", "Binh@n32160260", "localhost", "catholic_web"
safe_password = urllib.parse.quote_plus(DB_PASS)
engine = create_engine(f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}/{DB_NAME}?charset=utf8mb4")

def scrape_catholic_calendar_2026():
    # URL tổng quát bạn đã dùng thành công
    url = "https://loichuahomnay.vn/lich-cong-giao"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"--- Đang bắt đầu cào dữ liệu năm 2026 ---")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"❌ Lỗi truy cập: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        final_data = []
        seen_dates = set()

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2: 
                continue
            
            # Lấy văn bản từ các ô dựa trên cấu trúc vng, vtl, vbd
            date_text = cols[0].get_text(" ", strip=True)
            info_text = cols[1].get_text(" ", strip=True)
            row_class = row.get('class', []) # Lấy class của hàng (trletrong, trlenho)

            # Trích xuất ngày/tháng (ví dụ: 05/04)
            date_match = re.search(r'(\d{1,2}/\d{1,2})', date_text)
            if date_match:
                day_month = date_match.group(1)
                d, m = day_month.split('/')
                
                # Chỉ lấy dữ liệu thuộc năm 2026
                full_date_str = f"2026-{m.zfill(2)}-{d.zfill(2)}"
                
                if full_date_str not in seen_dates:
                    # 1. XÁC ĐỊNH MÀU SẮC (Bắt ký hiệu trong ngoặc hoặc chữ)
                    color = "Xanh"
                    info_low = info_text.lower()
                    if "(tm)" in info_low or "tím" in info_low: color = "Tím"
                    elif "(tr)" in info_low or "trắng" in info_low: color = "Trắng"
                    elif "(đ)" in info_low or "đỏ" in info_low: color = "Đỏ"
                    elif "(x)" in info_low or "xanh" in info_low: color = "Xanh"

                    # 2. PHÂN LOẠI CẤP BẬC LỄ (Thứ tự ưu tiên chuẩn Phụng vụ)
                    check_text = (date_text + " " + info_text).lower()
                    
                    # Ưu tiên 1: Lễ Trọng (bao gồm cả Chúa Nhật Phục Sinh, Giáng Sinh)
                    if "trletrong" in row_class or "lễ trọng" in check_text:
                        feast_type = "Lễ trọng"
                    
                    # Ưu tiên 2: Tất cả các ngày Chúa Nhật (Mặc định là Lễ Trọng)
                    elif "chúa nhật" in check_text:
                        feast_type = "Lễ trọng"
                    
                    # Ưu tiên 3: Lễ Kính
                    elif "lễ kính" in check_text:
                        feast_type = "Lễ kính"
                    
                    # Ưu tiên 4: Lễ Nhớ (Dựa vào class màu vàng hoặc chữ)
                    elif "trlenho" in row_class or "lễ nhớ" in check_text:
                        feast_type = "Lễ nhớ"
                    
                    # Ưu tiên 5: Ngày thường
                    else:
                        feast_type = "Ngày thường"

                    # 3. LÀM SẠCH TÊN LỄ
                    # Loại bỏ phần ngày tháng khỏi tên (ví dụ "05/04 CHÚA NHẬT..." -> "CHÚA NHẬT...")
                    clean_name = date_text.replace(day_month, "").strip()
                    if not clean_name: # Nếu cột 1 chỉ có ngày, lấy tên từ đầu cột 2
                        clean_name = info_text.split('.')[0]

                    final_data.append({
                        "date": full_date_str,
                        "year": 2026,
                        "name": clean_name,
                        "feast_type": feast_type,
                        "liturgical_color": color
                    })
                    seen_dates.add(full_date_str)

        # ... (giữ nguyên phần code phía trên của bạn)

        if final_data:
            df = pd.DataFrame(final_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date')
            
            # Lưu vào Database (giữ nguyên nếu bạn muốn dùng cho việc khác)
            df.to_sql('liturgical_days', con=engine, if_exists='replace', index=False)
            
            # --- PHẦN THÊM MỚI: XUẤT JSON CHO WEB ---
            # Chuyển format date về string để JSON có thể đọc được
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            # Xuất ra file
            df.to_json('bible_data.json', orient='records', force_ascii=False, indent=4)
            
            print(f"✅ THÀNH CÔNG: Đã lưu MySQL và xuất file bible_data.json.")

    except Exception as e:
        print(f"❌ Lỗi phát sinh: {e}")

if __name__ == "__main__":
    scrape_catholic_calendar_2026()