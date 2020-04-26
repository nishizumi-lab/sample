app.boot("/view/writehistory.html", function() {
  var $content, $table, $view, NUMBER_OF_DATA_IN_ONCE, isInLoadArea, isLoadedEnd, load, loadAddCount, threadList;
  $view = document.documentElement;
  $content = $$.C("content")[0];
  new app.view.TabContentView($view);
  $table = $__("table");
  threadList = new UI.ThreadList($table, {
    th: ["title", "writtenRes", "name", "mail", "message", "writtenDate"],
    searchbox: $view.C("searchbox")[0]
  });
  app.DOMData.set($view, "threadList", threadList);
  app.DOMData.set($view, "selectableItemList", threadList);
  $content.addLast($table);
  NUMBER_OF_DATA_IN_ONCE = 500;
  loadAddCount = 0;
  isLoadedEnd = false;
  load = async function({add = false} = {}) {
    var data, offset;
    if ($view.hasClass("loading")) {
      return;
    }
    if ($view.C("button_reload")[0].hasClass("disabled") && !add) {
      return;
    }
    if (add && isLoadedEnd) {
      return;
    }
    $view.addClass("loading");
    if (add) {
      offset = loadAddCount * NUMBER_OF_DATA_IN_ONCE;
    } else {
      offset = void 0;
    }
    data = (await app.WriteHistory.get(offset, NUMBER_OF_DATA_IN_ONCE));
    if (add) {
      loadAddCount++;
    } else {
      threadList.empty();
      loadAddCount = 1;
    }
    if (data.length < NUMBER_OF_DATA_IN_ONCE) {
      isLoadedEnd = true;
    }
    threadList.addItem(data);
    $view.removeClass("loading");
    if (add && data.length === 0) {
      return;
    }
    $view.emit(new Event("view_loaded"));
    $view.C("button_reload")[0].addClass("disabled");
    await app.wait5s();
    $view.C("button_reload")[0].removeClass("disabled");
  };
  $view.on("request_reload", load);
  load();
  isInLoadArea = false;
  $content.on("scroll", function() {
    var offsetHeight, scrollHeight, scrollPosition, scrollTop;
    ({offsetHeight, scrollHeight, scrollTop} = $content);
    scrollPosition = offsetHeight + scrollTop;
    if (scrollHeight - scrollPosition < 100) {
      if (isInLoadArea) {
        return;
      }
      isInLoadArea = true;
      load({
        add: true
      });
    } else {
      isInLoadArea = false;
    }
  }, {
    passive: true
  });
  $view.C("button_history_clear")[0].on("click", async function() {
    if ((await UI.Dialog("confirm", {
      message: "履歴を削除しますか？"
    }))) {
      try {
        await app.WriteHistory.clear();
        load();
      } catch (error) {}
    }
  });
});
