var BookmarkIO, HistoryIO, SettingIO, _checkExcute, _clearExcute, _excuteFunction, _excuteProcess, _funcName, _procName;

SettingIO = (function() {
  class SettingIO {
    constructor({
        name: name1,
        importFunc: importFunc1,
        exportFunc: exportFunc1
      }) {
      this.name = name1;
      this.importFunc = importFunc1;
      this.exportFunc = exportFunc1;
      this.$status = $$.I(`${this.name}_status`);
      if (this.importFunc != null) {
        this.$fileSelectButton = $$.C(`${this.name}_file_show`)[0];
        this.$fileSelectButtonHidden = $$.C(`${this.name}_file_hide`)[0];
        this.$importButton = $$.C(`${this.name}_import_button`)[0];
        this.setupFileSelectButton();
        this.setupImportButton();
      }
      if (this.exportFunc != null) {
        this.$exportButton = $$.C(`${this.name}_export_button`)[0];
        this.setupExportButton();
      }
      return;
    }

    setupFileSelectButton() {
      this.$fileSelectButton.on("click", () => {
        if (!_checkExcute(this.name, "file_select")) {
          return;
        }
        this.$status.setClass("");
        this.$fileSelectButtonHidden.click();
        _clearExcute();
      });
      this.$fileSelectButtonHidden.on("change", (e) => {
        var file, reader;
        file = e.target.files;
        reader = new FileReader();
        reader.readAsText(file[0]);
        reader.onload = () => {
          this.importFile = reader.result;
          this.$status.addClass("select");
          this.$status.textContent = "ファイル選択完了";
        };
      });
    }

    setupImportButton() {
      this.$importButton.on("click", async() => {
        if (!_checkExcute(this.name, "import")) {
          return;
        }
        if (this.importFile !== "") {
          this.$status.setClass("loading");
          this.$status.textContent = "更新中";
          try {
            await this.importFunc(this.importFile);
            this.$status.addClass("done");
            this.$status.textContent = "インポート完了";
          } catch (error) {
            this.$status.addClass("fail");
            this.$status.textContent = "インポート失敗";
          }
        } else {
          this.$status.addClass("fail");
          this.$status.textContent = "ファイルを選択してください";
        }
        _clearExcute();
      });
    }

    setupExportButton() {
      this.$exportButton.on("click", () => {
        var $a, blob, url;
        if (!_checkExcute(this.name, "export")) {
          return;
        }
        blob = new Blob([this.exportFunc()], {
          type: "text/plain"
        });
        $a = $__("a").addClass("hidden");
        url = URL.createObjectURL(blob);
        $a.href = url;
        $a.download = `read.crx-2_${this.name}.json`;
        this.$exportButton.addAfter($a);
        $a.click();
        $a.remove();
        URL.revokeObjectURL(url);
        _clearExcute();
      });
    }

  };

  SettingIO.prototype.importFile = "";

  return SettingIO;

}).call(this);

