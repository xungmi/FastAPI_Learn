#!/bin/bash

# Lấy danh sách PID đang sử dụng cổng 8000
PIDS=$(lsof -ti :8000)

if [ -z "$PIDS" ]; then
    echo "✅ Không có process nào đang sử dụng cổng 8000."
else
    echo "⚠️ Đang kill các process trên cổng 8000: $PIDS"
    kill -9 $PIDS
    echo "✅ Đã kill xong tất cả process trên cổng 8000."
fi
