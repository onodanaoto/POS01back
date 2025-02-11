FROM node:18-alpine

WORKDIR /app

# 依存関係のインストール
COPY package*.json ./
RUN npm install

# ソースコードのコピー
COPY . .

# 本番用ビルド
RUN npm run build

EXPOSE 3000

# 本番環境では dev ではなく start を使用
CMD ["npm", "start"] 