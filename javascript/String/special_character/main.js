// HTML特殊文字変換（通常文字 → 特殊文字）
var htmlsce = (function() {
	const map = {' ':'&nbsp;','<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&apos;','©':'&copy;'};
	return function(text, charset) {
	  charset = charset && charset.replace(/([\x00-\x2F\x3A-\x40\x5B-\x60\x7B-\x7F])/g, '\\$&') || '';
	  return text.replace(new RegExp('[ <>&"\'©'+charset+']', 'g'), function(match) {
		if (map.hasOwnProperty(match)) {
		  return map[match];
		} else {
		  return '&#'+match.charCodeAt(match)+';';
		}
	  });
	};
  })();

// HTML特殊文字変換（特殊文字 → 通常文字）
var htmlscd = (function() {
  const re = /&#x([0-9A-Fa-f]+);|&#(\d+);|&\w+;/g;
  const map = {'&nbsp;':' ','&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"','&apos;':"'",'&copy;':'©'};
  return function(text) {
    return text.replace(re, function(match, p1, p2) {
      if (match.charAt(1) == '#') {
        // 数値文字参照
        if (match.charAt(2) == 'x') {
          return String.fromCharCode(parseInt(p1, 16));
        } else {
          return String.fromCharCode(p2-0);
        }
      } else if (map.hasOwnProperty(match)) {
        // 定義済み文字実体参照
        return map[match];
      }
      return match;
    });
  };
})();

// ファイルアップロード判定
function main() {
	var src = '<html>CONTENT</html>';

	// 通常文字 → 特殊文字
	var dst = htmlsce(src);
	console.log(dst);  // &lt;html&gt;CONTENT&lt;/html&gt;

	// 特殊文字 → 通常文字
	var src = '&lt;html&gt;CONTENT&lt;&#47;html&gt;';
	var dst = htmlscd(src);
	console.log(dst);  // <html>CONTENT</html>
};

main();
