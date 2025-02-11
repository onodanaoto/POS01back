FROM python:3.12-slim

WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# 環境変数の設定
ENV PORT=8000
ENV HOST=0.0.0.0

# アプリケーションの起動コマンドを修正
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 