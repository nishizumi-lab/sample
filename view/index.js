var indexOf = [].indexOf;

if (app.view == null) {
  app.view = {};
}

/**
@namespace app.view
@class Index
@extends app.view.View
@constructor
@param {Element} element
*/
app.view.Index = class Index extends app.view.View {
  constructor(element) {
    super(element);
    this._insertUserCSS();
    //iframe以外の部分がクリックされた時にフォーカスをiframe内に戻す
    this.$element.on("click", () => {
      var target;
      target = this.$element.$(".tab_content.iframe_focused");
      target || (target = $$.I("left_pane"));
      this.focus(target);
    });
    //iframeがクリックされた時にフォーカスを移動
    this.$element.on("request_focus", ({
        target,
        detail: {focus}
      }) => {
      if (!target.matches("iframe:not(.iframe_focused)")) {
        return;
      }
      this.focus(target, focus);
    });
    //タブが選択された時にフォーカスを移動
    this.$element.on("tab_selected", ({target}) => {
      if (!target.hasClass("tab_content")) {
        return;
      }
      this.focus(target);
    });
    //.tab内の最後のタブが削除された時にフォーカスを移動
    this.$element.on("tab_removed", async({target}) => {
      var $tab, $tmp, dom, i, j, len, len1, ref, ref1;
      if (!target.hasClass("tab_content")) {
        return;
      }
      ref = target.parent().$$(":scope > .tab_content");
      for (i = 0, len = ref.length; i < len; i++) {
        dom = ref[i];
        if (dom !== target) {
          return;
        }
      }
      await app.defer();
      ref1 = $$.C("tab");
      for (j = 0, len1 = ref1.length; j < len1; j++) {
        $tab = ref1[j];
        if (!($tab.C("tab_selected") != null)) {
          continue;
        }
        $tmp = $tab;
        break;
      }
      if (($tmp != null ? $tmp.$(".tab_selected.tab_content") : void 0) != null) {
        this.focus($tmp.$(".tab_selected.tab_content"));
      } else {
        //フォーカス対象のタブが無い場合、板一覧にフォーカスする
        this.focus($$.I("left_pane"));
      }
    });
    //フォーカスしているコンテンツが再描画された場合、フォーカスを合わせ直す
    this.$element.on("view_loaded", ({target}) => {
      if (target.matches(".tab_content.iframe_focused")) {
        return;
      }
      this.focus(target);
    });
    app.message.on("requestFocusMove", async({command, repeatCount}) => {
      var $target, i, j, len, len1, t;
      switch (command) {
        case "focusUpFrame":
          this.focusUp();
          break;
        case "focusDownFrame":
          this.focusDown();
          break;
        case "focusLeftFrame":
          this.focusLeft(repeatCount);
          break;
        case "focusRightFrame":
          this.focusRight(repeatCount);
      }
      $target = this.$element.C("iframe_focused");
// shortQueryがまだ読み込まれていないことがあるので標準APIで
      for (i = 0, len = $target.length; i < len; i++) {
        t = $target[i];
        t.contentDocument.getElementsByClassName("view")[0].classList.add("focus_effect");
      }
      await app.wait(200);
      for (j = 0, len1 = $target.length; j < len1; j++) {
        t = $target[j];
        t.contentDocument.getElementsByClassName("view")[0].classList.remove("focus_effect");
      }
    });
    app.message.on("showKeyboardHelp", () => {
      this.showKeyboardHelp();
    });
    return;
  }

  /**
  @method focus
  @param {Element} iframe
  @param {Boolean} [focus=true]
  trueだと実際にフォーカスを移動する処理が行われる。
  */
  focus($iframe, focus = true) {
    var fn, focusIframe, ref, ref1, ref2;
    if (!$iframe.hasClass("iframe_focused")) {
      if ((ref = this.$element.C("iframe_focused")[0]) != null) {
        ref.removeClass("iframe_focused");
      }
      $iframe.addClass("iframe_focused");
    }
    focusIframe = function($iframe) {
      var ref1, ref2, ref3, ref4;
      if ((ref1 = $iframe.contentDocument) != null) {
        if ((ref2 = ref1.activeElement) != null) {
          ref2.blur();
        }
      }
      if ((ref3 = $iframe.contentDocument) != null) {
        if ((ref4 = ref3.getElementsByClassName("content")[0]) != null) {
          ref4.focus();
        }
      }
    };
    if (focus) {
      if (!$iframe.src.endsWith("empty.html") && (((ref1 = $iframe.contentDocument) != null ? (ref2 = ref1.getElementsByClassName("content")) != null ? ref2[0] : void 0 : void 0) != null)) {
        focusIframe($iframe);
      } else {
        $iframe.on("load", fn = function() {
          if ($iframe.src.endsWith("empty.html")) {
            return;
          }
          $iframe.off("load", fn);
          focusIframe($iframe);
        });
      }
    }
  }

  /**
  @method _getLeftFrame
  @private
  @param {Element} iframe
  @return {Element|null} leftFrame
  */
  _getLeftFrame($iframe) {
    var $leftTabLi, leftTabId, tabId;
    if (!$iframe.hasClass("tab_content")) {
      // 既に#left_paneにフォーカスが当たっている場合
      return null;
    }
    // 同一.tab内での候補探索
    tabId = $iframe.dataset.tabid;
    $leftTabLi = this.$element.$(`li[data-tabid="${tabId}"]`).prev();
    if ($leftTabLi != null) {
      leftTabId = $leftTabLi.dataset.tabid;
      return this.$element.$(`.tab_content[data-tabid="${leftTabId}"]`);
    }
    // 同一.tab内で候補がなかった場合
    // 左に.tabが存在し、タブが存在する場合はそちらを優先する
    if ($$.I("body").hasClass("pane-3h") && $iframe.closest(".tab").id === "tab_b") {
      return this.$element.$("#tab_a .tab_content.tab_selected");
    }
    // そうでなければ#left_paneで確定
    return $$.I("left_pane");
  }

  /**
  @method focusLeft
  @param {number} [repeat=1]
  */
  focusLeft(repeat = 1) {
    var $currentFrame, $prevTargetFrame, $targetFrame, i, ref, targetTabId;
    $currentFrame = this.$element.C("iframe_focused")[0];
    $targetFrame = $currentFrame;
    for (i = 0, ref = repeat; (0 <= ref ? i < ref : i > ref); 0 <= ref ? i++ : i--) {
      $prevTargetFrame = $targetFrame;
      $targetFrame = this._getLeftFrame($targetFrame) || $targetFrame;
      if ($targetFrame === $prevTargetFrame) {
        break;
      }
    }
    if ($targetFrame !== $currentFrame) {
      if ($targetFrame.hasClass("tab_content")) {
        targetTabId = $targetFrame.dataset.tabid;
        app.DOMData.get($targetFrame.closest(".tab"), "tab").update(targetTabId, {
          selected: true
        });
      } else {
        this.focus($targetFrame);
      }
    }
  }

  /**
  @method _getRightFrame
  @private
  @param {Element} iframe
  @return {Element|null} rightFrame
  */
  _getRightFrame($iframe) {
    var $rightTabLi, $targetFrame, rightTabId, tabId;
    // サイドメニューにフォーカスが当たっている場合
    if ($iframe.id === "left_pane") {
      $targetFrame = this.$element.$("#tab_a .tab_content.tab_selected");
      if ($targetFrame == null) {
        $targetFrame = this.$element.$("#tab_b .tab_content.tab_selected");
      }
      return $targetFrame;
    }
    // タブ内コンテンツにフォーカスが当たっている場合
    // 同一.tab内での候補探索
    tabId = $iframe.dataset.tabid;
    $rightTabLi = this.$element.$(`li[data-tabid="${tabId}"]`).next();
    if ($rightTabLi != null) {
      rightTabId = $rightTabLi.dataset.tabid;
      return this.$element.$(`.tab_content[data-tabid="${rightTabId}"]`);
    }
    // タブ内で候補が見つからなかった場合
    // 右に.tabが存在し、タブが存在する場合はそれを選択する
    if ($$.I("body").hasClass("pane-3h") && $iframe.closest(".tab").id === "tab_a") {
      return this.$element.$("#tab_b .tab_content.tab_selected");
    }
    return null;
  }

  /**
  @method focusRight
  @param {number} [repeat = 1]
  */
  focusRight(repeat = 1) {
    var $currentFrame, $prevTargetFrame, $targetFrame, i, ref, targetTabId;
    $currentFrame = this.$element.C("iframe_focused")[0];
    $targetFrame = $currentFrame;
    for (i = 0, ref = repeat; (0 <= ref ? i < ref : i > ref); 0 <= ref ? i++ : i--) {
      $prevTargetFrame = $targetFrame;
      $targetFrame = this._getRightFrame($targetFrame) || $targetFrame;
      if ($targetFrame === $prevTargetFrame) {
        break;
      }
    }
    if ($targetFrame !== $currentFrame) {
      if ($targetFrame.hasClass("tab_content")) {
        targetTabId = $targetFrame.dataset.tabid;
        app.DOMData.get($targetFrame.closest(".tab"), "tab").update(targetTabId, {
          selected: true
        });
      } else {
        this.focus($targetFrame);
      }
    }
  }

  /**
  @method focusUp
  */
  focusUp() {
    var iframe, ref;
    if ($$.I("body").hasClass("pane-3") && ((ref = this.$element.C("iframe_focused")[0].closest(".tab")) != null ? ref.id : void 0) === "tab_b") {
      iframe = this.$element.$("#tab_a iframe.tab_selected");
    }
    if (iframe) {
      this.focus(iframe);
    }
  }

  /**
  @method focusDown
  */
  focusDown() {
    var iframe, ref;
    if ($$.I("body").hasClass("pane-3") && ((ref = this.$element.C("iframe_focused")[0].closest(".tab")) != null ? ref.id : void 0) === "tab_a") {
      iframe = this.$element.$("#tab_b iframe.tab_selected");
    }
    if (iframe) {
      this.focus(iframe);
    }
  }

  /**
  @method showKeyboardHelp
  */
  async showKeyboardHelp() {
    var $help, ani;
    $help = this.$element.C("keyboard_help")[0];
    ani = (await UI.Animate.fadeIn($help));
    ani.on("finish", () => {
      $help.focus();
      $help.on("click", () => {
        this.hideKeyboardHelp();
      }, {
        once: true
      });
      return $help.on("keydown", () => {
        this.hideKeyboardHelp();
      }, {
        once: true
      });
    }, {
      once: true
    });
  }

  /**
  @method hideKeyboardHelp
  */
  async hideKeyboardHelp() {
    var ani;
    ani = (await UI.Animate.fadeOut(this.$element.C("keyboard_help")[0]));
    ani.on("finish", function() {
      var iframe;
      iframe = $$.C("iframe_focused")[0];
      if (iframe != null) {
        iframe.contentDocument.C("content")[0].focus();
      }
    });
  }

};

