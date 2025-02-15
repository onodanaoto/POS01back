FROM python:3.12-slim

WORKDIR /home/site/wwwroot  # Azure App Serviceのデフォルトパス

# システムパッケージのインストール
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# 環境変数の設定
ENV PORT=8000
ENV HOST=0.0.0.0

# スタートアップスクリプトの作成
RUN echo "#!/bin/bash\ncd /home/site/wwwroot && pip install uvicorn && uvicorn app.main:app --host 0.0.0.0 --port 8000" > /startup.sh && \
    chmod +x /startup.sh

# スタートアップスクリプトを実行
CMD ["/startup.sh"] 