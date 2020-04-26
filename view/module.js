(function() {
  var i, len, module, modules;
  if (frameElement) {
    modules = ["BoardTitleSolver", "History", "WriteHistory", "Thread", "bookmark", "bookmarkEntryList", "config", "ContextMenus", "DOMData", "HTTP", "ImageReplaceDat", "module", "ReplaceStrTxt", "NG", "Notification", "ReadState", "URL", "util"];
    for (i = 0, len = modules.length; i < len; i++) {
      module = modules[i];
      app[module] = parent.app[module];
    }
    window.on("unload", function() {
      var app;
      document.body.removeChildren();
      app = null;
    });
  }
})();

if (app.view == null) {
  app.view = {};
}

/**
@namespace app.view
@class View
@constructor
@param {Element} element
*/
app.view.View = class View {
  constructor($element1) {
    this.$element = $element1;
    this._setupTheme();
    this._setupOpenInRcrx();
    return;
  }

  /**
  @method _changeTheme
  @private
  @param {String} themeId
  */
  _changeTheme(themeId) {
    // テーマ適用
    this.$element.removeClass("theme_default", "theme_dark", "theme_none");
    this.$element.addClass(`theme_${themeId}`);
  }

  /**
  @method _setScrollbarDesign
  @private
  @param {String} val
  */
  _setScrollbarDesign(val) {
    if (val === "on") {
      this.$element.addClass("default_scrollbar");
    } else {
      this.$element.removeClass("default_scrollbar");
    }
  }

  /**
  @method _setupTheme
  @private
  */
  _setupTheme() {
    // テーマ適用
    this._changeTheme(app.config.get("theme_id"));
    this._setScrollbarDesign(app.config.get("default_scrollbar"));
    // テーマ更新反映
    app.message.on("config_updated", ({key, val}) => {
      switch (key) {
        case "theme_id":
          this._changeTheme(val);
          break;
        case "default_scrollbar":
          this._setScrollbarDesign(val);
      }
    });
  }

  /**
  @method _insertUserCSS
  @private
  */
  _insertUserCSS() {
    var style;
    style = $__("style");
    style.id = "user_css";
    style.textContent = app.config.get("user_css");
    document.head.addLast(style);
  }

  /**
  @method _setupOpenInRcrx
  @private
  */
  _setupOpenInRcrx() {
    // .open_in_rcrxリンクの処理
    this.$element.on("mousedown", function(e) {
      var background, newTab, newWindow, paramResFlg, paramResNum, target, title, url, writtenResNum;
      target = e.target.closest(".open_in_rcrx");
      if (target == null) {
        return;
      }
      e.preventDefault();
      if (e.button === 2) {
        return;
      }
      url = target.dataset.href || target.href;
      title = target.dataset.title || target.textContent;
      writtenResNum = target.getAttr("ignore-res-number") === "on" ? null : target.dataset.writtenResNum;
      paramResFlg = (app.config.isOn("enable_link_with_res_number") && target.getAttr("toggle-param-res-num") !== "on") || (!app.config.isOn("enable_link_with_res_number") && target.getAttr("toggle-param-res-num") === "on");
      paramResNum = paramResFlg ? target.dataset.paramResNum : null;
      target.removeAttr("toggle-param-res-num");
      target.removeAttr("ignore-res-number");
      ({newTab, newWindow, background} = app.util.getHowToOpen(e));
      newTab || (newTab = app.config.isOn("always_new_tab") || newWindow);
      app.message.send("open", {
        url,
        new_tab: newTab,
        background,
        title,
        written_res_num: writtenResNum,
        param_res_num: paramResNum
      });
    });
    this.$element.on("click", function(e) {
      if (e.target.hasClass("open_in_rcrx")) {
        e.preventDefault();
      }
    });
  }

};