app.boot("/view/index.html", ["BBSMenu"], async function(BBSMenu) {
  var appPath, currentTab, i, j, len, len1, menu, query, ref, tab, win, windows;
  query = app.URL.parseQuery(location.search).get("q");
  [currentTab, windows] = (await Promise.all([
    browser.tabs.getCurrent(),
    browser.windows.getAll({
      populate: true
    })
  ]));
  appPath = browser.runtime.getURL("/view/index.html");
  for (i = 0, len = windows.length; i < len; i++) {
    win = windows[i];
    ref = win.tabs;
    for (j = 0, len1 = ref.length; j < len1; j++) {
      tab = ref[j];
      if (!(tab.id !== currentTab.id && tab.url === appPath)) {
        continue;
      }
      browser.windows.update(win.id, {
        focused: true
      });
      browser.tabs.update(tab.id, {
        active: true
      });
      if (query) {
        browser.runtime.sendMessage({
          type: "open",
          query
        });
      }
      browser.tabs.remove(currentTab.id);
      return;
    }
  }
  history.replaceState(null, null, "/view/index.html");
  app.main();
  ({menu} = (await BBSMenu.get()));
  await app.URL.pushServerInfo(menu);
  BBSMenu.target.on("change", function({
      detail: {menu}
    }) {
    return app.URL.pushServerInfo(menu);
  });
  if (!query) {
    return;
  }
  app.message.send("open", {
    url: query,
    new_tab: true
  });
});

