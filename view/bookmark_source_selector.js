app.boot("/view/bookmark_source_selector.html", async function() {
  var $view, arrayOfTree, fn;
  $view = document.documentElement;
  new app.view.IframeView($view);
  $view.on("click", function({target}) {
    var ref, ref1, sourceSelector;
    if (!target.hasClass("node")) {
      return;
    }
    sourceSelector = target.closest(".view_bookmark_source_selector");
    if ((ref = sourceSelector.C("selected")[0]) != null) {
      ref.removeClass("selected");
    }
    if ((ref1 = sourceSelector.C("submit")[0]) != null) {
      ref1.disabled = false;
    }
    target.addClass("selected");
  });
  $view.C("submit")[0].on("click", function({target}) {
    var bookmarkId;
    ({bookmarkId} = (target.closest(".view_bookmark_source_selector").$(".node.selected").dataset));
    app.config.set("bookmark_id", bookmarkId);
    app.bookmarkEntryList.setRootNodeId(bookmarkId);
    parent.postMessage({
      type: "request_killme"
    }, location.origin);
  });
  fn = function(arrayOfTree, ul) {
    var children, cul, i, id, len, li, span, title;
    for (i = 0, len = arrayOfTree.length; i < len; i++) {
      ({title, id, children} = arrayOfTree[i]);
      if (!(children != null)) {
        continue;
      }
      li = $__("li");
      span = $__("span").addClass("node");
      span.textContent = title;
      span.dataset.bookmarkId = id;
      li.addLast(span);
      ul.addLast(li);
      cul = $__("ul");
      li.addLast(cul);
      fn(children, cul);
    }
  };
  arrayOfTree = (await parent.browser.bookmarks.getTree());
  fn(arrayOfTree[0].children, $view.$(".node_list > ul"));
});