app.view.IframeView = (function() {
  /**
  @namespace app.view
  @class IframeView
  @extends app.view.View
  @constructor
  @param {Element} element
  */
  class IframeView extends app.view.View {
    constructor(element) {
      super(element);
      this._setupKeyboard();
      this._setupCommandBox();
      this._numericInput = "";
      return;
    }

    /**
    @method close
    */
    close() {
      parent.postMessage({
        type: "request_killme"
      }, location.origin);
    }

    _write(param = {}) {
      var height, htmlname, windowX, windowY;
      if (this.$element.hasClass("view_thread")) {
        htmlname = "submit_res";
        height = "300";
      } else if (this.$element.hasClass("view_board")) {
        htmlname = "submit_thread";
        height = "400";
      }
      param.title = document.title;
      param.url = this.$element.dataset.url;
      windowX = app.config.get("write_window_x");
      windowY = app.config.get("write_window_y");
      open(`/write/${htmlname}.html?${app.URL.buildQuery(param)}`, void 0, `width=600,height=${height},left=${windowX},top=${windowY}`);
    }

    /**
    @method execCommand
    @param {String} command
    @param {Number} [repeatCount]
    */
    execCommand(command, repeatCount = 1) {
      var $a, i, j, len, len1, m, message, num, ref, ref1, ref2, ref3, ref4, ref5, ref6, ref7, ref8, ref9;
      // 数値コマンド
      if (/^\d+$/.test(command)) {
        if ((ref = app.DOMData.get(this.$element, "selectableItemList")) != null) {
          ref.select(+command);
        }
      }
      if (this.$element.hasClass("view_thread")) {
        // 返信レス
        if ((m = /^w(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)$/.exec(command))) {
          message = "";
          ref1 = m[1].split(",");
          for (i = 0, len = ref1.length; i < len; i++) {
            num = ref1[i];
            message += `>>${num}\n`;
          }
          this._write({message});
        } else if ((m = /^w-(\d+(?:,\d+)*)$/.exec(command))) {
          message = "";
          ref2 = m[1].split(",");
          for (j = 0, len1 = ref2.length; j < len1; j++) {
            num = ref2[j];
            message += `>>${num}\n${this.$element.C("content")[0].child()[num - 1].$(".message").textContent.replace(/^/gm, '>')}\n`;
          }
          this._write({message});
        }
      }
      if (this.$element.hasClass("view_thread") || this.$element.hasClass("view_board")) {
        if (command === "w") {
          this._write();
        }
      }
      switch (command) {
        case "up":
          if ((ref3 = app.DOMData.get(this.$element, "selectableItemList")) != null) {
            ref3.selectPrev(repeatCount);
          }
          break;
        case "down":
          if ((ref4 = app.DOMData.get(this.$element, "selectableItemList")) != null) {
            ref4.selectNext(repeatCount);
          }
          break;
        case "left":
          if (this.$element.hasClass("view_sidemenu")) {
            $a = this.$element.$("li > a.selected");
            if ($a != null) {
              app.DOMData.get(this.$element, "accordion").select($a.closest("ul").prev());
            }
          }
          break;
        case "right":
          if (this.$element.hasClass("view_sidemenu")) {
            $a = this.$element.$("h3.selected + ul a");
            if ($a != null) {
              app.DOMData.get(this.$element, "accordion").select($a);
            }
          }
          break;
        case "clearSelect":
          if ((ref5 = app.DOMData.get(this.$element, "selectableItemList")) != null) {
            ref5.clearSelect();
          }
          break;
        case "focusUpFrame":
        case "focusDownFrame":
        case "focusLeftFrame":
        case "focusRightFrame":
          app.message.send("requestFocusMove", {command, repeatCount});
          break;
        case "r":
          this.$element.emit(new Event("request_reload"));
          break;
        case "q":
          this.close();
          break;
        case "openCommandBox":
          this._openCommandBox();
          break;
        case "enter":
          if ((ref6 = this.$element.C("selected")[0]) != null) {
            ref6.emit(new Event("mousedown", {
              bubbles: true
            }));
          }
          if ((ref7 = this.$element.C("selected")[0]) != null) {
            ref7.emit(new Event("mouseup", {
              bubbles: true
            }));
          }
          break;
        case "shift+enter":
          if ((ref8 = this.$element.C("selected")[0]) != null) {
            ref8.emit(new MouseEvent("mousedown", {
              shiftKey: true,
              bubbles: true
            }));
          }
          if ((ref9 = this.$element.C("selected")[0]) != null) {
            ref9.emit(new MouseEvent("mouseup", {
              shiftKey: true,
              bubbles: true
            }));
          }
          break;
        case "help":
          app.message.send("showKeyboardHelp");
      }
    }

    /**
    @method _setupCommandBox
    */
    _setupCommandBox() {
      var $input;
      $input = $__("input").addClass("command", "hidden");
      $input.on("keydown", ({key, target}) => {
        switch (key) {
          case "Enter":
            this.execCommand(target.value.replace(/\s/g, ""));
            this._closeCommandBox();
            break;
          case "Escape":
            this._closeCommandBox();
        }
      });
      this.$element.addLast($input);
    }

    /**
    @method _openCommandBox
    */
    _openCommandBox() {
      var $command;
      $command = this.$element.C("command")[0];
      app.DOMData.set($command, "lastActiveElement", document.activeElement);
      $command.removeClass("hidden");
      $command.focus();
    }

    /**
    @method _closeCommandBox
    */
    _closeCommandBox() {
      var $command, ref;
      $command = this.$element.C("command")[0];
      $command.value = "";
      $command.addClass("hidden");
      if ((ref = app.DOMData.get($command, "lastActiveElement")) != null) {
        ref.focus();
      }
    }

    /**
    @method _setupKeyboard
    @private
    */
    _setupKeyboard() {
      this.$element.on("keydown", (e) => {
        var command, ctrlKey, key, metaKey, ref, ref1, ref2, shiftKey, target;
        ({target, key, shiftKey, ctrlKey, metaKey} = e);
        // F5 or Ctrl+r or ⌘+r
        if (key === "F5" || ((ctrlKey || metaKey) && key === "r")) {
          e.preventDefault();
          command = "r";
        } else if (ctrlKey || metaKey) {
          return;
        }
        // Windows版ChromeでのBackSpace誤爆対策
        if (key === "Backspace" && !((ref = target.tagName) === "INPUT" || ref === "TEXTAREA")) {
          e.preventDefault();
        // Esc (空白の入力欄に入力された場合)
        } else if (key === "Escape" && ((ref1 = target.tagName) === "INPUT" || ref1 === "TEXTAREA") && target.value === "" && !target.hasClass("command")) {
          this.$element.C("content")[0].focus();
        // 入力欄内では発動しない系
        } else if (!((ref2 = target.tagName) === "INPUT" || ref2 === "TEXTAREA")) {
          if (this._keyboardCommandMap.has(key)) {
            command = this._keyboardCommandMap.get(key);
          } else if (key === "Enter") {
            if (shiftKey) {
              command = "shift+enter";
            } else {
              command = "enter";
            }
          } else if (key === ":") {
            e.preventDefault(); // コマンド入力欄に:が入力されるのを防ぐため
            command = "openCommandBox";
          } else if (key === "/") {
            e.preventDefault();
            this.$element.$(".searchbox, form.search > input[type=\"search\"]").focus();
          } else if (/^\d$/.test(key)) {
            // 数値
            this._numericInput += key;
          }
        }
        if (command != null) {
          this.execCommand(command, Math.max(1, +this._numericInput));
        }
        // 0-9かShift以外が押された場合は数値入力を終了
        if (!(/^\d$/.test(key) || key === "Shift")) {
          this._numericInput = "";
        }
      });
    }

  };

  IframeView.prototype._keyboardCommandMap = new Map([["Escape", "clearSelect"], ["h", "left"], ["H", "focusLeftFrame"], ["l", "right"], ["L", "focusRightFrame"], ["k", "up"], ["K", "focusUpFrame"], ["j", "down"], ["J", "focusDownFrame"], ["R", "r"], ["W", "q"], ["?", "help"]]);

  return IframeView;

}).call(this);

