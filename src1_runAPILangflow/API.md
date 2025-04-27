```bash
curl --request POST \
  --url 'https://api.langflow.astra.datastax.com/lf/28c59750-7ad2-49ac-b013-bafe55d30330/api/v1/run/18b6014b-e8ba-4119-9b7c-9a92fab2038c?stream=false' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer AstraCS:peEHDhrGjxhNmTYOxbahatRj:' \
  --data '{
  "input_value": "What is the document is about?",
  "output_type": "chat",
  "input_type": "chat"
}'
```

```
{
    "session_id": "18b6014b-e8ba-4119-9b7c-9a92fab2038c",
    "outputs": [
        {
            "inputs": {
                "input_value": "What is the document is about?"
            },
            "outputs": [
                {
                    "results": {
                        "message": {
                            "text_key": "text",
                            "data": {
                                "timestamp": "2025-04-27T02:41:35+00:00",
                                "sender": "Machine",
                                "sender_name": "AI",
                                "session_id": "18b6014b-e8ba-4119-9b7c-9a92fab2038c",
                                "text": "The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level. It highlights how the program helps learners understand methods, expand their vocabulary, and improve their communication skills. Additionally, it mentions features such as displaying learning summaries, speaking proficiency tests, rankings, and account settings.",
                                "files": [],
                                "error": false,
                                "edit": false,
                                "properties": {
                                    "text_color": "",
                                    "background_color": "",
                                    "edited": false,
                                    "source": {
                                        "id": "OpenAIModel-OumPZ",
                                        "display_name": "OpenAI",
                                        "source": "gpt-4o-mini"
                                    },
                                    "icon": "OpenAI",
                                    "allow_markdown": false,
                                    "positive_feedback": null,
                                    "state": "complete",
                                    "targets": []
                                },
                                "category": "message",
                                "content_blocks": [],
                                "id": "28d8e5c2-5705-462c-9b31-2d9db54936d5",
                                "flow_id": "18b6014b-e8ba-4119-9b7c-9a92fab2038c"
                            },
                            "default_value": "",
                            "text": "The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level. It highlights how the program helps learners understand methods, expand their vocabulary, and improve their communication skills. Additionally, it mentions features such as displaying learning summaries, speaking proficiency tests, rankings, and account settings.",
                            "sender": "Machine",
                            "sender_name": "AI",
                            "files": [],
                            "session_id": "18b6014b-e8ba-4119-9b7c-9a92fab2038c",
                            "timestamp": "2025-04-27T02:41:35+00:00",
                            "flow_id": "18b6014b-e8ba-4119-9b7c-9a92fab2038c",
                            "error": false,
                            "edit": false,
                            "properties": {
                                "text_color": "",
                                "background_color": "",
                                "edited": false,
                                "source": {
                                    "id": "OpenAIModel-OumPZ",
                                    "display_name": "OpenAI",
                                    "source": "gpt-4o-mini"
                                },
                                "icon": "OpenAI",
                                "allow_markdown": false,
                                "positive_feedback": null,
                                "state": "complete",
                                "targets": []
                            },
                            "category": "message",
                            "content_blocks": []
                        }
                    },
                    "artifacts": {
                        "message": "The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level. It highlights how the program helps learners understand methods, expand their vocabulary, and improve their communication skills. Additionally, it mentions features such as displaying learning summaries, speaking proficiency tests, rankings, and account settings.",
                        "sender": "Machine",
                        "sender_name": "AI",
                        "files": [],
                        "type": "object"
                    },
                    "outputs": {
                        "message": {
                            "message": "The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level. It highlights how the program helps learners understand methods, expand their vocabulary, and improve their communication skills. Additionally, it mentions features such as displaying learning summaries, speaking proficiency tests, rankings, and account settings.",
                            "type": "text"
                        }
                    },
                    "logs": {
                        "message": []
                    },
                    "messages": [
                        {
                            "message": "The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level. It highlights how the program helps learners understand methods, expand their vocabulary, and improve their communication skills. Additionally, it mentions features such as displaying learning summaries, speaking proficiency tests, rankings, and account settings.",
                            "sender": "Machine",
                            "sender_name": "AI",
                            "session_id": "18b6014b-e8ba-4119-9b7c-9a92fab2038c",
                            "stream_url": null,
                            "component_id": "ChatOutput-7a5Kv",
                            "files": [],
                            "type": "text"
                        }
                    ],
                    "timedelta": null,
                    "duration": null,
                    "component_display_name": "Chat Output",
                    "component_id": "ChatOutput-7a5Kv",
                    "used_frozen_result": false
                }
            ]
        }
    ]
}
```

