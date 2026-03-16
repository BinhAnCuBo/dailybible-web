from flask import Flask, render_template
import mysql.connector
from datetime import date

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",      # <-- Điền mật khẩu MySQL của chị
        database="your_database_name"  # <-- Điền tên database của chị
    )

def get_today_verse():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    today = date.today().strftime('%Y-%m-%d')
    
    # Kết nối 2 bảng để lấy cả Lời Chúa và thông tin Phụng vụ
    query = """
        SELECT 
            q.content, q.reference, q.explanation,
            l.name AS feast_name, 
            l.feast_type, 
            l.liturgical_color
        FROM bible_quotes q
        LEFT JOIN liturgical_days l ON DATE(q.quote_date) = DATE(l.date)
        WHERE DATE(q.quote_date) = %s
    """
    cursor.execute(query, (today,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return result

@app.route('/')
def index():
    verse = get_today_verse()
    
    # Hiển thị Thứ và Ngày (VD: Thứ Bảy, 07/03/2026)
    days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chúa Nhật"]
    weekday = days[date.today().weekday()]
    display_date = f"{weekday}, {date.today().strftime('%d/%m/%Y')}"
    
    return render_template('index.html', verse=verse, today=display_date)

if __name__ == '__main__':
    app.run(debug=True)