/**
@namespace app.view
@class PaneContentView
@extends app.view.IframeView
@constructor
@param {Element} element
*/
app.view.PaneContentView = class PaneContentView extends app.view.IframeView {
  constructor($element) {
    super($element);
    this._setupEventConverter();
    this._insertUserCSS();
    return;
  }

  /**
  @method _setupEventConverter
  @private
  */
  _setupEventConverter() {
    window.on("message", ({
        origin,
        data: message
      }) => {
      var ref, ref1, ref2, ref3, ref4, ref5, ref6, ref7;
      if (origin !== location.origin) {
        return;
      }
      // request_reload(postMessage) -> request_reload(event) 翻訳処理
      if (message.type === "request_reload") {
        this.$element.emit(new CustomEvent("request_reload", {
          detail: {
            force_update: message.force_update === true,
            kind: (ref = message.kind) != null ? ref : null,
            mes: (ref1 = message.mes) != null ? ref1 : null,
            name: (ref2 = message.name) != null ? ref2 : null,
            mail: (ref3 = message.mail) != null ? ref3 : null,
            title: (ref4 = message.title) != null ? ref4 : null,
            thread_url: (ref5 = message.thread_url) != null ? ref5 : null,
            written_res_num: (ref6 = message.written_res_num) != null ? ref6 : null,
            param_res_num: (ref7 = message.param_res_num) != null ? ref7 : null
          }
        }));
      // tab_selected(postMessage) -> tab_selected(event) 翻訳処理
      } else if (message.type === "tab_selected") {
        this.$element.emit(new Event("tab_selected", {
          bubbles: true
        }));
      }
    });
    // request_focus送出処理
    this.$element.on("mousedown", function({target}) {
      var ref;
      parent.postMessage({
        type: "request_focus",
        focus: !((ref = target.tagName) === "INPUT" || ref === "TEXTAREA")
      }, location.origin);
    });
    // view_loaded翻訳処理
    this.$element.on("view_loaded", function() {
      parent.postMessage({
        type: "view_loaded"
      }, location.origin);
    });
  }

};

