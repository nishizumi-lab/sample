app.boot("/view/inputurl.html", function() {
  var $view;
  $view = document.documentElement;
  new app.view.TabContentView($view);
  $view.T("form")[0].on("submit", function(e) {
    var ele, guessType, url, urlStr;
    e.preventDefault();
    urlStr = this.url.value;
    urlStr = urlStr.replace(/^(ttps?):\/\//, "h$1://");
    if (!/^https?:\/\//.test(urlStr)) {
      urlStr = `http://${urlStr}`;
    }
    url = new app.URL.URL(urlStr);
    ({
      type: guessType
    } = url.guessType());
    if (guessType === "thread" || guessType === "board") {
      app.message.send("open", {
        url: url.href,
        new_tab: true
      });
      parent.postMessage({
        type: "request_killme"
      }, location.origin);
    } else {
      ele = $view.C("notice")[0];
      ele.textContent = "未対応形式のURLです";
      UI.Animate.fadeIn(ele);
    }
  });
});
