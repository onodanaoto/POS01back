#!/bin/bash

# 環境変数の設定
export ACR_NAME="your-acr-name"
export RESOURCE_GROUP="your-resource-group"
export LOCATION="japaneast"

# Azure Container Registryの作成
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# ACRへのログイン
az acr login --name $ACR_NAME

# イメージのビルドとプッシュ
docker-compose build
docker-compose push

# Azure Database for MySQLの作成
az mysql flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name ${ACR_NAME}-mysql \
  --admin-user $DB_USER \
  --admin-password $DB_PASSWORD \
  --sku-name Standard_B1ms

# Container Appsの作成
az containerapp create \
  --resource-group $RESOURCE_GROUP \
  --name ${ACR_NAME}-backend \
  --image ${ACR_NAME}.azurecr.io/pos-lv1-backend:latest \
  --environment ${ACR_NAME}-env

az containerapp create \
  --resource-group $RESOURCE_GROUP \
  --name ${ACR_NAME}-frontend \
  --image ${ACR_NAME}.azurecr.io/pos-lv1-frontend:latest \
  --environment ${ACR_NAME}-env 