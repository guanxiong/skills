# 样式规范

## 颜色方案

```css
:root {
  --primary-color: #E88A7A;
  --primary-light: #F0A898;
  --primary-dark: #D86A5A;
  --bg-color: #FFF9F7;
  --card-bg: #FFFFFF;
  --text-primary: #3D3A38;
  --text-secondary: #6B6662;
  --border-color: #F0EBE7;
}
```

## 响应式断点

```css
/* 小屏 */
@media (max-width: 374px) { }

/* 平板 */
@media (min-width: 768px) { }

/* PC */
@media (min-width: 1200px) { }
```

## 关键样式类

### 页面容器
```css
.page-wrapper {
  min-height: 100vh;
  background: var(--bg-color);
  padding-bottom: calc(env(safe-area-inset-bottom) + 60px);
}

body.in-miniprogram .page-wrapper {
  padding-bottom: calc(env(safe-area-inset-bottom) + 80px);
}
```

### 头部
```css
.header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  padding: 32px 20px;
  color: white;
}

.header-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.header-subtitle {
  font-size: 14px;
  opacity: 0.9;
}
```

### 内容卡片
```css
.content-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  margin: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.content-card h2 {
  color: var(--text-primary);
  font-size: 18px;
  margin: 20px 0 12px;
}

.content-card p {
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 12px;
}
```

### 强调框
```css
.emphasis-box {
  background: #FAF3F1;
  border-left: 3px solid var(--primary-color);
  padding: 16px;
  margin: 16px 0;
  border-radius: 4px;
}
```

### 底部
```css
.footer {
  margin-top: 40px;
  padding: 32px 20px;
  text-align: center;
  border-top: 1px solid var(--border-color);
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
}

.footer-links a:hover {
  color: var(--primary-color);
}

.footer-copyright {
  color: var(--text-secondary);
  font-size: 12px;
}
```

### 返回顶部按钮
```css
.back-top {
  position: fixed;
  right: 16px;
  bottom: 16px;
  width: 44px;
  height: 44px;
  background: var(--primary-color);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition: all 0.25s ease;
  z-index: 100;
}

body.in-miniprogram .back-top {
  bottom: calc(env(safe-area-inset-bottom) + 16px);
}

.back-top.visible {
  opacity: 1;
  visibility: visible;
}

.back-top:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}
```

## 小程序适配

### 安全区域处理
```css
/* 刘海屏底部安全区域 */
.page-wrapper {
  padding-bottom: env(safe-area-inset-bottom);
}

/* 底部固定元素上移 */
.footer,
.back-top {
  padding-bottom: env(safe-area-inset-bottom);
  bottom: calc(16px + env(safe-area-inset-bottom));
}
```

### 小程序环境样式
```css
body.in-miniprogram .header {
  padding-top: calc(32px + env(safe-area-inset-top));
}
```
