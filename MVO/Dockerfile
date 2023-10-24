# Sử dụng một hình ảnh cơ sở có sẵn cho Python
FROM python:3.9

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tệp yêu cầu và mã nguồn ứng dụng vào container
COPY requirements.txt .
COPY . .

# Cài đặt các thư viện yêu cầu
RUN apt-get update 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Mở cổng 5001 để cho phép Flask chạy
EXPOSE 5001

# Khởi chạy ứng dụng Flask
CMD ["python", "main.py"]