HistoryIO = class HistoryIO extends SettingIO {
  constructor({
      name,
      countFunc: countFunc,
      importFunc,
      exportFunc,
      clearFunc: clearFunc,
      clearRangeFunc: clearRangeFunc,
      afterChangedFunc: afterChangedFunc
    }) {
    super({name, importFunc, exportFunc});
    this.countFunc = countFunc;
    this.clearFunc = clearFunc;
    this.clearRangeFunc = clearRangeFunc;
    this.afterChangedFunc = afterChangedFunc;
    this.name = name;
    this.importFunc = importFunc;
    this.exportFunc = exportFunc;
    this.$count = $$.I(`${this.name}_count`);
    this.$progress = $$.I(`${this.name}_progress`);
    this.$clearButton = $$.C(`${this.name}_clear`)[0];
    this.$clearRangeButton = $$.C(`${this.name}_range_clear`)[0];
    this.showCount();
    this.setupClearButton();
    this.setupClearRangeButton();
    return;
  }

  async showCount() {
    var count;
    count = (await this.countFunc());
    this.$count.textContent = `${count}件`;
  }

  setupClearButton() {
    this.$clearButton.on("click", async() => {
      var ref, result;
      if (!_checkExcute(this.name, "clear")) {
        return;
      }
      result = (await UI.Dialog("confirm", {
        message: "本当に削除しますか？"
      }));
      if (!result) {
        _clearExcute();
        return;
      }
      this.$status.textContent = ":削除中";
      try {
        await this.clearFunc();
        this.$status.textContent = ":削除完了";
        if ((ref = parent.$$.$(`iframe[src="/view/${this.name}.html"]`)) != null) {
          ref.contentDocument.C("view")[0].emit(new Event("request_reload"));
        }
      } catch (error) {
        this.$status.textContent = ":削除失敗";
      }
      this.showCount();
      this.afterChangedFunc();
      _clearExcute();
    });
  }

  setupClearRangeButton() {
    this.$clearRangeButton.on("click", async() => {
      var ref, result;
      if (!_checkExcute(this.name, "clear_range")) {
        return;
      }
      result = (await UI.Dialog("confirm", {
        message: "本当に削除しますか？"
      }));
      if (!result) {
        _clearExcute();
        return;
      }
      this.$status.textContent = ":範囲指定削除中";
      try {
        await this.clearRangeFunc(parseInt($$.C(`${this.name}_date_range`)[0].value));
        this.$status.textContent = ":範囲指定削除完了";
        if ((ref = parent.$$.$(`iframe[src="/view/${this.name}.html"]`)) != null) {
          ref.contentDocument.C("view")[0].emit(new Event("request_reload"));
        }
      } catch (error) {
        this.$status.textContent = ":範囲指定削除失敗";
      }
      this.showCount();
      this.afterChangedFunc();
      _clearExcute();
    });
  }

  setupImportButton() {
    this.$importButton.on("click", async() => {
      var count;
      if (!_checkExcute(this.name, "import")) {
        return;
      }
      if (this.importFile !== "") {
        this.$status.setClass("loading");
        this.$status.textContent = ":更新中";
        try {
          await this.importFunc(JSON.parse(this.importFile), this.$progress);
          count = (await this.countFunc());
          this.$status.setClass("done");
          this.$status.textContent = ":インポート完了";
        } catch (error) {
          this.$status.setClass("fail");
          this.$status.textContent = ":インポート失敗";
        }
        this.showCount();
        this.afterChangedFunc();
      } else {
        this.$status.addClass("fail");
        this.$status.textContent = ":ファイルを選択してください";
      }
      this.$progress.textContent = "";
      _clearExcute();
    });
  }

  setupExportButton() {
    this.$exportButton.on("click", async() => {
      var $a, blob, data, exportText, url;
      if (!_checkExcute(this.name, "export")) {
        return;
      }
      data = (await this.exportFunc());
      exportText = JSON.stringify(data);
      blob = new Blob([exportText], {
        type: "text/plain"
      });
      $a = $__("a").addClass("hidden");
      url = URL.createObjectURL(blob);
      $a.href = url;
      $a.download = `read.crx-2_${this.name}.json`;
      this.$exportButton.addAfter($a);
      $a.click();
      $a.remove();
      URL.revokeObjectURL(url);
      _clearExcute();
    });
  }

};

