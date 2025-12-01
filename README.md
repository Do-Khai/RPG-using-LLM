# RPG Proxy Service - LLM-Powered Battle & Chat Engine

Dự án này là một service proxy sử dụng FastAPI, đóng vai trò trung gian giữa backend của một game RPG và các mô hình ngôn ngữ lớn (LLM) của Ollama. Service cung cấp các API để tạo ra các kịch bản chiến đấu theo lượt (turn-based) và các đoạn hội thoại một cách tự động, dựa trên các chỉ số và ngữ cảnh được cung cấp.

## Công nghệ sử dụng

- **Framework**: FastAPI
- **HTTP Client**: httpx
- **Validation**: Pydantic
- **Retry Logic**: Tenacity
- **Environment Management**: python-dotenv
- **LLM Provider**: Ollama

## Cài đặt

1.  Clone repository về máy của bạn:
    ```bash
    git clone https://github.com/Do-Khai/RPG-using-LLM.git
    cd dog-defense
    ```

2.  Tạo và kích hoạt môi trường ảo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

## Chạy ứng dụng

Sử dụng `uvicorn` để khởi động server:

```bash
uvicorn app:app --reload
```

Sau khi server khởi động, bạn có thể truy cập các API tại `http://127.0.0.1:8000`.

Để xem tài liệu API tự động (Swagger UI), truy cập: `http://127.0.0.1:8000/docs`.

## Sử dụng API

### 1. Mô phỏng trận đấu

- **Endpoint**: `POST /api/v1/player-battle`
- **Mô tả**: Nhận chỉ số của hai người chơi và trả về một kịch bản trận đấu chi tiết dưới dạng JSON.
- **Request Body**:

  ```json
  {
    "battleType": "CASUAL",
    "playerDisplayName": "Kiếm Khách Vô Danh",
    "playerStats": {
      "hp": 120,
      "atk": 90,
      "def": 30,
      "critPercentage": 5.05,
      "critDamage": 240,
      "dodge": 10,
      "speed": 24
    },
    "enemyDisplayName": "Ma Tôn Bất Bại",
    "enemyStats": {
      "hp": 100,
      "atk": 95,
      "def": 25,
      "critPercentage": 8.0,
      "critDamage": 260,
      "dodge": 5,
      "speed": 30
    }
  }
  ```

### 2. Kiểm tra trạng thái

- **Endpoint**: `GET /health`
- **Mô tả**: Một endpoint đơn giản để kiểm tra xem service có đang hoạt động hay không. Trả về `{"ok": true}` nếu thành công.