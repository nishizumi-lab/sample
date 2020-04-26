app.boot("/view/board.html", ["Board"], function(Board) {
  var $table, $view, $writeButton, load, openedAt, ref, tableSorter, threadList, url, urlStr, write;
  try {
    url = app.URL.parseQuery(location.search).get("q");
  } catch (error) {
    alert("不正な引数です");
    return;
  }
  url = new app.URL.URL(url);
  urlStr = url.href;
  openedAt = Date.now();
  $view = document.documentElement;
  $view.dataset.url = urlStr;
  $table = $__("table");
  threadList = new UI.ThreadList($table, {
    th: ["bookmark", "title", "res", "unread", "heat", "createdDate"],
    searchbox: $view.C("searchbox")[0]
  });
  app.DOMData.set($view, "threadList", threadList);
  app.DOMData.set($view, "selectableItemList", threadList);
  tableSorter = new UI.TableSorter($table);
  app.DOMData.set($table, "tableSorter", tableSorter);
  $$.C("content")[0].addLast($table);
  write = function(param = {}) {
    var openUrl, windowX, windowY;
    param.title = document.title;
    param.url = urlStr;
    windowX = app.config.get("write_window_x");
    windowY = app.config.get("write_window_y");
    openUrl = `/write/submit_thread.html?${app.URL.buildQuery(param)}`;
    if ("chrome" === "firefox" || navigator.userAgent.includes("Vivaldi")) {
      open(openUrl, void 0, `width=600,height=300,left=${windowX},top=${windowY}`);
    } else if ("chrome" === "chrome") {
      parent.browser.windows.create({
        type: "popup",
        url: openUrl,
        width: 600,
        height: 300,
        left: parseInt(windowX),
        top: parseInt(windowY)
      });
    }
  };
  $writeButton = $view.C("button_write")[0];
  if ((ref = url.getTsld()) === "5ch.net" || ref === "shitaraba.net" || ref === "bbspink.com" || ref === "2ch.sc" || ref === "open2ch.net") {
    $writeButton.on("click", function() {
      write();
    });
  } else {
    $writeButton.remove();
  }
  (function() {    // ソート関連
    var lastBoardSort;
    lastBoardSort = app.config.get("last_board_sort_config");
    if (lastBoardSort != null) {
      tableSorter.updateSnake(JSON.parse(lastBoardSort));
    }
    $table.on("table_sort_updated", function({detail}) {
      app.config.set("last_board_sort_config", JSON.stringify(detail));
    });
    //.sort_item_selectorが非表示の時、各種項目のソート切り替えを
    //降順ソート→昇順ソート→標準ソートとする
    $table.on("click", function({target}) {
      if (!(target.tagName === "TH" && target.hasClass("table_sort_asc"))) {
        return;
      }
      if ($view.C("sort_item_selector")[0].offsetWidth !== 0) {
        return;
      }
      $table.on("table_sort_before_update", function(e) {
        e.preventDefault();
        tableSorter.update({
          sortAttribute: "data-thread-number",
          sortOrder: "asc"
        });
      }, {
        once: true
      });
    });
  })();
  new app.view.TabContentView($view);
  (async function() {
    var title;
    title = (await app.BoardTitleSolver.ask(url));
    if (title) {
      document.title = title;
    }
    if (!app.config.isOn("no_history")) {
      app.History.add(urlStr, title || urlStr, openedAt, title || urlStr);
    }
  })();
  load = async function(ex) {
    var $button, board, bookmark, getBoardPromise, getReadStatePromise, i, item, j, k, key, len, len1, len2, readState, readStateArray, readStateIndex, ref1, thread, threadNumber, writeFlag;
    $view.addClass("loading");
    app.message.send("request_update_read_state", {
      board_url: urlStr
    });
    getReadStatePromise = (async function() {
      // request_update_read_stateを待つ
      await app.wait(150);
      return (await app.ReadState.getByBoard(urlStr));
    })();
    getBoardPromise = (async function() {
      var $messageBar, data, message, status;
      ({status, message, data} = (await Board.get(url)));
      $messageBar = $view.C("message_bar")[0];
      if (status === "error") {
        $messageBar.addClass("error");
        $messageBar.innerHTML = message;
      } else {
        $messageBar.removeClass("error");
        $messageBar.removeChildren();
      }
      if (data != null) {
        return data;
      }
      throw new Error("板の取得に失敗しました");
    })();
    try {
      [readStateArray, board] = (await Promise.all([getReadStatePromise, getBoardPromise]));
      readStateIndex = {};
      for (key = i = 0, len = readStateArray.length; i < len; key = ++i) {
        readState = readStateArray[key];
        readStateIndex[readState.url] = key;
      }
      threadList.empty();
      item = [];
      for (threadNumber = j = 0, len1 = board.length; j < len1; threadNumber = ++j) {
        thread = board[threadNumber];
        readState = readStateArray[readStateIndex[thread.url]];
        if (((ref1 = (bookmark = app.bookmark.get(thread.url))) != null ? ref1.readState : void 0) != null) {
          if (app.util.isNewerReadState(readState, bookmark.readState)) {
            ({readState} = bookmark);
          }
        }
        thread.readState = readState;
        thread.threadNumber = threadNumber;
        item.push(thread);
      }
      threadList.addItem(item);
      // スレ建て後の処理
      if (ex != null) {
        writeFlag = !app.config.isOn("no_writehistory");
        if (ex.kind === "own") {
          if (writeFlag) {
            await app.WriteHistory.add({
              url: ex.thread_url,
              res: 1,
              title: ex.title,
              name: ex.name,
              mail: ex.mail,
              message: ex.mes,
              date: Date.now().valueOf()
            });
          }
          app.message.send("open", {
            url: ex.thread_url,
            new_tab: true
          });
        } else {
          for (k = 0, len2 = board.length; k < len2; k++) {
            thread = board[k];
            if (!(thread.title.includes(ex.title))) {
              continue;
            }
            if (writeFlag) {
              await app.WriteHistory.add({
                url: thread.url,
                res: 1,
                title: ex.title,
                name: ex.name,
                mail: ex.mail,
                message: ex.mes,
                date: thread.createdAt
              });
            }
            app.message.send("open", {
              url: thread.url,
              new_tab: true
            });
            break;
          }
        }
      }
      tableSorter.update();
    } catch (error) {}
    $view.removeClass("loading");
    if ($table.hasClass("table_search")) {
      $view.C("searchbox")[0].emit(new Event("input"));
    }
    $view.emit(new Event("view_loaded"));
    $button = $view.C("button_reload")[0];
    $button.addClass("disabled");
    await app.wait5s();
    $button.removeClass("disabled");
  };
  $view.on("request_reload", function({detail}) {
    if ($view.hasClass("loading")) {
      return;
    }
    if ($view.C("button_reload")[0].hasClass("disabled")) {
      return;
    }
    load(detail);
  });
  load();
});