BookmarkIO = class BookmarkIO extends SettingIO {
  constructor({
      name,
      countFunc: countFunc,
      importFunc,
      exportFunc,
      clearFunc: clearFunc,
      clearExpiredFunc: clearExpiredFunc,
      afterChangedFunc: afterChangedFunc
    }) {
    super({name, importFunc, exportFunc});
    this.countFunc = countFunc;
    this.clearFunc = clearFunc;
    this.clearExpiredFunc = clearExpiredFunc;
    this.afterChangedFunc = afterChangedFunc;
    this.name = name;
    this.importFunc = importFunc;
    this.exportFunc = exportFunc;
    this.$count = $$.I(`${this.name}_count`);
    this.$progress = $$.I(`${this.name}_progress`);
    this.$clearButton = $$.C(`${this.name}_clear`)[0];
    this.$clearExpiredButton = $$.C(`${this.name}_expired_clear`)[0];
    this.showCount();
    this.setupClearButton();
    this.setupClearExpiredButton();
    return;
  }

  async showCount() {
    var count;
    count = (await this.countFunc());
    this.$count.textContent = `${count}件`;
  }

  setupClearButton() {
    this.$clearButton.on("click", async() => {
      var result;
      if (!_checkExcute(this.name, "clear")) {
        return;
      }
      result = (await UI.Dialog("confirm", {
        message: "本当に削除しますか？"
      }));
      if (!result) {
        _clearExcute();
        return;
      }
      this.$status.textContent = ":削除中";
      try {
        await this.clearFunc();
        this.$status.textContent = ":削除完了";
      } catch (error) {
        this.$status.textContent = ":削除失敗";
      }
      this.showCount();
      this.afterChangedFunc();
      _clearExcute();
    });
  }

  setupClearExpiredButton() {
    this.$clearExpiredButton.on("click", async() => {
      var result;
      if (!_checkExcute(this.name, "clear_expired")) {
        return;
      }
      result = (await UI.Dialog("confirm", {
        message: "本当に削除しますか？"
      }));
      if (!result) {
        _clearExcute();
        return;
      }
      this.$status.textContent = ":dat落ち削除中";
      try {
        await this.clearExpiredFunc();
        this.$status.textContent = ":dat落ち削除完了";
      } catch (error) {
        this.$status.textContent = ":dat落ち削除失敗";
      }
      this.showCount();
      this.afterChangedFunc();
      _clearExcute();
    });
  }

  setupImportButton() {
    this.$importButton.on("click", async() => {
      var count;
      if (!_checkExcute(this.name, "import")) {
        return;
      }
      if (this.importFile !== "") {
        this.$status.setClass("loading");
        this.$status.textContent = ":更新中";
        try {
          await this.importFunc(JSON.parse(this.importFile), this.$progress);
          count = (await this.countFunc());
          this.$status.setClass("done");
          this.$status.textContent = ":インポート完了";
        } catch (error) {
          this.$status.setClass("fail");
          this.$status.textContent = ":インポート失敗";
        }
        this.showCount();
        this.afterChangedFunc();
      } else {
        this.$status.addClass("fail");
        this.$status.textContent = ":ファイルを選択してください";
      }
      this.$progress.textContent = "";
      _clearExcute();
    });
  }

  setupExportButton() {
    this.$exportButton.on("click", async() => {
      var $a, blob, data, exportText, url;
      if (!_checkExcute(this.name, "export")) {
        return;
      }
      data = (await this.exportFunc());
      exportText = JSON.stringify(data);
      blob = new Blob([exportText], {
        type: "text/plain"
      });
      $a = $__("a").addClass("hidden");
      url = URL.createObjectURL(blob);
      $a.href = url;
      $a.download = `read.crx-2_${this.name}.json`;
      this.$exportButton.addAfter($a);
      $a.click();
      $a.remove();
      URL.revokeObjectURL(url);
      _clearExcute();
    });
  }

};

// 処理の排他制御用
_excuteProcess = null;

_excuteFunction = null;

_procName = {
  "history": "閲覧履歴",
  "writehistory": "書込履歴",
  "bookmark": "ブックマーク",
  "cache": "キャッシュ",
  "config": "設定"
};

_funcName = {
  "import": "インポート",
  "export": "エクスポート",
  "clear": "削除",
  "clear_range": "範囲指定削除",
  "clear_expired": "dat落ち削除",
  "file_select": "ファイル読み込み"
};

_checkExcute = function(procId, funcId) {
  var message;
  if (!_excuteProcess) {
    _excuteProcess = procId;
    _excuteFunction = funcId;
    return true;
  }
  message = null;
  if (_excuteProcess === procId) {
    if (_excuteFunction === funcId) {
      message = "既に実行中です。";
    } else {
      message = `${_funcName[_excuteFunction]}の実行中です。`;
    }
  } else {
    message = `${_procName[_excuteProcess]}の処理中です。`;
  }
  if (message) {
    new app.Notification("現在この機能は使用できません", message, "", "invalid");
  }
  return false;
};

_clearExcute = function() {
  _excuteProcess = null;
  _excuteFunction = null;
};