app.view_setup_resizer = function() {
  var $body, $rightPane, $tabA, MIN_TAB_HEIGHT, max, min, offset, tmp, updateInfo, val, valAxis, valC;
  MIN_TAB_HEIGHT = 100;
  $body = $$.I("body");
  $tabA = $$.I("tab_a");
  $rightPane = $$.I("right_pane");
  val = null;
  valC = null;
  valAxis = null;
  min = null;
  max = null;
  offset = null;
  updateInfo = function() {
    if ($body.hasClass("pane-3")) {
      val = "height";
      valC = "Height";
      valAxis = "Y";
      offset = $rightPane.offsetTop;
    } else if ($body.hasClass("pane-3h")) {
      val = "width";
      valC = "Width";
      valAxis = "X";
      offset = $rightPane.offsetLeft;
    }
    min = MIN_TAB_HEIGHT;
    max = $rightPane[`offset${valC}`] - MIN_TAB_HEIGHT;
  };
  updateInfo();
  tmp = app.config.get(`tab_a_${val}`);
  if (tmp) {
    $tabA.style[val] = Math.max(Math.min(tmp, max), min) + "px";
  }
  $$.I("tab_resizer").on("mousedown", function(e) {
    var $div;
    e.preventDefault();
    updateInfo();
    $div = $__("div");
    $div.style.cssText = `position: absolute;\nleft: 0;\ntop: 0;\nwidth: 100%;\nheight: 100%;\nz-index: 999;\ncursor: ${(valAxis === "X" ? "col-resize" : "row-resize")}`;
    $div.on("mousemove", (e) => {
      $tabA.style[val] = Math.max(Math.min(e[`page${valAxis}`] - offset, max), min) + "px";
    });
    $div.on("mouseup", function() {
      this.remove();
      app.config.set(`tab_a_${val}`, "" + parseInt($tabA.style[val], 10));
    });
    document.body.addLast($div);
  });
};

