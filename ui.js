var UI = (function (exports) {
  'use strict';

  var AANoOverflow;

  var AANoOverflow$1 = AANoOverflow = (function() {
    var _AA_CLASS_NAME, _MINI_AA_CLASS_NAME, _SCROLL_AA_CLASS_NAME;

    class AANoOverflow {
      // minRatioはパーセント
      constructor($view, {minRatio: minRatio = 40, maxFont: maxFont = 16} = {}) {
        this.$view = $view;
        this.minRatio = minRatio;
        this.maxFont = maxFont;
        if (this.minRatio >= 100) {
          return;
        }
        this.canvasEle = $__("canvas");
        this.ctx = this.canvasEle.getContext("2d");
        this.ctx.font = this.maxFont + 'px "MS PGothic", "IPAMonaPGothic", "Konatu", "Monapo", "Textar"';
        this.$view.on("view_loaded", () => {
          this._setFontSizes();
        });
        return;
      }

      // Todo: observe resize
      _getStrLength(str) {
        // canvas上での幅(おそらくhtml上でも同様)
        return this.ctx.measureText(str).width;
      }

      _setFontSize($article, width) {
        var $message, charCountInLine, heightOld, ratio, textMaxWidth;
        $message = $article.C("message")[0];
        charCountInLine = $message.innerText.split("\n").map(this._getStrLength.bind(this));
        textMaxWidth = Math.max(...charCountInLine);
        // リセット
        $message.removeClass(_MINI_AA_CLASS_NAME, _SCROLL_AA_CLASS_NAME);
        $message.style.transform = null;
        $message.style.width = null;
        $message.style.marginBottom = null;
        if (width > textMaxWidth) {
          return;
        }
        ratio = width / textMaxWidth;
        ratio = Math.floor(ratio * 100) / 100;
        if (ratio < this.minRatio / 100) {
          ratio = this.minRatio / 100;
          $message.addClass(_SCROLL_AA_CLASS_NAME);
          $message.style.width = `${width / ratio}px`;
        }
        $message.addClass(_MINI_AA_CLASS_NAME);
        heightOld = $message.clientHeight;
        $message.style.transform = `scale(${ratio})`;
        $message.style.marginBottom = `${-(1 - ratio) * heightOld}px`;
      }

      async _setFontSizes() {
        var $aaArticles, $article, width;
        await app.waitAF();
        $aaArticles = this.$view.C("content")[0].C(_AA_CLASS_NAME);
        if (!($aaArticles.length > 0)) {
          return;
        }
        // レスの幅はすべて同じと考える
        width = this.$view.C("content")[0].C("message")[0].clientWidth;
        for ($article of $aaArticles) {
          this._setFontSize($article, width);
        }
      }

      setMiniAA($article) {
        $article.addClass(_AA_CLASS_NAME);
        this._setFontSize($article, $article.C("message")[0].clientWidth);
      }

      unsetMiniAA($article) {
        var $message;
        $article.removeClass(_AA_CLASS_NAME);
        $message = $article.C("message")[0];
        $message.removeClass(_MINI_AA_CLASS_NAME, _SCROLL_AA_CLASS_NAME);
        $message.style.transform = null;
        $message.style.width = null;
        $message.style.marginBottom = null;
      }

    }
    _AA_CLASS_NAME = "aa";

    _MINI_AA_CLASS_NAME = "mini_aa";

    _SCROLL_AA_CLASS_NAME = "scroll_aa";

    return AANoOverflow;

  }).call(window);

  var _FADE_IN_FRAMES, _FADE_OUT_FRAMES, _INVALIDED_EVENT, _TIMING, _animatingMap, _getOriginHeight, _resetAnimatingMap;

  _TIMING = {
    duration: 250,
    easing: "ease-in-out"
  };

  _FADE_IN_FRAMES = {
    opacity: [0, 1]
  };

  _FADE_OUT_FRAMES = {
    opacity: [1, 0]
  };

  _INVALIDED_EVENT = new Event("invalided");

  _getOriginHeight = function(ele) {
    var e, height;
    e = ele.cloneNode(true);
    e.style.cssText = "contain: content;\nheight: auto;\nposition: absolute;\nvisibility: hidden;\ndisplay: block;";
    document.body.appendChild(e);
    height = e.clientHeight;
    e.remove();
    return height;
  };

  _animatingMap = new WeakMap();

  _resetAnimatingMap = function(ele) {
    var ref;
    if ((ref = _animatingMap.get(ele)) != null) {
      ref.emit(_INVALIDED_EVENT);
    }
  };

  var fadeIn = async function(ele) {
    var ani;
    await app.waitAF();
    _resetAnimatingMap(ele);
    ele.removeClass("hidden");
    ani = ele.animate(_FADE_IN_FRAMES, _TIMING);
    _animatingMap.set(ele, ani);
    ani.on("finish", function() {
      _animatingMap.delete(ele);
    }, {
      once: true
    });
    return ani;
  };

  var fadeOut = function(ele) {
    var ani, invalided;
    _resetAnimatingMap(ele);
    ani = ele.animate(_FADE_OUT_FRAMES, _TIMING);
    _animatingMap.set(ele, ani);
    invalided = false;
    ani.on("invalided", function() {
      invalided = true;
    }, {
      once: true
    });
    ani.on("finish", async function() {
      if (!invalided) {
        await app.waitAF();
        ele.addClass("hidden");
        _animatingMap.delete(ele);
      }
    }, {
      once: true
    });
    return Promise.resolve(ani);
  };

  var slideDown = async function(ele) {
    var ani, h;
    await app.waitAF();
    h = _getOriginHeight(ele);
    _resetAnimatingMap(ele);
    ele.removeClass("hidden");
    ani = ele.animate({
      height: ["0px", `${h}px`]
    }, _TIMING);
    _animatingMap.set(ele, ani);
    ani.on("finish", function() {
      _animatingMap.delete(ele);
    }, {
      once: true
    });
    return ani;
  };

  var slideUp = async function(ele) {
    var ani, h, invalided;
    await app.waitAF();
    h = ele.clientHeight;
    _resetAnimatingMap(ele);
    // Firefoxでアニメーションが終了してから
    // .hiddenが付加されるまで時間がかかってチラつくため
    // heightであらかじめ消す(animateで上書きされる)
    ele.style.height = "0px";
    ani = ele.animate({
      height: [`${h}px`, "0px"]
    }, _TIMING);
    _animatingMap.set(ele, ani);
    invalided = false;
    ani.on("invalided", function() {
      invalided = true;
    }, {
      once: true
    });
    ani.on("finish", async function() {
      if (!invalided) {
        await app.waitAF();
        ele.addClass("hidden");
        ele.style.height = null;
        _animatingMap.delete(ele);
      }
    }, {
      once: true
    });
    return ani;
  };

  var Animate = /*#__PURE__*/Object.freeze({
    fadeIn: fadeIn,
    fadeOut: fadeOut,
    slideDown: slideDown,
    slideUp: slideUp
  });

  var ContextMenu, altParent, cleanup, doc, eventFn;

  altParent = null;

  cleanup = function() {
    var ref;
    if ((ref = $$.C("contextmenu_menu")[0]) != null) {
      ref.remove();
    }
    if (altParent) {
      altParent.removeClass("has_contextmenu");
      altParent.$(".popup.has_contextmenu").removeClass("has_contextmenu");
      altParent.emit(new Event("contextmenu_removed"));
      altParent = null;
    }
  };

  eventFn = function(e) {
    var ref, ref1, ref2;
    if (((ref = e.target) != null ? ref.hasClass("contextmenu_menu") : void 0) || ((ref1 = e.target) != null ? (ref2 = ref1.parent()) != null ? ref2.hasClass("contextmenu_menu") : void 0 : void 0)) {
      return;
    }
    cleanup();
  };

  doc = document.documentElement;

  doc.on("keydown", function({key}) {
    if (key === "Escape") {
      cleanup();
    }
  });

  doc.on("mousedown", eventFn);

  doc.on("contextmenu", eventFn);

  window.on("blur", function() {
    cleanup();
  });

  ContextMenu = function($menu, x, y, $parent = null) {
    var menuWidth;
    cleanup();
    $menu.addClass("contextmenu_menu");
    $menu.style.position = "fixed";
    menuWidth = $menu.offsetWidth;
    $menu.style.left = `${x}px`;
    $menu.style.top = `${y}px`;
    if ($parent) {
      altParent = $parent;
      altParent.addClass("has_contextmenu");
    }
    if (window.innerWidth < $menu.offsetLeft + menuWidth) {
      $menu.style.left = null;
      $menu.style.right = "1px";
    }
    if (window.innerHeight < $menu.offsetTop + $menu.offsetHeight) {
      $menu.style.top = `${Math.max($menu.offsetTop - $menu.offsetHeight, 0)}px`;
    }
  };

  ContextMenu.remove = function() {
    cleanup();
  };

  var ContextMenu$1 = ContextMenu;

  var Dialog, templateConfirm;

  templateConfirm = function({message, labelOk = "はい", labelNo = "いいえ"}) {
    return `<div class="dialog_spacer"></div>\n<div class="dialog_body">\n  <div class="dialog_message">${message}</div>\n  <div class="dialog_bottom">\n    <button class="dialog_ok">${labelOk}</button>\n    <button class="dialog_no">${labelNo}</button>\n  </div>\n</div>\n<div class="dialog_spacer"></div>`;
  };

  var Dialog$1 = Dialog = function(method, prop) {
    return new Promise(function(resolve, reject) {
      var $dialog;
      //prop.message, prop.labelOk, prop.labelNo
      if (method === "confirm") {
        $dialog = $__("div");
        $dialog.setClass("dialog dialog_confirm dialog_overlay");
        $dialog.innerHTML = templateConfirm(prop);
        $dialog.C("dialog_ok")[0].on("click", function() {
          $dialog.remove();
          return resolve(true);
        });
        $dialog.C("dialog_no")[0].on("click", function() {
          $dialog.remove();
          return resolve(false);
        });
        document.body.addLast($dialog);
        $dialog.C("dialog_no")[0].focus();
      } else {
        reject();
      }
    });
  };

  // @ts-ignore
  class LazyLoad {
      constructor(container) {
          this.isManualLoad = false;
          this.medias = [];
          this.pause = false;
          this.noNeedAttrs = new Set([
              "data-src",
              "data-type",
              "data-extract",
              "data-extract-referrer",
              "data-pattern",
              "data-cookie",
              "data-cookie-referrer",
              "data-referrer",
              "data-user-agent"
          ]);
          this.container = container;
          this.isManualLoad = app.config.isOn("manual_image_load");
          if (this.isManualLoad)
              return;
          this.observer = new IntersectionObserver(this.onChange.bind(this), { root: this.container, rootMargin: "10px" });
          this.container.on("scrollstart", this.onScrollStart.bind(this));
          this.container.on("scrollfinish", this.onScrollFinish.bind(this));
          this.container.on("searchstart", this.onSearchStart.bind(this));
          this.container.on("searchfinish", this.onSearchFinish.bind(this));
          this.container.on("immediateload", this.onImmediateLoad.bind(this));
          this.scan();
      }
      onChange(changes) {
          if (this.pause)
              return;
          for (const change of changes) {
              if (change.isIntersecting) {
                  this.load(change.target);
              }
          }
      }
      // スクロール中に無駄な画像ロードが発生するのを防止する
      onScrollStart() {
          this.pause = true;
      }
      onScrollFinish() {
          this.pause = false;
      }
      // 検索中に無駄な画像ロードが発生するのを防止する
      onSearchStart() {
          this.pause = true;
      }
      onSearchFinish() {
          this.pause = false;
      }
      onImmediateLoad(e) {
          this.immediateLoad(e.target);
      }
      immediateLoad(media) {
          if (media.tagName === "IMG" || media.tagName === "VIDEO") {
              if (media.dataset.src === undefined)
                  return;
              this.load(media);
          }
      }
      async load($media) {
          const imgFlg = ($media.tagName === "IMG");
          const faviconFlg = $media.hasClass("favicon");
          // immediateLoadにて処理済みのものを除外する
          if ($media.dataset.src === undefined)
              return;
          const $newImg = $__("img");
          if (imgFlg && !faviconFlg) {
              const attrs = Array.from($media.attributes);
              for (const { name, value } of attrs) {
                  if (!this.noNeedAttrs.has(name)) {
                      $newImg.setAttr(name, value);
                  }
              }
          }
          const load = ({ type, currentTarget }) => {
              $newImg.off("load", load);
              $newImg.off("error", load);
              $media.parent().replaceChild(currentTarget, $media);
              if (type === "load") {
                  fadeIn(currentTarget);
              }
          };
          $newImg.on("load", load);
          $newImg.on("error", load);
          const loadmetadata = e => {
              if (imgFlg && (faviconFlg || $media.hasClass("loading"))) {
                  return;
              }
              $media.off("loadedmetadata", loadmetadata);
              $media.off("error", loadmetadata);
          };
          $media.on("loadedmetadata", loadmetadata);
          $media.on("error", loadmetadata);
          const mdata = $media.dataset;
          if (imgFlg && !faviconFlg) {
              $media.src = "/img/loading.webp";
              switch (mdata.type) {
                  case "default":
                      $newImg.src = mdata.src;
                      break;
                  case "referrer":
                      $newImg.src = this.getWithReferrer(mdata.src, mdata.referrer, mdata.userAgent);
                      break;
                  case "extract":
                      try {
                          $newImg.src = await this.getWithExtract(mdata.src, mdata.extract, mdata.pattern, mdata.extractReferrer, mdata.userAgent);
                      }
                      catch (_a) {
                          $newImg.src = "";
                      }
                      break;
                  case "cookie":
                      try {
                          $newImg.src = await this.getWithCookie(mdata.src, mdata.cookie, mdata.cookieReferrer, mdata.userAgent);
                      }
                      catch (_b) {
                          $newImg.src = "";
                      }
                      break;
                  default: $newImg.src = mdata.src;
              }
          }
          else {
              $media.src = $media.dataset.src;
          }
          $media.removeAttr("data-src");
          if (!this.isManualLoad) {
              this.observer.unobserve($media);
          }
      }
      scan() {
          this.medias = Array.from(this.container.$$("img[data-src], audio[data-src], video[data-src]"));
          for (const media of this.medias) {
              this.observer.observe(media);
          }
      }
      getWithReferrer(link, referrer, userAgent, cookie = "") {
          //TODO: use browser.webRequest, browser.cookies
          //if(referrer !== ""){ req.setRequestHeader("Referer", referrer); }
          //if(userAgent !== ""){ req.setRequestHeader("User-Agent", userAgent); }
          //if(cookie !== ""){ req.setRequestHeader("Set-Cookie", cookie); }
          return link;
      }
      async getWithCookie(link, cookieLink, referrer, userAgent) {
          const req = new app.HTTP.Request("GET", cookieLink);
          //TODO: use browser.webRequest
          //if(referrer !== ""){ req.headers["Referer"] = referrer); }
          //if(userAgent !== ""){ req.headers["User-Agent"] = userAgent; }
          try {
              const res = await req.send();
              if (res.status === 200) {
                  const cookie = res.headers["Set-Cookie"];
                  return this.getWithReferrer(link, "", userAgent, cookie);
              }
          }
          catch (_a) { }
          throw new Error("通信に失敗しました");
      }
      async getWithExtract(link, extractLink, pattern, referrer, userAgent) {
          const req = new app.HTTP.Request("GET", extractLink);
          //TODO: use browser.webRequest
          //if(referrer !== ""){ req.headers["Referer"] = referrer); }
          //if(userAgent !== ""){ req.headers["User-Agent"] = userAgent; }
          try {
              const res = await req.send();
              if (res.status === 200) {
                  const m = res.body.match(new RegExp(pattern));
                  if (m !== null) {
                      return link.replace(/\$EXTRACT(\d+)?/g, (str, n) => {
                          return (n === null) ? m[1] : m[n];
                      });
                  }
              }
          }
          catch (_a) { }
          throw new Error("通信に失敗しました");
      }
  }

  /**
  @class MediaContainer
  @constructor
  @param {Element} container
  */
  var MediaContainer;

  var MediaContainer$1 = MediaContainer = class MediaContainer {
    constructor(container) {
      this.container = container;
      /**
      @property _videoPlayTime
      @type Number
      @private
      */
      this._videoPlayTime = 0;
      this.setVideoEvents();
      this.setHoverEvents();
      return;
    }

    /**
    @method setHoverEvents
    */
    setHoverEvents() {
      var imageRatio, isImageOn, isVideoOn, videoRatio;
      isImageOn = app.config.isOn("hover_zoom_image");
      isVideoOn = app.config.isOn("hover_zoom_video");
      imageRatio = app.config.get("zoom_ratio_image") / 100;
      videoRatio = app.config.get("zoom_ratio_video") / 100;
      this.container.on("mouseenter", function({target}) {
        var zoomWidth;
        if (!target.matches(".thumbnail > a > img.image, .thumbnail > video")) {
          return;
        }
        if (isImageOn && target.tagName === "IMG") {
          zoomWidth = parseInt(target.offsetWidth * imageRatio);
        } else if (isVideoOn && target.tagName === "VIDEO") {
          // Chromeでmouseenterイベントが複数回発生するのを回避するため
          {
            if (target.style.width !== "") {
              return;
            }
          }
          zoomWidth = parseInt(target.offsetWidth * videoRatio);
        } else {
          return;
        }
        target.closest(".thumbnail").addClass("zoom");
        target.style.width = `${zoomWidth}px`;
        target.style.maxWidth = null;
        target.style.maxHeight = null;
      }, true);
      this.container.on("mouseleave", function({target}) {
        if (!(target.matches(".thumbnail > a > img.image, .thumbnail > video") && ((isImageOn && target.tagName === "IMG") || (isVideoOn && target.tagName === "VIDEO")))) {
          return;
        }
        target.closest(".thumbnail").removeClass("zoom");
        target.style.width = null;
        if (target.tagName === "IMG") {
          target.style.maxWidth = `${app.config.get("image_width")}px`;
          target.style.maxHeight = `${app.config.get("image_height")}px`;
        } else if (target.tagName === "VIDEO") {
          target.style.maxWidth = `${app.config.get("video_width")}px`;
          target.style.maxHeight = `${app.config.get("video_height")}px`;
        }
      }, true);
    }

    /**
    @method setVideoEvents
    */
    setVideoEvents() {
      // VIDEOの再生/一時停止
      this.container.on("click", function({target}) {
        if (!target.matches(".thumbnail > video:not([data-src])")) {
          return;
        }
        if (target.preload === "metadata") {
          target.preload = "auto";
        }
        if (target.paused) {
          target.play();
        } else {
          target.pause();
        }
      });
      // VIDEO再生中はマウスポインタを消す
      this.container.on("mouseenter", ({target}) => {
        var func;
        if (!target.matches(".thumbnail > video:not([data-src])")) {
          return;
        }
        func = ({type}) => {
          this._controlVideoCursor(target, type);
        };
        target.on("play", func);
        target.on("timeupdate", func);
        target.on("pause", func);
        target.on("ended", func);
      }, true);
      // マウスポインタのリセット
      this.container.on("mousemove", ({target, type}) => {
        if (!target.matches(".thumbnail > video:not([data-src])")) {
          return;
        }
        this._controlVideoCursor(target, type);
      });
    }

    /**
    @method _setImageBlurOne
    @param {Element} thumbnail
    @param {Boolean} blurMode
    @static
    @private
    */
    static _setImageBlurOne(thumbnail, blurMode) {
      var media, v;
      media = thumbnail.$("a > img.image, video");
      if (blurMode) {
        v = app.config.get("image_blur_length");
        thumbnail.addClass("image_blur");
        media.style.WebkitFilter = `blur(${v}px)`;
      } else {
        thumbnail.removeClass("image_blur");
        media.style.WebkitFilter = "none";
      }
    }

    /**
    @method setImageBlur
    @param {Element} res
    @param {Boolean} blurMode
    @static
    */
    static setImageBlur(res, blurMode) {
      var i, len, ref, thumb;
      ref = res.$$(".thumbnail[media-type='image'], .thumbnail[media-type='video']");
      for (i = 0, len = ref.length; i < len; i++) {
        thumb = ref[i];
        MediaContainer._setImageBlurOne(thumb, blurMode);
      }
    }

    /**
    @method _controlVideoCursor
    @param {Element} ele
    @param {String} act
    @private
    */
    _controlVideoCursor(ele, act) {
      switch (act) {
        case "play":
          this._videoPlayTime = Date.now();
          break;
        case "timeupdate":
          if (ele.style.cursor === "none") {
            return;
          }
          if (Date.now() - this._videoPlayTime > 2000) {
            ele.style.cursor = "none";
          }
          break;
        case "pause":
        case "ended":
          ele.style.cursor = "auto";
          this._videoPlayTime = 0;
          break;
        case "mousemove":
          if (this._videoPlayTime === 0) {
            return;
          }
          ele.style.cursor = "auto";
          this._videoPlayTime = Date.now();
      }
    }

  };

  var PopupView;

  /**
  @class PopupView
  @constructor
  @param {Element} defaultParent
  */
  var PopupView$1 = PopupView = class PopupView {
    constructor(defaultParent) {
      /**
      @method _onMouseEnter
      @param {Object} Event
      */
      this._onMouseEnter = this._onMouseEnter.bind(this);
      /**
      @method _onMouseLeave
      @param {Object} Event
      */
      this._onMouseLeave = this._onMouseLeave.bind(this);
      /**
      @method _onMouseMove
      @param {Object} Event
      */
      this._onMouseMove = this._onMouseMove.bind(this);
      /**
      @method _onRemoveContextmenu
      */
      this._onRemoveContextmenu = this._onRemoveContextmenu.bind(this);
      this.defaultParent = defaultParent;
      /**
      @property _popupStack
      @type Array
      @private
      */
      this._popupStack = [];
      /**
      @property _popupArea
      @type Object
      @private
      */
      this._popupArea = this.defaultParent.C("popup_area")[0];
      /**
      @property _popupStyle
      @type Object
      @private
      */
      this._popupStyle = null;
      /**
      @property _popupMarginHeight
      @type Number
      @private
      */
      this._popupMarginHeight = -1;
      /**
      @property _currentX
      @type Number
      @private
      */
      this._currentX = 0;
      /**
      @property _currentY
      @type Number
      @private
      */
      this._currentY = 0;
      /**
      @property _delayTime
      @type Number
      @private
      */
      this._delayTime = parseInt(app.config.get("popup_delay_time"));
      /**
      @property _delayTimeoutID
      @type Number
      @private
      */
      this._delayTimeoutID = 0;
      /**
      @property _delayRemoveTimeoutID
      @type Number
      @private
      */
      this._delayRemoveTimeoutID = 0;
      return;
    }

    /**
    @method show
    @param {Element} popup
    @param {Number} mouseX
    @param {Number} mouseY
    @param {Element} source
    */
    async show(popup1, mouseX, mouseY, source1) {
      var popupInfo, setDispPosition, setupNewNode;
      this.popup = popup1;
      this.mouseX = mouseX;
      this.mouseY = mouseY;
      this.source = source1;
      // 同一ソースからのポップアップが既に有る場合は、処理を中断
      if (this._popupStack.length > 0) {
        popupInfo = this._popupStack[this._popupStack.length - 1];
        if (this.source === popupInfo.source) {
          return;
        }
      }
      // sourceがpopup内のものならば、兄弟ノードの削除
      // それ以外は、全てのノードを削除
      if (this.source.closest(".popup")) {
        this.source.closest(".popup").addClass("active");
        this._remove(false);
      } else {
        this._remove(true);
      }
      // 待機中の処理があればキャンセルする
      if (this._delayTimeoutID !== 0) {
        clearTimeout(this._delayTimeoutID);
        this._delayTimeoutID = 0;
      }
      // コンテキストメニューの破棄
      ContextMenu$1.remove();
      // 表示位置の決定
      setDispPosition = (popupNode) => {
        var bodyHeight, bodyWidth, cssBottom, cssTop, cursorTop, margin, maxWidth, outerHeight, space, viewHeight, viewTop;
        margin = 20;
        ({
          offsetHeight: bodyHeight,
          offsetWidth: bodyWidth
        } = document.body);
        viewTop = this.defaultParent.$(".nav_bar").offsetHeight;
        viewHeight = bodyHeight - viewTop;
        maxWidth = bodyWidth - margin * 2;
        // カーソルの上下左右のスペースを測定
        space = {
          left: this.mouseX,
          right: bodyWidth - this.mouseX,
          top: this.mouseY,
          bottom: bodyHeight - this.mouseY
        };
        // 通常はカーソル左か右のスペースを用いるが、そのどちらもが狭い場合は上下に配置する
        if (Math.max(space.left, space.right) > 400) {
          // 例え右より左が広くても、右に十分なスペースが有れば右に配置
          if (space.right > 350) {
            popupNode.style.left = `${space.left + margin}px`;
            popupNode.style.maxWidth = `${maxWidth - space.left}px`;
          } else {
            popupNode.style.right = `${space.right + margin}px`;
            popupNode.style.maxWidth = `${maxWidth - space.right}px`;
          }
          cursorTop = Math.max(space.top, viewTop + margin * 2);
          outerHeight = this._getOuterHeight(popupNode, true);
          if (viewHeight > outerHeight + margin) {
            cssTop = Math.min(cursorTop, bodyHeight - outerHeight) - margin;
          } else {
            cssTop = viewTop + margin;
          }
          popupNode.style.top = `${cssTop}px`;
          popupNode.style.maxHeight = `${bodyHeight - cssTop - margin}px`;
        } else {
          popupNode.style.left = `${margin}px`;
          popupNode.style.maxWidth = `${maxWidth}px`;
          // 例え上より下が広くても、上に十分なスペースが有れば上に配置
          if (space.top > Math.min(350, space.bottom)) {
            cssBottom = Math.max(space.bottom, margin);
            popupNode.style.bottom = `${cssBottom}px`;
            popupNode.style.maxHeight = `${viewHeight - cssBottom - margin}px`;
          } else {
            cssTop = bodyHeight - space.bottom + margin;
            popupNode.style.top = `${cssTop}px`;
            popupNode.style.maxHeight = `${viewHeight - cssTop - margin}px`;
          }
        }
      };
      // マウス座標とコンテキストメニューの監視
      if (this._popupStack.length === 0) {
        this._currentX = this.mouseX;
        this._currentY = this.mouseY;
        this.defaultParent.on("mousemove", this._onMouseMove);
        this._popupArea.on("contextmenu_removed", this._onRemoveContextmenu);
      }
      // 新規ノードの設定
      setupNewNode = (sourceNode, popupNode) => {
        // CSSContainmentの恩恵を受けるために表示位置決定前にクラスを付加する
        popupNode.addClass("popup");
        // 表示位置の決定
        setDispPosition(popupNode);
        // ノードの設定
        sourceNode.addClass("popup_source");
        sourceNode.setAttr("stack-index", this._popupStack.length);
        sourceNode.on("mouseenter", this._onMouseEnter);
        sourceNode.on("mouseleave", this._onMouseLeave);
        if (app.config.get("aa_font") === "aa") {
          popupNode.addClass("config_use_aa_font");
        }
        popupNode.setAttr("stack-index", this._popupStack.length);
        popupNode.on("mouseenter", this._onMouseEnter);
        popupNode.on("mouseleave", this._onMouseLeave);
        // リンク情報の保管
        popupInfo = {
          source: sourceNode,
          popup: popupNode
        };
        this._popupStack.push(popupInfo);
      };
      // 即時表示の場合
      if (this._delayTime < 100) {
        // 新規ノードの設定
        setupNewNode(this.source, this.popup);
        // popupの表示
        this._popupArea.addLast(this.popup);
        // ノードのアクティブ化
        await app.defer();
        this._activateNode();
      } else {
        // 遅延表示の場合
        ((sourceNode, popupNode) => {
          this._delayTimeoutID = setTimeout(() => {
            var ele;
            this._delayTimeoutID = 0;
            // マウス座標がポップアップ元のままの場合のみ実行する
            ele = document.elementFromPoint(this._currentX, this._currentY);
            if (ele === sourceNode) {
              // 新規ノードの設定
              setupNewNode(sourceNode, popupNode);
              // ノードのアクティブ化
              sourceNode.addClass("active");
              // popupの表示
              return this._popupArea.addLast(popupNode);
            }
          }, this._delayTime);
        })(this.source, this.popup);
      }
    }

    /**
    @method _remove
    @param {Boolean} forceRemove
    */
    _remove(forceRemove) {
      var i, popup, ref, source;
      if (this._popupArea.hasClass("has_contextmenu")) {
        return;
      }
      ref = this._popupStack;
      for (i = ref.length - 1; i >= 0; i += -1) {
        ({popup, source} = ref[i]);
        if (!forceRemove && (source.hasClass("active") || popup.hasClass("active"))) {
          // 末端の非アクティブ・ノードを選択
          break;
        }
        // 該当ノードの除去
        source.off("mouseenter", this._onMouseEnter);
        source.off("mouseleave", this._onMouseLeave);
        popup.off("mouseenter", this._onMouseEnter);
        popup.off("mouseleave", this._onMouseLeave);
        source.removeClass("popup_source");
        source.removeAttr("stack-index");
        popup.remove();
        this._popupStack.pop();
        // コンテキストメニューの破棄
        if (this._popupArea.hasClass("has_contextmenu")) {
          ContextMenu$1.remove();
        }
      }
      // マウス座標とコンテキストメニューの監視終了
      if (this._popupStack.length === 0) {
        this.defaultParent.off("mousemove", this._onMouseMove);
        this._popupArea.off("contextmenu_removed", this._onRemoveContextmenu);
      }
    }

    /**
    @method _delayRemove
    @param {Boolean} forceRemove
    */
    _delayRemove(forceRemove) {
      if (this._delayRemoveTimeoutID !== 0) {
        clearTimeout(this._delayRemoveTimeoutID);
      }
      this._delayRemoveTimeoutID = setTimeout(() => {
        this._delayRemoveTimeoutID = 0;
        return this._remove(forceRemove);
      }, 300);
    }

    _onMouseEnter({
        currentTarget: target
      }) {
      var stackIndex;
      target.addClass("active");
      // ペア・ノードの非アクティブ化
      stackIndex = target.getAttr("stack-index");
      if (target.hasClass("popup")) {
        this._popupStack[stackIndex].source.removeClass("active");
      } else if (target.hasClass("popup_source")) {
        this._popupStack[stackIndex].popup.removeClass("active");
      }
      // 末端ノードの非アクティブ化
      if (this._popupStack.length - 1 > stackIndex) {
        this._popupStack[this._popupStack.length - 1].source.removeClass("active");
        this._popupStack[this._popupStack.length - 1].popup.removeClass("active");
        this._delayRemove(false);
      }
    }

    _onMouseLeave({
        currentTarget: target
      }) {
      target.removeClass("active");
      if (this._popupArea.hasClass("has_contextmenu")) {
        return;
      }
      this._delayRemove(false);
    }

    _onMouseMove({clientX, clientY}) {
      this._currentX = clientX;
      this._currentY = clientY;
    }

    /**
    @method _activateNode
    */
    _activateNode() {
      var ele;
      ele = document.elementFromPoint(this._currentX, this._currentY);
      if (ele === this.source) {
        this.source.addClass("active");
      } else if ((ele === this.popup) || (ele.closest(".popup") === this.popup)) {
        this.popup.addClass("active");
      } else if (ele.hasClass("popup_source") || ele.hasClass("popup")) {
        ele.addClass("active");
      } else if (ele.closest(".popup")) {
        ele.closest(".popup").addClass("active");
      } else {
        this.source.removeClass("active");
        this.popup.removeClass("active");
        this._delayRemove(false);
      }
    }

    _onRemoveContextmenu() {
      this._activateNode();
      this._remove(false);
    }

    /**
    @method _getOuterHeight
    @param {Object} ele
    @param {Boolean} margin
    */
    // .outerHeight()の代用関数
    _getOuterHeight(ele, margin = false) {
      var boxShadow, outerHeight, tmp;
      // 下層に表示してoffsetHeightを取得する
      ele.style.zIndex = "-1";
      this._popupArea.addLast(ele);
      outerHeight = ele.offsetHeight;
      ele.remove();
      ele.style.zIndex = "3"; // ソースでは"3"だが、getComputedStyleでは"0"になるため
      // 表示済みのノードが存在すればCSSの値を取得する
      if (this._popupStyle === null && this._popupStack.length > 0) {
        this._popupStyle = getComputedStyle(this._popupStack[0].popup, null);
      }
      // margin等の取得
      if (margin && this._popupStyle !== null) {
        if (this._popupMarginHeight < 0) {
          this._popupMarginHeight = 0;
          this._popupMarginHeight += parseInt(this._popupStyle.marginTop);
          this._popupMarginHeight += parseInt(this._popupStyle.marginBottom);
          boxShadow = this._popupStyle.boxShadow;
          tmp = /rgba?\(.*\) (-?[\d]+)px (-?[\d]+)px ([\d]+)px (-?[\d]+)px/.exec(boxShadow);
          this._popupMarginHeight += Math.abs(parseInt(tmp[2]));
          this._popupMarginHeight += Math.abs(parseInt(tmp[4]));
        }
        outerHeight += this._popupMarginHeight;
      }
      ele.style.zIndex = null;
      return outerHeight;
    }

  };

  // @ts-ignore
  class SearchNextThread {
      constructor($element) {
          this.$element = $element;
          this.$element.C("close")[0].on("click", () => {
              this.hide();
          });
      }
      show() {
          fadeIn(this.$element);
      }
      hide() {
          fadeOut(this.$element);
      }
      async search(url, title, resString) {
          const $ol = this.$element.T("ol")[0];
          $ol.innerHTML = "";
          this.$element.C("current")[0].textContent = title;
          this.$element.C("status")[0].textContent = "検索中";
          try {
              const res = await app.util.searchNextThread(url, title, resString);
              for (const thread of res) {
                  const $li = $__("li").addClass("open_in_rcrx");
                  $li.textContent = thread.title;
                  $li.dataset.href = thread.url;
                  $ol.addLast($li);
                  if (app.bookmark.get(thread.url)) {
                      $li.addClass("bookmarked");
                  }
              }
              this.$element.C("status")[0].textContent = "";
          }
          catch (_a) {
              this.$element.C("status")[0].textContent = "次スレ検索に失敗しました";
          }
      }
  }

  // @ts-ignore
  class Accordion {
      constructor($element) {
          this.$element = $element;
          this.$element.addClass("accordion");
          const openAccordions = this.$element.C("accordion_open");
          for (let i = openAccordions.length - 1; i >= 0; i--) {
              openAccordions[i].removeClass("accordion_open");
          }
          this.$element.on("click", ({ target }) => {
              if (target.parent() === this.$element && target.tagName === "H3") {
                  if (target.hasClass("accordion_open")) {
                      this.close(target);
                  }
                  else {
                      this.open(target);
                  }
              }
          });
      }
      update() {
          for (const dom of this.$element.$$("h3 + *")) {
              dom.addClass("hidden");
          }
          this.setOpen(this.$element.$("h3"));
      }
      setOpen($header) {
          $header.addClass("accordion_open");
          $header.next().removeClass("hidden");
      }
      open($header) {
          $header.addClass("accordion_open");
          slideDown($header.next());
          for (const dom of $header.parent().child()) {
              if (dom !== $header && dom.hasClass("accordion_open")) {
                  this.close(dom);
              }
          }
      }
      close($header) {
          $header.removeClass("accordion_open");
          slideUp($header.next());
      }
  }

  /*
  .select対応のAccordion。
  Accordionと違って汎用性が無い。
  */
  class SelectableAccordion extends Accordion {
      constructor($element) {
          super($element);
          this.$element.on("click", () => {
              const selected = this.$element.C("selected");
              if (selected.length > 0) {
                  selected[0].removeClass("selected");
              }
          });
      }
      getSelected() {
          return this.$element.$("h3.selected, a.selected") || null;
      }
      select(target) {
          this.clearSelect();
          if (target.tagName === "H3") {
              this.close(target);
          }
          else if (target.tagName === "A") {
              const targetHeader = target.parent().parent().prev();
              if (!targetHeader.hasClass("accordion_open")) {
                  this.open(targetHeader);
              }
          }
          target.addClass("selected");
          target.scrollIntoView({ behavior: "instant", block: "center", inline: "center" });
      }
      clearSelect() {
          const selected = this.getSelected();
          if (selected) {
              selected.removeClass("selected");
          }
      }
      selectNext(repeat = 1) {
          let current = this.getSelected();
          if (current) {
              for (let key = 0; key < repeat; key++) {
                  const prevCurrent = current;
                  if (current.tagName === "A" && current.parent().next()) {
                      current = current.parent().next().first();
                  }
                  else {
                      let currentH3 = current;
                      if (current.tagName === "A") {
                          currentH3 = current.parent().parent().prev();
                      }
                      let nextH3 = currentH3.next();
                      while (nextH3 && nextH3.tagName !== "H3") {
                          nextH3 = nextH3.next();
                      }
                      if (nextH3) {
                          if (nextH3.hasClass("accordion_open")) {
                              current = nextH3.next().$("li > a");
                          }
                          else {
                              current = nextH3;
                          }
                      }
                  }
                  if (current === prevCurrent) {
                      break;
                  }
              }
          }
          else {
              current = this.$element.$(".accordion_open + ul a");
              current = current || this.$element.$("h3");
          }
          if (current && current !== this.getSelected()) {
              this.select(current);
          }
      }
      selectPrev(repeat = 1) {
          let current = this.getSelected();
          if (current) {
              for (let key = 0; key < repeat; key++) {
                  const prevCurrent = current;
                  if (current.tagName === "A" && current.parent().prev()) {
                      current = current.parent().prev().first();
                  }
                  else {
                      let currentH3 = current;
                      if (current.tagName === "A") {
                          currentH3 = current.parent().parent().prev();
                      }
                      let prevH3 = currentH3.prev();
                      while (prevH3 && prevH3.tagName !== "H3") {
                          prevH3 = prevH3.prev();
                      }
                      if (prevH3) {
                          if (prevH3.hasClass("accordion_open")) {
                              current = prevH3.next().$("li:last-child > a");
                          }
                          else {
                              current = prevH3;
                          }
                      }
                  }
                  if (current === prevCurrent) {
                      break;
                  }
              }
          }
          else {
              current = this.$element.$(".accordion_open + ul a");
              current = current || this.$element.$("h3");
          }
          if (current && current !== this.getSelected()) {
              this.select(current);
          }
      }
  }

  class Sortable {
      constructor(container, option = {}) {
          this.isSorting = false;
          //ドラッグ開始時の場所
          this.start = null;
          //ドラッグ中の場所
          this.last = null;
          //ドラッグしているDOM
          this.target = null;
          //ドラッグしているDOMの戻るときの中央座標
          this.targetCenter = null;
          // requestAnimationFrameId
          this.rAFId = 0;
          this.clicks = 1;
          this.clickTimer = 0;
          this.animate = this._animate.bind(this);
          this.container = container;
          this.option = option;
          this.container.addClass("sortable");
          this.overlay = $__("div").addClass("sortable_overlay");
          this.overlay.on("contextmenu", this.onContextMenu);
          this.container.on("mousedown", this.onMousedown.bind(this));
          this.overlay.on("mousemove", this.onMove.bind(this));
          this.overlay.on("mouseup", this.onFinish.bind(this));
          this.overlay.on("mouseout", this.onFinish.bind(this));
      }
      setTarget(target) {
          this.target = target;
          this.target.addClass("sortable_dragging");
          this.target.style["will-change"] = "transform";
          this.targetCenter = {
              x: target.offsetLeft + target.offsetWidth / 2,
              y: target.offsetTop + target.offsetHeight / 2
          };
      }
      removeTarget() {
          if (!this.target)
              return;
          this.target.removeClass("sortable_dragging");
          this.target.style.transform = null;
          this.target.style["will-change"] = null;
          this.target = null;
          this.targetCenter = null;
      }
      changeStart(func) {
          const beforeLeft = this.target.offsetLeft;
          const beforeTop = this.target.offsetTop;
          func();
          const diffX = this.target.offsetLeft - beforeLeft;
          const diffY = this.target.offsetTop - beforeTop;
          this.start = {
              x: this.start.x + diffX,
              y: this.start.y + diffY
          };
          this.targetCenter = {
              x: this.targetCenter.x + diffX,
              y: this.targetCenter.y + diffY
          };
      }
      onMousedown({ target, button }) {
          if (target === this.container)
              return;
          if (button !== 0)
              return;
          if (this.option.exclude &&
              target.matches(this.option.exclude))
              return;
          if (this.clickTimer !== 0) {
              clearTimeout(this.clickTimer);
          }
          // 0.5秒待ってダブルクリックかシングルクリックか判定する
          this.clickTimer = window.setTimeout(() => {
              this.clicks = 1;
          }, 500);
          if (this.clicks === 1) {
              this.onStart(target);
              this.clicks = 1;
          }
          else if (this.clicks === 2) {
              this.clicks = 1;
          }
          this.clicks++;
      }
      onStart(target) {
          if (!target)
              return;
          while (target.parent() !== this.container) {
              target = target.parent();
          }
          this.setTarget(target);
          document.body.addLast(this.overlay);
      }
      onMove({ pageX, pageY }) {
          if (!this.isSorting) {
              this.start = {
                  x: pageX,
                  y: pageY
              };
              this.isSorting = true;
          }
          if (!this.target)
              return;
          this.last = {
              x: pageX,
              y: pageY
          };
          if (this.rAFId === 0) {
              this.animate();
          }
      }
      _animate() {
          let tmp = this.container.first();
          let diffX = this.last.x - this.start.x;
          let diffY = this.last.y - this.start.y;
          // もっているものの中央座標
          const x = this.targetCenter.x + diffX;
          const y = this.targetCenter.y + diffY;
          while (tmp) {
              const { offsetLeft: tLeft, offsetTop: tTop, offsetWidth: tWidth, offsetHeight: tHeight } = tmp;
              if (tmp !== this.target &&
                  !(x < tLeft || y < tTop || x > tLeft + tWidth || y > tTop + tHeight)) {
                  if (this.target.compareDocumentPosition(tmp) === 4 &&
                      (x > tLeft + tWidth / 2 || y > tTop + tHeight / 2)) {
                      this.changeStart(() => {
                          tmp.addAfter(this.target);
                      });
                  }
                  else if (x < tLeft + tWidth / 2 || y < tTop + tHeight / 2) {
                      this.changeStart(() => {
                          tmp.addBefore(this.target);
                      });
                  }
                  diffX = this.last.x - this.start.x;
                  diffY = this.last.y - this.start.y;
                  break;
              }
              tmp = tmp.next();
          }
          this.target.style.transform = `translate(${diffX}px, ${diffY}px)`;
          this.rAFId = requestAnimationFrame(this.animate);
      }
      onFinish() {
          // removeするとmouseoutも発火するので二重に呼ばれる
          this.isSorting = false;
          if (this.rAFId !== 0) {
              cancelAnimationFrame(this.rAFId);
              this.rAFId = 0;
          }
          if (this.target) {
              this.removeTarget();
              this.overlay.remove();
          }
      }
      onContextMenu(e) {
          e.preventDefault();
      }
  }

  class VirtualNotch {
      constructor(element, threshold = 100) {
          this.element = element;
          this.threshold = threshold;
          this.wheelDelta = 0;
          this.lastMouseWheel = Date.now();
          this.element.on("wheel", this.onMouseWheel.bind(this), { passive: true });
          setInterval(this.onInterval.bind(this), 500);
      }
      onInterval() {
          if (this.lastMouseWheel < Date.now() - 500) {
              this.wheelDelta = 0;
          }
      }
      onMouseWheel(e) {
          switch (e.deltaMode) {
              case WheelEvent.DOM_DELTA_PIXEL:
                  this.wheelDelta += e.deltaY + e.deltaX;
                  break;
              case WheelEvent.DOM_DELTA_LINE:
                  this.wheelDelta += e.deltaY * 40 + e.deltaX * 40;
                  break;
              case WheelEvent.DOM_DELTA_PAGE:
                  this.wheelDelta += e.deltaY * 120 + e.deltaX * 120;
                  break;
              default:
                  this.wheelDelta += e.deltaY + e.deltaX;
                  return;
          }
          this.lastMouseWheel = Date.now();
          while (Math.abs(this.wheelDelta) >= this.threshold) {
              const event = new MouseEvent("notchedmousewheel");
              event.wheelDelta = this.threshold * Math.sign(this.wheelDelta);
              this.wheelDelta -= event.wheelDelta;
              this.element.emit(event);
          }
      }
  }

  class Tab {
      constructor($element) {
          this.$element = $element;
          this.recentClosed = [];
          this.historyStore = new Map();
          const $ele = this.$element.addClass("tab");
          const $ul = $__("ul").addClass("tab_tabbar");
          $ul.on("notchedmousewheel", (e) => {
              if (app.config.isOn("mousewheel_change_tab")) {
                  e.preventDefault();
                  const tmp = (e.wheelDelta < 0) ? "prev" : "next";
                  const next = (this.$element.$("li.tab_selected") || {})[tmp]();
                  if (next) {
                      this.update(next.dataset.tabid, { selected: true });
                  }
              }
          });
          $ul.on("mousedown", (e) => {
              if (e.target.tagName === "IMG") {
                  e.preventDefault();
                  return;
              }
              const target = e.target.closest("li");
              if (target === null)
                  return;
              if (e.button === 2)
                  return;
              if (e.button === 1 && !target.hasClass("tab_locked")) {
                  this.remove(target.dataset.tabid);
              }
              else {
                  this.update(target.dataset.tabid, { selected: true });
              }
          });
          $ul.on("click", ({ target }) => {
              if (target.tagName === "IMG") {
                  this.remove(target.parent().dataset.tabid);
              }
          });
          new VirtualNotch($ul);
          const $div = $__("div").addClass("tab_container");
          $ele.addLast($ul, $div);
          window.on("message", ({ origin, data: message, source }) => {
              if (origin !== location.origin)
                  return;
              if (![
                  "requestTabHistory",
                  "requestTabBack",
                  "requestTabForward"
              ].includes(message.type)) {
                  return;
              }
              if (!this.$element.contains(source.frameElement)) {
                  return;
              }
              const tabId = source.frameElement.dataset.tabid;
              const history = this.historyStore.get(tabId);
              switch (message.type) {
                  case "requestTabHistory":
                      source.postMessage({
                          type: "responseTabHistory",
                          history
                      }, origin);
                      break;
                  case "requestTabBack":
                      if (history.current > 0) {
                          if (message.newTab) {
                              this.add(history.stack[history.current - 1].url, {
                                  title: history.stack[history.current - 1].title,
                                  selected: !message.background,
                                  lazy: message.background
                              });
                          }
                          else {
                              history.current--;
                              this.update(tabId, {
                                  title: history.stack[history.current].title,
                                  url: history.stack[history.current].url,
                                  _internal: true
                              });
                          }
                      }
                      break;
                  case "requestTabForward":
                      if (history.current < history.stack.length - 1) {
                          if (message.newTab) {
                              this.add(history.stack[history.current + 1].url, {
                                  title: history.stack[history.current + 1].title,
                                  selected: !message.background,
                                  lazy: message.background
                              });
                          }
                          else {
                              history.current++;
                              this.update(tabId, {
                                  title: history.stack[history.current].title,
                                  url: history.stack[history.current].url,
                                  _internal: true
                              });
                          }
                      }
                      break;
              }
          });
      }
      static genId() {
          return "tabId" + ++Tab.idSeed;
      }
      static saveTabs() {
          const data = [];
          for (const { formatedUrl, title, selected, locked } of this.tabA.getAll().concat(this.tabB.getAll())) {
              data.push({
                  url: formatedUrl,
                  title,
                  selected,
                  locked
              });
          }
          app.LocalStorage.set("tab_state", data, true);
      }
      getAll() {
          const res = [];
          for (const li of this.$element.$$("li")) {
              res.push({
                  tabId: li.dataset.tabid,
                  url: li.dataset.tabsrc,
                  formatedUrl: this.$element.$(`iframe[data-tabid=${li.dataset.tabid}]`).dataset.url,
                  title: li.title,
                  selected: li.hasClass("tab_selected"),
                  locked: li.hasClass("tab_locked")
              });
          }
          return res;
      }
      getSelected() {
          const li = this.$element.$("li.tab_selected");
          if (!li)
              return null;
          return {
              tabId: li.dataset.tabid,
              url: li.dataset.tabsrc,
              title: li.title,
              selected: true,
              locked: li.hasClass("tab_locked")
          };
      }
      add(url, { title = null, selected = true, locked = false, lazy = false, restore = false } = {}) {
          title = title === null ? url : title;
          const tabId = Tab.genId();
          this.historyStore.set(tabId, {
              current: 0,
              stack: [{ url: url, title: url }]
          });
          // 既存のタブが一つも無い場合、強制的にselectedオン
          if (!this.$element.$(".tab_tabbar > li")) {
              selected = true;
          }
          const $li = $__("li");
          $li.dataset.tabid = tabId;
          $li.dataset.tabsrc = url;
          const $img = $__("img");
          $img.src = "/img/close_16x16.webp";
          $img.title = "閉じる";
          $li.addLast($__("span"), $img);
          this.$element.$(".tab_tabbar").addLast($li);
          const $iframe = $__("iframe").addClass("tab_content");
          $iframe.src = lazy ? "/view/empty.html" : url;
          $iframe.dataset.tabid = tabId;
          this.$element.$(".tab_container").addLast($iframe);
          this.update(tabId, { title, selected, locked, restore });
          return tabId;
      }
      async update(tabId, param) {
          if (typeof param.url === "string") {
              if (!param._internal) {
                  const history = this.historyStore.get(tabId);
                  history.stack.splice(history.current + 1);
                  history.stack.push({ url: param.url, title: param.url });
                  history.current++;
              }
              this.$element.$(`li[data-tabid="${tabId}"]`).dataset.tabsrc = param.url;
              const $tmptab = this.$element.$(`iframe[data-tabid="${tabId}"]`);
              $tmptab.emit(new Event("tab_beforeurlupdate", { "bubbles": true }));
              $tmptab.src = param.url;
              $tmptab.emit(new Event("tab_urlupdated", { "bubbles": true }));
          }
          if (typeof param.title === "string") {
              const history = this.historyStore.get(tabId);
              history.stack[history.current].title = param.title;
              const $tmptab = this.$element.$(`li[data-tabid="${tabId}"]`);
              $tmptab.title = param.title;
              $tmptab.T("span")[0].textContent = param.title;
          }
          if (param.selected) {
              let $iframe;
              const $selected = this.$element.C("tab_selected");
              for (let i = $selected.length - 1; i >= 0; i--) {
                  $selected[i].removeClass("tab_selected");
              }
              for (const dom of this.$element.$$(`[data-tabid="${tabId}"]`)) {
                  dom.addClass("tab_selected");
                  if (dom.hasClass("tab_content")) {
                      $iframe = dom;
                  }
              }
              $iframe.emit(new Event("tab_selected", { "bubbles": true }));
              // 遅延ロード指定のタブをロードする
              // 連続でlazy指定のタブがaddされた時のために非同期処理
              await app.defer();
              const selectedTab = this.getSelected();
              if (selectedTab) {
                  const iframe = this.$element.$(`iframe[data-tabid="${selectedTab.tabId}"]`);
                  if (iframe.getAttr("src") !== selectedTab.url) {
                      iframe.src = selectedTab.url;
                  }
              }
          }
          if (param.locked) {
              const $tmptab = this.$element.$(`li[data-tabid="${tabId}"]`);
              $tmptab.addClass("tab_locked");
          }
          else if (!(param.locked === void 0 || param.locked === null)) {
              const $tmptab = this.$element.$(`li[data-tabid="${tabId}"].tab_locked`);
              if ($tmptab !== null) {
                  $tmptab.removeClass("tab_locked");
              }
          }
          if (!param.restore) {
              Tab.saveTabs();
          }
      }
      remove(tabId) {
          const $tmptab = this.$element.$(`li[data-tabid="${tabId}"]`);
          const tabsrc = $tmptab.dataset.tabsrc;
          for (const [key, { url }] of this.recentClosed.entries()) {
              if (url === tabsrc) {
                  this.recentClosed.splice(key, 1);
              }
          }
          this.recentClosed.push({
              tabId: $tmptab.dataset.tabid,
              url: tabsrc,
              title: $tmptab.title,
              locked: $tmptab.hasClass("tab_locked")
          });
          if (this.recentClosed.length > 50) {
              const tmp = this.recentClosed.shift();
              this.historyStore.delete(tmp.tabId);
          }
          if ($tmptab.hasClass("tab_selected")) {
              const next = $tmptab.next() || $tmptab.prev();
              if (next) {
                  this.update(next.dataset.tabid, { selected: true });
              }
          }
          $tmptab.remove();
          const $tmptabcon = this.$element.$(`iframe[data-tabid="${tabId}"]`);
          $tmptabcon.emit(new Event("tab_removed", { "bubbles": true }));
          $tmptabcon.remove();
          Tab.saveTabs();
      }
      getRecentClosed() {
          return app.deepCopy(this.recentClosed);
      }
      restoreClosed(tabId) {
          for (const [key, tab] of this.recentClosed.entries()) {
              if (tab.tabId === tabId) {
                  this.recentClosed.splice(key, 1);
                  return this.add(tab.url, { title: tab.title });
              }
          }
          return null;
      }
      isLocked(tabId) {
          const tab = this.$element.$(`li[data-tabid="${tabId}"]`);
          return (tab !== null && tab.hasClass("tab_locked"));
      }
  }
  Tab.idSeed = 0;
  Tab.tabA = null;
  Tab.tabB = null;

  var TableSearch;

  var TableSearch$1 = TableSearch = function($table, method, prop) {
    var $td, $tr, dom, hitCount, i, j, k, len, ref, ref1, ref2;
    $table.addClass("hidden");
    $table.removeAttr("data-table-search-hit-count");
    ref = $table.C("table_search_hit");
    for (i = ref.length - 1; i >= 0; i += -1) {
      dom = ref[i];
      dom.removeClass("table_search_hit");
    }
    ref1 = $table.C("table_search_not_hit");
    for (j = ref1.length - 1; j >= 0; j += -1) {
      dom = ref1[j];
      dom.removeClass("table_search_not_hit");
    }
    // prop.query, prop.search_col
    if (method === "search") {
      prop.query = app.util.normalize(prop.query);
      $table.addClass("table_search");
      hitCount = 0;
      ref2 = $table.T("tbody")[0].child();
      for (k = 0, len = ref2.length; k < len; k++) {
        $tr = ref2[k];
        $td = $tr.child()[prop.target_col - 1];
        if (!$tr.hasClass("hidden") && app.util.normalize($td.textContent).includes(prop.query)) {
          $tr.addClass("table_search_hit");
          hitCount++;
        } else {
          $tr.addClass("table_search_not_hit");
        }
      }
      $table.dataset.tableSearchHitCount = hitCount;
    } else if (method === "clear") {
      $table.removeClass("table_search");
    }
    $table.removeClass("hidden");
    return $table;
  };

  /**
  @class TableSorter
  @constructor
  @param {Element} table
  */
  var TableSorter;

  var TableSorter$1 = TableSorter = (function() {
    class TableSorter {
      constructor(table) {
        this.table = table;
        this.table.addClass("table_sort");
        this.table.on("click", ({target}) => {
          var order;
          if (target.tagName !== "TH") {
            return;
          }
          order = target.hasClass("table_sort_desc") ? "asc" : "desc";
          this.clearSortClass();
          target.addClass(`table_sort_${order}`);
          this.table.$(`col.${target.dataset.key}`).addClass(`table_sort_${order}`);
          this.update();
        });
        return;
      }

      /**
      @method update
      @param {Object} [param]
      @param {String} [param.sortIndex]
      @param {String} [param.sortAttribute]
      @param {String} [param.sortOrder]
      */
      update({sortIndex, sortAttribute, sortOrder} = {}) {
        var $tbody, $td, $th, $tr, data, dataKeys, event, exparam, i, j, k, key, l, len, len1, len2, len3, name, ref, ref1, ref2, tmp, value;
        event = new Event("table_sort_before_update");
        this.table.emit(event);
        if (event.defaultPrevented) {
          return;
        }
        if ((sortIndex != null) && (sortOrder != null)) {
          this.clearSortClass();
          $th = this.table.$(`th:nth-child(${sortIndex + 1})`);
          $th.addClass(`table_sort_${sortOrder}`);
          this.table.$(`col.${$th.dataset.key}`).addClass(`table_sort_${sortOrder}`);
        } else if (sortAttribute == null) {
          $th = this.table.$("th.table_sort_asc, th.table_sort_desc");
          if (!$th) {
            return;
          }
          sortIndex = 0;
          tmp = $th;
          while (tmp = tmp.prev()) {
            sortIndex++;
          }
          sortOrder = $th.hasClass("table_sort_asc") ? "asc" : "desc";
        }
        if (sortIndex != null) {
          data = {};
          ref = this.table.$$(`td:nth-child(${sortIndex + 1})`);
          for (i = 0, len = ref.length; i < len; i++) {
            $td = ref[i];
            data[name = $td.textContent] || (data[name] = []);
            data[$td.textContent].push($td.parent());
          }
        } else if (sortAttribute != null) {
          this.clearSortClass();
          data = {};
          ref1 = this.table.$("tbody").T("tr");
          for (j = 0, len1 = ref1.length; j < len1; j++) {
            $tr = ref1[j];
            value = $tr.getAttr(sortAttribute);
            if (data[value] == null) {
              data[value] = [];
            }
            data[value].push($tr);
          }
        }
        dataKeys = Object.keys(data);
        dataKeys.sort(function(a, b) {
          var diff;
          diff = TableSorter.collator.compare(a, b);
          if (sortOrder === "desc") {
            diff *= -1;
          }
          return diff;
        });
        $tbody = this.table.$("tbody");
        $tbody.innerHTML = "";
        for (k = 0, len2 = dataKeys.length; k < len2; k++) {
          key = dataKeys[k];
          ref2 = data[key];
          for (l = 0, len3 = ref2.length; l < len3; l++) {
            $tr = ref2[l];
            $tbody.addLast($tr);
          }
        }
        exparam = {
          sort_order: sortOrder
        };
        if (sortIndex != null) {
          exparam.sort_index = sortIndex;
        } else {
          exparam.sort_attribute = sortAttribute;
        }
        this.table.emit(new CustomEvent("table_sort_updated", {
          detail: exparam
        }));
      }

      /**
      @method updateSnake
      @param {Object} [param]
      @param {String} [param.sort_index]
      @param {String} [param.sort_attribute]
      @param {String} [param.sort_order]
      */
      updateSnake({sort_index = null, sort_attribute = null, sort_order = null}) {
        this.update({
          sortIndex: sort_index,
          sortAttribute: sort_attribute,
          sortOrder: sort_order
        });
      }

      /**
      @method updateSnake
      */
      clearSortClass() {
        var $dom, i, j, ref, ref1;
        ref = this.table.C("table_sort_asc");
        for (i = ref.length - 1; i >= 0; i += -1) {
          $dom = ref[i];
          $dom.removeClass("table_sort_asc");
        }
        ref1 = this.table.C("table_sort_desc");
        for (j = ref1.length - 1; j >= 0; j += -1) {
          $dom = ref1[j];
          $dom.removeClass("table_sort_desc");
        }
      }

    }
    TableSorter.collator = new Intl.Collator("ja", {
      numeric: true
    });

    return TableSorter;

  }).call(window);

  /**
  @class ThreadContent
  @constructor
  @param {String} URL
  @param {Element} container
  */
  var ThreadContent;

  var ThreadContent$1 = ThreadContent = (function() {
    var _OVER1000_DATA;

    class ThreadContent {
      constructor(url, container) {
        /**
        @method setNG
        @param {Element} res
        @param {string} ngType
        */
        this.setNG = this.setNG.bind(this);
        /**
        @method _chainNG
        @param {Element} res
        @private
        */
        this._chainNG = this._chainNG.bind(this);
        /**
        @method _chainNgById
        @param {String} id
        @private
        */
        this._chainNgById = this._chainNgById.bind(this);
        /**
        @method _chainNgBySlip
        @param {String} slip
        @private
        */
        this._chainNgBySlip = this._chainNgBySlip.bind(this);
        /**
        @method _checkNG
        @param {Object} objRes
        @param {String} bbsType
        @return {Object|null}
        @private
        */
        this._checkNG = this._checkNG.bind(this);
        /**
        @method _getNgType
        @param {Object} objRes
        @param {String} bbsType
        @return {Object|null}
        @private
        */
        this._getNgType = this._getNgType.bind(this);
        /**
        @method refreshNG
        */
        this.refreshNG = this.refreshNG.bind(this);
        this.container = container;
        /**
        @property url
        @type app.URL.URL
        */
        this.url = url;
        /**
        @property urlStr
        @type String
        */
        this.urlStr = this.url.href;
        /**
        @property idIndex
        @type Object
        */
        this.idIndex = new Map();
        /**
        @property slipIndex
        @type Object
        */
        this.slipIndex = new Map();
        /**
        @property tripIndex
        @type Object
        */
        this.tripIndex = new Map();
        /**
        @property repIndex
        @type Object
        */
        this.repIndex = new Map();
        /**
        @property repNgIndex
        @type Object
        */
        this.repNgIndex = new Map();
        /**
        @property ancIndex
        @type Object
        */
        this.ancIndex = new Map();
        /**
        @property harmImgIndex
        @type Array
        */
        this.harmImgIndex = new Set();
        /**
        @property oneId
        @type null | String
        */
        this.oneId = null;
        /**
        @property over1000ResNum
        @type Number
        */
        this.over1000ResNum = null;
        /**
        @property _lastScrollInfo
        @type Object
        @private
        */
        this._lastScrollInfo = {
          resNum: 0,
          animate: false,
          offset: 0,
          animateTo: 0,
          animateChange: 0
        };
        /**
        @property _timeoutID
        @type Number
        @private
        */
        this._timeoutID = 0;
        /**
        @property _existIdAtFirstRes
        @type Boolean
        @private
        */
        this._existIdAtFirstRes = false;
        /**
        @property _existSlipAtFirstRes
        @type Boolean
        @private
        */
        this._existSlipAtFirstRes = false;
        /**
        @property _hiddenSelectors
        @type
        @private
        */
        this._hiddenSelectors = null;
        /**
        @property _isScrolling
        @type Boolean
        @private
        */
        this._isScrolling = false;
        /**
        @property _scrollRequestID
        @type Number
        @private
        */
        this._scrollRequestID = 0;
        /**
        @property _rawResData
        @type Array
        @private
        */
        this._rawResData = [];
        /**
        @property _ngIdForChain
        @type Object
        @private
        */
        this._ngIdForChain = new Set();
        /**
        @property _ngSlipForChain
        @type Object
        @private
        */
        this._ngSlipForChain = new Set();
        /**
        @property _resMessageMap
        @type Object
        @private
        */
        this._resMessageMap = new Map();
        /**
        @property _threadTitle
        @type String|null
        @private
        */
        this._threadTitle = null;
        try {
          this.harmfulReg = new RegExp(app.config.get("image_blur_word"));
          this.findHarmfulFlag = true;
        } catch (error) {
          app.message.send("notify", {
            message: "画像ぼかしの正規表現を読み込むのに失敗しました\n画像ぼかし機能は無効化されます",
            background_color: "red"
          });
          this.findHarmfulFlag = false;
        }
        this.container.on("scrollstart", () => {
          this._isScrolling = true;
        });
        this.container.on("scrollfinish", () => {
          this._isScrolling = false;
        });
        return;
      }

      /**
      @method _reScrollTo
      @private
      */
      _reScrollTo() {
        this.scrollTo(this._lastScrollInfo.resNum, this._lastScrollInfo.animate, this._lastScrollInfo.offset, true);
      }

      /**
      @method isHidden
      */
      isHidden(ele) {
        var css, j, len, selectorText, style, type;
        if (this._hiddenSelectors == null) {
          this._hiddenSelectors = [];
          css = $$.I("user_css").sheet.cssRules;
          for (j = 0, len = css.length; j < len; j++) {
            ({selectorText, style, type} = css[j]);
            if (type === 1) {
              if (style.display === "none") {
                this._hiddenSelectors.push(selectorText);
              }
            }
          }
        }
        return (ele.hasClass("ng") && !app.config.isOn("display_ng")) || this._hiddenSelectors.some(function(selector) {
          return ele.matches(selector);
        });
      }

      /**
      @method _loadNearlyImages
      @param {Number} resNum
      @param {Number} [offset=0]
      @return {Boolean} loadFlag
      */
      _loadNearlyImages(resNum, offset = 0) {
        var containerHeight, containerScroll, delayScrollTime, isHidden, loadFlag, loadImageByElement, target, tmpTarget, viewBottom, viewTop;
        loadFlag = false;
        target = this.container.children[resNum - 1];
        ({
          offsetHeight: containerHeight,
          scrollHeight: containerScroll
        } = this.container);
        viewTop = target.offsetTop;
        if (offset < 0) {
          viewTop += offset;
        }
        viewBottom = viewTop + containerHeight;
        if (viewBottom > containerScroll) {
          viewBottom = containerScroll;
          viewTop = viewBottom - containerHeight;
        }
        // 遅延ロードの解除
        loadImageByElement = (targetElement) => {
          var j, len, media, ref;
          ref = targetElement.$$("img[data-src], video[data-src]");
          for (j = 0, len = ref.length; j < len; j++) {
            media = ref[j];
            loadFlag = true;
            media.emit(new Event("immediateload", {
              "bubbles": true
            }));
          }
        };
        // 表示範囲内の要素をスキャンする
        // (上方)
        tmpTarget = target;
        while (tmpTarget && ((isHidden = this.isHidden(tmpTarget)) || tmpTarget.offsetTop + tmpTarget.offsetHeight > viewTop)) {
          if (!isHidden) {
            loadImageByElement(tmpTarget);
          }
          tmpTarget = tmpTarget.prev();
        }
        // (下方)
        tmpTarget = target.next();
        while (tmpTarget && ((isHidden = this.isHidden(tmpTarget)) || tmpTarget.offsetTop < viewBottom)) {
          if (!isHidden) {
            loadImageByElement(tmpTarget);
          }
          tmpTarget = tmpTarget.next();
        }
        // 遅延スクロールの設定
        if ((loadFlag || this._timeoutID !== 0) && !app.config.isOn("image_height_fix")) {
          if (this._timeoutID !== 0) {
            clearTimeout(this._timeoutID);
          }
          delayScrollTime = parseInt(app.config.get("delay_scroll_time"));
          this._timeoutID = setTimeout(() => {
            this._timeoutID = 0;
            return this._reScrollTo();
          }, delayScrollTime);
        }
        return loadFlag;
      }

      /**
      @method scrollTo
      @param {Element | Number} target
      @param {Boolean} [animate=false]
      @param {Number} [offset=0]
      @param {Boolean} [rerun=false]
      */
      scrollTo(target, animate = false, offset = 0, rerun = false) {
        var loadFlag, replaced, rerunAndCancel, resNum;
        if (typeof target === "number") {
          resNum = target;
        } else {
          resNum = +target.C("num")[0].textContent;
        }
        this._lastScrollInfo.resNum = resNum;
        this._lastScrollInfo.animate = animate;
        this._lastScrollInfo.offset = offset;
        loadFlag = false;
        target = this.container.children[resNum - 1];
        // 検索中で、ターゲットが非ヒット項目で非表示の場合、スクロールを中断
        if (target && this.container.hasClass("searching") && !target.hasClass("search_hit")) {
          target = null;
        }
        // もしターゲットがNGだった場合、その直前/直後の非NGレスをターゲットに変更する
        if (target && this.isHidden(target)) {
          replaced = target;
          while ((replaced = replaced.prev())) {
            if (!this.isHidden(replaced)) {
              target = replaced;
              break;
            }
            if (replaced == null) {
              replaced = target;
              while ((replaced = replaced.next())) {
                if (!this.isHidden(replaced)) {
                  target = replaced;
                  break;
                }
              }
            }
          }
        }
        if (target) {
          if (!rerun) {
            // 前後に存在する画像を事前にロードする
            loadFlag = this._loadNearlyImages(resNum, offset);
          }
          // offsetが比率の場合はpxを求める
          if ((0 < offset && offset < 1)) {
            offset = Math.round(target.offsetHeight * offset);
          }
          // 遅延スクロール時の実行必要性確認
          if (rerun && this.container.scrollTop === target.offsetTop + offset) {
            return;
          }
          // スクロールの実行
          if (animate) {
            rerunAndCancel = false;
            if (this._isScrolling) {
              cancelAnimationFrame(this._scrollRequestID);
              if (rerun) {
                rerunAndCancel = true;
              }
            }
            (() => {
              var _scrollInterval, change, max, min, movingHeight, to;
              this.container.emit(new Event("scrollstart"));
              to = target.offsetTop + offset;
              movingHeight = to - this.container.scrollTop;
              if (rerunAndCancel && to === this._lastScrollInfo.animateTo) {
                change = this._lastScrollInfo.animateChange;
              } else {
                change = Math.max(Math.round(movingHeight / 15), 1);
              }
              min = Math.min(to - change, to + change);
              max = Math.max(to - change, to + change);
              if (!rerun) {
                this._lastScrollInfo.animateTo = to;
                this._lastScrollInfo.animateChange = change;
              }
              return this._scrollRequestID = requestAnimationFrame(_scrollInterval = () => {
                var before, ref;
                before = this.container.scrollTop;
                // 画像のロードによる座標変更時の補正
                if (to !== target.offsetTop + offset) {
                  to = target.offsetTop + offset;
                  if (to - this.container.scrollTop > movingHeight) {
                    movingHeight = to - this.container.scrollTop;
                    change = Math.max(Math.round(movingHeight / 15), 1);
                  }
                  min = Math.min(to - change, to + change);
                  max = Math.max(to - change, to + change);
                  if (!rerun) {
                    this._lastScrollInfo.animateTo = to;
                    this._lastScrollInfo.animateChange = change;
                  }
                }
                // 例外発生時の停止処理
                if ((change > 0 && this.container.scrollTop > max) || (change < 0 && this.container.scrollTop < min)) {
                  this.container.scrollTop = to;
                  this.container.emit(new Event("scrollfinish"));
                  return;
                }
                // 正常時の処理
                if ((min <= (ref = this.container.scrollTop) && ref <= max)) {
                  this.container.scrollTop = to;
                  this.container.emit(new Event("scrollfinish"));
                  return;
                } else {
                  this.container.scrollTop += change;
                }
                if (this.container.scrollTop === before) {
                  this.container.emit(new Event("scrollfinish"));
                  return;
                }
                this._scrollRequestID = requestAnimationFrame(_scrollInterval);
              });
            })();
          } else {
            this.container.scrollTop = target.offsetTop + offset;
          }
        }
      }

      /**
      @method getRead
      @param {Number} beforeRead 直近に読んでいたレスの番号
      @return {Number} 現在読んでいると推測されるレスの番号
      */
      getRead(beforeRead = 1) {
        var $last, $next, $prev, $read, containerBottom, nextTop, prevTop, read, readTop;
        containerBottom = this.container.scrollTop + this.container.clientHeight;
        $read = this.container.children[beforeRead - 1];
        readTop = $read != null ? $read.offsetTop : void 0;
        if (!$read || ((readTop < containerBottom && containerBottom < readTop + $read.offsetHeight))) {
          return beforeRead;
        }
        // 最後のレスはcontainerの余白の関係で取得できないので別で判定
        $last = this.container.last();
        if ($last.offsetTop < containerBottom) {
          return this.container.children.length;
        }
        // 直近に読んでいたレスの上下を順番に調べる
        $next = $read.next();
        $prev = $read.prev();
        while (true) {
          if ($next != null) {
            nextTop = $next.offsetTop;
            if ((nextTop < containerBottom && containerBottom < nextTop + $next.offsetHeight)) {
              read = $next.C("num")[0].textContent;
              break;
            }
            $next = $next.next();
          }
          if ($prev != null) {
            prevTop = $prev.offsetTop;
            if ((prevTop < containerBottom && containerBottom < prevTop + $prev.offsetHeight)) {
              read = $prev.C("num")[0].textContent;
              break;
            }
            $prev = $prev.prev();
          }
          // どのレスも判定されなかった場合
          if (($next == null) && ($prev == null)) {
            break;
          }
        }
        // >>1の底辺が表示領域外にはみ出していた場合対策
        if (read == null) {
          return 1;
        }
        return parseInt(read);
      }

      /**
      @method getDisplay
      @param {Number} beforeRead 直近に読んでいたレスの番号
      @return {Object|null} 現在表示していると推測されるレスの番号とオフセット
      */
      getDisplay(beforeRead) {
        var $next, $prev, $read, containerBottom, containerTop, nextTop, prevTop, readTop, resRead;
        containerTop = this.container.scrollTop;
        containerBottom = containerTop + this.container.clientHeight;
        resRead = {
          resNum: 1,
          offset: 0,
          bottom: false
        };
        // 既に画面の一番下までスクロールしている場合
        // (いつのまにか位置がずれていることがあるので余裕を設ける)
        if (containerBottom >= this.container.scrollHeight - 60) {
          resRead.bottom = true;
        }
        $read = this.container.children[beforeRead - 1];
        if (!$read) {
          return null;
        }
        readTop = $read.offsetTop;
        if (!((readTop < containerTop && containerTop < readTop + $read.offsetHeight))) {
          // 直近に読んでいたレスの上下を順番に調べる
          $next = $read.next();
          $prev = $read.prev();
          while (true) {
            if ($next != null) {
              nextTop = $next.offsetTop;
              if ((nextTop <= containerTop && containerTop < nextTop + $next.offsetHeight)) {
                $read = $next;
                break;
              }
              $next = $next.next();
            }
            if ($prev != null) {
              prevTop = $prev.offsetTop;
              if ((prevTop <= containerTop && containerTop < prevTop + $prev.offsetHeight)) {
                $read = $prev;
                break;
              }
              $prev = $prev.prev();
            }
            // どのレスも判定されなかった場合
            if (($next == null) && ($prev == null)) {
              break;
            }
          }
        }
        resRead.resNum = parseInt($read.C("num")[0].textContent);
        resRead.offset = (containerTop - $read.offsetTop) / $read.offsetHeight;
        return resRead;
      }

      /**
      @method getSelected
      @return {Element|null}
      */
      getSelected() {
        return this.container.$("article.selected");
      }

      /**
      @method select
      @param {Element | Number} target
      @param {Boolean} [preventScroll = false]
      @param {Boolean} [animate = false]
      @param {Number} [offset = 0]
      */
      select(target, preventScroll = false, animate = false, offset = 0) {
        var ref;
        if ((ref = this.container.$("article.selected")) != null) {
          ref.removeClass("selected");
        }
        if (typeof target === "number") {
          target = this.container.$(`article:nth-child(${target}), article:last-child`);
        }
        if (!target) {
          return;
        }
        target.addClass("selected");
        if (!preventScroll) {
          this.scrollTo(target, animate, offset);
        }
      }

      /**
      @method clearSelect
      */
      clearSelect() {
        var ref;
        if ((ref = this.getSelected()) != null) {
          ref.removeClass("selected");
        }
      }

      /**
      @method selectNext
      @param {number} [repeat = 1]
      */
      selectNext(repeat = 1) {
        var bottom, containerHeight, current, j, prevTarget, ref, target, targetBottom, targetHeight, top;
        current = this.getSelected();
        containerHeight = this.container.offsetHeight;
        if (current) {
          ({top, bottom} = current.getBoundingClientRect());
          // 現在選択されているレスが表示範囲外だった場合、それを無視する
          if (top >= containerHeight || bottom <= 0) {
            current = null;
          }
        }
        if (!current) {
          this.select(this.container.child()[this.getRead() - 1], true);
        } else {
          target = current;
          for (j = 0, ref = repeat; (0 <= ref ? j < ref : j > ref); 0 <= ref ? j++ : j--) {
            prevTarget = target;
            ({
              bottom: targetBottom
            } = target.getBoundingClientRect());
            if (targetBottom <= containerHeight && target.next()) {
              target = target.next();
              while (target && this.isHidden(target)) {
                target = target.next();
              }
            }
            if (!target) {
              target = prevTarget;
              break;
            }
            ({
              bottom: targetBottom,
              height: targetHeight
            } = target.getBoundingClientRect());
            if (containerHeight < targetBottom) {
              if (targetHeight >= containerHeight) {
                this.container.scrollTop += containerHeight * 0.5;
              } else {
                this.container.scrollTop += targetBottom - containerHeight + 10;
              }
            } else if (!target.next()) {
              this.container.scrollTop += containerHeight * 0.5;
              if (target === prevTarget) {
                break;
              }
            }
          }
          if (target && target !== current) {
            this.select(target, true);
          }
        }
      }

      /**
      @method selectPrev
      @param {number} [repeat = 1]
      */
      selectPrev(repeat = 1) {
        var bottom, containerHeight, current, j, prevTarget, ref, target, targetHeight, targetTop, top;
        current = this.getSelected();
        containerHeight = this.container.offsetHeight;
        if (current) {
          ({top, bottom} = current.getBoundingClientRect());
          // 現在選択されているレスが表示範囲外だった場合、それを無視する
          if (top >= containerHeight || bottom <= 0) {
            current = null;
          }
        }
        if (!current) {
          this.select(this.container.child()[this.getRead() - 1], true);
        } else {
          target = current;
          for (j = 0, ref = repeat; (0 <= ref ? j < ref : j > ref); 0 <= ref ? j++ : j--) {
            prevTarget = target;
            ({
              top: targetTop,
              height: targetHeight
            } = target.getBoundingClientRect());
            if (0 <= targetTop && target.prev()) {
              target = target.prev();
              while (target && this.isHidden(target)) {
                target = target.prev();
              }
            }
            if (!target) {
              target = prevTarget;
              break;
            }
            ({
              top: targetTop,
              height: targetHeight
            } = target.getBoundingClientRect());
            if (targetTop < 0) {
              if (targetHeight >= containerHeight) {
                this.container.scrollTop -= containerHeight * 0.5;
              } else {
                this.container.scrollTop = target.offsetTop - 10;
              }
            } else if (!target.prev()) {
              this.container.scrollTop -= containerHeight * 0.5;
              if (target === prevTarget) {
                break;
              }
            }
          }
          if (target && target !== current) {
            this.select(target, true);
          }
        }
      }

      /**
      @method addItem
      @param {Object | Array}
      */
      async addItem(items, threadTitle) {
        var $article, $fragment, $header, $mail, $message, $name, $num, $other, bbsType, color, id, j, k, len, len1, ngObj, ngType, protocol, ref, ref1, ref2, res, resNum, slip, startResNum, tmp, writtenHistory, writtenRes;
        if (!Array.isArray(items)) {
          items = [items];
        }
        if (!(items.length > 0)) {
          return;
        }
        resNum = this.container.child().length;
        startResNum = resNum + 1;
        ({bbsType} = this.url.guessType());
        writtenRes = (await app.WriteHistory.getByUrl(this.urlStr));
        this._threadTitle = threadTitle;
        $fragment = $_F();
        for (j = 0, len = items.length; j < len; j++) {
          res = items[j];
          resNum++;
          res.num = resNum;
          res.class = [];
          ({protocol} = this.url);
          res = app.ReplaceStrTxt.replace(this.urlStr, document.title, res);
          if (/(?:\u3000{5}|\u3000\u0020|[^>]\u0020\u3000)(?!<br>|$)/i.test(res.message)) {
            res.class.push("aa");
          }
          for (k = 0, len1 = writtenRes.length; k < len1; k++) {
            writtenHistory = writtenRes[k];
            if (!(writtenHistory.res === resNum)) {
              continue;
            }
            res.class.push("written");
            break;
          }
          $article = $__("article");
          $header = $__("header");
          //.num
          $num = $__("span").addClass("num");
          $num.textContent = resNum;
          $header.addLast($num);
          //.name
          $name = $__("span").addClass("name");
          if (/^\s*(?:&gt;|\uff1e){0,2}([\d\uff10-\uff19]+(?:[\-\u30fc][\d\uff10-\uff19]+)?(?:\s*,\s*[\d\uff10-\uff19]+(?:[\-\u30fc][\d\uff10-\uff19]+)?)*)\s*$/.test(res.name)) {
            $name.addClass("name_anchor");
          }
          $name.innerHTML = res.name.replace(/<\/?a[^>]*>/g, "").replace(/<(?!\/?(?:b|small|font(?: color="?[#a-zA-Z0-9]+"?)?)>)/g, "&lt;").replace(/<\/b>\(([^<>]+? [^<>]+?)\)<b>$/, ($0, $1) => {
            res.slip = $1;
            if (resNum === 1) {
              this._existSlipAtFirstRes = true;
            }
            if (!this.slipIndex.has($1)) {
              this.slipIndex.set($1, new Set());
            }
            this.slipIndex.get($1).add(resNum);
            return "";
          }).replace(/<\/b> ?(◆[^<>]+?) ?<b>/, ($0, $1) => {
            res.trip = $1;
            if (!this.tripIndex.has($1)) {
              this.tripIndex.set($1, new Set());
            }
            this.tripIndex.get($1).add(resNum);
            return `<span class="trip">${$1}</span>`;
          }).replace(/<\/b>(.*?)<b>/g, "<span class=\"ob\">$1</span>").replace(/&lt;span[^>]*?>(.*?)&lt;\/span>/g, "<span class=\"ob\">$1</span>");
          $header.addLast($name);
          //.mail
          $mail = $__("span").addClass("mail");
          $mail.innerHTML = res.mail.replace(/<.*?(?:>|$)/g, "");
          $header.addLast($mail);
          //.other
          $other = $__("span").addClass("other");
          //be
          //タグ除去
          //.id
          tmp = res.other.replace(/<\/div><div class="be[^>]*?"><a href="(https?:\/\/be\.[25]ch\.net\/user\/\d+?)"[^>]*>(.*?)<\/a>/, "<a class=\"beid\" href=\"$1\" target=\"_blank\">$2</a>").replace(/<(?!(?:a class="beid"[^>]*|\/a)>).*?(?:>|$)/g, "").replace(" ID:???", "ID:???").replace(/(?:^| |(\d))(ID:(?!\?\?\?)[^ <>"']+|発信元:\d+.\d+.\d+.\d+)/, ($0, $1, $2) => {
            var fixedId, str;
            fixedId = $2;
            //末尾●除去
            if (fixedId.endsWith("\u25cf")) {
              fixedId = fixedId.slice(0, -1);
            }
            res.id = fixedId;
            if (resNum === 1) {
              this.oneId = fixedId;
              this._existIdAtFirstRes = true;
            }
            if (fixedId === this.oneId) {
              res.class.push("one");
            }
            if (fixedId.endsWith(".net")) {
              res.class.push("net");
            }
            if (!this.idIndex.has(fixedId)) {
              this.idIndex.set(fixedId, new Set());
            }
            this.idIndex.get(fixedId).add(resNum);
            str = $1 != null ? $1 : "";
            // slip追加(IDが存在しているとき)
            if (res.slip != null) {
              str += `<span class="slip">SLIP:${res.slip}</span>`;
            }
            str += `<span class="id">${$2}</span>`;
            return str;
          //.beid
          }).replace(/(?:^| )(BE:(\d+)\-[A-Z\d]+\(\d+\))/, `<a class="beid" href="${        //.date
protocol}//be.5ch.net/test/p.php?i=$3" target="_blank">$1</a>`).replace(/\d{4}\/\d{1,2}\/\d{1,2}\(.\)\s\d{1,2}:\d\d(?::\d\d(?:\.\d+)?)?/, "<time class=\"date\">$&</time>");
          // slip追加(IDが存在していないとき)
          if ((res.slip != null) && (res.id == null)) {
            tmp += `<span class="slip">SLIP:${res.slip}</span>`;
          }
          $other.innerHTML = tmp;
          $header.addLast($other);
          $article.addLast($header);
          // スレッド終端の自動追加メッセージの確認
          if (bbsType === "2ch" && tmp.startsWith(_OVER1000_DATA) && !this.over1000ResNum) {
            this.over1000ResNum = resNum;
          }
          //文字色
          color = (ref = res.message.match(/<font color="(.*?)">/i)) != null ? ref[1] : void 0;
          // id, slip, tripが取り終わったタイミングでNG判定を行う
          // NG判定されるものは、ReplaceStrTxtで置き換え後のテキストなので注意すること
          if (ngObj = this._checkNG(res, bbsType)) {
            res.class.push("ng");
            ngType = ngObj.type;
            if (ngObj.name != null) {
              ngType += ":" + ngObj.name;
            }
          }
          // resデータの保管
          this._rawResData[resNum] = res;
          //imgタグ変換
          tmp = res.message.replace(/<img src="([\w]+):\/\/(.*?)"[^>]*>/ig, "$1://$2").replace(/<img src="\/\/(.*?)"[^>]*>/ig, `${        //Rock54
//SLIPが変わったという表示
//タグ除去
//URLリンク
//Beアイコン埋め込み表示
protocol}//$1`).replace(/(?:<small[^>]*>&#128064;|<i>&#128064;<\/i>)<br>Rock54: (Caution|Warning)\(([^<>()]+)\) ?.*?(?:<\/small>)?/ig, "<br><div-block class=\"rock54\">&#128064; Rock54: $1($2)</div-block>").replace(/<hr>VIPQ2_EXTDAT: ([^<>]+): EXT was configured /i, "<br><div-block class=\"slipchange\">VIPQ2_EXTDAT: $1: EXT configure</div-block>").replace(/<(?!(?:br|hr|\/?div-block[^<>]*|\/?b)>).*?(?:>|$)/ig, "").replace(/<(\/)?div-block([^<>]*)>/g, "<$1div$2>").replace(/(h)?(ttps?:\/\/(?!img\.[25]ch\.net\/(?:ico|emoji|premium)\/[\w\-_]+\.gif)(?:[a-hj-zA-HJ-Z\d_\-.!~*'();\/?:@=+$,%#]|\&(?!gt;)|[iI](?![dD]:)+)+)/g, '<a href="h$2" target="_blank">$1$2</a>').replace(/^(?:\s*sssp|https?):\/\/(img\.[25]ch\.net\/(?:ico|premium)\/[\w\-_]+\.gif)\s*<br>/, ($0, $1) => {
            var ref1;
            if ((ref1 = this.url.getTsld()) === "5ch.net" || ref1 === "bbspink.com" || ref1 === "2ch.sc") {
              return `<img class="beicon" src="/img/dummy_1x1.webp" data-src="${protocol}//${$1}"><br>`;
            }
            return $0;
          //エモーティコン埋め込み表示
          }).replace(/(?:\s*sssp|https?):\/\/(img\.[25]ch\.net\/emoji\/[\w\-_]+\.gif)\s*/g, ($0, $1) => {
            var ref1;
            if ((ref1 = this.url.getTsld()) === "5ch.net" || ref1 === "bbspink.com" || ref1 === "2ch.sc") {
              return `<img class="beicon emoticon" src="/img/dummy_1x1.webp" data-src="${protocol}//${$1}">`;
            }
            return $0;
          //アンカーリンク
          }).replace(app.util.Anchor.reg.ANCHOR, ($0) => {
            var anchor, disabled, disabledReason, isThatHarmImg, l, len2, ref1, segment, target;
            anchor = app.util.Anchor.parseAnchor($0);
            if (anchor.targetCount >= 25) {
              disabled = true;
              disabledReason = "指定されたレスの量が極端に多いため、ポップアップを表示しません";
            } else if (anchor.targetCount === 0) {
              disabled = true;
              disabledReason = "指定されたレスが存在しません";
            } else {
              disabled = false;
            }
            //グロ/死ねの返信レス
            isThatHarmImg = this.findHarmfulFlag && this.harmfulReg.test(res.message);
            if (isThatHarmImg) {
              res.class.push("has_harm_word");
            }
            //rep_index更新
            if (!disabled) {
              ref1 = anchor.segments;
              for (l = 0, len2 = ref1.length; l < len2; l++) {
                segment = ref1[l];
                target = segment[0];
                while (target <= segment[1]) {
                  if (!this.repIndex.has(target)) {
                    this.repIndex.set(target, new Set());
                  }
                  this.repIndex.get(target).add(resNum);
                  if (isThatHarmImg) {
                    this.harmImgIndex.add(target);
                  }
                  if (!this.ancIndex.has(resNum)) {
                    this.ancIndex.set(resNum, new Set());
                  }
                  this.ancIndex.get(resNum).add(target);
                  target++;
                }
              }
            }
            return "<a href=\"javascript:undefined;\" class=\"anchor" + (disabled ? ` disabled" data-disabled-reason="${disabledReason}"` : "\"") + `>${$0}</a>`;
          //IDリンク
          }).replace(/id:(?:[a-hj-z\d_\+\/\.\!]|i(?!d:))+/ig, "<a href=\"javascript:undefined;\" class=\"anchor_id\">$&</a>");
          $message = $__("div").addClass("message");
          if (color != null) {
            $message.style.color = `#${color}`;
          }
          $message.innerHTML = tmp;
          $article.addLast($message);
          if (res.class.length > 0) {
            $article.setClass(...res.class);
          }
          if (res.id != null) {
            $article.dataset.id = res.id;
          }
          if (res.slip != null) {
            $article.dataset.slip = res.slip;
          }
          if (res.trip != null) {
            $article.dataset.trip = res.trip;
          }
          if (res.class.includes("ng")) {
            this.setNG($article, ngType);
          }
          $fragment.addLast($article);
        }
        this.updateFragmentIds($fragment, startResNum);
        this.container.addLast($fragment);
        this.updateIds(startResNum);
        // NG判定されたIDとSLIPの連鎖NG
        if (app.config.isOn("chain_ng_id")) {
          ref1 = this._ngIdForChain;
          for (id of ref1) {
            this._chainNgById(id);
          }
        }
        if (app.config.isOn("chain_ng_slip")) {
          ref2 = this._ngSlipForChain;
          for (slip of ref2) {
            this._chainNgBySlip(slip);
          }
        }
        // 返信数の更新
        this.updateRepCount();
        try {
          //サムネイル追加処理
          await Promise.all(Array.from(this.container.$$(".message > a:not(.anchor):not(.thumbnail):not(.has_thumbnail):not(.expandedURL):not(.has_expandedURL)")).map(async(a) => {
            var err, href, link, mediaType;
            ({a, link} = (await this.checkUrlExpand(a)));
            ({res, err} = app.ImageReplaceDat.replace(link));
            if (err == null) {
              href = res.text;
            } else {
              href = a.href;
            }
            mediaType = app.URL.getExtType(href, {
              audio: app.config.isOn("audio_supported"),
              video: app.config.isOn("audio_supported"),
              oggIsAudio: app.config.isOn("audio_supported_ogg"),
              oggIsVideo: app.config.isOn("video_supported_ogg")
            });
            if (err == null) {
              if (mediaType == null) {
                mediaType = "image";
              }
            }
            if (mediaType) {
              // サムネイルの追加
              this.addThumbnail(a, href, mediaType, res);
            }
          }));
          // harmImg更新
          this.updateHarmImages();
        } catch (error) {}
      }

      /**
      @method updateId
      @param {String} className
      @param {Map} map
      @param {String} prefix
      */
      updateId({startRes = 1, endRes, dom}, className, map, prefix) {
        var count, ele, i, id, index, resNum, x;
        for (x of map) {
          [id, index] = x;
          count = index.size;
          i = 0;
          for (resNum of index) {
            i++;
            if (!(startRes <= resNum && ((endRes == null) || resNum <= endRes))) {
              continue;
            }
            ele = dom.child()[resNum - startRes].C(className)[0];
            ele.textContent = `${prefix}${id}(${i}/${count})`;
            if (count >= 5) {
              ele.removeClass("link");
              ele.addClass("freq");
            } else if (count >= 2) {
              ele.addClass("link");
            }
          }
        }
      }

      /**
      @method updateFragmentIds
      */
      updateFragmentIds($fragment, startRes) {
        //id, slip, trip更新
        this.updateId({
          startRes,
          dom: $fragment
        }, "id", this.idIndex, "");
        this.updateId({
          startRes,
          dom: $fragment
        }, "slip", this.slipIndex, "SLIP:");
        this.updateId({
          startRes,
          dom: $fragment
        }, "trip", this.tripIndex, "");
      }

      /**
      @method updateIds
      */
      updateIds(endRes) {
        //id, slip, trip更新
        this.updateId({
          endRes,
          dom: this.container
        }, "id", this.idIndex, "");
        this.updateId({
          endRes,
          dom: this.container
        }, "slip", this.slipIndex, "SLIP:");
        this.updateId({
          endRes,
          dom: this.container
        }, "trip", this.tripIndex, "");
        (() => {        //参照関係再構築
          var index, r, ref, res, resKey, x;
          ref = this.repIndex;
          for (x of ref) {
            [resKey, index] = x;
            res = this.container.child()[resKey - 1];
            if (!res) {
              continue;
            }
            //連鎖NG
            if (app.config.isOn("chain_ng") && res.hasClass("ng")) {
              this._chainNG(res);
            }
            //自分に対してのレス
            if (res.hasClass("written")) {
              for (r of index) {
                this.container.child()[r - 1].addClass("to_written");
              }
            }
          }
        })();
      }

      /**
      @method updateRepCount
      */
      updateRepCount() {
        var ele, index, newFlg, ref, res, resCount, resKey, x;
        ref = this.repIndex;
        for (x of ref) {
          [resKey, index] = x;
          res = this.container.child()[resKey - 1];
          if (!res) {
            continue;
          }
          resCount = index.size;
          if (app.config.isOn("reject_ng_rep") && this.repNgIndex.has(resKey)) {
            resCount -= this.repNgIndex.get(resKey).size;
          }
          if (ele = res.C("rep")[0]) {
            newFlg = false;
          } else {
            newFlg = true;
            if (resCount > 0) {
              ele = $__("span");
            }
          }
          if (resCount > 0) {
            ele.textContent = `返信 (${resCount})`;
            ele.className = resCount >= 5 ? "rep freq" : "rep link";
            res.dataset.rescount = (function() {
              var results = [];
              for (var j = 1; 1 <= resCount ? j <= resCount : j >= resCount; 1 <= resCount ? j++ : j--){ results.push(j); }
              return results;
            }).apply(this).join(" ");
            if (newFlg) {
              res.C("other")[0].addLast(document.createTextNode(" "), ele);
            }
          } else if (ele) {
            res.removeAttr("data-rescount");
            ele.remove();
          }
        }
      }

      setNG(res, ngType) {
        var ref, resNum, rn;
        res.addClass("ng");
        if (app.config.isOn("display_ng")) {
          res.addClass("disp_ng");
        }
        res.setAttr("ng-type", ngType);
        resNum = +res.C("num")[0].textContent;
        if (this.ancIndex.has(resNum)) {
          ref = this.ancIndex.get(resNum);
          for (rn of ref) {
            if (!this.repNgIndex.has(rn)) {
              this.repNgIndex.set(rn, new Set());
            }
            this.repNgIndex.get(rn).add(resNum);
          }
        }
      }

      _chainNG(res) {
        var getRes, id, r, ref, resNum, rn, slip;
        resNum = +res.C("num")[0].textContent;
        if (!this.repIndex.has(resNum)) {
          return;
        }
        ref = this.repIndex.get(resNum);
        for (r of ref) {
          if (r <= resNum) {
            continue;
          }
          getRes = this.container.child()[r - 1];
          if (getRes.hasClass("ng")) {
            continue;
          }
          rn = +getRes.C("num")[0].textContent;
          if (app.NG.isIgnoreResNumForAuto(rn, app.NG.TYPE.AUTO_CHAIN)) {
            continue;
          }
          if (app.NG.isThreadIgnoreNgType(this._rawResData[rn], this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_CHAIN)) {
            continue;
          }
          this.setNG(getRes, app.NG.TYPE.AUTO_CHAIN);
          // NG連鎖IDの登録
          if (app.config.isOn("chain_ng_id") && app.config.isOn("chain_ng_id_by_chain")) {
            if (id = getRes.getAttr("data-id")) {
              if (!this._ngIdForChain.has(id)) {
                this._ngIdForChain.add(id);
              }
              this._chainNgById(id);
            }
          }
          // NG連鎖SLIPの登録
          if (app.config.isOn("chain_ng_slip") && app.config.isOn("chain_ng_slip_by_chain")) {
            if (slip = getRes.getAttr("data-slip")) {
              if (!this._ngSlipForChain.has(slip)) {
                this._ngSlipForChain.add(slip);
              }
              this._chainNgBySlip(slip);
            }
          }
          this._chainNG(getRes);
        }
      }

      _chainNgById(id) {
        var j, len, r, ref, rn;
        ref = this.container.$$(`article[data-id="${id}"]`);
        // 連鎖IDのNG
        for (j = 0, len = ref.length; j < len; j++) {
          r = ref[j];
          if (r.hasClass("ng")) {
            continue;
          }
          rn = +r.C("num")[0].textContent;
          if (app.NG.isIgnoreResNumForAuto(rn, app.NG.TYPE.AUTO_CHAIN_ID)) {
            continue;
          }
          if (app.NG.isThreadIgnoreNgType(this._rawResData[rn], this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_CHAIN_ID)) {
            continue;
          }
          this.setNG(r, app.NG.TYPE.AUTO_CHAIN_ID);
          if (app.config.isOn("chain_ng")) {
            // 連鎖NG
            this._chainNG(r);
          }
        }
      }

      _chainNgBySlip(slip) {
        var j, len, r, ref, rn;
        ref = this.container.$$(`article[data-slip="${slip}"]`);
        // 連鎖SLIPのNG
        for (j = 0, len = ref.length; j < len; j++) {
          r = ref[j];
          if (r.hasClass("ng")) {
            continue;
          }
          rn = +r.C("num")[0].textContent;
          if (app.NG.isIgnoreResNumForAuto(rn, app.NG.TYPE.AUTO_CHAIN_SLIP)) {
            continue;
          }
          if (app.NG.isThreadIgnoreNgType(this._rawResData[rn], this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_CHAIN_SLIP)) {
            continue;
          }
          this.setNG(r, app.NG.TYPE.AUTO_CHAIN_SLIP);
          if (app.config.isOn("chain_ng")) {
            // 連鎖NG
            this._chainNG(r);
          }
        }
      }

      _checkNG(objRes, bbsType) {
        var ngObj, ref, ref1;
        if (ngObj = this._getNgType(objRes, bbsType)) {
          // NG連鎖IDの登録
          if (app.config.isOn("chain_ng_id") && (objRes.id != null) && !((ref = ngObj.type) === app.NG.TYPE.ID || ref === app.NG.TYPE.AUTO_CHAIN_ID)) {
            if (!this._ngIdForChain.has(objRes.id)) {
              this._ngIdForChain.add(objRes.id);
            }
          }
          // NG連鎖SLIPの登録
          if (app.config.isOn("chain_ng_slip") && (objRes.slip != null) && !((ref1 = ngObj.type) === app.NG.TYPE.SLIP || ref1 === app.NG.TYPE.AUTO_CHAIN_SLIP)) {
            if (!this._ngSlipForChain.has(objRes.slip)) {
              this._ngSlipForChain.add(objRes.slip);
            }
          }
        }
        return ngObj;
      }

      _getNgType(objRes, bbsType) {
        var anc, anchor, j, judgementIdType, k, len, len1, m, ngFlag, ngObj, ref, resMessage, segment, target;
        if ((this.over1000ResNum != null) && objRes.num >= this.over1000ResNum) {
          return null;
        }
        // 登録ワードのNG
        if ((ngObj = app.NG.isNGThread(objRes, this._threadTitle, this.urlStr)) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, ngObj.type)) {
          return ngObj;
        }
        if (bbsType === "2ch") {
          judgementIdType = app.config.get("how_to_judgment_id");
          // idなしをNG
          if (app.config.isOn("nothing_id_ng") && (objRes.id == null) && ((judgementIdType === "first_res" && this._existIdAtFirstRes) || (judgementIdType === "exists_once" && this.idIndex.size !== 0)) && !app.NG.isIgnoreResNumForAuto(objRes.num, app.NG.TYPE.AUTO_NOTHING_ID) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_NOTHING_ID)) {
            return {
              type: app.NG.TYPE.AUTO_NOTHING_ID
            };
          }
          // slipなしをNG
          if (app.config.isOn("nothing_slip_ng") && (objRes.slip == null) && ((judgementIdType === "first_res" && this._existSlipAtFirstRes) || (judgementIdType === "exists_once" && this.slipIndex.size !== 0)) && !app.NG.isIgnoreResNumForAuto(objRes.num, app.NG.TYPE.AUTO_NOTHING_SLIP) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_NOTHING_SLIP)) {
            return {
              type: app.NG.TYPE.AUTO_NOTHING_SLIP
            };
          }
        }
        // 連鎖IDのNG
        if (app.config.isOn("chain_ng_id") && (objRes.id != null) && this._ngIdForChain.has(objRes.id) && !app.NG.isIgnoreResNumForAuto(objRes.num, app.NG.TYPE.AUTO_CHAIN_ID) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_CHAIN_ID)) {
          return {
            type: app.NG.TYPE.AUTO_CHAIN_ID
          };
        }
        // 連鎖SLIPのNG
        if (app.config.isOn("chain_ng_slip") && (objRes.slip != null) && this._ngSlipForChain.has(objRes.slip) && !app.NG.isIgnoreResNumForAuto(objRes.num, app.NG.TYPE.AUTO_CHAIN_SLIP) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_CHAIN_SLIP)) {
          return {
            type: app.NG.TYPE.AUTO_CHAIN_SLIP
          };
        }
        // 連投レスをNG
        if (app.config.get("repeat_message_ng_count") > 1) {
          // アンカーの削除
          // <a>タグの削除
          // 行末ブランクの削除
          // 空行の削除
          // 前後ブランクの削除
          resMessage = objRes.message.replace(/<a [^>]*>(?:&gt;){1,2}\d+(?:[-,]\d+)*<\/a>/g, "").replace(/<\/?a[^>]*>/g, "").replace(/\s+<br>/g, "<br>").replace(/^<br>/, "").replace(/(?:<br>){2,}/g, "<br>").trim();
          if (!this._resMessageMap.has(resMessage)) {
            this._resMessageMap.set(resMessage, new Set());
          }
          this._resMessageMap.get(resMessage).add(objRes.num);
          if (this._resMessageMap.get(resMessage).size >= +app.config.get("repeat_message_ng_count") && !app.NG.isIgnoreResNumForAuto(objRes.num, app.NG.TYPE.AUTO_REPEAT_MESSAGE) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_REPEAT_MESSAGE)) {
            return {
              type: app.NG.TYPE.AUTO_REPEAT_MESSAGE
            };
          }
        }
        // 前方参照をNG
        if (app.config.isOn("forward_link_ng") && !app.NG.isIgnoreResNumForAuto(objRes.num, app.NG.TYPE.AUTO_FORWARD_LINK) && !app.NG.isThreadIgnoreNgType(objRes, this._threadTitle, this.urlStr, app.NG.TYPE.AUTO_FORWARD_LINK)) {
          ngFlag = false;
          // <a>タグの削除
          resMessage = objRes.message.replace(/<\/?a[^>]*>/g, "");
          m = resMessage.match(app.util.Anchor.reg.ANCHOR);
          if (m) {
            for (j = 0, len = m.length; j < len; j++) {
              anc = m[j];
              anchor = app.util.Anchor.parseAnchor(anc);
              ref = anchor.segments;
              for (k = 0, len1 = ref.length; k < len1; k++) {
                segment = ref[k];
                target = segment[0];
                while (target <= segment[1]) {
                  if (target > objRes.num) {
                    ngFlag = true;
                    break;
                  }
                  target++;
                }
                if (ngFlag) {
                  break;
                }
              }
              if (ngFlag) {
                break;
              }
            }
          }
          if (ngFlag) {
            return {
              type: app.NG.TYPE.AUTO_FORWARD_LINK
            };
          }
        }
        return null;
      }

      refreshNG() {
        var bbsType, id, j, k, len, len1, ngObj, ngType, ref, ref1, ref2, ref3, res, resNum, slip;
        ({bbsType} = this.url.guessType());
        this._ngIdForChain.clear();
        this._ngSlipForChain.clear();
        this._resMessageMap.clear();
        this.repNgIndex.clear();
        ref = this.container.$$("article.ng");
        // NGの解除
        for (j = 0, len = ref.length; j < len; j++) {
          res = ref[j];
          res.removeClass("ng", "disp_ng");
          res.removeAttr("ng-type");
        }
        ref1 = this.container.$$("article");
        // NGの再設定
        for (k = 0, len1 = ref1.length; k < len1; k++) {
          res = ref1[k];
          if (res.hasClass("ng")) {
            continue;
          }
          resNum = +res.C("num")[0].textContent;
          if (ngObj = this._checkNG(this._rawResData[resNum], bbsType)) {
            ngType = ngObj.type;
            if (ngObj.name != null) {
              ngType += ":" + ngObj.name;
            }
            this.setNG(res, ngType);
            // 連鎖NG
            if (app.config.isOn("chain_ng") && this.repIndex.has(resNum)) {
              this._chainNG(res);
            }
          }
        }
        // NG判定されたIDとSLIPの連鎖NG
        if (app.config.isOn("chain_ng_id")) {
          ref2 = this._ngIdForChain;
          for (id of ref2) {
            this._chainNgById(id);
          }
        }
        if (app.config.isOn("chain_ng_slip")) {
          ref3 = this._ngSlipForChain;
          for (slip of ref3) {
            this._chainNgBySlip(slip);
          }
        }
        // 返信数の更新
        this.updateRepCount();
        // harmImg更新
        this.updateHarmImages();
        // 表示更新通知
        this.container.emit(new Event("view_refreshed", {
          "bubbles": true
        }));
      }

      /**
      @method updateHarmImages
      */
      updateHarmImages() {
        var ele, imageBlur, isBlur, ref, ref1, rep, repEle, res;
        imageBlur = app.config.isOn("image_blur");
        ref = this.harmImgIndex;
        for (res of ref) {
          ele = this.container.child()[res - 1];
          if (!ele) {
            continue;
          }
          isBlur = false;
          ref1 = this.repIndex.get(res);
          for (rep of ref1) {
            repEle = this.container.child()[rep - 1];
            if (!repEle) {
              continue;
            }
            if (!repEle.hasClass("has_harm_word")) {
              continue;
            }
            if (repEle.hasClass("ng")) {
              continue;
            }
            isBlur = true;
            break;
          }
          if (isBlur && !ele.hasClass("has_blur_word")) {
            ele.addClass("has_blur_word");
            if (ele.hasClass("has_image") && imageBlur) {
              MediaContainer$1.setImageBlur(ele, true);
            }
          } else if (!isBlur && ele.hasClass("has_blur_word")) {
            ele.removeClass("has_blur_word");
            if (ele.hasClass("has_image") && imageBlur) {
              MediaContainer$1.setImageBlur(ele, false);
            }
          }
        }
      }

      /**
      @method addThumbnail
      @param {HTMLAElement} sourceA
      @param {String} thumbnailPath
      @param {String} [mediaType="image"]
      @param {Object} res
      */
      addThumbnail(sourceA, thumbnailPath, mediaType = "image", res) {
        var article, h, pre, ref, sib, thumbnail, thumbnailFavicon, thumbnailImg, thumbnailLink, v, webkitFilter;
        sourceA.addClass("has_thumbnail");
        thumbnail = $__("div").addClass("thumbnail");
        thumbnail.setAttr("media-type", mediaType);
        if (mediaType === "image" || mediaType === "video") {
          article = sourceA.closest("article");
          article.addClass("has_image");
          // グロ画像に対するぼかし処理
          if (article.hasClass("has_blur_word") && app.config.isOn("image_blur")) {
            thumbnail.addClass("image_blur");
            v = app.config.get("image_blur_length");
            webkitFilter = `blur(${v}px)`;
          } else {
            webkitFilter = "none";
          }
        }
        switch (mediaType) {
          case "image":
            thumbnailLink = $__("a");
            thumbnailLink.href = app.safeHref(sourceA.href);
            thumbnailLink.target = "_blank";
            thumbnailImg = $__("img").addClass("image");
            thumbnailImg.src = "/img/dummy_1x1.webp";
            thumbnailImg.style.WebkitFilter = webkitFilter;
            thumbnailImg.style.maxWidth = `${app.config.get("image_width")}px`;
            thumbnailImg.style.maxHeight = `${app.config.get("image_height")}px`;
            thumbnailImg.dataset.src = thumbnailPath;
            thumbnailImg.dataset.type = res.type;
            if (res.extract != null) {
              thumbnailImg.dataset.extract = res.extract;
            }
            if (res.extractReferrer != null) {
              thumbnailImg.dataset.extractReferrer = res.extractReferrer;
            }
            if (res.pattern != null) {
              thumbnailImg.dataset.pattern = res.pattern;
            }
            if (res.cookie != null) {
              thumbnailImg.dataset.cookie = res.cookie;
            }
            if (res.cookieReferrer != null) {
              thumbnailImg.dataset.cookieReferrer = res.cookieReferrer;
            }
            if (res.referrer != null) {
              thumbnailImg.dataset.referrer = res.referrer;
            }
            if (res.userAgent != null) {
              thumbnailImg.dataset.userAgent = res.userAgent;
            }
            thumbnailLink.addLast(thumbnailImg);
            thumbnailFavicon = $__("img").addClass("favicon");
            thumbnailFavicon.src = "/img/dummy_1x1.webp";
            thumbnailFavicon.dataset.src = `https://www.google.com/s2/favicons?domain=${sourceA.hostname}`;
            thumbnailLink.addLast(thumbnailFavicon);
            break;
          case "audio":
          case "video":
            thumbnailLink = $__(mediaType);
            thumbnailLink.src = "";
            thumbnailLink.dataset.src = thumbnailPath;
            thumbnailLink.preload = "metadata";
            switch (mediaType) {
              case "audio":
                thumbnailLink.style.width = `${app.config.get("audio_width")}px`;
                thumbnailLink.controls = true;
                break;
              case "video":
                thumbnailLink.style.WebkitFilter = webkitFilter;
                thumbnailLink.style.maxWidth = `${app.config.get("video_width")}px`;
                thumbnailLink.style.maxHeight = `${app.config.get("video_height")}px`;
                if (app.config.isOn("video_controls")) {
                  thumbnailLink.controls = true;
                }
            }
        }
        thumbnail.addLast(thumbnailLink);
        // 高さ固定の場合
        if (app.config.isOn("image_height_fix")) {
          switch (mediaType) {
            case "image":
              h = parseInt(app.config.get("image_height"));
              break;
            case "video":
              h = parseInt(app.config.get("video_height"));
              break;
            default:
              h = 100; // 最低高
          }
          thumbnail.style.height = `${h}px`;
        }
        sib = sourceA;
        while (true) {
          pre = sib;
          sib = pre.next();
          if ((sib == null) || sib.tagName === "BR") {
            if (sib != null ? (ref = sib.next()) != null ? ref.hasClass("thumbnail") : void 0 : void 0) {
              continue;
            }
            pre.addAfter(thumbnail);
            if (!pre.hasClass("thumbnail")) {
              pre.addAfter($__("br"));
            }
            break;
          }
        }
      }

      /**
      @method addExpandedURL
      @param {HTMLAElement} sourceA
      @param {String} finalUrl
      */
      addExpandedURL(sourceA, finalUrl) {
        var expandedURL, expandedURLLink, pre, ref, sib;
        sourceA.addClass("has_expandedURL");
        expandedURL = $__("div").addClass("expandedURL");
        expandedURL.setAttr("short-url", sourceA.href);
        if (app.config.get("expand_short_url") === "popup") {
          expandedURL.addClass("hide_data");
        }
        if (finalUrl) {
          expandedURLLink = $__("a");
          expandedURLLink.textContent = finalUrl;
          expandedURLLink.href = app.safeHref(finalUrl);
          expandedURLLink.target = "_blank";
          expandedURL.addLast(expandedURLLink);
        } else {
          expandedURL.addClass("expand_error");
          expandedURLLink = null;
        }
        sib = sourceA;
        while (true) {
          pre = sib;
          sib = pre.next();
          if ((sib == null) || sib.tagName === "BR") {
            if (sib != null ? (ref = sib.next()) != null ? ref.hasClass("expandedURL") : void 0 : void 0) {
              continue;
            }
            pre.addAfter(expandedURL);
            if (!pre.hasClass("expandedURL")) {
              pre.addAfter($__("br"));
            }
            break;
          }
        }
        return expandedURLLink;
      }

      /**
      @method checkUrlExpand
      @param {HTMLAnchorElement} a
      */
      async checkUrlExpand(a) {
        var finalUrl, newLink;
        if (app.config.get("expand_short_url") !== "none" && app.URL.SHORT_URL_LIST.has(a.hostname)) {
          // 短縮URLの展開
          finalUrl = (await app.URL.expandShortURL(a.href));
          newLink = this.addExpandedURL(a, finalUrl);
          if (finalUrl) {
            return {
              a,
              link: newLink.href
            };
          }
        }
        return {
          a,
          link: a.href
        };
      }

      /**
      @method addClassWithOrg
      @param {Element} $res
      @param {String} className
      */
      addClassWithOrg($res, className) {
        var resnum;
        $res.addClass(className);
        resnum = parseInt($res.C("num")[0].textContent);
        this.container.child()[resnum - 1].addClass(className);
      }

      /**
      @method removeClassWithOrg
      @param {Element} $res
      @param {String} className
      */
      removeClassWithOrg($res, className) {
        var resnum;
        $res.removeClass(className);
        resnum = parseInt($res.C("num")[0].textContent);
        this.container.child()[resnum - 1].removeClass(className);
      }

      /**
      @method addWriteHistory
      @param {Element} $res
      */
      addWriteHistory($res) {
        var date;
        date = app.util.stringToDate($res.C("other")[0].textContent).valueOf();
        if (date != null) {
          app.WriteHistory.add({
            url: this.urlStr,
            res: parseInt($res.C("num")[0].textContent),
            title: document.title,
            name: $res.C("name")[0].textContent,
            mail: $res.C("mail")[0].textContent,
            message: $res.C("message")[0].textContent,
            date
          });
        }
      }

      /**
      @method removeWriteHistory
      @param {Element} $res
      */
      removeWriteHistory($res) {
        var resnum;
        resnum = parseInt($res.C("num")[0].textContent);
        app.WriteHistory.remove(this.urlStr, resnum);
      }

    }
    _OVER1000_DATA = "Over 1000";

    return ThreadContent;

  }).call(window);

  /**
  @class ThreadList
  @constructor
  @param {Element} table
  @param {Object} option
    @param {Boolean} [option.bookmark=false]
    @param {Boolean} [option.title=false]
    @param {Boolean} [option.boardTitle=false]
    @param {Boolean} [option.res=false]
    @param {Boolean} [option.unread=false]
    @param {Boolean} [option.heat=false]
    @param {Boolean} [option.createdDate=false]
    @param {Boolean} [option.viewedDate=false]
    @param {Boolean} [option.bookmarkAddRm=false]
    @param {Element} [option.searchbox]
  */
  var ThreadList,
    indexOf = [].indexOf;

  var ThreadList$1 = ThreadList = (function() {
    class ThreadList {
      constructor(table, option) {
        var $col, $cols, $searchbox, $table, $th, $thead, $tr, className, column, i, key, keyToLabel, selector, titleIndex, val;
        this.table = table;
        /**
        @property _flg
        @type Object
        @private
        */
        this._flg = {
          bookmark: false,
          title: false,
          boardTitle: false,
          res: false,
          writtenRes: false,
          unread: false,
          heat: false,
          name: false,
          mail: false,
          message: false,
          createdDate: false,
          viewedDate: false,
          writtenDate: false,
          bookmarkAddRm: !!option.bookmarkAddRm,
          searchbox: void 0
        };
        keyToLabel = {
          bookmark: "★",
          title: "タイトル",
          boardTitle: "板名",
          res: "レス数",
          writtenRes: "レス番号",
          unread: "未読数",
          heat: "勢い",
          name: "名前",
          mail: "メール",
          message: "本文",
          createdDate: "作成日時",
          viewedDate: "閲覧日時",
          writtenDate: "書込日時"
        };
        $table = this.table;
        $thead = $__("thead");
        $table.addLast($thead, $__("tbody"));
        $tr = $__("tr");
        $thead.addLast($tr);
        //項目のツールチップ表示
        $table.on("mouseenter", async function({target}) {
          if (target.tagName === "TD") {
            await app.defer();
            target.title = target.textContent;
          }
        }, true);
        $table.on("mouseleave", function({target}) {
          if (target.tagName === "TD") {
            target.removeAttr("title");
          }
        }, true);
        $cols = $_F();
        selector = {};
        column = {};
        i = 0;
        for (key in keyToLabel) {
          val = keyToLabel[key];
          if (!(indexOf.call(option.th, key) >= 0)) {
            continue;
          }
          i++;
          className = key.replace(/([A-Z])/g, function($0, $1) {
            return "_" + $1.toLowerCase();
          });
          $th = $__("th").addClass(className);
          $th.textContent = val;
          $th.dataset.key = className;
          $tr.addLast($th);
          this._flg[key] = true;
          selector[key] = `td:nth-child(${i})`;
          column[key] = i;
          $col = $__("col").addClass(className);
          $col.span = 1;
          $cols.addLast($col);
        }
        $table.addFirst($cols);
        //ブックマーク更新時処理
        app.message.on("bookmark_updated", async({type, bookmark}) => {
          var boardTitle, boardUrl, oldResCount, oldUnread, td, tr, unread, url;
          if (bookmark.type !== "thread") {
            return;
          }
          if (type === "expired") {
            $tr = $table.$(`tr[data-href="${bookmark.url}"]`);
            if ($tr != null) {
              if (bookmark.expired) {
                $tr.addClass("expired");
                if (app.config.isOn("bookmark_show_dat")) {
                  $tr.removeClass("hidden");
                } else {
                  $tr.addClass("hidden");
                }
              } else {
                $tr.removeClass("expired");
              }
            }
          }
          if (type === "errored") {
            $tr = $table.$(`tr[data-href="${bookmark.url}"]`);
            if ($tr != null) {
              $tr.addClass("errored");
            }
          }
          if (type === "updated") {
            $tr = $table.$(`tr[data-href="${bookmark.url}"]`);
            if ($tr != null) {
              $tr.removeClass("errored");
            }
          }
          if (this._flg.bookmark) {
            if (type === "added") {
              $tr = $table.$(`tr[data-href="${bookmark.url}"]`);
              if ($tr != null) {
                $tr.$(selector.bookmark).textContent = "★";
              }
            } else if (type === "removed") {
              $tr = $table.$(`tr[data-href="${bookmark.url}"]`);
              if ($tr != null) {
                $tr.$(selector.bookmark).textContent = "";
              }
            }
          }
          if (this._flg.bookmarkAddRm) {
            if (type === "added") {
              url = new app.URL.URL(bookmark.url);
              boardUrl = url.toBoard();
              try {
                boardTitle = (await app.BoardTitleSolver.ask(boardUrl));
              } catch (error) {
                boardTitle = "";
              }
              this.addItem({
                title: bookmark.title,
                url: bookmark.url,
                resCount: bookmark.resCount || 0,
                readState: bookmark.readState || null,
                createdAt: /\/(\d+)\/$/.exec(url.pathname)[1] * 1000,
                boardUrl: boardUrl.href,
                boardTitle,
                expired: bookmark.expired,
                isHttps: url.isHttps()
              });
            } else if (type === "removed") {
              $table.$(`tr[data-href="${bookmark.url}"]`).remove();
            }
          }
          if (this._flg.res && type === "res_count") {
            tr = $table.$(`tr[data-href="${bookmark.url}"]`);
            if (tr) {
              td = tr.$(selector.res);
              oldResCount = +td.textContent;
              td.textContent = bookmark.resCount;
              td.dataset.beforeres = oldResCount;
              if (this._flg.unread) {
                td = tr.$(selector.unread);
                oldUnread = +td.textContent;
                unread = oldUnread + (bookmark.resCount - oldResCount);
                td.textContent = unread || "";
                if (unread > 0) {
                  tr.addClass("updated");
                } else {
                  tr.removeClass("updated");
                }
              }
              if (this._flg.heat) {
                td = tr.$(selector.heat);
                td.textContent = ThreadList._calcHeat(Date.now(), /\/(\d+)\/$/.exec(bookmark.url)[1] * 1000, bookmark.resCount);
              }
            }
          }
          if (this._flg.title && type === "title") {
            $tr = $table.$(`tr[data-href="${bookmark.url}"]`);
            if ($tr != null) {
              $tr.$(selector.title).textContent = bookmark.title;
            }
          }
        });
        //未読数更新
        if (this._flg.unread) {
          app.message.on("read_state_updated", function({read_state}) {
            var res, tr, unread, unreadCount;
            tr = $table.$(`tr[data-href="${read_state.url}"]`);
            if (tr) {
              res = tr.$(selector.res);
              if (+res.textContent < read_state.received) {
                res.textContent = read_state.received;
              }
              unread = tr.$(selector.unread);
              unreadCount = Math.max(+res.textContent - read_state.read, 0);
              unread.textContent = unreadCount || "";
              if (unreadCount > 0) {
                tr.addClass("updated");
              } else {
                tr.removeClass("updated");
              }
            }
          });
          app.message.on("read_state_removed", function({url}) {
            var tr;
            tr = $table.$(`tr[data-href="${url}"]`);
            if (tr) {
              tr.$(selector.unread).textContent = "";
              tr.removeClass("updated");
            }
          });
        }
        //リスト内検索
        if (typeof option.searchbox === "object") {
          titleIndex = column.title;
          $searchbox = option.searchbox;
          $searchbox.on("compositionend", function() {
            this.emit(new Event("input"));
          });
          $searchbox.on("input", function({isComposing}) {
            var dom, hitCount, j, k, len, len1, ref, ref1;
            if (isComposing) {
              return;
            }
            if (this.value !== "") {
              TableSearch$1($table, "search", {
                query: this.value,
                target_col: titleIndex
              });
              hitCount = $table.dataset.tableSearchHitCount;
              ref = this.parent().child();
              for (j = 0, len = ref.length; j < len; j++) {
                dom = ref[j];
                if (dom.hasClass("hit_count")) {
                  dom.textContent = hitCount + "hit";
                }
              }
            } else {
              TableSearch$1($table, "clear");
              ref1 = this.parent().child();
              for (k = 0, len1 = ref1.length; k < len1; k++) {
                dom = ref1[k];
                if (dom.hasClass("hit_count")) {
                  dom.textContent = "";
                }
              }
            }
          });
          $searchbox.on("keyup", function({key}) {
            if (key === "Escape") {
              this.value = "";
              this.emit(new Event("input"));
            }
          });
        }
        //コンテキストメニュー
        if (this._flg.bookmark || this._flg.bookmarkAddRm || this._flg.writtenRes || this._flg.viewedDate) {
          (() => {
            return $table.on("contextmenu", async(e) => {
              var $menu, fn, ref, ref1, ref2, url;
              $tr = e.target.closest("tbody > tr");
              if (!$tr) {
                return;
              }
              e.preventDefault();
              await app.defer();
              $menu = $$.I("template_thread_list_contextmenu").content.$(".thread_list_contextmenu").cloneNode(true);
              $table.closest(".view").addLast($menu);
              url = $tr.dataset.href;
              if (app.bookmark.get(url)) {
                if ((ref = $menu.C("add_bookmark")[0]) != null) {
                  ref.remove();
                }
              } else {
                if ((ref1 = $menu.C("del_bookmark")[0]) != null) {
                  ref1.remove();
                }
              }
              if (!this._flg.unread || !/^\d+$/.test($tr.$(selector.unread).textContent) || (app.bookmark.get(url) != null)) {
                if ((ref2 = $menu.C("del_read_state")[0]) != null) {
                  ref2.remove();
                }
              }
              $menu.on("click", fn = function({target}) {
                var dateValue, ref3, ref4, ref5, ref6, ref7, ref8, threadRes, threadTitle, threadURL, threadWrittenRes;
                if (target.tagName !== "LI") {
                  return;
                }
                $menu.off("click", fn);
                if ($tr == null) {
                  return;
                }
                threadURL = $tr.dataset.href;
                threadTitle = (ref3 = $tr.$(selector.title)) != null ? ref3.textContent : void 0;
                threadRes = parseInt((ref4 = (ref5 = $tr.$(selector.res)) != null ? ref5.textContent : void 0) != null ? ref4 : 0);
                threadWrittenRes = parseInt((ref6 = (ref7 = $tr.$(selector.writtenRes)) != null ? ref7.textContent : void 0) != null ? ref6 : 0);
                dateValue = (ref8 = $tr.$(selector.viewedDate)) != null ? ref8.getAttr("date-value") : void 0;
                switch (false) {
                  case !target.hasClass("add_bookmark"):
                    app.bookmark.add(threadURL, threadTitle, threadRes);
                    break;
                  case !target.hasClass("del_bookmark"):
                    app.bookmark.remove(threadURL);
                    break;
                  case !target.hasClass("del_history"):
                    app.History.remove(threadURL, +dateValue);
                    $tr.remove();
                    break;
                  case !target.hasClass("del_writehistory"):
                    app.WriteHistory.remove(threadURL, threadWrittenRes);
                    $tr.remove();
                    break;
                  case !target.hasClass("ignore_res_number"):
                    $tr.setAttr("ignore-res-number", "on");
                    $tr.emit(new Event("mousedown", {
                      bubbles: true
                    }));
                    break;
                  case !target.hasClass("del_read_state"):
                    app.ReadState.remove(threadURL);
                }
                this.remove();
              });
              ContextMenu$1($menu, e.clientX, e.clientY);
            });
          })();
          return;
        }
        return;
      }

      /**
      @method _calcHeat
      @static
      @private
      @param {Number} now
      @param {Number} created
      @param {Number} resCount
      @return {String}
      */
      static _calcHeat(now, created, resCount) {
        var elapsed;
        if (!/^\d+$/.test(created)) {
          created = (new Date(created)).getTime();
        }
        if (created > now) {
          return "0.0";
        }
        elapsed = Math.max((now - created) / 1000, 1) / (24 * 60 * 60);
        return (resCount / elapsed).toFixed(1);
      }

      /**
      @method addItem
      @param {Object|Array}
      */
      addItem(arg) {
        var $fragment, $tbody, $td, $tr, item, j, len, now;
        if (!Array.isArray(arg)) {
          arg = [arg];
        }
        $tbody = this.table.$("tbody");
        now = Date.now();
        $fragment = $_F();
        for (j = 0, len = arg.length; j < len; j++) {
          item = arg[j];
          $tr = $__("tr").addClass("open_in_rcrx");
          if (item.expired) {
            $tr.addClass("expired");
          }
          if (item.ng) {
            $tr.addClass("ng_thread");
          }
          if (item.isNet) {
            $tr.addClass("net");
          }
          if (item.isHttps) {
            $tr.addClass("https");
          }
          if (item.expired && !app.config.isOn("bookmark_show_dat")) {
            $tr.addClass("hidden");
          }
          $tr.dataset.href = app.escapeHtml(item.url);
          $tr.dataset.title = app.escapeHtml(item.title);
          if (item.threadNumber != null) {
            $tr.dataset.threadNumber = app.escapeHtml("" + item.threadNumber);
          }
          if (this._flg.writtenRes && item.res > 0) {
            $tr.dataset.writtenResNum = item.res;
          }
          //ブックマーク状況
          if (this._flg.bookmark) {
            $td = $__("td");
            if (app.bookmark.get(item.url)) {
              $td.textContent = "★";
            }
            $tr.addLast($td);
          }
          //タイトル
          if (this._flg.title) {
            $td = $__("td");
            $td.textContent = item.title;
            $tr.addLast($td);
          }
          //板名
          if (this._flg.boardTitle) {
            $td = $__("td");
            $td.textContent = item.boardTitle;
            $tr.addLast($td);
          }
          //レス数
          if (this._flg.res) {
            $td = $__("td");
            if (item.resCount > 0) {
              $td.textContent = item.resCount;
            }
            $tr.addLast($td);
          }
          //レス番号
          if (this._flg.writtenRes) {
            $td = $__("td");
            if (item.res > 0) {
              $td.textContent = item.res;
            }
            $tr.addLast($td);
          }
          //未読数
          if (this._flg.unread) {
            $td = $__("td");
            if (item.readState && item.resCount > item.readState.read) {
              $td.textContent = item.resCount - item.readState.read;
              $tr.addClass("updated");
            }
            $tr.addLast($td);
          }
          //勢い
          if (this._flg.heat) {
            $td = $__("td");
            $td.textContent = ThreadList._calcHeat(now, item.createdAt, item.resCount);
            $tr.addLast($td);
          }
          //名前
          if (this._flg.name) {
            $td = $__("td");
            $td.textContent = item.name;
            $tr.addLast($td);
          }
          //メール
          if (this._flg.mail) {
            $td = $__("td");
            $td.textContent = item.mail;
            $tr.addLast($td);
          }
          //本文
          if (this._flg.message) {
            $td = $__("td");
            $td.textContent = item.message;
            $tr.addLast($td);
          }
          //作成日時
          if (this._flg.createdDate) {
            $td = $__("td");
            $td.textContent = ThreadList._dateToString(new Date(item.createdAt));
            $tr.addLast($td);
          }
          //閲覧日時
          if (this._flg.viewedDate) {
            $td = $__("td");
            $td.setAttr("date-value", item.date);
            $td.textContent = ThreadList._dateToString(new Date(item.date));
            $tr.addLast($td);
          }
          //書込日時
          if (this._flg.writtenDate) {
            $td = $__("td");
            $td.textContent = ThreadList._dateToString(new Date(item.date));
            $tr.addLast($td);
          }
          $fragment.addLast($tr);
        }
        $tbody.addLast($fragment);
      }

      /**
      @method empty
      */
      empty() {
        this.table.$("tbody").innerHTML = "";
      }

      /**
      @method getSelected
      @return {Element|null}
      */
      getSelected() {
        return this.table.$("tr.selected");
      }

      /**
      @method select
      @param {Element|number} tr
      */
      select(target) {
        this.clearSelect();
        if (typeof target === "number") {
          target = this.table.$(`tbody > tr:nth-child(${target}), tbody > tr:last-child`);
        }
        if (!target) {
          return;
        }
        target.addClass("selected");
        target.scrollIntoView({
          behavior: "instant",
          block: "center",
          inline: "center"
        });
      }

      /**
      @method selectNext
      @param {number} [repeat = 1]
      */
      selectNext(repeat = 1) {
        var current, j, prevCurrent, ref;
        current = this.getSelected();
        if (current) {
          for (j = 0, ref = repeat; (0 <= ref ? j < ref : j > ref); 0 <= ref ? j++ : j--) {
            prevCurrent = current;
            current = current.next();
            while (current && current.offsetHeight === 0) {
              current = current.next();
            }
            if (!current) {
              current = prevCurrent;
              break;
            }
          }
        } else {
          current = this.table.$("tbody > tr");
        }
        if (current) {
          this.select(current);
        }
      }

      /**
      @method selectPrev
      @param {number} [repeat = 1]
      */
      selectPrev(repeat = 1) {
        var current, j, prevCurrent, ref;
        current = this.getSelected();
        if (current) {
          for (j = 0, ref = repeat; (0 <= ref ? j < ref : j > ref); 0 <= ref ? j++ : j--) {
            prevCurrent = current;
            current = current.prev();
            while (current && current.offsetHeight === 0) {
              current = current.prev();
            }
            if (!current) {
              current = prevCurrent;
              break;
            }
          }
        } else {
          current = this.table.$("tbody > tr");
        }
        if (current) {
          this.select(current);
        }
      }

      /**
      @method clearSelect
      */
      clearSelect() {
        var ref;
        if ((ref = this.getSelected()) != null) {
          ref.removeClass("selected");
        }
      }

    }
    /**
    @method _dateToString
    @static
    @private
    @param {Date}
    @return {String}
    */
    ThreadList._dateToString = (function() {
      var fn;
      fn = function(a) {
        return (a < 10 ? "0" : "") + a;
      };
      return function(date) {
        return date.getFullYear() + "/" + fn(date.getMonth() + 1) + "/" + fn(date.getDate()) + " " + fn(date.getHours()) + ":" + fn(date.getMinutes());
      };
    })();

    return ThreadList;

  }).call(window);

  exports.AANoOverflow = AANoOverflow$1;
  exports.Animate = Animate;
  exports.ContextMenu = ContextMenu$1;
  exports.Dialog = Dialog$1;
  exports.LazyLoad = LazyLoad;
  exports.MediaContainer = MediaContainer$1;
  exports.PopupView = PopupView$1;
  exports.SearchNextThread = SearchNextThread;
  exports.SelectableAccordion = SelectableAccordion;
  exports.Sortable = Sortable;
  exports.Tab = Tab;
  exports.TableSearch = TableSearch$1;
  exports.TableSorter = TableSorter$1;
  exports.ThreadContent = ThreadContent$1;
  exports.ThreadList = ThreadList$1;
  exports.VirtualNotch = VirtualNotch;

  return exports;

}({}));