app.boot("/view/config.html", ["Cache", "BBSMenu"], function(Cache, BBSMenu) {
  var $dom, $tabbar, $tabs, $view, dom, formatBytes, i, j, k, l, len, len1, len2, len3, len4, len5, len6, len7, m, n, o, p, ref, ref1, ref2, ref3, ref4, ref5, ref6, ref7, ref8, resetBBSMenu, updateIndexedDBUsage, whenClose;
  $view = document.documentElement;
  new app.view.IframeView($view);
  // タブ
  $tabbar = $view.C("tabbar")[0];
  $tabs = $view.C("container")[0];
  $tabbar.on("click", function({target}) {
    if (target.tagName !== "LI") {
      target = target.closest("li");
    }
    if (target == null) {
      return;
    }
    if (target.hasClass("selected")) {
      return;
    }
    $tabbar.C("selected")[0].removeClass("selected");
    target.addClass("selected");
    $tabs.C("selected")[0].removeClass("selected");
    $tabs.$(`[name="${target.dataset.name}"]`).addClass("selected");
  });
  whenClose = function() {
    var changeFlag, dom;
    //NG設定
    dom = $view.$("textarea[name=\"ngwords\"]");
    if (dom.getAttr("changed") != null) {
      dom.removeAttr("changed");
      app.NG.set(dom.value);
    }
    //ImageReplaceDat設定
    dom = $view.$("textarea[name=\"image_replace_dat\"]");
    if (dom.getAttr("changed") != null) {
      dom.removeAttr("changed");
      app.ImageReplaceDat.set(dom.value);
    }
    //ReplaceStrTxt設定
    dom = $view.$("textarea[name=\"replace_str_txt\"]");
    if (dom.getAttr("changed") != null) {
      dom.removeAttr("changed");
      app.ReplaceStrTxt.set(dom.value);
    }
    //bbsmenu設定
    changeFlag = false;
    dom = $view.$("textarea[name=\"bbsmenu\"]");
    if (dom.getAttr("changed") != null) {
      dom.removeAttr("changed");
      app.config.set("bbsmenu", dom.value);
      changeFlag = true;
    }
    dom = $view.$("textarea[name=\"bbsmenu_option\"]");
    if (dom.getAttr("changed") != null) {
      dom.removeAttr("changed");
      app.config.set("bbsmenu_option", dom.value);
      changeFlag = true;
    }
    if (changeFlag) {
      $view.C("bbsmenu_reload")[0].click();
    }
  };
  //閉じるボタン
  $view.C("button_close")[0].on("click", function() {
    if (frameElement) {
      parent.postMessage({
        type: "request_killme"
      }, location.origin);
    }
    whenClose();
  });
  window.on("beforeunload", function() {
    whenClose();
  });
  ref = $view.C("open_in_rcrx");
  //掲示板を開いたときに閉じる
  for (i = 0, len = ref.length; i < len; i++) {
    dom = ref[i];
    dom.on("click", function() {
      $view.C("button_close")[0].click();
    });
  }
  ref1 = $view.$$("input.direct[type=\"text\"], textarea.direct");
  //汎用設定項目
  for (j = 0, len1 = ref1.length; j < len1; j++) {
    dom = ref1[j];
    dom.value = app.config.get(dom.name) || "";
    dom.on("input", function() {
      app.config.set(this.name, this.value);
      this.setAttr("changed", "true");
    });
  }
  ref2 = $view.$$("input.direct[type=\"number\"]");
  for (k = 0, len2 = ref2.length; k < len2; k++) {
    dom = ref2[k];
    dom.value = app.config.get(dom.name) || "0";
    dom.on("input", function() {
      app.config.set(this.name, Number.isNaN(this.valueAsNumber) ? "0" : this.value);
    });
  }
  ref3 = $view.$$("input.direct[type=\"checkbox\"]");
  for (l = 0, len3 = ref3.length; l < len3; l++) {
    dom = ref3[l];
    dom.checked = app.config.get(dom.name) === "on";
    dom.on("change", function() {
      app.config.set(this.name, this.checked ? "on" : "off");
    });
  }
  ref4 = $view.$$("input.direct[type=\"radio\"]");
  for (m = 0, len4 = ref4.length; m < len4; m++) {
    dom = ref4[m];
    if (dom.value === app.config.get(dom.name)) {
      dom.checked = true;
    }
    dom.on("change", function() {
      var val;
      val = $view.$(`input[name="${this.name}"]:checked`).value;
      app.config.set(this.name, val);
    });
  }
  ref5 = $view.$$("input.direct[type=\"range\"]");
  for (n = 0, len5 = ref5.length; n < len5; n++) {
    dom = ref5[n];
    dom.value = app.config.get(dom.name) || "0";
    $$.I(`${dom.name}_text`).textContent = dom.value;
    dom.on("input", function() {
      $$.I(`${this.name}_text`).textContent = this.value;
      app.config.set(this.name, this.value);
    });
  }
  ref6 = $view.$$("select.direct");
  for (o = 0, len6 = ref6.length; o < len6; o++) {
    dom = ref6[o];
    dom.value = app.config.get(dom.name) || "";
    dom.on("change", function() {
      app.config.set(this.name, this.value);
    });
  }
  (async function() {    //バージョン情報表示
    var name, version;
    ({name, version} = (await app.manifest));
    $view.C("version_text")[0].textContent = `${name} v${version} + ${navigator.userAgent}`;
  })();
  $view.C("version_copy")[0].on("click", function() {
    app.clipboardWrite($$.C("version_text")[0].textContent);
  });
  $view.C("keyboard_help")[0].on("click", function(e) {
    e.preventDefault();
    app.message.send("showKeyboardHelp");
  });
  //板覧更新ボタン
  $view.C("bbsmenu_reload")[0].on("click", async function({
      currentTarget: $button
    }) {
    var $status;
    $status = $$.I("bbsmenu_reload_status");
    $button.disabled = true;
    $status.setClass("loading");
    $status.textContent = "更新中";
    dom = $view.$("textarea[name=\"bbsmenu\"]");
    dom.removeAttr("changed");
    app.config.set("bbsmenu", dom.value);
    dom = $view.$("textarea[name=\"bbsmenu_option\"]");
    dom.removeAttr("changed");
    app.config.set("bbsmenu_option", dom.value);
    try {
      await BBSMenu.get(true);
      $status.setClass("done");
      $status.textContent = "更新完了";
    } catch (error) {
      $status.setClass("fail");
      $status.textContent = "更新失敗";
    }
    $button.disabled = false;
  });
  //履歴
  new HistoryIO({
    name: "history",
    countFunc: function() {
      return app.History.count();
    },
    importFunc: async function({
        history,
        read_state: readState,
        historyVersion = 1,
        readstateVersion = 1
      }, $progress) {
      var _rs, count, hs, len7, len8, p, q, rs, total;
      total = history.length + readState.length;
      count = 0;
      for (p = 0, len7 = history.length; p < len7; p++) {
        hs = history[p];
        if (historyVersion === 1) {
          hs.boardTitle = "";
        }
        await app.History.add(hs.url, hs.title, hs.date, hs.boardTitle);
        $progress.textContent = `:${Math.floor((count++ / total) * 100)}%`;
      }
      for (q = 0, len8 = readState.length; q < len8; q++) {
        rs = readState[q];
        if (readstateVersion === 1) {
          rs.date = null;
        }
        _rs = (await app.ReadState.get(rs.url));
        if (app.util.isNewerReadState(_rs, rs)) {
          await app.ReadState.set(rs);
        }
        $progress.textContent = `:${Math.floor((count++ / total) * 100)}%`;
      }
    },
    exportFunc: async function() {
      var history, readState;
      [readState, history] = (await Promise.all([app.ReadState.getAll(), app.History.getAll()]));
      return {
        "read_state": readState,
        "history": history,
        "historyVersion": app.History.DB_VERSION,
        "readstateVersion": app.ReadState.DB_VERSION
      };
    },
    clearFunc: function() {
      return Promise.all([app.History.clear(), app.ReadState.clear()]);
    },
    clearRangeFunc: function(day) {
      return app.History.clearRange(day);
    },
    afterChangedFunc: function() {
      updateIndexedDBUsage();
    }
  });
  new HistoryIO({
    name: "writehistory",
    countFunc: function() {
      return app.WriteHistory.count();
    },
    importFunc: async function({writehistory = null, dbVersion = 1}, $progress) {
      var count, date, len7, p, total, unixTime201710, whis;
      if (!writehistory) {
        return Promise.resolve();
      }
      total = writehistory.length;
      count = 0;
      unixTime201710 = 1506783600; // 2017/10/01 0:00:00
      for (p = 0, len7 = writehistory.length; p < len7; p++) {
        whis = writehistory[p];
        whis.inputName = whis.input_name;
        whis.inputMail = whis.input_mail;
        if (dbVersion < 2) {
          if (+whis.date <= unixTime201710 && whis.res > 1) {
            date = new Date(+whis.date);
            date.setMonth(date.getMonth() - 1);
            whis.date = date.valueOf();
          }
        }
        await app.WriteHistory.add(whis);
        $progress.textContent = `:${Math.floor((count++ / total) * 100)}%`;
      }
    },
    exportFunc: async function() {
      return {
        "writehistory": (await app.WriteHistory.getAll()),
        "dbVersion": app.WriteHistory.DB_VERSION
      };
    },
    clearFunc: function() {
      return app.WriteHistory.clear();
    },
    clearRangeFunc: function(day) {
      return app.WriteHistory.clearRange(day);
    },
    afterChangedFunc: function() {
      updateIndexedDBUsage();
    }
  });
  // ブックマーク
  new BookmarkIO({
    name: "bookmark",
    countFunc: function() {
      return app.bookmark.getAll().length;
    },
    importFunc: async function({bookmark, readState, readstateVersion = 1}, $progress) {
      var _rs, bm, count, len7, len8, p, q, rs, total;
      total = bookmark.length + readState.length;
      count = 0;
      for (p = 0, len7 = bookmark.length; p < len7; p++) {
        bm = bookmark[p];
        await app.bookmark.import(bm);
        $progress.textContent = `:${Math.floor((count++ / total) * 100)}%`;
      }
      for (q = 0, len8 = readState.length; q < len8; q++) {
        rs = readState[q];
        if (readstateVersion === 1) {
          rs.date = null;
        }
        _rs = (await app.ReadState.get(rs.url));
        if (app.util.isNewerReadState(_rs, rs)) {
          await app.ReadState.set(rs);
        }
        $progress.textContent = `:${Math.floor((count++ / total) * 100)}%`;
      }
    },
    exportFunc: async function() {
      var bookmark, readState;
      [bookmark, readState] = (await Promise.all([app.bookmark.getAll(), app.ReadState.getAll()]));
      return {
        "bookmark": bookmark,
        "readState": readState,
        "readstateVersion": app.ReadState.DB_VERSION
      };
    },
    clearFunc: function() {
      return app.bookmark.removeAll();
    },
    clearExpiredFunc: function() {
      return app.bookmark.removeAllExpired();
    },
    afterChangedFunc: function() {
      updateIndexedDBUsage();
    }
  });
  (function() {
    var $clearButton, $clearRangeButton, $count, $status, setCount;
    //キャッシュ削除ボタン
    $clearButton = $view.C("cache_clear")[0];
    $status = $$.I("cache_status");
    $count = $$.I("cache_count");
    (setCount = async function() {
      var count;
      count = (await Cache.count());
      $count.textContent = `${count}件`;
    })();
    $clearButton.on("click", async function() {
      var result;
      if (!_checkExcute("cache", "clear")) {
        return;
      }
      result = (await UI.Dialog("confirm", {
        message: "本当に削除しますか？"
      }));
      if (!result) {
        _clearExcute();
        return;
      }
      $status.textContent = ":削除中";
      try {
        await Cache.delete();
        $status.textContent = ":削除完了";
      } catch (error) {
        $status.textContent = ":削除失敗";
      }
      setCount();
      updateIndexedDBUsage();
      _clearExcute();
    });
    //キャッシュ範囲削除ボタン
    $clearRangeButton = $view.C("cache_range_clear")[0];
    $clearRangeButton.on("click", async function() {
      var result;
      if (!_checkExcute("cache", "clear_range")) {
        return;
      }
      result = (await UI.Dialog("confirm", {
        message: "本当に削除しますか？"
      }));
      if (!result) {
        _clearExcute();
        return;
      }
      $status.textContent = ":範囲指定削除中";
      try {
        await Cache.clearRange(parseInt($view.C("cache_date_range")[0].value));
        $status.textContent = ":削除完了";
      } catch (error) {
        $status.textContent = ":削除失敗";
      }
      setCount();
      updateIndexedDBUsage();
      _clearExcute();
    });
  })();
  (function() {
    var updateName;
    //ブックマークフォルダ変更ボタン
    $view.C("bookmark_source_change")[0].on("click", function() {
      app.message.send("open", {
        url: "bookmark_source_selector"
      });
    });
    //ブックマークフォルダ表示
    (updateName = async function() {
      var folder;
      [folder] = (await parent.browser.bookmarks.get(app.config.get("bookmark_id")));
      $$.I("bookmark_source_name").textContent = folder.title;
    })();
    app.message.on("config_updated", function({key}) {
      if (key === "bookmark_id") {
        updateName();
      }
    });
  })();
  //「テーマなし」設定
  if (app.config.get("theme_id") === "none") {
    $view.C("theme_none")[0].checked = true;
  }
  app.message.on("config_updated", function({key, val}) {
    if (key === "theme_id") {
      $view.C("theme_none")[0].checked = val === "none";
    }
  });
  $view.C("theme_none")[0].on("click", function() {
    app.config.set("theme_id", this.checked ? "none" : "default");
  });
  //bbsmenu設定
  resetBBSMenu = async function() {
    await app.config.del("bbsmenu");
    $view.$("textarea[name=\"bbsmenu\"]").value = app.config.get("bbsmenu");
    $$.C("bbsmenu_reload")[0].click();
  };
  if ($view.$("textarea[name=\"bbsmenu\"]").value === "") {
    resetBBSMenu();
  }
  $view.C("bbsmenu_reset")[0].on("click", async function() {
    var result;
    result = (await UI.Dialog("confirm", {
      message: "設定内容をリセットします。よろしいですか？"
    }));
    if (!result) {
      return;
    }
    resetBBSMenu();
  });
  ref7 = $view.$$("input[type=\"radio\"]");
  for (p = 0, len7 = ref7.length; p < len7; p++) {
    $dom = ref7[p];
    if (!((ref8 = $dom.name) === "ng_id_expire" || ref8 === "ng_slip_expire")) {
      continue;
    }
    $dom.on("change", function() {
      if (this.checked) {
        $$.I(this.name).dataset.value = this.value;
      }
    });
    $dom.emit(new Event("change"));
  }
  // ImageReplaceDatのリセット
  $view.C("dat_file_reset")[0].on("click", async function() {
    var resetData, result;
    result = (await UI.Dialog("confirm", {
      message: "設定内容をリセットします。よろしいですか？"
    }));
    if (!result) {
      return;
    }
    await app.config.del("image_replace_dat");
    resetData = app.config.get("image_replace_dat");
    $view.$("textarea[name=\"image_replace_dat\"]").value = resetData;
    app.ImageReplaceDat.set(resetData);
  });
  // ぼかし判定用正規表現のリセット
  $view.C("image_blur_reset")[0].on("click", async function() {
    var resetData, result;
    result = (await UI.Dialog("confirm", {
      message: "設定内容をリセットします。よろしいですか？"
    }));
    if (!result) {
      return;
    }
    await app.config.del("image_blur_word");
    resetData = app.config.get("image_blur_word");
    $view.$("input[name=\"image_blur_word\"]").value = resetData;
  });
  // NG設定のリセット
  $view.C("ngwords_reset")[0].on("click", async function() {
    var resetData, result;
    result = (await UI.Dialog("confirm", {
      message: "設定内容をリセットします。よろしいですか？"
    }));
    if (!result) {
      return;
    }
    await app.config.del("ngwords");
    resetData = app.config.get("ngwords");
    $view.$("textarea[name=\"ngwords\"]").value = resetData;
    app.NG.set(resetData);
  });
  // 設定をインポート/エクスポート
  new SettingIO({
    name: "config",
    importFunc: function(file) {
      var $key, $keySelect, $keyTextArea, $themeNone, json, key, len8, q, ref9, value;
      json = JSON.parse(file);
      for (key in json) {
        value = json[key];
        key = key.slice(7);
        if (key !== "theme_id") {
          $key = $view.$(`input[name="${key}"]`);
          if ($key != null) {
            switch ($key.getAttr("type")) {
              case "text":
              case "range":
              case "number":
                $key.value = value;
                $key.emit(new Event("input"));
                break;
              case "checkbox":
                $key.checked = value === "on";
                $key.emit(new Event("change"));
                break;
              case "radio":
                ref9 = $view.$$(`input.direct[name="${key}"]`);
                for (q = 0, len8 = ref9.length; q < len8; q++) {
                  dom = ref9[q];
                  if (dom.value === value) {
                    dom.checked = true;
                  }
                }
                $key.emit(new Event("change"));
            }
          } else {
            $keyTextArea = $view.$(`textarea[name="${key}"]`);
            if ($keyTextArea != null) {
              $keyTextArea.value = value;
              $keyTextArea.emit(new Event("input"));
            }
            $keySelect = $view.$(`select[name="${key}"]`);
            if ($keySelect != null) {
              $keySelect.value = value;
              $keySelect.emit(new Event("change"));
            }
          }
        } else {
          //config_theme_idは「テーマなし」の場合があるので特例化
          if (value === "none") {
            $themeNone = $view.C("theme_none")[0];
            if (!$themeNone.checked) {
              $themeNone.click();
            }
          } else {
            $view.$("input[name=\"theme_id\"]").value = value;
            $view.$("input[name=\"theme_id\"]").emit(new Event("change"));
          }
        }
      }
    },
    exportFunc: function() {
      var content;
      content = app.config.getAll();
      delete content.config_last_board_sort_config;
      delete content.config_last_version;
      return JSON.stringify(content);
    }
  });
  // ImageReplaceDatをインポート
  new SettingIO({
    name: "dat",
    importFunc: function(file) {
      var datDom;
      datDom = $view.$("textarea[name=\"image_replace_dat\"]");
      datDom.value = file;
      datDom.emit(new Event("input"));
    }
  });
  // ReplaceStrTxtをインポート
  new SettingIO({
    name: "replacestr",
    importFunc: function(file) {
      var replacestrDom;
      replacestrDom = $view.$("textarea[name=\"replace_str_txt\"]");
      replacestrDom.value = file;
      replacestrDom.emit(new Event("input"));
    }
  });
  formatBytes = function(bytes) {
    if (bytes < 1048576) {
      return (bytes / 1024).toFixed(2) + "KB";
    }
    if (bytes < 1073741824) {
      return (bytes / 1048576).toFixed(2) + "MB";
    }
    return (bytes / 1073741824).toFixed(2) + "GB";
  };
  // indexeddbの使用状況
  (updateIndexedDBUsage = async function() {
    var $meter, quota, usage;
    ({quota, usage} = (await navigator.storage.estimate()));
    $view.C("indexeddb_max")[0].textContent = formatBytes(quota);
    $view.C("indexeddb_using")[0].textContent = formatBytes(usage);
    $meter = $view.C("indexeddb_meter")[0];
    $meter.max = quota;
    $meter.high = quota * 0.9;
    $meter.low = quota * 0.8;
    $meter.value = usage;
  })();
  return (async function() {    // localstorageの使用状況
    var $meter, quota, usage;
    if (parent.browser.storage.local.getBytesInUse != null) {
      // 無制限なのでindexeddbの最大と一致する
      ({quota} = (await navigator.storage.estimate()));
      $view.C("localstorage_max")[0].textContent = formatBytes(quota);
      $meter = $view.C("localstorage_meter")[0];
      $meter.max = quota;
      $meter.high = quota * 0.9;
      $meter.low = quota * 0.8;
      usage = (await parent.browser.storage.local.getBytesInUse());
      $view.C("localstorage_using")[0].textContent = formatBytes(usage);
      $meter.value = usage;
    } else {
      $meter = $view.C("localstorage_meter")[0].remove();
      $view.C("localstorage_max")[0].textContent = "";
      $view.C("localstorage_using")[0].textContent = "このブラウザでは取得できません";
    }
  })();
});
