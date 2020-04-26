app.boot("/view/sidemenu.html", ["BBSMenu"], function(BBSMenu) {
  var $view, accordion, boardToLi, entryToLi;
  $view = document.documentElement;
  new app.view.PaneContentView($view);
  accordion = new UI.SelectableAccordion(document.body);
  app.DOMData.set($view, "accordion", accordion);
  app.DOMData.set($view, "selectableItemList", accordion);
  boardToLi = function(board) {
    var $a, $li;
    $li = $__("li");
    $a = $__("a");
    $a.setClass("open_in_rcrx");
    $a.title = board.title;
    $a.textContent = board.title;
    $a.href = app.safeHref(board.url);
    if (app.URL.isHttps(board.url)) {
      $a.addClass("https");
    }
    $li.addLast($a);
    return $li;
  };
  entryToLi = function(entry) {
    var $li;
    $li = boardToLi(entry);
    $li.addClass("bookmark");
    return $li;
  };
  //スレタイ検索ボックス
  $view.C("search")[0].on("keydown", function({key}) {
    if (key === "Escape") {
      this.q.value = "";
    }
  });
  $view.C("search")[0].on("submit", function(e) {
    e.preventDefault();
    app.message.send("open", {
      url: `search:${this.q.value}`,
      new_tab: true
    });
    this.q.value = "";
  });
  (function() {    //ブックマーク関連
    //初回ブックマーク表示構築
    app.bookmarkEntryList.ready.add(function() {
      var entry, frag, i, len, ref;
      frag = $_F();
      ref = app.bookmark.getAllBoards();
      for (i = 0, len = ref.length; i < len; i++) {
        entry = ref[i];
        frag.addLast(entryToLi(entry));
      }
      $view.$("ul:first-of-type").addLast(frag);
      accordion.update();
    });
    //ブックマーク更新時処理
    app.message.on("bookmark_updated", function({type, bookmark}) {
      var $a;
      if (bookmark.type !== "board") {
        return;
      }
      $a = $view.$(`li.bookmark > a[href="${bookmark.url}"]`);
      switch (type) {
        case "added":
          if ($a == null) {
            $view.$("ul:first-of-type").addLast(entryToLi(bookmark));
          }
          break;
        case "removed":
          $a.parent().remove();
          break;
        case "title":
          $a.textContent = bookmark.title;
      }
    });
    $view.on("contextmenu", async(e) => {
      var $menu, fn, ref, ref1, target, title, url;
      target = e.target.closest("a");
      if (!target) {
        return;
      }
      url = target.href;
      title = target.title;
      if (url == null) {
        return;
      }
      e.preventDefault();
      await app.defer();
      $menu = $$.I("template_contextmenu").content.$(".contextmenu").cloneNode(true);
      $view.addLast($menu);
      if (app.bookmark.get(url)) {
        if ((ref = $menu.C("add_bookmark")[0]) != null) {
          ref.remove();
        }
      } else {
        if ((ref1 = $menu.C("del_bookmark")[0]) != null) {
          ref1.remove();
        }
      }
      $menu.on("click", fn = function({target}) {
        if (target.tagName !== "LI") {
          return;
        }
        $menu.off("click", fn);
        if (target.hasClass("add_bookmark")) {
          app.bookmark.add(url, title);
        } else if (target.hasClass("del_bookmark")) {
          app.bookmark.remove(url);
        }
        this.remove();
      });
      UI.ContextMenu($menu, e.clientX, e.clientY);
    });
  })();
  (function() {    //板覧関連
    var load, setupDOM;
    setupDOM = function({status, menu, message}) {
      var $h3, $ul, board, category, dom, frag, i, j, k, len, len1, len2, ref, ref1;
      ref = $view.$$("h3:not(:first-of-type), ul:not(:first-of-type)");
      for (i = 0, len = ref.length; i < len; i++) {
        dom = ref[i];
        dom.remove();
      }
      if (status === "error") {
        app.message.send("notify", {
          message: message,
          background_color: "red"
        });
      }
      if (menu != null) {
        frag = $_F();
        for (j = 0, len1 = menu.length; j < len1; j++) {
          category = menu[j];
          $h3 = $__("h3");
          $h3.textContent = category.title;
          frag.addLast($h3);
          $ul = $__("ul");
          ref1 = category.board;
          for (k = 0, len2 = ref1.length; k < len2; k++) {
            board = ref1[k];
            $ul.addLast(boardToLi(board));
          }
          frag.addLast($ul);
        }
        document.body.addLast(frag);
      }
      accordion.update();
      $view.removeClass("loading");
    };
    load = async function() {
      var obj;
      $view.addClass("loading");
      // 表示用板一覧の取得
      obj = (await BBSMenu.get());
      setupDOM(obj);
      BBSMenu.target.on("change", function({
          detail: obj
        }) {
        setupDOM(obj);
      });
    };
    $view.on("request_reload", function() {
      load();
    });
    load();
  })();
});