/**
@namespace app.view
@class TabContentView
@extends app.view.PaneContentView
@constructor
@param {Element} element
*/
app.view.TabContentView = class TabContentView extends app.view.PaneContentView {
  constructor(element) {
    super(element);
    this._setupTitleReporter();
    this._setupReloadButton();
    this._setupNavButton();
    this._setupBookmarkButton();
    this._setupSortItemSelector();
    this._setupSchemeButton();
    this._setupAutoReload();
    this._setupRegExpButton();
    this._setupToolMenu();
    return;
  }

  /**
  @method _setupTitleReporter
  @private
  */
  _setupTitleReporter() {
    var sendTitleUpdated;
    sendTitleUpdated = () => {
      parent.postMessage({
        type: "title_updated",
        title: this.$element.T("title")[0].textContent
      }, location.origin);
    };
    if (this.$element.T("title")[0].textContent) {
      sendTitleUpdated();
    }
    new MutationObserver(function(recs) {
      sendTitleUpdated();
    }).observe(this.$element.T("title")[0], {
      childList: true
    });
  }

  /**
  @method _setupReloadButton
  @private
  */
  _setupReloadButton() {
    var ref;
    // View内リロードボタン
    if ((ref = this.$element.C("button_reload")[0]) != null) {
      ref.on("click", ({currentTarget}) => {
        if (!currentTarget.hasClass("disabled")) {
          this.$element.emit(new Event("request_reload"));
        }
      });
    }
  }

  /**
  @method _setupNavButton
  @private
  */
  _setupNavButton() {
    var dom, i, len, ref;
    // 戻る/進むボタン管理
    parent.postMessage({
      type: "requestTabHistory"
    }, location.origin);
    window.on("message", ({
        origin,
        data: {
          type,
          history: {current, stack} = {}
        }
      }) => {
      if (!(origin === location.origin && type === "responseTabHistory")) {
        return;
      }
      if (current > 0) {
        this.$element.C("button_back")[0].removeClass("disabled");
      }
      if (current < stack.length - 1) {
        this.$element.C("button_forward")[0].removeClass("disabled");
      }
      if (stack.length === 1 && app.config.isOn("always_new_tab")) {
        this.$element.C("button_back")[0].remove();
        this.$element.C("button_forward")[0].remove();
      }
    });
    ref = this.$element.$$(".button_back, .button_forward");
    for (i = 0, len = ref.length; i < len; i++) {
      dom = ref[i];
      dom.on("mousedown", function(e) {
        var background, newTab, newWindow, tmp;
        if (e.button !== 2) {
          ({newTab, newWindow, background} = app.util.getHowToOpen(e));
          newTab || (newTab = newWindow);
          if (this.hasClass("disabled")) {
            return;
          }
          tmp = this.hasClass("button_back") ? "Back" : "Forward";
          parent.postMessage({
            type: `requestTab${tmp}`,
            newTab,
            background
          }, location.origin);
        }
      });
    }
  }

  /**
  @method _setupBookmarkButton
  @private
  */
  _setupBookmarkButton() {
    var $button, url;
    $button = this.$element.C("button_bookmark")[0];
    if (!$button) {
      return;
    }
    ({url} = this.$element.dataset);
    if (/^https?:\/\/\w/.test(url)) {
      if (app.bookmark.get(url)) {
        $button.addClass("bookmarked");
      } else {
        $button.removeClass("bookmarked");
      }
      app.message.on("bookmark_updated", function({type, bookmark}) {
        if (bookmark.url === url) {
          if (type === "added") {
            $button.addClass("bookmarked");
          } else if (type === "removed") {
            $button.removeClass("bookmarked");
          }
        }
      });
      $button.on("click", () => {
        var resCount, title;
        if (app.bookmark.get(url)) {
          app.bookmark.remove(url);
        } else {
          title = document.title || url;
          if (this.$element.hasClass("view_thread")) {
            resCount = this.$element.C("content")[0].child().length;
          }
          if ((resCount != null) && resCount > 0) {
            app.bookmark.add(url, title, resCount);
          } else {
            app.bookmark.add(url, title);
          }
        }
      });
    } else {
      $button.remove();
    }
  }

  /**
  @method _setupSortItemSelector
  @private
  */
  _setupSortItemSelector() {
    var $selector, $table;
    $table = this.$element.C("table_sort")[0];
    $selector = this.$element.C("sort_item_selector")[0];
    if ($table != null) {
      $table.on("table_sort_updated", function({detail}) {
        var dom, i, len, ref;
        ref = $selector.T("option");
        for (i = 0, len = ref.length; i < len; i++) {
          dom = ref[i];
          dom.selected = false;
          if (String(detail.sort_attribute || detail.sort_index) === dom.dataset.sortIndex) {
            dom.selected = true;
          }
        }
      });
    }
    if ($selector != null) {
      $selector.on("change", function() {
        var $selected, config, val;
        $selected = this.child()[this.selectedIndex];
        config = {};
        config.sortOrder = $selected.dataset.sortOrder || "desc";
        val = $selected.dataset.sortIndex;
        if (/^\d+$/.test(val)) {
          config.sortIndex = +val;
        } else {
          config.sortAttribute = val;
        }
        app.DOMData.get($table, "tableSorter").update(config);
      });
    }
  }

  /**
  @method _setupSchemeButton
  @private
  */
  _setupSchemeButton() {
    var $button, isViewSearch, protocol, ref, url, urlObj;
    $button = this.$element.C("button_scheme")[0];
    if (!$button) {
      return;
    }
    ({url} = this.$element.dataset);
    if (!(url.startsWith("search:") || /^https?:/.test(url))) {
      $button.remove();
      return;
    }
    isViewSearch = url.startsWith("search:");
    if (isViewSearch) {
      protocol = (ref = this.$element.getAttr("scheme") + ":") != null ? ref : "http:";
    } else {
      urlObj = new app.URL.URL(url);
      ({protocol} = urlObj);
    }
    if (protocol === "https:") {
      $button.addClass("https");
    } else {
      $button.removeClass("https");
    }
    $button.on("click", function() {
      var obj;
      obj = {
        new_tab: app.config.isOn("button_change_scheme_newtab")
      };
      if (isViewSearch) {
        obj.url = url;
        obj.scheme = protocol === "http:" ? "https" : "http";
      } else {
        obj.url = urlObj.createProtocolToggled().href;
      }
      app.message.send("open", obj);
    });
  }

  /**
  @method _setupAutoReloadPauseButton
  @private
  */
  _setupAutoReload() {
    var $button, autoLoad, autoLoadInterval, cfgName, minSeconds;
    $button = this.$element.C("button_pause")[0];
    if (!(this.$element.hasClass("view_thread") || this.$element.hasClass("view_board") || this.$element.hasClass("view_bookmark"))) {
      if ($button) {
        $button.remove();
      }
      return;
    }
    switch (false) {
      case !this.$element.hasClass("view_thread"):
        cfgName = "";
        minSeconds = 5000;
        break;
      case !this.$element.hasClass("view_board"):
        cfgName = "_board";
        minSeconds = 20000;
        break;
      case !this.$element.hasClass("view_bookmark"):
        cfgName = "_bookmark";
        minSeconds = 20000;
    }
    autoLoad = () => {
      var second;
      second = parseInt(app.config.get(`auto_load_second${cfgName}`));
      if (second >= minSeconds) {
        this.$element.addClass("autoload");
        $button.removeClass("hidden");
        if (this.$element.hasClass("view_bookmark")) {
          return setInterval(() => {
            this.$element.emit(new CustomEvent("request_reload", {
              detail: true
            }));
          }, second);
        } else {
          return setInterval(() => {
            var url;
            ({url} = this.$element.dataset);
            if (app.config.isOn("auto_load_all") || parent.$$.$(`.tab_container > iframe[data-url="${url}"]`).hasClass("tab_selected")) {
              this.$element.emit(new Event("request_reload"));
            }
          }, second);
        }
      } else {
        this.$element.removeClass("autoload");
        $button.addClass("hidden");
      }
    };
    autoLoadInterval = autoLoad();
    app.message.on("config_updated", function({key}) {
      if (key === `auto_load_second${cfgName}`) {
        clearInterval(autoLoadInterval);
        autoLoadInterval = autoLoad();
      }
    });
    $button.on("click", () => {
      this.$element.toggleClass("autoload_pause");
      $button.toggleClass("pause");
      if ($button.hasClass("pause")) {
        clearInterval(autoLoadInterval);
      } else {
        autoLoadInterval = autoLoad();
      }
    });
    window.on("view_unload", function() {
      clearInterval(autoLoadInterval);
    });
  }

  /**
  @method _setupRegExpButton
  @private
  */
  _setupRegExpButton() {
    var $button;
    $button = this.$element.C("button_regexp")[0];
    if (!$button) {
      return;
    }
    if (!this.$element.hasClass("view_thread")) {
      if ($button) {
        $button.remove();
      }
      return;
    }
    if (this.$element.hasClass("search_regexp")) {
      $button.addClass("regexp");
    } else {
      $button.removeClass("regexp");
    }
    $button.on("click", () => {
      $button.toggleClass("regexp");
      this.$element.emit(new Event("change_search_regexp"));
    });
  }

  /**
  @method _setupToolMenu
  @private
  */
  _setupToolMenu() {
    var ref, ref1, ref2, ref3, ref4, ref5;
    //メニューの表示/非表示制御
    if ((ref = this.$element.C("button_tool")[0]) != null) {
      ref.on("click", async({currentTarget}) => {
        var $ul;
        $ul = currentTarget.T("ul")[0];
        $ul.toggleClass("hidden");
        if (!$ul.hasClass("hidden")) {
          return;
        }
        await app.defer();
        this.$element.on("click", ({target}) => {
          if (!target.hasClass("button_tool")) {
            this.$element.$(".button_tool > ul").addClass("hidden");
          }
        }, {
          once: true
        });
        this.$element.on("contextmenu", ({target}) => {
          if (!target.hasClass("button_tool")) {
            this.$element.$(".button_tool > ul").addClass("hidden");
          }
        }, {
          once: true
        });
      });
    }
    window.on("blur", () => {
      var ref1;
      if ((ref1 = this.$element.$(".button_tool > ul")) != null) {
        ref1.addClass("hidden");
      }
    });
    (() => {      // ブラウザで直接開く
      var ref1, ref2, url;
      ({url} = this.$element.dataset);
      if (url === "bookmark") {
        if ("chrome" === "chrome") {
          url = `chrome://bookmarks/?id=${app.config.get("bookmark_id")}`;
        } else {
          if ((ref1 = this.$element.$(".button_link > a")) != null) {
            ref1.remove();
          }
        }
      } else if (url != null ? url.startsWith("search:") : void 0) {
        return;
      } else {
        url = app.safeHref(url);
      }
      if ((ref2 = this.$element.$(".button_link > a")) != null) {
        ref2.on("click", function(e) {
          e.preventDefault();
          parent.browser.tabs.create({
            url: url
          });
        });
      }
    })();
    // dat落ちを表示/非表示
    if ((ref1 = this.$element.C("button_toggle_dat")[0]) != null) {
      ref1.on("click", () => {
        var dom, i, len, ref2;
        ref2 = this.$element.C("expired");
        for (i = 0, len = ref2.length; i < len; i++) {
          dom = ref2[i];
          dom.toggleClass("hidden");
        }
      });
    }
    // 未読スレッドを全て開く
    if ((ref2 = this.$element.C("button_open_updated")[0]) != null) {
      ref2.on("click", () => {
        var dom, i, lazy, len, ref3, title, url;
        ref3 = this.$element.C("updated");
        for (i = 0, len = ref3.length; i < len; i++) {
          dom = ref3[i];
          ({
            href: url,
            title
          } = dom.dataset);
          title = app.util.decodeCharReference(title);
          lazy = app.config.isOn("open_all_unread_lazy");
          app.message.send("open", {
            url,
            title,
            new_tab: true,
            lazy
          });
        }
      });
    }
    // タイトルをコピー
    if ((ref3 = this.$element.C("button_copy_title")[0]) != null) {
      ref3.on("click", () => {
        app.clipboardWrite(document.title);
      });
    }
    // URLをコピー
    if ((ref4 = this.$element.C("button_copy_url")[0]) != null) {
      ref4.on("click", () => {
        app.clipboardWrite(this.$element.dataset.url);
      });
    }
    // タイトルとURLをコピー
    if ((ref5 = this.$element.C("button_copy_title_and_url")[0]) != null) {
      ref5.on("click", () => {
        app.clipboardWrite(document.title + " " + this.$element.dataset.url);
      });
    }
    return (() => {
      var ref10, ref6, ref7, ref8, ref9, url, urlStr;
      urlStr = this.$element.dataset.url;
      if (!/^https?:/.test(urlStr)) {
        return;
      }
      url = new app.URL.URL(urlStr);
      // 2ch.net/2ch.scに切り替え
      if ((ref6 = url.getTsld()) === "5ch.net" || ref6 === "2ch.sc") {
        if ((ref7 = this.$element.C("button_change_netsc")[0]) != null) {
          ref7.on("click", async() => {
            var msg;
            try {
              app.message.send("open", {
                url: ((await url.createNetScConverted())).href,
                new_tab: app.config.isOn("button_change_netsc_newtab")
              });
            } catch (error) {
              msg = "スレッド/板のURLが古いか新しいため、板一覧に5ch.netと2ch.scのペアが存在しません。\n板一覧が更新されるのを待つか、板一覧を更新してみてください。";
              new app.Notification("現在この機能は使用できません", msg, "", "invalid");
            }
          });
        }
      } else {
        if ((ref8 = this.$element.C("button_change_netsc")[0]) != null) {
          ref8.remove();
        }
      }
      //2ch.scでscの投稿だけ表示(スレ&レス)
      if (url.getTsld() === "2ch.sc") {
        if ((ref9 = this.$element.C("button_only_sc")[0]) != null) {
          ref9.on("click", () => {
            var dom, i, len, ref10;
            ref10 = this.$element.C("net");
            for (i = 0, len = ref10.length; i < len; i++) {
              dom = ref10[i];
              dom.toggleClass("hidden");
            }
          });
        }
      } else {
        if ((ref10 = this.$element.C("button_only_sc")[0]) != null) {
          ref10.remove();
        }
      }
    })();
  }

};
