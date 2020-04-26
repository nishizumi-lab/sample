app.boot("/view/bookmark.html", ["Board"], function(Board) {
  var $table, $view, getPromises, notify, resIndex, tableHeaders, tableSorter, threadList, titleIndex, trUpdatedObserver, unreadIndex;
  $view = document.documentElement;
  $table = $__("table");
  tableHeaders = ["title", "boardTitle", "res", "unread", "heat", "createdDate"];
  threadList = new UI.ThreadList($table, {
    th: tableHeaders,
    bookmarkAddRm: true,
    searchbox: $view.C("searchbox")[0]
  });
  app.DOMData.set($view, "threadList", threadList);
  app.DOMData.set($view, "selectableItemList", threadList);
  $$.C("content")[0].addLast($table);
  tableSorter = new UI.TableSorter($table);
  app.DOMData.set($table, "tableSorter", tableSorter);
  (function() {    // ソート関連
    var DEFAULT_SORT, lastSort;
    DEFAULT_SORT = {
      sort_index: 3,
      sort_order: "desc"
    };
    lastSort = (function() {
      switch (app.config.get("bookmark_sort_save_type")) {
        case "none":
          return DEFAULT_SORT;
        case "board":
          return JSON.parse(app.config.get("last_board_sort_config"));
        case "bookmark":
          return JSON.parse(app.config.get("last_bookmark_sort_config"));
      }
    })();
    if (lastSort.sort_attribute === "data-thread-number") {
      lastSort = DEFAULT_SORT;
    }
    tableSorter.updateSnake(lastSort);
    $table.on("table_sort_updated", function({detail}) {
      app.config.set("last_bookmark_sort_config", JSON.stringify(detail));
    });
  })();
  new app.view.TabContentView($view);
  trUpdatedObserver = new MutationObserver(function(records) {
    var $record, i, len;
    for (i = 0, len = records.length; i < len; i++) {
      ({
        target: $record
      } = records[i]);
      if ($record.matches("tr.updated")) {
        $record.parent().addLast($record);
      }
    }
  });
  //リロード時処理
  $view.on("request_reload", function({
      detail: auto = false
    } = {}) {
    var $loadingOverlay, $reloadButton, boardList, boardThreadTable, boardUrl, count, fn, i, len, loadingServer, ref, url;
    if ($view.hasClass("loading")) {
      return;
    }
    $reloadButton = $view.C("button_reload")[0];
    if ($reloadButton.hasClass("disabled")) {
      return;
    }
    $view.addClass("loading");
    $view.C("searchbox")[0].disabled = true;
    $loadingOverlay = $view.C("loading_overlay")[0];
    $reloadButton.addClass("disabled");
    trUpdatedObserver.observe($view.T("tbody")[0], {
      subtree: true,
      attributes: true,
      attributeFilter: ["class"]
    });
    // TODO: Collection Normalization Proposalで書くとよりよく
    // ES2019 Stage 2(2019/02/05現在)
    // https://github.com/tc39/proposal-collection-normalization
    boardList = new Set();
    boardThreadTable = new Map();
    ref = app.bookmark.getAllThreads();
    for (i = 0, len = ref.length; i < len; i++) {
      ({url} = ref[i]);
      boardUrl = app.URL.threadToBoard(url);
      boardList.add(boardUrl);
      if (boardThreadTable.has(boardUrl)) {
        boardThreadTable.get(boardUrl).push(url);
      } else {
        boardThreadTable.set(boardUrl, [url]);
      }
    }
    count = {
      all: boardList.size,
      success: 0,
      error: 0
    };
    loadingServer = new Set();
    fn = function(res) {
      var board, j, k, len1, len2, ref1, ref2, server, status;
      if (res != null) {
        loadingServer.delete(app.URL.getDomain(this.prev));
        status = res.status === "success" ? "success" : "error";
        count[status]++;
        if (status === "error") {
          ref1 = boardThreadTable.get(this.prev);
          for (j = 0, len1 = ref1.length; j < len1; j++) {
            board = ref1[j];
            app.message.send("bookmark_updated", {
              type: "errored",
              bookmark: {
                type: "thread",
                url: board
              }
            });
          }
        } else {
          ref2 = boardThreadTable.get(this.prev);
          for (k = 0, len2 = ref2.length; k < len2; k++) {
            board = ref2[k];
            app.message.send("bookmark_updated", {
              type: "updated",
              bookmark: {
                type: "thread",
                url: board
              }
            });
          }
        }
      }
      if (count.all === count.success + count.error) {
        (async function() {          //更新完了
          //ソート後にブックマークが更新されてしまう場合に備えて、少し待つ
          var l, len3, ref3, tr;
          await app.wait(500);
          tableSorter.clearSortClass();
          ref3 = $view.$$("tr:not(.updated)");
          for (l = 0, len3 = ref3.length; l < len3; l++) {
            tr = ref3[l];
            tr.parent().addLast(tr);
          }
          trUpdatedObserver.disconnect();
          $view.removeClass("loading");
          if (app.config.isOn("auto_bookmark_notify") && auto) {
            notify();
          }
          $view.C("searchbox")[0].disabled = false;
          await app.wait(10 * 1000);
          $reloadButton.removeClass("disabled");
        })();
      }
// 同一サーバーへの最大接続数: 1
      for (board of boardList) {
        server = app.URL.getDomain(board);
        if (loadingServer.has(server)) {
          continue;
        }
        loadingServer.add(server);
        boardList.delete(board);
        Board.get(new URL(board)).then(fn.bind({
          prev: board
        }));
        fn();
        break;
      }
      //ステータス表示更新
      $loadingOverlay.C("success")[0].textContent = count.success;
      $loadingOverlay.C("error")[0].textContent = count.error;
      $loadingOverlay.C("pending")[0].textContent = count.all - count.success - count.error;
    };
    fn();
  });
  getPromises = app.bookmark.getAllThreads().map(async function({title, url, resCount = 0, readState = {
        url: url,
        read: 0,
        received: 0,
        last: 0
      }, expired}) {
    var boardTitle, boardUrlObj, urlObj;
    urlObj = new app.URL.URL(url);
    boardUrlObj = urlObj.toBoard();
    try {
      boardTitle = (await app.BoardTitleSolver.ask(boardUrlObj));
    } catch (error) {
      boardTitle = "";
    }
    threadList.addItem({
      title,
      url,
      resCount,
      readState,
      createdAt: /\/(\d+)\/$/.exec(urlObj.pathname)[1] * 1000,
      expired,
      boardUrl: boardUrlObj.href,
      boardTitle,
      isHttps: urlObj.isHttps()
    });
  });
  (async function() {
    await Promise.all(getPromises);
    app.message.send("request_update_read_state");
    tableSorter.update();
    $view.emit(new Event("view_loaded"));
  })();
  titleIndex = tableHeaders.indexOf("title");
  resIndex = tableHeaders.indexOf("res");
  unreadIndex = tableHeaders.indexOf("unread");
  // 新着通知
  notify = function() {
    var after, before, i, len, notifyStr, ref, tds, title, tr, unreadRes;
    notifyStr = "";
    ref = $view.$$("tr.updated");
    for (i = 0, len = ref.length; i < len; i++) {
      tr = ref[i];
      tds = tr.T("td");
      title = tds[titleIndex].textContent;
      if (title.length >= 10) {
        title = title.slice(0, 15 - 3) + "...";
      }
      before = parseInt(tds[resIndex].dataset.beforeres);
      after = parseInt(tds[resIndex].textContent);
      unreadRes = tds[unreadIndex].textContent;
      if (after > before) {
        notifyStr += `タイトル: ${title}  新規: ${after - before}  未読: ${unreadRes}\n`;
      }
    }
    if (notifyStr !== "") {
      new app.Notification("ブックマークの更新", notifyStr, "bookmark", "bookmark");
    }
  };
});