app.main = function() {
  var $view, adjustWindowSize, dom, i, iframeSrcToUrl, j, k, len, len1, len2, onRemove, ref, ref1, ref2, tabA, tabB, urlToIframeInfo;
  urlToIframeInfo = function(url, obj = {}) {
    var param, ref, ref1, res, type, urlObj;
    switch (url) {
      case "config":
        return {
          src: "/view/config.html",
          url: "config",
          modal: true
        };
      case "history":
        return {
          src: "/view/history.html",
          url: "history"
        };
      case "writehistory":
        return {
          src: "/view/writehistory.html",
          url: "writehistory"
        };
      case "bookmark":
        return {
          src: "/view/bookmark.html",
          url: "bookmark"
        };
      case "inputurl":
        return {
          src: "/view/inputurl.html",
          url: "inputurl"
        };
      case "bookmark_source_selector":
        return {
          src: "/view/bookmark_source_selector.html",
          url: "bookmark_source_selector",
          modal: true
        };
    }
    if (res = /^search:(.+)$/.exec(url)) {
      param = {
        query: res[1],
        scheme: (ref = (ref1 = obj.scheme) != null ? ref1 : app.config.get("thread_search_last_mode")) != null ? ref : "http"
      };
      return {
        src: `/view/search.html?${app.URL.buildQuery(param)}`,
        url: url
      };
    }
    urlObj = new app.URL.URL(url);
    urlObj.convertFromPhone();
    url = urlObj.href;
    ({type} = urlObj.guessType());
    if (type === "board") {
      return {
        src: `/view/board.html?${app.URL.buildQuery({
          q: url
        })}`,
        url: url
      };
    }
    if (type === "thread") {
      return {
        src: `/view/thread.html?${app.URL.buildQuery({
          q: url
        })}`,
        url: url
      };
    }
    return null;
  };
  iframeSrcToUrl = function(src) {
    var res;
    if (res = /^\/view\/(\w+)\.html$/.exec(src)) {
      return res[1];
    }
    if (res = /^\/view\/search\.html(\?.+)$/.exec(src)) {
      return app.URL.parseQuery(res[1], true).get("query");
    }
    if (res = /^\/view\/(?:thread|board)\.html(\?.+)$/.exec(src)) {
      return app.URL.parseQuery(res[1], true).get("q");
    }
    return null;
  };
  $view = document.documentElement;
  new app.view.Index($view);
  (function() {
    // bookmark_idが未設定の場合、わざと無効な値を渡してneedReconfigureRootNodeId
    // をcallさせる。
    app.bookmark = new app.Bookmark(app.config.get("bookmark_id") || "dummy");
    app.bookmarkEntryList = app.bookmark.bel;
    app.bookmarkEntryList.needReconfigureRootNodeId.add(function() {
      app.message.send("open", {
        url: "bookmark_source_selector"
      });
    });
  })();
  app.bookmarkEntryList.ready.add(function() {
    $$.I("left_pane").src = "/view/sidemenu.html";
  });
  (async function() {
    document.title = ((await app.manifest)).name;
  })();
  app.message.on("notify", function({
      message: text,
      html,
      background_color = "#777"
    }) {
    var $div, $div2, func;
    $div = $__("div");
    $div.style.backgroundColor = background_color;
    $div2 = $__("div");
    if (html != null) {
      $div2.innerHTML = html;
    } else {
      $div2.textContent = text;
    }
    $div.addLast($div2, $__("div"));
    $div.on("click", func = async function({
        target,
        currentTarget: cTarget
      }) {
      var ani;
      if (!target.matches("a, div:last-child")) {
        return;
      }
      $div.off("click", func);
      ani = (await UI.Animate.fadeOut(cTarget));
      ani.on("finish", () => {
        cTarget.remove();
      });
    });
    $$.I("app_notice_container").addLast($div);
    UI.Animate.fadeIn($div);
  });
  (async function() {    //前回起動時のバージョンと違うバージョンだった場合、アップデート通知を送出
    var lastVersion, name, version;
    lastVersion = app.config.get("last_version");
    ({name, version} = (await app.manifest));
    if (lastVersion != null) {
      if (version !== lastVersion) {
        app.message.send("notify", {
          html: `${name} が ${lastVersion} から\n${version} にアップデートされました。\n <a href="https://readcrx-2.github.io/read.crx-2/changelog.html#v${version}" target="_blank">更新履歴</a>`,
          background_color: "green"
        });
      } else {
        return;
      }
    }
    app.config.set("last_version", version);
  })();
  //更新通知
  browser.runtime.onUpdateAvailable.addListener(async function({
      version: newVer
    }) {
    var name, oldVer;
    ({
      name,
      version: oldVer
    } = (await app.manifest));
    if (newVer === oldVer) {
      return;
    }
    app.message.send("notify", {
      message: `${name} の ${newVer} が利用可能です`,
      background_color: "green"
    });
  });
  // ウィンドウサイズ関連処理
  adjustWindowSize = new app.Callbacks();
  (function() {
    var resizeTo, saveWindowSize, startAutoSave;
    resizeTo = async function(width, height) {
      var win;
      win = (await browser.windows.getCurrent());
      await browser.windows.update(win.id, {width, height});
    };
    saveWindowSize = async function() {
      var win;
      win = (await browser.windows.getCurrent());
      app.config.set("window_width", win.width.toString(10));
      app.config.set("window_height", win.height.toString(10));
    };
    startAutoSave = function() {
      var isResized;
      isResized = false;
      saveWindowSize();
      window.on("resize", function() {
        isResized = true;
      });
      setInterval(function() {
        if (!isResized) {
          return;
        }
        isResized = false;
        saveWindowSize();
      }, 1000);
    };
    (async function() {      // 起動時にウィンドウサイズが極端に小さかった場合、前回終了時のサイズに復元
      var win;
      win = (await browser.windows.getCurrent({
        populate: true
      }));
      if (win.tabs.length === 1 && win.width < 300 || win.height < 300) {
        await resizeTo(+app.config.get("window_width"), +app.config.get("window_height"));
        await app.defer();
      }
      adjustWindowSize.call();
    })();
    adjustWindowSize.add(startAutoSave);
  })();
  //タブ・ペインセットアップ
  $$.I("body").addClass(app.config.get("layout"));
  tabA = new UI.Tab($$.I("tab_a"));
  app.DOMData.set($$.I("tab_a"), "tab", tabA);
  UI.Tab.tabA = tabA;
  tabB = new UI.Tab($$.I("tab_b"));
  app.DOMData.set($$.I("tab_b"), "tab", tabB);
  UI.Tab.tabB = tabB;
  ref = $$(".tab .tab_tabbar");
  for (i = 0, len = ref.length; i < len; i++) {
    dom = ref[i];
    new UI.Sortable(dom, {
      exclude: "img"
    });
  }
  adjustWindowSize.add(app.view_setup_resizer);
  $view.on("tab_urlupdated", function({target}) {
    if (target.tagName !== "IFRAME") {
      return;
    }
    target.dataset.url = iframeSrcToUrl(target.getAttr("src"));
  });
  app.message.on("config_updated", function({key, val}) {
    var $body, $tabA, $tabB, iframe, j, k, len1, len2, ref1, ref2, tmp, tmpURL;
    if (key !== "layout") {
      return;
    }
    $body = $$.I("body");
    $body.removeClass("pane-3", "pane-3h", "pane-2");
    $body.addClass(val);
    $tabA = $$.I("tab_a");
    $tabB = $$.I("tab_b");
    $tabA.style.width = "";
    $tabA.style.height = "";
    $tabB.style.width = "";
    $tabB.style.height = "";
    //タブ移動
    //2->3
    if (val === "pane-3" || val === "pane-3h") {
      ref1 = tabA.getAll();
      for (j = 0, len1 = ref1.length; j < len1; j++) {
        tmp = ref1[j];
        iframe = $$.$(`iframe[data-tabid="${tmp.tabId}"]`);
        tmpURL = iframe.dataset.url;
        if (!/^https?:/.test(tmpURL)) {
          continue;
        }
        if ((new app.URL.URL(tmpURL)).guessType().type !== "thread") {
          continue;
        }
        app.message.send("open", {
          new_tab: true,
          lazy: true,
          url: tmpURL,
          title: tmp.title
        });
        tabA.remove(tmp.tabId);
      }
    }
    //3->2
    if (val === "pane-2") {
      ref2 = tabB.getAll();
      for (k = 0, len2 = ref2.length; k < len2; k++) {
        tmp = ref2[k];
        iframe = $$.$(`iframe[data-tabid="${tmp.tabId}"]`);
        tmpURL = iframe.dataset.url;
        app.message.send("open", {
          new_tab: true,
          lazy: true,
          url: tmpURL,
          title: tmp.title
        });
        tabB.remove(tmp.tabId);
      }
    }
  });
  app.bookmarkEntryList.ready.add(async function() {
    var isRestored, j, len1, tab, tabState;
    // タブ復元
    // TODO: 少ししたら消す
    if (localStorage.tab_state != null) {
      tabState = JSON.parse(localStorage.tab_state);
      delete localStorage.tab_state;
    } else {
      tabState = (await app.LocalStorage.get("tab_state", true));
    }
    if (tabState != null) {
      for (j = 0, len1 = tabState.length; j < len1; j++) {
        tab = tabState[j];
        isRestored = true;
        app.message.send("open", {
          url: tab.url,
          title: tab.title,
          lazy: !tab.selected,
          locked: tab.locked,
          new_tab: true,
          restore: true
        });
      }
    }
    //もし、タブが一つも復元されなかったらブックマークタブを開く
    if (!isRestored) {
      app.message.send("open", {
        url: "bookmark"
      });
    }
  });
  // コンテキストメニューの作成
  app.ContextMenus.createAll();
  window.on("beforeunload", async function() {
    var id;
    // コンテキストメニューの削除
    app.ContextMenus.removeAll();
    // 既読情報の処理
    window.emit(new Event("beforezombie"));
    // zombieの起動
    if ("chrome" === "chrome") {
      ({id} = (await browser.windows.create({
        top: 0,
        left: 0,
        height: 100,
        width: 250,
        url: "/zombie.html",
        type: "popup",
        focused: false
      })));
      await browser.windows.update(id, {
        state: "minimized"
      });
    } else if ("chrome" === "firefox") {
      await browser.windows.create({
        url: "/zombie.html",
        type: "popup",
        state: "minimized"
      });
    }
  });
  window.on("unload", function() {
    // 終了通知の送信
    browser.runtime.sendMessage({
      type: "rcrx_exit"
    });
  });
  // NGデータの有効期限設定
  app.NG.execExpire();
  //openメッセージ受信部
  app.message.on("open", function({url, title, background, lazy, locked, restore, scheme, new_tab, param_res_num = null, written_res_num = null}) {
    var $iframe, $iframeEle, $li, $tab, iframeInfo, selectedTab, tabId, target;
    iframeInfo = urlToIframeInfo(url, {scheme});
    if (!iframeInfo) {
      return;
    }
    if (iframeInfo.modal) {
      if ($view.$(`iframe[src="${iframeInfo.src}"]`) == null) {
        $iframeEle = $__("iframe").addClass("fade");
        $iframeEle.src = iframeInfo.src;
        $iframeEle.dataset.url = iframeInfo.url;
        $iframeEle.dataset.title = title || iframeInfo.url;
        $$.I("modal").addLast($iframeEle);
        UI.Animate.fadeIn($iframeEle);
      }
    } else {
      $li = $view.$(`.tab_tabbar > li[data-tabsrc="${iframeInfo.src}"]`);
      if (app.config.isOn("enable_link_with_res_number") && /^https?:/.test(url)) {
        if (param_res_num == null) {
          param_res_num = app.URL.getResNumber(url);
        }
      }
      if ($li != null) {
        app.DOMData.get($li.closest(".tab"), "tab").update($li.dataset.tabid, {
          selected: true
        });
        if (url !== "bookmark") { //ブックマーク更新は時間がかかるので例外扱い
          $iframe = $view.$(`iframe[data-tabid="${$li.dataset.tabid}"]`);
          $iframe.contentWindow.postMessage({
            type: "request_reload",
            written_res_num,
            param_res_num
          }, location.origin);
        }
      } else {
        target = tabA;
        if (iframeInfo.src.slice(0, 17) === "/view/thread.html" && !$$.I("body").hasClass("pane-2")) {
          target = tabB;
        }
        if (new_tab || !(selectedTab = target.getSelected())) {
          tabId = target.add(iframeInfo.src, {
            title: title || iframeInfo.url,
            selected: !(background || lazy),
            locked,
            lazy,
            restore
          });
        } else {
          tabId = selectedTab.tabId;
          target.update(tabId, {
            url: iframeInfo.src,
            title: title || iframeInfo.url,
            selected: true,
            locked
          });
        }
        $tab = $view.$(`iframe[data-tabid="${tabId}"]`);
        $tab.dataset.url = iframeInfo.url;
        $tab.dataset.writtenResNum = written_res_num != null ? written_res_num : "";
        $tab.dataset.paramResNum = param_res_num != null ? param_res_num : "";
      }
    }
  });
  //openリクエストの監視
  browser.runtime.onMessage.addListener(function({type, query}) {
    if (type !== "open") {
      return;
    }
    app.message.send("open", {
      url: query,
      new_tab: true
    });
  });
  //書き込み完了メッセージの監視
  browser.runtime.onMessage.addListener(function({type, kind, url, mes, name, mail, title, thread_url}) {
    var iframe;
    if (type !== "written" && type !== "written?") {
      return;
    }
    iframe = document.$(`iframe[data-url="${url}"]`);
    if (iframe) {
      iframe.contentWindow.postMessage({
        type: "request_reload",
        force_update: true,
        kind,
        mes,
        name,
        mail,
        title,
        thread_url
      }, location.origin);
    }
  });
  //書き込みウィンドウ場所保存メッセージの監視
  browser.runtime.onMessage.addListener(function({type, x, y}) {
    if (type !== "write_position") {
      return;
    }
    app.config.set("write_window_x", "" + x);
    app.config.set("write_window_y", "" + y);
  });
  // リクエスト・ヘッダーの監視
  browser.webRequest.onBeforeSendHeaders.addListener(function({method, url, requestHeaders}) {
    var replaceHeader;
    replaceHeader = function(name, value) {
      var header, j, len1;
      for (j = 0, len1 = requestHeaders.length; j < len1; j++) {
        header = requestHeaders[j];
        if (header.name.toLowerCase() === name) {
          header.value = value;
          break;
        }
      }
    };
    // 短縮URLの展開でのt.coに対する例外
    if (method === "HEAD" && app.URL.getDomain(url) === "t.co") {
      replaceHeader("user-agent", "");
    }
    return {requestHeaders};
  }, {
    urls: ["*://t.co/*"],
    types: ["xmlhttprequest"]
  }, ["blocking", "requestHeaders"]);
  //viewからのメッセージを監視
  window.on("message", async function({
      origin,
      source,
      data: message
    }) {
    var $iframe, ani, title, type;
    if (origin !== location.origin) {
      return;
    }
    $iframe = source != null ? source.frameElement : void 0;
    if ($iframe == null) {
      return;
    }
    ({type, title} = message);
    switch (type) {
      //タブ内コンテンツがtitle_updatedを送出した場合、タブのタイトルを更新
      case "title_updated":
        if ($iframe.hasClass("tab_content")) {
          app.DOMData.get($iframe.closest(".tab"), "tab").update($iframe.dataset.tabid, {title});
        }
        break;
      // スレがover1000になったとき
      case "became_over1000":
        if ($iframe.hasClass("tab_content")) {
          $view.$(`li[data-tabid="${$iframe.dataset.tabid}"]`).addClass("over1000");
        }
        break;
      // スレがdat落ちになったとき
      case "became_expired":
        if ($iframe.hasClass("tab_content")) {
          $view.$(`li[data-tabid="${$iframe.dataset.tabid}"]`).addClass("expired");
        }
        break;
      //request_killmeの処理
      case "request_killme":
        //タブ内のviewが送ってきた場合
        if ($iframe.hasClass("tab_content")) {
          app.DOMData.get($iframe.closest(".tab"), "tab").remove($iframe.dataset.tabid);
        //モーダルのviewが送ってきた場合
        } else if ($iframe.matches("#modal > iframe")) {
          ani = (await UI.Animate.fadeOut($iframe));
          ani.on("finish", function() {
            $iframe.contentWindow.___e = new Event("view_unload", {
              bubbles: true
            });
            $iframe.contentWindow.emit($iframe.contentWindow.___e);
            $iframe.remove();
          });
        }
        break;
      //view_loadedの翻訳
      case "view_loaded":
        $iframe.emit(new Event("view_loaded"));
        break;
      //request_focusの翻訳
      case "request_focus":
        $iframe.emit(new CustomEvent("request_focus", {
          detail: message,
          bubbles: true
        }));
    }
  });
  onRemove = function({target}) {
    target = target.closest("iframe");
    if (target == null) {
      return;
    }
    target.contentWindow.___e = new Event("view_unload", {
      bubbles: true
    });
    // shortQuery.jsが読み込まれていないこともあるためdispatchEventで
    target.contentWindow.dispatchEvent(target.contentWindow.___e);
  };
  $view.on("tab_removed", onRemove);
  $view.on("tab_beforeurlupdate", onRemove);
  //tab_selected(event) -> tab_selected(postMessage) 翻訳処理
  $view.on("tab_selected", function({target}) {
    target = target.closest("iframe.tab_content");
    if (target == null) {
      return;
    }
    target.contentWindow.postMessage({
      type: "tab_selected"
    }, location.origin);
  });
  ref1 = $view.C("tab_tabbar");
  //タブコンテキストメニュー
  for (j = 0, len1 = ref1.length; j < len1; j++) {
    dom = ref1[j];
    dom.on("contextmenu", async function(e) {
      var $menu, $source, func, getLatestRestorableTabID, k, len2, ref2, ref3, sourceTabId, tab;
      e.preventDefault();
      $source = e.target.closest(".tab_tabbar, li");
      $menu = $$.I("template_tab_contextmenu").content.$(".tab_contextmenu").cloneNode(true);
      if ($source.tagName === "LI") {
        sourceTabId = $source.dataset.tabid;
      } else {
        ref2 = $menu.$$(":scope > :not(.restore)");
        for (k = 0, len2 = ref2.length; k < len2; k++) {
          dom = ref2[k];
          dom.remove();
        }
      }
      tab = app.DOMData.get($source.closest(".tab"), "tab");
      getLatestRestorableTabID = function() {
        var a, l, len3, list, ref3, tabURLList, tmpTab;
        tabURLList = (function() {
          var l, len3, ref3, results;
          ref3 = tab.getAll();
          results = [];
          for (l = 0, len3 = ref3.length; l < len3; l++) {
            a = ref3[l];
            results.push(a.url);
          }
          return results;
        })();
        list = tab.getRecentClosed();
        list.reverse();
        for (l = 0, len3 = list.length; l < len3; l++) {
          tmpTab = list[l];
          if (!(ref3 = tmpTab.url, indexOf.call(tabURLList, ref3) >= 0)) {
            return tmpTab.tabId;
          }
        }
        return null;
      };
      if (!getLatestRestorableTabID()) {
        $menu.C("restore")[0].remove();
      }
      if (tab.isLocked(sourceTabId)) {
        $menu.C("lock")[0].remove();
        $menu.C("close")[0].remove();
      } else {
        if ((ref3 = $menu.C("unlock")[0]) != null) {
          ref3.remove();
        }
      }
      if ($menu.child().length === 0) {
        return;
      }
      $menu.on("click", func = function({target}) {
        var l, m, ref4, ref5, tabid, tmp;
        if (target.tagName !== "LI") {
          return;
        }
        $menu.off("click", func);
        switch (false) {
          //閉じたタブを開く
          case !target.hasClass("restore"):
            if (tmp = getLatestRestorableTabID()) {
              tab.restoreClosed(tmp);
            }
            break;
          //再読み込み
          case !target.hasClass("reload"):
            $view.$(`iframe[data-tabid="${sourceTabId}"]`).contentWindow.postMessage({
              type: "request_reload"
            }, location.origin);
            break;
          //タブを固定
          case !target.hasClass("lock"):
            tab.update(sourceTabId, {
              locked: true
            });
            break;
          //タブの固定を解除
          case !target.hasClass("unlock"):
            tab.update(sourceTabId, {
              locked: false
            });
            break;
          //タブを閉じる
          case !target.hasClass("close"):
            tab.remove(sourceTabId);
            break;
          //タブを全て閉じる
          case !target.hasClass("close_all"):
            ref4 = $source.parent().child();
            for (l = ref4.length - 1; l >= 0; l += -1) {
              dom = ref4[l];
              tabid = dom.dataset.tabid;
              if (!tab.isLocked(tabid)) {
                tab.remove(tabid);
              }
            }
            break;
          //他のタブを全て閉じる
          case !target.hasClass("close_all_other"):
            ref5 = $source.parent().child();
            for (m = ref5.length - 1; m >= 0; m += -1) {
              dom = ref5[m];
              if (!(dom !== $source)) {
                continue;
              }
              tabid = dom.dataset.tabid;
              if (!tab.isLocked(tabid)) {
                tab.remove(tabid);
              }
            }
            break;
          //右側のタブを全て閉じる
          case !target.hasClass("close_right"):
            while (dom = $source.next()) {
              tabid = dom.dataset.tabid;
              if (!tab.isLocked(tabid)) {
                tab.remove(tabid);
              }
            }
        }
        $menu.remove();
      });
      await app.defer();
      document.body.addLast($menu);
      UI.ContextMenu($menu, e.clientX, e.clientY);
    });
  }
  ref2 = $view.C("tab_tabbar");
  // タブダブルクリックで更新
  for (k = 0, len2 = ref2.length; k < len2; k++) {
    dom = ref2[k];
    dom.on("dblclick", function({target}) {
      var $source, sourceTabId;
      if (target.matches("li")) {
        $source = target;
      } else if (target.closest(".tab_tabbar > li") != null) {
        $source = target.closest(".tab_tabbar > li");
      }
      if ($source == null) {
        return;
      }
      sourceTabId = $source.dataset.tabid;
      $view.$(`iframe[data-tabid="${sourceTabId}"]`).contentWindow.postMessage({
        type: "request_reload"
      }, location.origin);
    });
  }
};
