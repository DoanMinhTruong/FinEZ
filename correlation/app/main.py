from typing import Union
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
from sklearn.datasets import load_breast_cancer
from fastapi import FastAPI , Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc cấu hình danh sách các origin mà bạn muốn cho phép
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def plot_stock_correlation(stock1, stock2):
    # Tạo DataFrame từ dữ liệu cổ phiếu stock1
    stock1_df = stock1._get_numeric_data()

    # Tạo DataFrame từ dữ liệu cổ phiếu stock2
    stock2_df = stock2._get_numeric_data()

    # Kết hợp hai DataFrame thành một DataFrame chung
    merged_df = pd.concat([stock1_df, stock2_df], axis=1)

    # Tính ma trận tương quan giữa hai cột
    correlation_matrix = merged_df.corr()

    # Vẽ biểu đồ heatmap
    sns.set(style='white')
    plt.figure(figsize=(15, 9))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Stock Correlation Heatmap')

    # Lưu biểu đồ vào đối tượng StringIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Trả về đối tượng StringIO chứa ảnh
    return buffer

from fastapi.responses import StreamingResponse
import json
@app.get('/corr')
async def correlation_matrix(request:Request):
    r = await request.json()
    r = json.loads(r)
    data1 = r['stock_1']
    data2 = r['stock_2']

    inp1 = {}
    inp2 = {}
    for i in data1[0]:
        inp1[i] = []
        inp2[i] = []
    for i in range(len(data1)):
        for j in inp1:
            inp1[j].append(data1[i][j])
            inp2[j].append(data2[i][j])

    bytes_obj = plot_stock_correlation(pd.DataFrame(inp1) ,pd.DataFrame(inp2))
    
    return StreamingResponse(bytes_obj, media_type="image/png")


