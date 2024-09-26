javascript:(() => {
    // ページタイトルとURLを取得
    let url = document.URL;
    let title = document.title;

    // Markdown形式に整形してクリップボードに貼り付け
    let text = '- [' + title + '](' + url + ')\n';
    navigator.clipboard.writeText(text);
 
  })()