app.boot("/view/search.html", ["ThreadSearch"], async function(ThreadSearch) {
  var $buttonReload, $content, $messageBar, $table, $tbody, $view, load, onScroll, openedAt, queries, query, scheme, tableSorter, threadList, threadSearch;
  try {
    queries = app.URL.parseQuery(location.search);
    query = queries.get("query");
  } catch (error) {
    alert("不正な引数です");
    return;
  }
  scheme = queries.get("scheme");
  openedAt = Date.now();
  $view = document.documentElement;
  $view.dataset.url = `search:${query}`;
  $view.setAttr("scheme", scheme);
  $content = $$.C("content")[0];
  $messageBar = $view.C("message_bar")[0];
  $buttonReload = $view.C("button_reload")[0];
  $table = $__("table");
  threadList = new UI.ThreadList($table, {
    th: ["bookmark", "title", "boardTitle", "res", "heat", "createdDate"],
    searchbox: $view.C("searchbox")[0]
  });
  app.DOMData.set($view, "threadList", threadList);
  app.DOMData.set($view, "selectableItemList", threadList);
  tableSorter = new UI.TableSorter($table);
  app.DOMData.set($table, "tableSorter", tableSorter);
  $content.addFirst($table);
  new app.view.TabContentView($view);
  document.title = `検索:${query}`;
  if (!app.config.isOn("no_history")) {
    app.History.add($view.dataset.url, document.title, openedAt, "");
  }
  $view.$(".button_link > a").href = `${scheme}://dig.5ch.net/search?maxResult=500&keywords=${encodeURIComponent(query)}`;
  threadSearch = new ThreadSearch(query, `${scheme}:`);
  $tbody = $view.T("tbody")[0];
  load = async function(add = false) {
    var dom, empty, i, len, message, ref, result;
    if ($view.hasClass("loading") && !add) {
      return;
    }
    $view.addClass("loading");
    $buttonReload.addClass("disabled");
    $view.C("more")[0].textContent = "検索中";
    $view.C("more")[0].removeClass("hidden");
    try {
      result = (await threadSearch.read());
      $messageBar.removeClass("error");
      $messageBar.removeChildren();
      threadList.addItem(result);
      if ($tbody.child().length === 0) {
        $tbody.addClass("body_empty");
      } else {
        empty = true;
        ref = $tbody.child();
        for (i = 0, len = ref.length; i < len; i++) {
          dom = ref[i];
          if (!(dom.offsetHeight !== 0)) {
            continue;
          }
          empty = false;
          break;
        }
        if (empty) {
          $tbody.addClass("body_empty");
        } else {
          $tbody.removeClass("body_empty");
        }
      }
      $view.removeClass("loading");
    } catch (error) {
      ({message} = error);
      $messageBar.addClass("error");
      $messageBar.textContent = message;
      $view.removeClass("loading");
    }
    $view.C("more")[0].addClass("hidden");
    (async function() {
      await app.wait5s();
      $buttonReload.removeClass("disabled");
    })();
  };
  onScroll = function() {
    var offsetHeight, scrollHeight, scrollPosition, scrollTop;
    ({offsetHeight, scrollHeight, scrollTop} = $content);
    scrollPosition = offsetHeight + scrollTop;
    if (scrollHeight - scrollPosition < 100) {
      $content.off("scroll", onScroll);
      load(true);
    }
  };
  $content.on("scroll", onScroll, {
    passive: true
  });
  $buttonReload.on("click", async function() {
    if ($buttonReload.hasClass("disabled")) {
      return;
    }
    threadList.empty();
    threadSearch = new ThreadSearch(query, `${scheme}:`);
    await load();
    onScroll(); // 20件分がスクロールなしで表示できる場合
    $content.on("scroll", onScroll, {
      passive: true
    });
  });
  await load();
  onScroll(); // 20件分がスクロールなしで表示できる場合
  app.config.set("thread_search_last_mode", scheme);
});
