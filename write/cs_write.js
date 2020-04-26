(function() {
  var boot, exec, getJumpUrl, getMoveSec, getRefreshMeta, main, origin, sendMessageConfirm, sendMessageError, sendMessagePing, sendMessageSuccess, submitThreadFlag;
  origin = (typeof browser !== "undefined" && browser !== null ? browser : chrome).runtime.getURL("").slice(0, -1);
  submitThreadFlag = false;
  exec = function(javascript) {
    var script;
    script = document.createElement("script");
    script.innerHTML = javascript;
    document.body.appendChild(script);
  };
  sendMessagePing = function() {
    exec(`parent.postMessage({type: "ping"}, "${origin}");`);
  };
  sendMessageSuccess = function(moveMs) {
    var jumpUrl;
    if (submitThreadFlag) {
      jumpUrl = getJumpUrl();
      exec(`parent.postMessage({\n  type : "success",\n  key: "${jumpUrl}",\n  message: ${moveMs}\n}, "${origin}");`);
    } else {
      exec(`parent.postMessage({type: "success", message: ${moveMs}}, "${origin}");`);
    }
  };
  sendMessageConfirm = function() {
    exec(`parent.postMessage({type: "confirm"}, "${origin}");`);
  };
  sendMessageError = function(message) {
    if (typeof message === "string") {
      exec(`parent.postMessage({\n  type: "error",\n  message: "${message.replace(/\"/g, "&quot;")}"\n}, "${origin}");`);
    } else {
      exec(`parent.postMessage({type: "error"}, "${origin}");`);
    }
  };
  getRefreshMeta = function() {
    var $head, $heads;
    $heads = document.head.children;
    for ($head of $heads) {
      if ($head.getAttribute("http-equiv") === "refresh") {
        return $head;
      }
    }
    return null;
  };
  getMoveSec = function() {
    var $refreshMeta, content, m, ref, sec;
    sec = 3;
    $refreshMeta = getRefreshMeta();
    content = $refreshMeta != null ? $refreshMeta.content : void 0;
    if ((content == null) || content === "") {
      return sec;
    }
    m = content.match(/^(\d+);/);
    return (ref = m != null ? m[1] : void 0) != null ? ref : sec;
  };
  getJumpUrl = function() {
    var $meta, as, domain, ref, ref1, ref2;
    domain = location.hostname;
    if (domain.endsWith("5ch.net") || domain.endsWith("bbspink.com") || domain.endsWith("open2ch.net")) {
      $meta = getRefreshMeta();
      return (ref = $meta != null ? $meta.content : void 0) != null ? ref : "";
    }
    if (domain.endsWith("2ch.sc")) {
      as = document.getElementsByTagName("a");
      return (ref1 = as != null ? (ref2 = as[0]) != null ? ref2.href : void 0 : void 0) != null ? ref1 : "";
    }
    return "";
  };
  main = function() {
    var font, text, title, url;
    ({title} = document);
    url = location.href;
    //したらば投稿確認
    if (/^https?:\/\/jbbs\.shitaraba\.net\/bbs\/write.cgi\/\w+\/\d+\/(?:\d+|new)\/$/.test(url)) {
      if (title.includes("書きこみました")) {
        sendMessageSuccess(3 * 1000);
      } else if (title.includes("ERROR") || title.includes("スレッド作成規制中")) {
        sendMessageError();
      }
    // まちBBS投稿確認
    } else if (/^https?:\/\/(?:\w+\.)?machi\.to\/bbs\/write\.cgi/.test(url)) {
      if (title.includes("ＥＲＲＯＲ")) {
        sendMessageError();
      }
    } else if (/^https?:\/\/(?:\w+\.)?machi\.to/.test(url)) {
      sendMessageSuccess(1 * 1000);
    //open2ch投稿確認
    } else if (/^https?:\/\/\w+\.open2ch\.net\/test\/bbs\.cgi/.test(url)) {
      font = document.getElementsByTagName("font");
      text = title;
      if (font.length > 0) {
        text += font[0].innerText;
      }
      if (text.includes("書きこみました")) {
        sendMessageSuccess(getMoveSec() * 1000);
      } else if (text.includes("確認")) {
        setTimeout(sendMessageConfirm, 1000 * 6);
      } else if (text.includes("ＥＲＲＯＲ")) {
        sendMessageError();
      }
    //2ch型投稿確認
    } else if (/^https?:\/\/\w+\.\w+\.\w+\/test\/bbs\.cgi/.test(url)) {
      if (title.includes("書きこみました")) {
        sendMessageSuccess(getMoveSec() * 1000);
      } else if (title.includes("確認")) {
        setTimeout(sendMessageConfirm, 1000 * 6);
      } else if (title.includes("ＥＲＲＯＲ")) {
        sendMessageError();
      }
    }
  };
  boot = function() {
    window.addEventListener("message", function(e) {
      if (e.origin === origin) {
        if (e.data === "write_iframe_pong") {
          main();
        } else if (e.data === "write_iframe_pong:thread") {
          submitThreadFlag = true;
          main();
        }
      }
    });
    sendMessagePing();
  };
  setTimeout(boot, 0);
})();
