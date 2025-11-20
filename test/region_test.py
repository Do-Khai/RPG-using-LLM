import httpx
import json
import time
import logging

# Cấu hình logging
logging.basicConfig(filename="test/test.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# URL của backend service
BACKEND_URL = "http://localhost:8001/api/v1/chat"

# Payload chỉ chứa code
payload_codes = {
    "user_id": "test_user",
    "message": "/start",
    "all_region_data": ["VALORIA", "CELESTRA"],
    "current_stats": {"level": 1, "hp": 100, "atk": 10},
    "next_stats": {"level": 2, "hp": 120, "atk": 15},
    "user_state": {"faction": "LIGHT", "gender": "male"},
    "recent_messages": [],
}

# Payload chứa toàn bộ dữ liệu chi tiết
payload_full = {
    "user_id": "test_user",
    "message": "/start",
    "all_region_data": [
        {
		"id": "09026e2a-993e-4ca3-986b-1384490798d5",
		"code": "VALORIA",
		"name": "Thành Valoria",
		"description": "Thành phố thánh khởi đầu của hiệp sĩ Ánh Sáng. Valoria phát hiện dấu hiệu Phong Ấn Ánh Sáng bị suy yếu. Các hiệp sĩ điều tra nguyên nhân và phát hiện phe Dark đang tìm cách đánh cắp Tinh Thạch Khởi Nguyên. Người chơi bắt đầu hành trình bằng việc điều tra các đợt quái xâm nhập, cứu dân khỏi bóng ma lạc lối và khám phá thư viện cổ, biết về tiên tri Ma Thần Eclipse sẽ trở lại. Mục tiêu là bảo vệ Tinh Thạch Khởi Nguyên khỏi tay Dark.\nNPC:\n- Kaelen: Hiệp sĩ trưởng Valoria, giao nhiệm vụ chính và hướng dẫn ban đầu.\n- Liora: Linh mục trưởng Valoria, cung cấp thông tin tiên tri về ánh sáng và bóng tối.\n- Darius: Huấn luyện kỹ năng chiến đấu cơ bản. Có thể đưa nhiệm vụ phụ bảo vệ dân làng.\n- Elowen: Người tìm kiếm thông tin về quái vật lạc lối. Hướng dẫn cách sử dụng thẻ nhiệm vụ.\n- Fenric: Cung cấp nhiệm vụ phụ thu thập vật phẩm trong thành.",
		"levelRequired": 1,
		"faction": "LIGHT",
		"connectedRegions": [
			"CELESTRA"
		],
		"isStartingRegion": "true",
		"createdAt": "2025-11-17T21:29:43.002Z",
		"updatedAt": "2025-11-17T21:29:43.002Z"
	},
	{
		"id": "8aa0706f-6667-4400-9ddd-a34d8571a2d0",
		"code": "CELESTRA",
		"name": "Thung lũng Celestra",
		"description": "Nơi các linh mục được đào tạo, bao quanh bởi rừng linh hồn. Tại Thung lũng Celestra, rừng linh hồn nổi loạn, các linh mục nghi ngờ ai đó đang gọi hồn trái phép để phá vỡ giao ước với Ánh Sáng. Người chơi vào khu linh rừng sâu, giải cứu linh mục bị mất kiểm soát và tìm kẻ chủ mưu điều khiển vong hồn – một tướng Dark, khôi phục giao ước giữa Celestra và rừng linh hồn.\nNPC:\n- Amariel: Linh mục trưởng Celestra, dẫn người chơi vào rừng linh hồn. Giải thích về giao ước ánh sáng-rừng.\n- Serenya: Hướng dẫn sử dụng phép ánh sáng. Giao nhiệm vụ phụ tìm linh hồn bị lạc.\n- Tavric: Người canh rừng, cung cấp nhiệm vụ tuần tra.\n- Vaelith: Người thu thập thông tin về hoạt động tướng Dark.\n- Myrren: Hướng dẫn chế tạo bùa trấn yểm rừng.",
		"levelRequired": 1,
		"faction": "LIGHT",
		"connectedRegions": [
			"VALORIA",
			"SOLARIS"
		],
		"isStartingRegion": "false",
		"createdAt": "2025-11-17T21:29:43.002Z",
		"updatedAt": "2025-11-17T21:29:43.002Z"
	},
    ],
    "current_stats": {"level": 1, "hp": 100, "atk": 10},
    "next_stats": {"level": 2, "hp": 120, "atk": 15},
    "user_state": {"faction": "LIGHT", "gender": "male"},
    "recent_messages": [],
}

def measure_request_time(payload):
    """Gửi request và đo thời gian phản hồi."""
    with httpx.Client(timeout=60.0) as client:
        start_time = time.time()
        response = client.post(BACKEND_URL, json=payload)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return response.status_code, elapsed_time, response.text

def main():
    # Test với payload chỉ chứa code
    logging.info("Testing with codes only...")
    status_code, time_codes, response_codes = measure_request_time(payload_codes)
    logging.info(f"Status Code: {status_code}, Time Taken: {time_codes:.4f} seconds")
    logging.info(f"Response size (codes only): {len(response_codes)} characters")
    logging.info(f"Response: {response_codes}")

    # Test với payload chứa toàn bộ dữ liệu
    logging.info("\nTesting with full data...")
    status_code, time_full, response_full = measure_request_time(payload_full)
    logging.info(f"Status Code: {status_code}, Time Taken: {time_full:.4f} seconds")
    logging.info(f"Response size (full data): {len(response_full)} characters")
    logging.info(f"Response: {response_full}")

    # So sánh thời gian
    logging.info("\nComparison:")
    logging.info(f"Codes only: {time_codes:.4f} seconds")
    logging.info(f"Full data: {time_full:.4f} seconds")

if __name__ == "__main__":
    main()