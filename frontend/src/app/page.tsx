'use client'
import { useState } from 'react'
import styles from './page.module.css'

interface Product {
  CODE: string
  NAME: string
  PRICE: number
}

interface CartItem extends Product {
  quantity: number
}

// バックエンドのURLを環境変数から取得
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [productCode, setProductCode] = useState('')
  const [currentProduct, setCurrentProduct] = useState<Product | null>(null)
  const [cart, setCart] = useState<CartItem[]>([])

  // 商品コード読み込みボタンのハンドラー
  const handleReadProduct = async () => {
    try {
      const response = await fetch(`${API_URL}/products/${productCode}`)
      if (response.ok) {
        const product = await response.json()
        setCurrentProduct(product)
      } else {
        alert('商品が見つかりません')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('エラーが発生しました')
    }
  }

  // 追加ボタンのハンドラー
  const handleAddToCart = () => {
    if (!currentProduct) return

    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.CODE === currentProduct.CODE)
      if (existingItem) {
        return prevCart.map(item =>
          item.CODE === currentProduct.CODE
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }
      return [...prevCart, { ...currentProduct, quantity: 1 }]
    })

    // 商品追加後、入力欄とカレント商品をクリア
    setProductCode('')
    setCurrentProduct(null)
  }

  // 購入ボタンのハンドラー
  const handlePurchase = async () => {
    if (cart.length === 0) return

    try {
      const response = await fetch(`${API_URL}/purchase`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items: cart }),
      })

      if (response.ok) {
        alert('購入が完了しました')
        setCart([])
      } else {
        alert('購入処理に失敗しました')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('エラーが発生しました')
    }
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        {/* 商品コード入力エリア */}
        <div className={styles.inputArea}>
          <input
            type="text"
            value={productCode}
            onChange={(e) => setProductCode(e.target.value)}
            placeholder="商品コードを入力"
            maxLength={13}
            className={styles.input}
          />
          <button className={styles.styledButton} onClick={handleReadProduct}>
            商品コード 読み込み
          </button>
        </div>

        {/* 商品情報表示エリア */}
        {currentProduct && (
          <div className={styles.productInfo}>
            <div>{currentProduct.NAME}</div>
            <div>{currentProduct.PRICE}円</div>
            <button className={styles.styledButton} onClick={handleAddToCart}>
              追加
            </button>
          </div>
        )}

        {/* 購入リスト */}
        <div className={styles.cartList}>
          <h2>購入リスト</h2>
          {cart.map((item) => (
            <div key={item.CODE} className={styles.cartItem}>
              <span>{item.NAME}</span>
              <span>x{item.quantity}</span>
              <span>{item.PRICE}円</span>
              <span>{item.PRICE * item.quantity}円</span>
            </div>
          ))}
          {cart.length > 0 && (
            <button className={styles.styledButton} onClick={handlePurchase}>
              購入
            </button>
          )}
        </div>
      </div>
    </main>
  )
} 