Tôi sẽ giải thích chi tiết các key chính trong JSON output:

1. **session_id**: 
- Là ID duy nhất của phiên làm việc
- Ví dụ: "18b6014b-e8ba-4119-9b7c-9a92fab2038c"

2. **outputs**: Mảng chứa kết quả trả về
   - **inputs**: Chứa thông tin đầu vào
     - `input_value`: Câu hỏi đã gửi
   - **outputs**: Mảng chứa kết quả xử lý
     - **results**: Kết quả chính
       - **message**: Thông tin tin nhắn
         - `text_key`: Key cho text ("text")
         - `data`: Dữ liệu chi tiết
           - `timestamp`: Thời gian tạo tin nhắn
           - `sender`: Người gửi ("Machine")
           - `sender_name`: Tên người gửi ("AI")
           - `session_id`: ID phiên
           - `text`: Nội dung tin nhắn
           - `files`: Danh sách file đính kèm
           - `error`: Có lỗi hay không
           - `edit`: Có chỉnh sửa hay không
           - `properties`: Thuộc tính hiển thị
             - `source`: Thông tin model AI
               - `id`: ID model
               - `display_name`: Tên hiển thị
               - `source`: Tên model (gpt-4o-mini)
             - `icon`: Biểu tượng
             - `allow_markdown`: Cho phép markdown
             - `state`: Trạng thái
           - `category`: Loại tin nhắn
           - `content_blocks`: Các khối nội dung
           - `id`: ID tin nhắn
           - `flow_id`: ID luồng xử lý

3. **artifacts**: Thông tin bổ sung
   - `message`: Nội dung tin nhắn
   - `sender`: Người gửi
   - `sender_name`: Tên người gửi
   - `files`: Danh sách file
   - `type`: Loại dữ liệu

4. **outputs**: Kết quả đầu ra
   - `message`: 
     - `message`: Nội dung tin nhắn
     - `type`: Loại dữ liệu ("text")

5. **logs**: Thông tin log
   - `message`: Danh sách log

6. **messages**: Danh sách tin nhắn
   - `message`: Nội dung
   - `sender`: Người gửi
   - `sender_name`: Tên người gửi
   - `session_id`: ID phiên
   - `stream_url`: URL stream (nếu có)
   - `component_id`: ID component
   - `files`: Danh sách file
   - `type`: Loại dữ liệu

7. **timedelta**: Thời gian xử lý

8. **duration**: Thời lượng xử lý

9. **component_display_name**: Tên hiển thị component

10. **component_id**: ID component

11. **used_frozen_result**: Có sử dụng kết quả đóng băng hay không

Cấu trúc này được thiết kế để cung cấp đầy đủ thông tin về:
- Nội dung trả lời
- Metadata của tin nhắn
- Thông tin về hệ thống xử lý
- Trạng thái và thuộc tính của kết quả

---

Trong JSON output, phản hồi chính (nội dung trả lời) xuất hiện ở nhiều nơi, nhưng nội dung chính xác giống nhau. Có thể tìm thấy ở các vị trí sau:

1. **Vị trí chính và đầy đủ nhất**:
```json
"results": {
    "message": {
        "data": {
            "text": "The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level..."
        }
    }
}
```

2. **Các vị trí khác có cùng nội dung**:
- Trong `artifacts.message`
- Trong `outputs.message.message`
- Trong `messages[0].message`

Nội dung phản hồi chính là:
```
"The document is about the benefits of a learning platform or program designed for language learners at the A1-A2 level. It highlights how the program helps learners understand methods, expand their vocabulary, and improve their communication skills. Additionally, it mentions features such as displaying learning summaries, speaking proficiency tests, rankings, and account settings."
```

Lý do nội dung này xuất hiện nhiều lần là vì:
1. Mỗi phần phục vụ một mục đích khác nhau trong hệ thống
2. Đảm bảo tính nhất quán của dữ liệu
3. Hỗ trợ các chức năng khác nhau của API

Tuy nhiên, khi sử dụng API, bạn chỉ cần lấy nội dung từ một trong các vị trí trên là đủ, thường là từ `results.message.data.text` vì đây là vị trí chính thức và đầy đủ metadata nhất.
