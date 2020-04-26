app.boot("/zombie.html", function() {
  var alreadyRun, close, save;
  close = async function() {
    var id;
    ({id} = (await browser.tabs.getCurrent()));
    await browser.runtime.sendMessage({
      type: "zombie_done"
    });
    await browser.tabs.remove(id);
    // Vivaldiで閉じないことがあるため遅延してもう一度閉じる
    setTimeout(async function() {
      await browser.tabs.remove(id);
    }, 1000);
  };
  save = async function() {
    var arrayOfReadState, bkarray, rs, rsarray;
    arrayOfReadState = JSON.parse(localStorage.zombie_read_state);
    app.bookmark = new app.Bookmark(app.config.get("bookmark_id"));
    try {
      await app.bookmark.promiseFirstScan;
      rsarray = (function() {
        var i, len, results;
        results = [];
        for (i = 0, len = arrayOfReadState.length; i < len; i++) {
          rs = arrayOfReadState[i];
          results.push(app.ReadState.set(rs).catch(function() {}));
        }
        return results;
      })();
      bkarray = (function() {
        var i, len, results;
        results = [];
        for (i = 0, len = arrayOfReadState.length; i < len; i++) {
          rs = arrayOfReadState[i];
          results.push(app.bookmark.updateReadState(rs));
        }
        return results;
      })();
      await Promise.all(rsarray.concat(bkarray));
    } catch (error) {}
    await app.LocalStorage.del("zombie_read_state");
    close();
    delete localStorage.zombie_read_state;
  };
  browser.runtime.sendMessage({
    type: "zombie_ping"
  });
  alreadyRun = false;
  browser.runtime.onMessage.addListener(function({type}) {
    var $script;
    if (alreadyRun || type !== "rcrx_exit") {
      return;
    }
    alreadyRun = true;
    if (localStorage.zombie_read_state != null) {
      $script = $__("script");
      $script.on("load", save);
      $script.src = "/app_core.js";
      document.head.addLast($script);
    } else {
      close();
    }
  });
});
