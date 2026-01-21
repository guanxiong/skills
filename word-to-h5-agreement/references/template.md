# HTML 模板

## 完整 HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="format-detection" content="telephone=no, email=no">
  <title>协议标题</title>
  <style>
    /* CSS 在此内联，详见 styles.md */
  </style>
</head>
<body>
  <div class="page-wrapper">
    <header class="header">
      <div class="header-content">
        <h1 class="header-title">协议标题</h1>
        <p class="header-subtitle">生效日期</p>
      </div>
    </header>

    <main class="main-content">
      <article class="content-card">
        <!-- 协议内容 -->
      </article>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <nav class="footer-links">
          <a href="./user-agreement.html">用户协议</a>
          <a href="./privacy-agreement.html">隐私协议</a>
          <a href="./children-privacy.html">儿童隐私保护</a>
        </nav>
        <p class="footer-copyright">公司名称 © 年份</p>
      </div>
    </footer>

    <button class="back-top" id="backTop">▲</button>
  </div>

  <script>
    // 返回顶部功能
    const backTop = document.getElementById('backTop');
    function toggleBackTop() {
      if (window.scrollY > 300) {
        backTop.classList.add('visible');
      } else {
        backTop.classList.remove('visible');
      }
    }
    backTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    window.addEventListener('scroll', toggleBackTop);
    toggleBackTop();

    // 小程序环境检测
    const isMiniprogram = /miniprogram/i.test(navigator.userAgent) ||
                         window.__wxjs_environment === 'miniprogram';
    if (isMiniprogram) document.body.classList.add('in-miniprogram');
  </script>
</body>
</html>
```

## 关键元素说明

### Meta 标签
- `viewport-fit=cover`: 小程序全屏适配
- `format-detection`: 禁止自动识别电话/邮箱

### 页面结构
- `header`: 协议标题和生效日期
- `main`: 协议正文内容（使用 article 语义标签）
- `footer`: 导航链接和版权信息

### JavaScript 功能
1. 返回顶部按钮（滚动超过 300px 显示）
2. 小程序环境检测（添加 `in-miniprogram` class）
