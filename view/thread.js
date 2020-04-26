(async function() {
  var blob, font, fontface, response;
  if (navigator.platform.includes("Win")) {
    return;
  }
  try {
    font = localStorage.getItem("textar_font");
    if (font == null) {
      throw new Error("localstorageからのフォントの取得に失敗しました");
    }
  } catch (error1) {
    response = (await fetch("https://readcrx-2.github.io/read.crx-2/textar-min.woff2"));
    blob = (await response.blob());
    font = (await new Promise(function(resolve) {
      var fr;
      fr = new FileReader();
      fr.onload = function() {
        resolve(fr.result);
      };
      fr.readAsDataURL(blob);
    }));
    localStorage.setItem("textar_font", font);
  }
  fontface = new FontFace("Textar", `url(${font})`);
  document.fonts.add(fontface);
})();

app.viewThread = {};

app.boot("/view/thread.html", function() {
  var $content, $view, AANoOverflow, _getExpireDateString, canWrite, lazyLoad, mediaContainer, onHeaderMenu, onLink, popupHelper, popupView, removeWriteButton, searchNextThread, threadContent, viewUrl, viewUrlStr, write;
  try {
    viewUrlStr = app.URL.parseQuery(location.search).get("q");
  } catch (error1) {
    alert("不正な引数です");
    return;
  }
  viewUrl = new app.URL.URL(viewUrlStr);
  viewUrlStr = viewUrl.href;
  $view = document.documentElement;
  $view.dataset.url = viewUrlStr;
  $content = $view.C("content")[0];
  threadContent = new UI.ThreadContent(viewUrl, $content);
  mediaContainer = new UI.MediaContainer($view);
  lazyLoad = new UI.LazyLoad($content);
  app.DOMData.set($view, "threadContent", threadContent);
  app.DOMData.set($view, "selectableItemList", threadContent);
  app.DOMData.set($view, "lazyload", lazyLoad);
  new app.view.TabContentView($view);
  searchNextThread = new UI.SearchNextThread($view.C("next_thread_list")[0]);
  popupView = new UI.PopupView($view);
  if (app.config.get("aa_font") === "aa") {
    $content.addClass("config_use_aa_font");
    AANoOverflow = new UI.AANoOverflow($view, {
      minRatio: app.config.get("aa_min_ratio")
    });
  }
  $view.on("became_expired", function() {
    parent.postMessage({
      type: "became_expired"
    }, location.origin);
    return $view.addClass("expired");
  }, {
    once: true
  });
  $view.on("became_over1000", function() {
    parent.postMessage({
      type: "became_over1000"
    }, location.origin);
    return $view.addClass("over1000");
  }, {
    once: true
  });
  write = function(param = {}) {
    var openUrl, windowX, windowY;
    param.url = viewUrlStr;
    param.title = document.title;
    windowX = app.config.get("write_window_x");
    windowY = app.config.get("write_window_y");
    openUrl = `/write/submit_res.html?${app.URL.buildQuery(param)}`;
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
  popupHelper = async function(that, e, fn) {
    var $popup, dom, j, k, len, len1, ref, ref1;
    $popup = fn();
    if ($popup.child().length === 0) {
      return;
    }
    ref = $popup.T("article");
    for (j = 0, len = ref.length; j < len; j++) {
      dom = ref[j];
      dom.removeClass("last", "read", "received");
    }
    //ポップアップ内のサムネイルの遅延ロードを解除
    if (!lazyLoad.isManualLoad) {
      ref1 = $popup.$$("img[data-src], video[data-src]");
      for (k = 0, len1 = ref1.length; k < len1; k++) {
        dom = ref1[k];
        lazyLoad.immediateLoad(dom);
      }
    }
    await app.defer();
    // popupの表示
    popupView.show($popup, e.clientX, e.clientY, that);
  };
  canWrite = function() {
    return $view.C("button_write")[0] != null;
  };
  removeWriteButton = function() {
    var ref;
    if ((ref = $view.C("button_write")[0]) != null) {
      ref.remove();
    }
  };
  $view.on("became_expired", removeWriteButton, {
    once: true
  });
  $view.on("became_over1000", removeWriteButton, {
    once: true
  });
  // したらばの過去ログ
  if (viewUrl.isArchive()) {
    $view.emit(new Event("became_expired"));
  } else {
    $view.C("button_write")[0].on("click", function() {
      write();
    });
  }
  //リロード処理
  $view.on("request_reload", async function({
      detail: ex = {}
    }) {
    var date, i, j, jumpResNum, postMes, ref, ref1, ref2, t, thread;
    threadContent.refreshNG();
    //先にread_state更新処理を走らせるために、処理を飛ばす
    await app.defer();
    jumpResNum = +((ref = (ref1 = ex.written_res_num) != null ? ref1 : ex.param_res_num) != null ? ref : -1);
    if (!ex.force_update && ($view.hasClass("loading") || $view.C("button_reload")[0].hasClass("disabled"))) {
      if (jumpResNum > 0) {
        threadContent.select(jumpResNum, false, true, -60);
      }
      return;
    }
    thread = (await app.viewThread._draw($view, {
      forceUpdate: ex.force_update,
      jumpResNum
    }));
    if (!((ex.mes != null) && !app.config.isOn("no_writehistory"))) {
      return;
    }
    postMes = ex.mes.replace(/\s/g, "");
    ref2 = thread.res;
    for (i = j = ref2.length - 1; j >= 0; i = j += -1) {
      t = ref2[i];
      if (!(postMes === app.util.decodeCharReference(app.util.stripTags(t.message)).replace(/\s/g, ""))) {
        continue;
      }
      date = app.util.stringToDate(t.other).valueOf();
      if (date != null) {
        app.WriteHistory.add({
          url: viewUrlStr,
          res: i + 1,
          title: document.title,
          name: app.util.decodeCharReference(t.name),
          mail: app.util.decodeCharReference(t.mail),
          inputName: ex.name,
          inputMail: ex.mail,
          message: ex.mes,
          date
        });
      }
      threadContent.addClassWithOrg($content.child()[i], "written");
      break;
    }
  });
  (async function() {    //初回ロード処理
    var boardTitle, boardUrl, iframe, jumpResNum, openedAt;
    openedAt = Date.now();
    app.viewThread._readStateManager($view);
    $view.on("read_state_attached", function({
        detail: {jumpResNum, requestReloadFlag, loadCount} = {}
      }) {
      var defaultScroll, onScroll;
      onScroll = false;
      $content.on("scroll", function() {
        onScroll = true;
      }, {
        once: true
      });
      (defaultScroll = function() {
        var $last, lastNum, offset, ref;
        $last = $content.C("last")[0];
        lastNum = $content.$(":scope > article:last-child").C("num")[0].textContent;
        // 指定レス番号へ
        if ((0 < jumpResNum && jumpResNum <= lastNum)) {
          threadContent.select(jumpResNum, false, true, -60);
        // 最終既読位置へ
        } else if ($last != null) {
          offset = (ref = $last.attr("last-offset")) != null ? ref : 0;
          threadContent.scrollTo($last, false, +offset);
        }
      })();
      //スクロールされなかった場合も余所の処理を走らすためにscrollを発火
      if (!onScroll) {
        $content.emit(new Event("scroll"));
      }
      //二度目以降のread_state_attached時
      $view.on("read_state_attached", function({
          detail: {jumpResNum, requestReloadFlag, loadCount} = {}
        }) {
        var $res, $tmp, dom, j, k, lastNum, lastResNum, latest50ResNum, len, len1, moveMode, offset, ref, ref1, ref2, ref3, ref4, ref5;
        // リロード時の一回目の処理
        if (requestReloadFlag && loadCount === 1) {
          defaultScroll();
          return;
        }
        moveMode = "new";
        if ($view.hasClass("autoload") && !$view.hasClass("autoload_pause")) {
          //通常時と自動更新有効時で、更新後のスクロールの動作を変更する
          moveMode = app.config.get("auto_load_move");
        }
        switch (moveMode) {
          case "new":
            lastNum = +((ref = $content.$(":scope > article:last-child")) != null ? ref.C("num")[0].textContent : void 0);
            if ((0 < jumpResNum && jumpResNum <= lastNum)) {
              threadContent.select(jumpResNum, false, true, -60);
            } else {
              offset = -100;
              ref1 = $content.child();
              for (j = 0, len = ref1.length; j < len; j++) {
                dom = ref1[j];
                if (!(dom.matches(".last.received + article"))) {
                  continue;
                }
                $tmp = dom;
                break;
              }
              // 新着が存在しない場合はスクロールを実行するためにレスを探す
              if ($tmp == null) {
                $tmp = $content.$(":scope > article.last");
                offset = (ref2 = $tmp != null ? $tmp.attr("last-offset") : void 0) != null ? ref2 : -100;
              }
              if ($tmp == null) {
                $tmp = $content.$(":scope > article.read");
              }
              if ($tmp == null) {
                $tmp = $content.$(":scope > article:last-child");
              }
              if ($tmp != null) {
                threadContent.scrollTo($tmp, true, +offset);
              }
            }
            break;
          case "surely_new":
            ref3 = $content.child();
            for (k = 0, len1 = ref3.length; k < len1; k++) {
              dom = ref3[k];
              if (!(dom.matches(".last.received + article"))) {
                continue;
              }
              $res = dom;
              break;
            }
            if ($res != null) {
              threadContent.scrollTo($res, true);
            }
            break;
          case "latest50":
            lastResNum = +((ref4 = $content.$(":scope > article.last")) != null ? ref4.C("num")[0].textContent : void 0);
            latest50ResNum = +((ref5 = $content.$(":scope > article.latest50")) != null ? ref5.C("num")[0].textContent : void 0);
            if (latest50ResNum > lastResNum) {
              threadContent.scrollTo(latest50ResNum, true);
            }
            break;
          case "newest":
            $res = $content.$(":scope > article:last-child");
            if ($res != null) {
              threadContent.scrollTo($res, true);
            }
        }
      });
    }, {
      once: true
    });
    jumpResNum = -1;
    iframe = parent.$$.$(`iframe[data-url="${viewUrlStr}"]`);
    if (iframe) {
      jumpResNum = +iframe.dataset.writtenResNum;
      if (jumpResNum < 1) {
        jumpResNum = +iframe.dataset.paramResNum;
      }
    }
    try {
      await app.viewThread._draw($view, {jumpResNum});
    } catch (error1) {}
    boardUrl = viewUrl.toBoard();
    try {
      boardTitle = (await app.BoardTitleSolver.ask(boardUrl));
    } catch (error1) {
      boardTitle = "";
    }
    if (!app.config.isOn("no_history")) {
      app.History.add(viewUrlStr, document.title, openedAt, boardTitle);
    }
  })();
  //レスメニュー表示(ヘッダー上)
  onHeaderMenu = async function(e) {
    var $article, $menu, $toggleAaMode, altParent, target;
    target = e.target.closest("article > header");
    if (target == null) {
      return;
    }
    if (target.tagName === "A") {
      return;
    }
    // id/参照ポップアップの表示処理との競合回避
    if (e.type === "click" && app.config.get("popup_trigger") === "click" && e.target.matches(".id.link, .id.freq, .anchor_id, .slip.link, .slip.freq, .trip.link, .trip.freq, .rep.link, .rep.freq")) {
      return;
    }
    if (e.type === "contextmenu") {
      e.preventDefault();
    }
    $article = target.parent();
    $menu = $$.I("template_res_menu").content.$(".res_menu").cloneNode(true);
    $menu.addClass("hidden");
    altParent = null;
    if ($article.parent().hasClass("popup")) {
      altParent = $view.C("popup_area")[0];
      altParent.addLast($menu);
      $menu.setAttr("resnum", $article.C("num")[0].textContent);
      $article.parent().addClass("has_contextmenu");
    } else {
      $article.addLast($menu);
    }
    $toggleAaMode = $menu.C("toggle_aa_mode")[0];
    if ($article.parent().hasClass("config_use_aa_font")) {
      $toggleAaMode.textContent = $article.hasClass("aa") ? "AA表示モードを解除" : "AA表示モードに変更";
    } else {
      $toggleAaMode.remove();
    }
    if ($article.dataset.id == null) {
      $menu.C("copy_id")[0].remove();
      $menu.C("add_id_to_ngwords")[0].remove();
    }
    if ($article.dataset.slip == null) {
      $menu.C("copy_slip")[0].remove();
      $menu.C("add_slip_to_ngwords")[0].remove();
    }
    if ($article.dataset.trip == null) {
      $menu.C("copy_trip")[0].remove();
    }
    if (!canWrite()) {
      $menu.C("res_to_this")[0].remove();
      $menu.C("res_to_this2")[0].remove();
    }
    if ($article.hasClass("written")) {
      $menu.C("add_writehistory")[0].remove();
    } else {
      $menu.C("del_writehistory")[0].remove();
    }
    if (!$article.matches(".popup > article")) {
      $menu.C("jump_to_this")[0].remove();
    }
    // 画像にぼかしをかける/画像のぼかしを解除する
    if (!$article.hasClass("has_image")) {
      $menu.C("set_image_blur")[0].remove();
      $menu.C("reset_image_blur")[0].remove();
    } else {
      if ($article.$(".thumbnail.image_blur[media-type='image'], .thumbnail.image_blur[media-type='video']") != null) {
        $menu.C("set_image_blur")[0].remove();
      } else {
        $menu.C("reset_image_blur")[0].remove();
      }
    }
    await app.defer();
    if (getSelection().toString().length === 0) {
      $menu.C("copy_selection")[0].remove();
      $menu.C("search_selection")[0].remove();
    }
    $menu.removeClass("hidden");
    UI.ContextMenu($menu, e.clientX, e.clientY, altParent);
  };
  $view.on("click", onHeaderMenu);
  $view.on("contextmenu", onHeaderMenu);
  //レスメニュー表示(内容上)
  $view.on("contextmenu", function({target}) {
    if (!target.matches("article > .message")) {
      return;
    }
    // 選択範囲をNG登録
    app.ContextMenus.update("add_selection_to_ngwords", {
      onclick: function(info, tab) {
        var selectedText;
        selectedText = getSelection().toString();
        if (selectedText.length > 0) {
          app.NG.add(selectedText);
          threadContent.refreshNG();
        }
      }
    });
  });
  //レスメニュー項目クリック
  $view.on("click", function({target}) {
    var $res, addString, exDate, j, len, ref, res, rn, selectedText;
    if (!target.matches(".res_menu > li")) {
      return;
    }
    $res = target.closest("article");
    if (!$res) {
      rn = target.closest(".res_menu").getAttr("resnum");
      ref = $view.$$(".popup.has_contextmenu > article");
      for (j = 0, len = ref.length; j < len; j++) {
        res = ref[j];
        if (res.C("num")[0].textContent === rn) {
          $res = res;
          break;
        }
      }
    }
    if (target.hasClass("copy_selection")) {
      selectedText = getSelection().toString();
      if (selectedText.length > 0) {
        document.execCommand("copy");
      }
    } else if (target.hasClass("search_selection")) {
      selectedText = getSelection().toString();
      if (selectedText.length > 0) {
        open(`https://www.google.co.jp/search?q=${selectedText}`, "_blank");
      }
    } else if (target.hasClass("copy_id")) {
      app.clipboardWrite($res.dataset.id);
    } else if (target.hasClass("copy_slip")) {
      app.clipboardWrite($res.dataset.slip);
    } else if (target.hasClass("copy_trip")) {
      app.clipboardWrite($res.dataset.trip);
    } else if (target.hasClass("add_id_to_ngwords")) {
      addString = $res.dataset.id;
      exDate = _getExpireDateString("id");
      if (exDate) {
        addString = `expireDate:${exDate},${addString}`;
      }
      app.NG.add(addString);
      threadContent.refreshNG();
    } else if (target.hasClass("add_slip_to_ngwords")) {
      addString = "Slip:" + $res.dataset.slip;
      exDate = _getExpireDateString("slip");
      if (exDate) {
        addString = `expireDate:${exDate},${addString}`;
      }
      app.NG.add(addString);
      threadContent.refreshNG();
    } else if (target.hasClass("jump_to_this")) {
      threadContent.scrollTo($res, true);
    } else if (target.hasClass("res_to_this")) {
      write({
        message: `>>${($res.C("num")[0].textContent)}\n`
      });
    } else if (target.hasClass("res_to_this2")) {
      write({
        message: `>>${($res.C("num")[0].textContent)}\n${$res.C("message")[0].innerText.replace(/^/gm, '>')}\n`
      });
    } else if (target.hasClass("add_writehistory")) {
      threadContent.addWriteHistory($res);
      threadContent.addClassWithOrg($res, "written");
    } else if (target.hasClass("del_writehistory")) {
      threadContent.removeWriteHistory($res);
      threadContent.removeClassWithOrg($res, "written");
    } else if (target.hasClass("toggle_aa_mode")) {
      if ($res.hasClass("aa")) {
        AANoOverflow.unsetMiniAA($res);
      } else {
        AANoOverflow.setMiniAA($res);
      }
    } else if (target.hasClass("res_permalink")) {
      open(app.safeHref(viewUrlStr + $res.C("num")[0].textContent));
    // 画像をぼかす
    } else if (target.hasClass("set_image_blur")) {
      UI.MediaContainer.setImageBlur($res, true);
    // 画像のぼかしを解除する
    } else if (target.hasClass("reset_image_blur")) {
      UI.MediaContainer.setImageBlur($res, false);
    }
    target.parent().remove();
  });
  // アンカーポップアップ
  $view.on("mouseenter", function(e) {
    var anchor, target;
    ({target} = e);
    if (!(target.hasClass("anchor") || target.hasClass("name_anchor"))) {
      return;
    }
    anchor = target.innerHTML;
    if (!target.hasClass("anchor")) {
      anchor = anchor.trim();
    }
    popupHelper(target, e, () => {
      var $div, $popup, anchorData, end, i, j, k, len, now, popupCount, ref, ref1, ref2, res, resCount, start, tmp;
      $popup = $__("div");
      resCount = 0;
      if (target.hasClass("disabled")) {
        $div = $__("div").addClass("popup_disabled");
        $div.textContent = target.dataset.disabledReason;
        $popup.addLast($div);
      } else {
        anchorData = app.util.Anchor.parseAnchor(anchor);
        if (anchorData.targetCount >= 25) {
          $div = $__("div").addClass("popup_disabled");
          $div.textContent = "指定されたレスの量が極端に多いため、ポップアップを表示しません";
          $popup.addLast($div);
        } else if (0 < anchorData.targetCount) {
          resCount = anchorData.targetCount;
          tmp = $content.child();
          ref = anchorData.segments;
          for (j = 0, len = ref.length; j < len; j++) {
            [start, end] = ref[j];
            for (i = k = ref1 = start, ref2 = end; (ref1 <= ref2 ? k <= ref2 : k >= ref2); i = ref1 <= ref2 ? ++k : --k) {
              now = i - 1;
              if (!(res = tmp[now])) {
                break;
              }
              if (res.hasClass("ng") && !res.hasClass("disp_ng")) {
                continue;
              }
              $popup.addLast(res.cloneNode(true));
            }
          }
        }
      }
      popupCount = $popup.child().length;
      if (popupCount === 0) {
        $div = $__("div").addClass("popup_disabled");
        $div.textContent = "対象のレスが見つかりません";
        $popup.addLast($div);
      } else if (popupCount < resCount) {
        $div = $__("div").addClass("ng_count");
        $div.setAttr("ng-count", resCount - popupCount);
        $popup.addLast($div);
      }
      return $popup;
    });
  }, true);
  //アンカーリンク
  $view.on("click", function(e) {
    var ref, target, targetResNum, tmp;
    ({target} = e);
    if (!target.hasClass("anchor")) {
      return;
    }
    e.preventDefault();
    if (target.hasClass("disabled")) {
      return;
    }
    tmp = app.util.Anchor.parseAnchor(target.innerHTML);
    targetResNum = (ref = tmp.segments[0]) != null ? ref[0] : void 0;
    if (targetResNum != null) {
      threadContent.scrollTo(targetResNum, true);
    }
  });
  // サムネイルクリック読み込み
  if (lazyLoad.isManualLoad) {
    $view.on("click", function(e) {
      var $media, $medias, $target, j, len;
      ({
        target: $target
      } = e);
      if (!$target.hasClass("thumbnail")) {
        $target = $target.parent(".thumbnail");
        if ($target == null) {
          return;
        }
      }
      $medias = $target.$$("img[data-src], video[data-src]");
      if (!($medias.length > 0)) {
        return;
      }
      e.preventDefault();
      for (j = 0, len = $medias.length; j < len; j++) {
        $media = $medias[j];
        lazyLoad.immediateLoad($media);
      }
    });
  }
  //通常リンク
  onLink = async function(e) {
    var bbsType, flg, paramResNum, srcType, target, targetUrl, targetUrlStr;
    ({target} = e);
    if (!target.matches(".message a:not(.anchor)")) {
      return;
    }
    //http、httpsスキーム以外ならクリックを無効化する
    if (!/^https?:$/.test(target.protocol)) {
      e.preventDefault();
      return;
    }
    //.open_in_rcrxが付与されている場合、処理は他モジュールに任せる
    if (target.hasClass("open_in_rcrx")) {
      return;
    }
    targetUrlStr = target.href;
    targetUrl = new app.URL.URL(targetUrlStr);
    ({
      type: srcType,
      bbsType
    } = targetUrl.guessType());
    targetUrlStr = targetUrl.href;
    //read.crxで開けるURLかどうかを判定
    flg = (function() {
      if (srcType === "thread") {
        //スレのURLはほぼ確実に判定できるので、そのままok
        return true;
      }
      if (srcType === "board" && bbsType !== "2ch") {
        //2chタイプ以外の板urlもほぼ確実に判定できる
        return true;
      }
      //2chタイプの板は誤爆率が高いので、もう少し細かく判定する
      if (srcType === "board" && bbsType === "2ch") {
        if (targetUrl.getTsld() === "5ch.net") {
          //2ch自体の場合の判断はguess_typeを信じて板判定
          return true;
        }
        if (app.bookmark.get(targetUrlStr)) {
          //ブックマークされている場合も板として判定
          return true;
        }
      }
      return false;
    })();
    //read.crxで開ける板だった場合は.open_in_rcrxを付与して再度クリックイベント送出
    if (flg) {
      e.preventDefault();
      target.addClass("open_in_rcrx");
      target.dataset.href = targetUrlStr;
      target.href = "javascript:undefined;";
      if (srcType === "thread") {
        paramResNum = targetUrl.getResNumber();
        if (paramResNum) {
          target.dataset.paramResNum = paramResNum;
        }
      }
      await app.defer();
      target.emit(e);
    }
  };
  $view.on("click", onLink);
  $view.on("mousedown", onLink);
  //リンク先情報ポップアップ
  $view.on("mouseenter", async function(e) {
    var after, boardUrl, target, title, url;
    ({target} = e);
    if (!target.matches(".message a:not(.anchor)")) {
      return;
    }
    url = new app.URL.URL(target.href);
    url.convertFromPhone();
    switch (url.guessType().type) {
      case "board":
        boardUrl = url;
        after = "";
        break;
      case "thread":
        boardUrl = url.toBoard();
        after = "のスレ";
        break;
      default:
        return;
    }
    try {
      title = (await app.BoardTitleSolver.ask(boardUrl));
      popupHelper(target, e, () => {
        var $div, $div2;
        $div = $__("div").addClass("popup_linkinfo");
        $div2 = $__("div");
        $div2.textContent = title + after;
        $div.addLast($div2);
        return $div;
      });
    } catch (error1) {}
  }, true);
  //IDポップアップ
  $view.on(app.config.get("popup_trigger"), function(e) {
    var target;
    ({target} = e);
    if (!target.matches(".id.link, .id.freq, .anchor_id, .slip.link, .slip.freq, .trip.link, .trip.freq")) {
      return;
    }
    e.preventDefault();
    popupHelper(target, e, () => {
      var $article, $div, $parentArticle, $popup, id, nowPopuping, popupCount, ref, ref1, ref2, resCount, resNum, slip, targetRes, trip;
      $article = target.closest("article");
      $popup = $__("div");
      id = "";
      slip = "";
      trip = "";
      if (target.hasClass("anchor_id")) {
        id = target.textContent.replace(/^id:/i, "ID:").replace(/\(\d+\)$/, "").replace(/\u25cf$/, ""); //末尾●除去
        $popup.addClass("popup_id");
      } else if (target.hasClass("id")) {
        id = $article.dataset.id;
        $popup.addClass("popup_id");
      } else if (target.hasClass("slip")) {
        slip = $article.dataset.slip;
        $popup.addClass("popup_slip");
      } else if (target.hasClass("trip")) {
        trip = $article.dataset.trip;
        $popup.addClass("popup_trip");
      }
      nowPopuping = "";
      $parentArticle = $article.parent();
      if ($parentArticle.hasClass("popup_id") && $article.dataset.id === id) {
        nowPopuping = "IP/ID";
      } else if ($parentArticle.hasClass("popup_slip") && $article.dataset.slip === slip) {
        nowPopuping = "SLIP";
      } else if ($parentArticle.hasClass("popup_trip") && $article.dataset.trip === trip) {
        nowPopuping = "トリップ";
      }
      resCount = 0;
      if (nowPopuping !== "") {
        $div = $__("div").addClass("popup_disabled");
        $div.textContent = `現在ポップアップしている${nowPopuping}です`;
        $popup.addLast($div);
      } else if (threadContent.idIndex.has(id)) {
        resCount = threadContent.idIndex.get(id).size;
        ref = threadContent.idIndex.get(id);
        for (resNum of ref) {
          targetRes = $content.child()[resNum - 1];
          if (targetRes.hasClass("ng") && !targetRes.hasClass("disp_ng")) {
            continue;
          }
          $popup.addLast(targetRes.cloneNode(true));
        }
      } else if (threadContent.slipIndex.has(slip)) {
        resCount = threadContent.slipIndex.get(slip).size;
        ref1 = threadContent.slipIndex.get(slip);
        for (resNum of ref1) {
          targetRes = $content.child()[resNum - 1];
          if (targetRes.hasClass("ng") && !targetRes.hasClass("disp_ng")) {
            continue;
          }
          $popup.addLast(targetRes.cloneNode(true));
        }
      } else if (threadContent.tripIndex.has(trip)) {
        resCount = threadContent.tripIndex.get(trip).size;
        ref2 = threadContent.tripIndex.get(trip);
        for (resNum of ref2) {
          targetRes = $content.child()[resNum - 1];
          if (targetRes.hasClass("ng") && !targetRes.hasClass("disp_ng")) {
            continue;
          }
          $popup.addLast(targetRes.cloneNode(true));
        }
      }
      popupCount = $popup.child().length;
      if (popupCount === 0) {
        $div = $__("div").addClass("popup_disabled");
        $div.textContent = "対象のレスが見つかりません";
        $popup.addLast($div);
      } else if (popupCount < resCount) {
        $div = $__("div").addClass("ng_count");
        $div.setAttr("ng-count", resCount - popupCount);
        $popup.addLast($div);
      }
      return $popup;
    });
  }, true);
  //リプライポップアップ
  $view.on(app.config.get("popup_trigger"), function(e) {
    var target;
    ({target} = e);
    if (!target.hasClass("rep")) {
      return;
    }
    popupHelper(target, e, () => {
      var $div, $popup, frag, popupCount, ref, resCount, resNum, targetRes, targetResNum, tmp;
      tmp = $content.child();
      frag = $_F();
      resNum = +target.closest("article").C("num")[0].textContent;
      ref = threadContent.repIndex.get(resNum);
      for (targetResNum of ref) {
        targetRes = tmp[targetResNum - 1];
        if (targetRes.hasClass("ng") && (!targetRes.hasClass("disp_ng") || app.config.isOn("reject_ng_rep"))) {
          continue;
        }
        frag.addLast(targetRes.cloneNode(true));
      }
      $popup = $__("div");
      $popup.addLast(frag);
      resCount = threadContent.repIndex.get(resNum).size;
      popupCount = $popup.child().length;
      if (popupCount === 0) {
        $div = $__("div").addClass("popup_disabled");
        $div.textContent = "対象のレスが見つかりません";
        $popup.addLast($div);
      } else if (popupCount < resCount && !app.config.isOn("reject_ng_rep")) {
        $div = $__("div").addClass("ng_count");
        $div.setAttr("ng-count", resCount - popupCount);
        $popup.addLast($div);
      }
      return $popup;
    });
  }, true);
  // 展開済みURLのポップアップ
  $view.on("mouseenter", function(e) {
    var target;
    ({target} = e);
    if (!target.hasClass("has_expandedURL")) {
      return;
    }
    if (app.config.get("expand_short_url") !== "popup") {
      return;
    }
    popupHelper(target, e, () => {
      var $popup, frag, sib, targetUrl;
      targetUrl = target.href;
      frag = $_F();
      sib = target;
      while (true) {
        sib = sib.next();
        if ((sib != null ? sib.hasClass("expandedURL") : void 0) && (sib != null ? sib.getAttr("short-url") : void 0) === targetUrl) {
          frag.addLast(sib.cloneNode(true));
          break;
        }
      }
      frag.$(".expandedURL").removeClass("hide_data");
      $popup = $__("div");
      $popup.addLast(frag);
      return $popup;
    });
  }, true);
  // リンクのコンテキストメニュー
  $view.on("contextmenu", function({target}) {
    var enableFlg, menuTitle;
    if (!target.matches(".message > a")) {
      return;
    }
    // リンクアドレスをNG登録
    enableFlg = !(target.hasClass("anchor") || target.hasClass("anchor_id"));
    app.ContextMenus.update("add_link_to_ngwords", {
      enabled: enableFlg,
      onclick: (info, tab) => {
        app.NG.add(target.href);
        threadContent.refreshNG();
      }
    });
    // レス番号を指定してリンクを開く
    if (app.config.isOn("enable_link_with_res_number")) {
      menuTitle = "レス番号を無視してリンクを開く";
    } else {
      menuTitle = "レス番号を指定してリンクを開く";
    }
    enableFlg = target.hasClass("open_in_rcrx") && target.dataset.paramResNum !== void 0;
    app.ContextMenus.update("open_link_with_res_number", {
      title: menuTitle,
      enabled: enableFlg,
      onclick: async(info, tab) => {
        target.setAttr("toggle-param-res-num", "on");
        await app.defer();
        target.emit(new Event("mousedown", {
          "bubbles": true
        }));
      }
    });
  });
  // 画像のコンテキストメニュー
  $view.on("contextmenu", function({target}) {
    var menuTitle;
    if (!target.matches("img, video, audio")) {
      return;
    }
    switch (target.tagName) {
      case "IMG":
        menuTitle = "画像のアドレスをNG指定";
        // リンクアドレスをNG登録
        app.ContextMenus.update("add_link_to_ngwords", {
          enabled: true,
          onclick: (info, tab) => {
            app.NG.add(target.parent().href);
            threadContent.refreshNG();
          }
        });
        break;
      case "VIDEO":
        menuTitle = "動画のアドレスをNG指定";
        break;
      case "AUDIO":
        menuTitle = "音声のアドレスをNG指定";
    }
    // メディアのアドレスをNG登録
    app.ContextMenus.update("add_media_to_ngwords", {
      title: menuTitle,
      onclick: (info, tab) => {
        app.NG.add(target.src);
        threadContent.refreshNG();
      }
    });
  });
  //何もないところをダブルクリックすると更新する
  $view.on("dblclick", function({target}) {
    if (!app.config.isOn("dblclick_reload")) {
      return;
    }
    if (!target.hasClass("message")) {
      return;
    }
    if (target.tagName === "A" || target.hasClass("thumbnail")) {
      return;
    }
    $view.emit(new Event("request_reload"));
  });
  _getExpireDateString = function(type) {
    var d, dDay, dStr, exDate, t;
    dStr = null;
    exDate = null;
    if (type === "id" || type === "slip") {
      switch (app.config.get(`ng_${type}_expire`)) {
        case "date":
          d = Date.now() + +app.config.get(`ng_${type}_expire_date`) * 86400 * 1000;
          exDate = new Date(d);
          break;
        case "day":
          t = new Date();
          dDay = +app.config.get(`ng_${type}_expire_day`) - t.getDay();
          if (dDay < 1) {
            dDay += 7;
          }
          d = Date.now() + dDay * 86400 * 1000;
          exDate = new Date(d);
      }
    }
    if (exDate) {
      dStr = exDate.getFullYear() + "/" + (exDate.getMonth() + 1) + "/" + exDate.getDate();
    }
    return dStr;
  };
  (function() {    //クイックジャンプパネル
    var $jumpPanel, jumpArticleSelector;
    jumpArticleSelector = {
      ".jump_one": "article:first-child",
      ".jump_newest": "article:last-child",
      ".jump_not_read": "article.read + article",
      ".jump_new": "article.received + article",
      ".jump_last": "article.last",
      ".jump_latest50": "article.latest50"
    };
    $jumpPanel = $view.C("jump_panel")[0];
    $view.on("read_state_attached", function() {
      var already, panelItemSelector, res, resNum, targetResSelector;
      already = {};
      for (panelItemSelector in jumpArticleSelector) {
        targetResSelector = jumpArticleSelector[panelItemSelector];
        res = $view.$(targetResSelector);
        if (res) {
          resNum = +res.C("num")[0].textContent;
        }
        if (res && !already[resNum]) {
          $jumpPanel.$(panelItemSelector).style.display = "block";
          already[resNum] = true;
        } else {
          $jumpPanel.$(panelItemSelector).style.display = "none";
        }
      }
    });
    $jumpPanel.on("click", function({target}) {
      var $res, key, offset, ref, selector, val;
      for (key in jumpArticleSelector) {
        val = jumpArticleSelector[key];
        if (!(target.matches(key))) {
          continue;
        }
        selector = val;
        offset = key === ".jump_not_read" || key === ".jump_new" ? -100 : 0;
        break;
      }
      if (!selector) {
        return;
      }
      $res = $view.$(selector);
      if ($res != null) {
        if (key === ".jump_last") {
          offset = (ref = $res.attr("last-offset")) != null ? ref : offset;
        }
        threadContent.scrollTo($res, true, +offset);
      } else {
        app.log("warn", "[view_thread] .jump_panel: ターゲットが存在しません");
      }
    });
  })();
  (function() {    //検索ボックス
    var $searchbox, searchStoredScrollTop;
    searchStoredScrollTop = null;
    $searchbox = $view.C("searchbox")[0];
    $searchbox.on("compositionend", function() {
      this.emit(new Event("input"));
    });
    $searchbox.on("input", function({
        isComposing,
        detail: {isEnter = false} = {}
      }) {
      var dom, e, hitCount, j, k, len, query, ref, ref1, scrollTop, searchRegExp, searchRegExpMode;
      if (isComposing) {
        return;
      }
      searchRegExpMode = $content.hasClass("search_regexp");
      if (searchRegExpMode && !isEnter) {
        return;
      }
      searchRegExp = null;
      if (searchRegExpMode && this.value !== "") {
        try {
          searchRegExp = new RegExp(this.value, "i");
        } catch (error1) {
          e = error1;
          app.message.send("notify", {
            message: "正規表現が正しくありません。",
            background_color: "red"
          });
          return;
        }
      }
      $content.emit(new Event("searchstart"));
      if (this.value !== "") {
        if (typeof searchStoredScrollTop !== "number") {
          searchStoredScrollTop = $content.scrollTop;
        }
        hitCount = 0;
        query = app.util.normalize(this.value);
        scrollTop = $content.scrollTop;
        $content.addClass("searching");
        ref = $content.child();
        for (j = 0, len = ref.length; j < len; j++) {
          dom = ref[j];
          if (((searchRegExp && searchRegExp.test(dom.textContent)) || app.util.normalize(dom.textContent).includes(query)) && (!dom.hasClass("ng") || dom.hasClass("disp_ng"))) {
            dom.addClass("search_hit");
            hitCount++;
          } else {
            dom.removeClass("search_hit");
          }
        }
        $content.dataset.resSearchHitCount = hitCount;
        $view.C("hit_count")[0].textContent = `${hitCount}hit`;
        if (scrollTop === $content.scrollTop) {
          $content.emit(new Event("scroll"));
        }
      } else {
        $content.removeClass("searching");
        $content.removeAttr("data-res-search-hit-count");
        ref1 = $view.C("search_hit");
        for (k = ref1.length - 1; k >= 0; k += -1) {
          dom = ref1[k];
          dom.removeClass("search_hit");
        }
        $view.C("hit_count")[0].textContent = "";
        if (typeof searchStoredScrollTop === "number") {
          $content.scrollTop = searchStoredScrollTop;
          searchStoredScrollTop = null;
        }
      }
      $content.emit(new Event("searchfinish"));
    });
    $searchbox.on("keydown", function({key}) {
      if ($content.hasClass("search_regexp")) {
        if (key === "Enter" || key === "Escape") {
          if (key === "Escape") {
            this.value = "";
          }
          this.emit(new CustomEvent("input", {
            detail: {
              isEnter: true
            }
          }));
        }
        return;
      }
      if (key === "Escape") {
        if (this.value !== "") {
          this.value = "";
          this.emit(new Event("input"));
        }
      }
    });
    // 検索モードの切り替え
    $view.on("change_search_regexp", function() {
      $content.toggleClass("search_regexp");
      $searchbox.emit(new CustomEvent("input", {
        detail: {
          isEnter: true
        }
      }));
    });
  })();
  (function() {    //フッター表示処理
    var $nextUnread, $searchNextThread, canBeShown, dom, j, len, observer, ref, setObserve, updateThreadFooter;
    canBeShown = false;
    observer = new IntersectionObserver(function(changes) {
      var boundingClientRect, j, len, rootBounds;
      for (j = 0, len = changes.length; j < len; j++) {
        ({boundingClientRect, rootBounds} = changes[j]);
        canBeShown = boundingClientRect.top < rootBounds.height;
      }
      return updateThreadFooter();
    }, {
      root: $content,
      threshold: [0, 0.05, 0.5, 0.95, 1.0]
    });
    setObserve = function() {
      var $ele, $pEle;
      observer.disconnect();
      $ele = $content.last();
      if ($ele == null) {
        return;
      }
      while (threadContent.isHidden($ele)) {
        $pEle = $ele.prev();
        if ($pEle == null) {
          break;
        }
        $ele = $pEle;
      }
      if ($ele != null) {
        observer.observe($ele);
      }
    };
    //未読ブックマーク数表示
    $nextUnread = {
      _ele: $view.C("next_unread")[0],
      show: function() {
        var bookmark, bookmarks, iframe, j, len, next, read, ref, ref1, ref2, text;
        next = null;
        bookmarks = app.bookmark.getAll().filter(function({type, url}) {
          return (type === "thread") && (url !== viewUrlStr);
        });
        //閲覧中のスレッドに新着が有った場合は優先して扱う
        if (bookmark = app.bookmark.get(viewUrlStr)) {
          bookmarks.unshift(bookmark);
        }
        for (j = 0, len = bookmarks.length; j < len; j++) {
          bookmark = bookmarks[j];
          if (!(bookmark.resCount != null)) {
            continue;
          }
          read = null;
          if (iframe = parent.$$.$(`[data-url="${bookmark.url}"]`)) {
            read = (ref = iframe.contentWindow) != null ? typeof ref.$$ === "function" ? ref.$$(".content > article").length : void 0 : void 0;
          }
          if (!read) {
            read = ((ref1 = bookmark.readState) != null ? ref1.read : void 0) || 0;
          }
          if (bookmark.resCount > read) {
            next = bookmark;
            break;
          }
        }
        if (next) {
          if (next.url === viewUrlStr) {
            text = "新着レスがあります";
          } else {
            text = `未読ブックマーク: ${next.title}`;
          }
          if (next.resCount != null) {
            text += ` (未読${next.resCount - (((ref2 = next.readState) != null ? ref2.read : void 0) || 0)}件)`;
          }
          this._ele.href = app.safeHref(next.url);
          this._ele.textContent = text;
          this._ele.dataset.title = next.title;
          this._ele.removeClass("hidden");
        } else {
          this.hide();
        }
      },
      hide: function() {
        this._ele.addClass("hidden");
      }
    };
    $searchNextThread = {
      _ele: $view.C("search_next_thread")[0],
      show: function() {
        if ($content.child().length >= 1000 || $view.C("message_bar")[0].hasClass("error") || $view.hasClass("expired") || $view.hasClass("over1000")) {
          this._ele.removeClass("hidden");
        } else {
          this.hide();
        }
      },
      hide: function() {
        this._ele.addClass("hidden");
      }
    };
    updateThreadFooter = function() {
      if (canBeShown) {
        $nextUnread.show();
        $searchNextThread.show();
      } else {
        $nextUnread.hide();
        $searchNextThread.hide();
      }
    };
    $view.on("tab_selected", function() {
      updateThreadFooter();
    });
    $view.on("view_loaded", function() {
      setObserve();
      updateThreadFooter();
    });
    $view.on("view_refreshed", function() {
      setObserve();
      updateThreadFooter();
    });
    app.message.on("bookmark_updated", function() {
      if (canBeShown) {
        $nextUnread.show();
      }
    });
    $view.on("became_expired", function() {
      updateThreadFooter();
    });
    $view.on("became_over1000", function() {
      updateThreadFooter();
    });
    ref = $view.$$(".button_tool_search_next_thread, .search_next_thread");
    //次スレ検索
    for (j = 0, len = ref.length; j < len; j++) {
      dom = ref[j];
      dom.on("click", function() {
        searchNextThread.show();
        searchNextThread.search(viewUrlStr, document.title, $content.textContent);
      });
    }
  })();
  (async function() {    //パンくずリスト表示
    var $a, boardUrl, title;
    boardUrl = viewUrl.toBoard();
    try {
      title = ((await app.BoardTitleSolver.ask(boardUrl))).replace(/板$/, "");
    } catch (error1) {
      title = "";
    }
    $a = $view.$(".breadcrumb > li > a");
    $a.href = boardUrl.href;
    $a.textContent = `${title}板`;
    $a.addClass("hidden");
    // Windows版Chromeで描画が崩れる現象を防ぐため、わざとリフローさせる。
    await app.defer();
    $view.$(".breadcrumb > li > a").style.display = "inline-block";
  })();
});

app.viewThread._draw = async function($view, {forceUpdate = false, jumpResNum = -1} = {}) {
  var $reloadButton, fn, loadCount, ok, thread, threadContent, threadGetPromise, threadSetFromCacheBeforeHTTPPromise;
  threadContent = app.DOMData.get($view, "threadContent");
  $view.addClass("loading");
  $view.style.cursor = "wait";
  $reloadButton = $view.C("button_reload")[0];
  $reloadButton.addClass("disabled");
  loadCount = 0;
  fn = async function(thread, error) {
    var $messageBar, lazyLoad;
    $messageBar = $view.C("message_bar")[0];
    if (error) {
      $messageBar.addClass("error");
      $messageBar.innerHTML = thread.message;
    } else {
      $messageBar.removeClass("error");
      $messageBar.removeChildren();
    }
    if (thread.res == null) {
      throw new Error("スレの取得に失敗しました");
    }
    document.title = thread.title;
    await threadContent.addItem(thread.res.slice($view.C("content")[0].child().length), thread.title);
    loadCount++;
    lazyLoad = app.DOMData.get($view, "lazyload");
    if (!lazyLoad.isManualLoad) {
      lazyLoad.scan();
    }
    if (!$view.hasClass("expired") && thread.expired) {
      $view.emit(new Event("became_expired"));
    }
    if (!$view.hasClass("over1000") && (threadContent.over1000ResNum != null)) {
      $view.emit(new Event("became_over1000"));
    }
    if ($view.C("content")[0].hasClass("searching")) {
      $view.C("searchbox")[0].emit(new Event("input"));
    }
    $view.emit(new CustomEvent("view_loaded", {
      detail: {jumpResNum, loadCount}
    }));
    return thread;
  };
  thread = new app.Thread($view.dataset.url);
  threadSetFromCacheBeforeHTTPPromise = Promise.resolve();
  threadGetPromise = app.util.promiseWithState(thread.get(forceUpdate, function() {
    // 通信する前にキャッシュを取得して一旦表示する
    if (!threadGetPromise.isResolved()) {
      threadSetFromCacheBeforeHTTPPromise = fn(thread, false);
    }
  }));
  try {
    await threadGetPromise.promise;
  } catch (error1) {}
  try {
    await threadSetFromCacheBeforeHTTPPromise;
  } catch (error1) {}
  try {
    await fn(thread, !threadGetPromise.isResolved());
    ok = true;
  } catch (error1) {
    ok = false;
  }
  $view.removeClass("loading");
  $view.style.cursor = "auto";
  if (!ok) {
    throw new Error("スレの表示に失敗しました");
  }
  (async function() {
    await app.wait5s();
    $reloadButton.removeClass("disabled");
  })();
  return thread;
};

app.viewThread._readStateManager = async function($view) {
  var $content, allRead, attachedReadState, boardUrlStr, doneScroll, getReadState, isScaning, onBeforezombie, readState, readStateUpdated, requestReloadFlag, scan, scanAndSave, scanCountByReloaded, scrollWatcher, threadContent, viewUrl, viewUrlStr;
  threadContent = app.DOMData.get($view, "threadContent");
  $content = $view.C("content")[0];
  viewUrlStr = $view.dataset.url;
  viewUrl = new app.URL.URL(viewUrlStr);
  viewUrlStr = viewUrl.href;
  boardUrlStr = viewUrl.toBoard().href;
  requestReloadFlag = false;
  scanCountByReloaded = 0;
  attachedReadState = {
    last: 0,
    read: 0,
    received: 0,
    offset: null
  };
  readStateUpdated = false;
  allRead = false;
  //read_stateの取得
  getReadState = (async function() {
    var _readState, bookmark, readState, ref;
    readState = {
      received: 0,
      read: 0,
      last: 0,
      url: viewUrlStr,
      offset: null,
      date: null
    };
    readStateUpdated = false;
    if (((ref = (bookmark = app.bookmark.get(viewUrlStr))) != null ? ref.readState : void 0) != null) {
      ({readState} = bookmark);
    }
    _readState = (await app.ReadState.get(viewUrlStr));
    if (app.util.isNewerReadState(readState, _readState)) {
      readState = _readState;
    }
    return {readState, readStateUpdated};
  })();
  //スレの描画時に、read_state関連のクラスを付与する
  $view.on("view_loaded", async function({
      detail: {jumpResNum, loadCount}
    }) {
    var contentChild, contentLength, readState, ref, ref1, ref10, ref11, ref12, ref13, ref14, ref15, ref16, ref17, ref2, ref3, ref4, ref5, ref6, ref7, ref8, ref9, tmpReadState;
    contentChild = $content.child();
    contentLength = contentChild.length;
    if (loadCount === 1) {
      // 初回の処理
      ({readState, readStateUpdated} = (await getReadState));
      if ((ref = $content.C("last")[0]) != null) {
        ref.removeClass("last");
      }
      if ((ref1 = $content.C("read")[0]) != null) {
        ref1.removeClass("read");
      }
      if ((ref2 = $content.C("received")[0]) != null) {
        ref2.removeClass("received");
      }
      if ((ref3 = $content.C("latest50")[0]) != null) {
        ref3.removeClass("latest50");
      }
      // キャッシュの内容が古い場合にreadStateの内容の方が大きくなることがあるので
      // その場合は次回の処理に委ねる
      if (readState.last <= contentLength) {
        if ((ref4 = contentChild[readState.last - 1]) != null) {
          ref4.addClass("last");
        }
        if ((ref5 = contentChild[readState.last - 1]) != null) {
          ref5.attr("last-offset", readState.offset);
        }
        attachedReadState.last = -1;
      } else {
        attachedReadState.last = readState.last;
        attachedReadState.offset = readState.offset;
      }
      if (readState.read <= contentLength) {
        if ((ref6 = contentChild[readState.read - 1]) != null) {
          ref6.addClass("read");
        }
        attachedReadState.read = -1;
      } else {
        attachedReadState.read = readState.read;
      }
      if (readState.received <= contentLength) {
        if ((ref7 = contentChild[readState.received - 1]) != null) {
          ref7.addClass("received");
        }
        attachedReadState.received = -1;
      } else {
        attachedReadState.received = readState.received;
      }
      if (contentLength > 50) {
        if ((ref8 = contentChild[contentLength - 51]) != null) {
          ref8.addClass("latest50");
        }
      }
      $view.emit(new CustomEvent("read_state_attached", {
        detail: {jumpResNum, requestReloadFlag, loadCount}
      }));
      if (attachedReadState.read > 0 && attachedReadState.received > 0) {
        app.message.send("read_state_updated", {
          board_url: boardUrlStr,
          read_state: readState
        });
        if (allRead) {
          readState.date = Date.now();
          app.ReadState.set(readState);
          app.bookmark.updateReadState(readState);
          readStateUpdated = false;
          allRead = false;
        }
      }
      return;
    }
    // 2回目の処理
    // 画像のロードにより位置がずれることがあるので初回処理時の内容を使用する
    tmpReadState = {
      read: null,
      received: null,
      url: viewUrlStr
    };
    if (attachedReadState.last > 0) {
      if ((ref9 = $content.C("last")[0]) != null) {
        ref9.removeClass("last");
      }
      if ((ref10 = contentChild[attachedReadState.last - 1]) != null) {
        ref10.addClass("last");
      }
      if ((ref11 = contentChild[attachedReadState.last - 1]) != null) {
        ref11.attr("last-offset", attachedReadState.offset);
      }
    }
    if (attachedReadState.read > 0) {
      if ((ref12 = $content.C("read")[0]) != null) {
        ref12.removeClass("read");
      }
      if ((ref13 = contentChild[attachedReadState.read - 1]) != null) {
        ref13.addClass("read");
      }
      tmpReadState.read = attachedReadState.read;
    }
    if (attachedReadState.received > 0) {
      if ((ref14 = $content.C("received")[0]) != null) {
        ref14.removeClass("received");
      }
      if ((ref15 = contentChild[attachedReadState.received - 1]) != null) {
        ref15.addClass("received");
      }
      tmpReadState.received = attachedReadState.received;
    }
    if (contentLength > 50) {
      if ((ref16 = $content.C("latest50")[0]) != null) {
        ref16.removeClass("latest50");
      }
      if ((ref17 = contentChild[contentLength - 51]) != null) {
        ref17.addClass("latest50");
      }
    }
    $view.emit(new CustomEvent("read_state_attached", {
      detail: {jumpResNum, requestReloadFlag, loadCount}
    }));
    if (tmpReadState.read && tmpReadState.received) {
      app.message.send("read_state_updated", {
        board_url: boardUrlStr,
        read_state: tmpReadState
      });
      if (allRead) {
        attachedReadState.date = Date.now();
        app.ReadState.set(attachedReadState);
        app.bookmark.updateReadState(attachedReadState);
        readStateUpdated = false;
        allRead = false;
      }
    }
    requestReloadFlag = false;
  });
  ({readState, readStateUpdated} = (await getReadState));
  scan = function(byScroll = false) {
    var last, lastDisplay, received;
    received = $content.child().length;
    //onbeforeunload内で呼び出された時に、この値が0になる場合が有る
    if (received === 0) {
      return;
    }
    // 既読情報が存在しない場合readState.lastは0
    if (readState.last === 0) {
      last = threadContent.getRead(1);
    } else {
      last = threadContent.getRead(readState.last);
    }
    if (requestReloadFlag && !byScroll) {
      scanCountByReloaded++;
    }
    if (readState.received < received) {
      readState.received = received;
      readStateUpdated = true;
    }
    lastDisplay = threadContent.getDisplay(last);
    if (lastDisplay) {
      if ((!requestReloadFlag || scanCountByReloaded === 1) && !lastDisplay.bottom) {
        if (readState.last !== lastDisplay.resNum || readState.offset !== lastDisplay.offset) {
          readState.last = lastDisplay.resNum;
          readState.offset = lastDisplay.offset;
          readStateUpdated = true;
        }
      } else if (readState.last !== last) {
        readState.last = last;
        readState.offset = null;
        readStateUpdated = true;
      }
    }
    if (readState.read < last) {
      readState.read = last;
      readStateUpdated = true;
      if (readState.read === received) {
        allRead = true;
      }
    }
  };
  //アンロード時は非同期系の処理をzombie.htmlに渡す
  //そのためにlocalStorageに更新するread_stateの情報を渡す
  onBeforezombie = function() {
    var data;
    scan();
    if (readStateUpdated) {
      if (localStorage.zombie_read_state != null) {
        data = JSON.parse(localStorage["zombie_read_state"]);
      } else {
        data = [];
      }
      readState.date = Date.now();
      data.push(readState);
      localStorage["zombie_read_state"] = JSON.stringify(data);
    }
  };
  parent.window.on("beforezombie", onBeforezombie);
  //スクロールされたら定期的にスキャンを実行する
  doneScroll = false;
  isScaning = false;
  scrollWatcher = setInterval(function() {
    if (!doneScroll || isScaning) {
      return;
    }
    isScaning = true;
    (async function() {
      await app.waitAF();
      scan(true);
      if (readStateUpdated) {
        app.message.send("read_state_updated", {
          board_url: boardUrlStr,
          read_state: readState
        });
      }
      if (allRead) {
        readState.date = Date.now();
        app.ReadState.set(readState);
        app.bookmark.updateReadState(readState);
        readStateUpdated = false;
        allRead = false;
      }
      isScaning = false;
    })();
    doneScroll = false;
  }, 250);
  scanAndSave = function() {
    scan();
    if (readStateUpdated) {
      readState.date = Date.now();
      app.ReadState.set(readState);
      app.bookmark.updateReadState(readState);
      readStateUpdated = false;
    }
  };
  app.message.on("request_update_read_state", function({board_url} = {}) {
    if ((board_url == null) || board_url === boardUrlStr) {
      scanAndSave();
    }
  });
  $content.on("scroll", function() {
    doneScroll = true;
  }, {
    passive: true
  });
  $view.on("request_reload", function() {
    requestReloadFlag = true;
    scanCountByReloaded = 0;
    scanAndSave();
  });
  $view.on("view_refreshed", function() {
    scanAndSave();
  });
  window.on("view_unload", function() {
    clearInterval(scrollWatcher);
    parent.window.off("beforezombie", onBeforezombie);
    //ロード中に閉じられた場合、スキャンは行わない
    if ($view.hasClass("loading")) {
      return;
    }
    scanAndSave();
  });
};
