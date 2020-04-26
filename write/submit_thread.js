(function () {
  'use strict';

  class Request {
      constructor(method, url, { mimeType = null, headers = {}, timeout = 30000, preventCache = false } = {}) {
          this.method = method;
          this.url = url;
          this.mimeType = mimeType;
          this.timeout = timeout;
          this.headers = headers;
          this.preventCache = preventCache;
      }
      send() {
          const url = this.url;
          if (this.preventCache) {
              this.headers["Pragma"] = "no-cache";
              this.headers["Cache-Control"] = "no-cache";
          }
          return new Promise((resolve, reject) => {
              const xhr = new XMLHttpRequest();
              xhr.open(this.method, url);
              if (this.mimeType !== null) {
                  xhr.overrideMimeType(this.mimeType);
              }
              xhr.timeout = this.timeout;
              for (const [key, val] of Object.entries(this.headers)) {
                  xhr.setRequestHeader(key, val);
              }
              xhr.on("loadend", () => {
                  const resonseHeaders = Request.parseHTTPHeader(xhr.getAllResponseHeaders());
                  resolve(new Response(xhr.status, resonseHeaders, xhr.responseText, xhr.responseURL));
              });
              xhr.on("timeout", () => {
                  reject("timeout");
              });
              xhr.on("abort", () => {
                  reject("abort");
              });
              xhr.send();
              this.xhr = xhr;
              return;
          });
      }
      abort() {
          this.xhr.abort();
      }
      static parseHTTPHeader(str) {
          const reg = /^(?:([a-z\-]+):\s*|([ \t]+))(.+)\s*$/gim;
          const headers = {};
          let last;
          let res;
          while (res = reg.exec(str)) {
              if (typeof res[1] !== "undefined") {
                  headers[res[1]] = res[3];
                  last = res[1];
              }
              else if (typeof last !== "undefined") {
                  headers[last] += res[2] + res[3];
              }
          }
          return headers;
      }
  }
  class Response {
      constructor(status, headers = {}, body, responseURL) {
          this.status = status;
          this.headers = headers;
          this.body = body;
          this.responseURL = responseURL;
      }
  }

  var $span;

  //文字参照をデコード
  $span = $__("span");

  var indexedDBRequestToPromise = function(req) {
    return new Promise(function(resolve, reject) {
      req.onsuccess = resolve;
      req.onerror = reject;
    });
  };

  /**
  @class Cache
  @constructor
  @param {String} key
  */
  var Cache;

  Cache = (function() {
    class Cache {
      constructor(key1) {
        this.key = key1;
        /**
        @property data
        @type String
        */
        this.data = null;
        /**
        @property parsed
        @type Object
        */
        this.parsed = null;
        /**
        @property lastUpdated
        @type Number
        */
        this.lastUpdated = null;
        /**
        @property lastModified
        @type Number
        */
        this.lastModified = null;
        /**
        @property etag
        @type String
        */
        this.etag = null;
        /**
        @property resLength
        @type Number
        */
        this.resLength = null;
        /**
        @property datSize
        @type Number
        */
        this.datSize = null;
        /**
        @property readcgiVer
        @type Number
        */
        this.readcgiVer = null;
      }

      /**
      @method count
      @static
      @return {Promise}
      */
      static async count() {
        var db, e, req, res;
        try {
          db = (await this._dbOpen);
          req = db.transaction("Cache").objectStore("Cache").count();
          res = (await indexedDBRequestToPromise(req));
        } catch (error) {
          e = error;
          app.log("error", "Cache.count: トランザクション中断");
          throw new Error(e);
        }
        return res.target.result;
      }

      /**
      @method delete
      @static
      @return {Promise}
      */
      static async delete() {
        var db, e, req;
        try {
          db = (await this._dbOpen);
          req = db.transaction("Cache", "readwrite").objectStore("Cache").clear();
          await indexedDBRequestToPromise(req);
        } catch (error) {
          e = error;
          app.log("error", "Cache.delete: トランザクション中断");
          throw new Error(e);
        }
      }

      /**
      @method clearRange
      @param {Number} day
      @static
      @return {Promise}
      */
      static async clearRange(day) {
        var dayUnix, db, e, keys, req, store;
        dayUnix = Date.now() - day * 24 * 60 * 60 * 1000;
        try {
          db = (await this._dbOpen);
          store = db.transaction("Cache", "readwrite").objectStore("Cache");
          req = store.index("last_updated").getAllKeys(IDBKeyRange.upperBound(dayUnix, true));
          ({
            target: {
              result: keys
            }
          } = (await indexedDBRequestToPromise(req)));
          await Promise.all(keys.map(async function(key) {
            req = store.delete(key);
            await indexedDBRequestToPromise(req);
          }));
        } catch (error) {
          e = error;
          app.log("error", "Cache.clearRange: トランザクション中断");
          throw new Error(e);
        }
      }

      /**
      @method get
      @return {Promise}
      */
      async get() {
        var data, db, e, key, newKey, req, result, val;
        try {
          db = (await Cache._dbOpen);
          req = db.transaction("Cache").objectStore("Cache").get(this.key);
          ({
            target: {result}
          } = (await indexedDBRequestToPromise(req)));
          if (result == null) {
            throw new Error("キャッシュが存在しません");
          }
          data = app.deepCopy(result);
          for (key in data) {
            val = data[key];
            newKey = (function() {
              switch (key) {
                case "last_updated":
                  return "lastUpdated";
                case "last_modified":
                  return "lastModified";
                case "res_length":
                  return "resLength";
                case "dat_size":
                  return "datSize";
                case "readcgi_ver":
                  return "readcgiVer";
                default:
                  return key;
              }
            })();
            this[newKey] = val != null ? val : null;
          }
        } catch (error) {
          e = error;
          if (e.message !== "キャッシュが存在しません") {
            app.log("error", "Cache::get: トランザクション中断");
          }
          throw new Error(e);
        }
      }

      /**
      @method put
      @return {Promise}
      */
      async put() {
        var data, db, e, req;
        if (!(typeof this.key === "string" && (((this.data != null) && typeof this.data === "string") || ((this.parsed != null) && this.parsed instanceof Object)) && typeof this.lastUpdated === "number" && ((this.lastModified == null) || typeof this.lastModified === "number") && ((this.etag == null) || typeof this.etag === "string") && ((this.resLength == null) || Number.isFinite(this.resLength)) && ((this.datSize == null) || Number.isFinite(this.datSize)) && ((this.readcgiVer == null) || Number.isFinite(this.readcgiVer)))) {
          app.log("error", "Cache::put: データが不正です", this);
          throw new Error("キャッシュしようとしたデータが不正です");
        }
        data = this.data != null ? app.replaceAll(this.data, "\u0000", "\u0020") : null;
        try {
          db = (await Cache._dbOpen);
          req = db.transaction("Cache", "readwrite").objectStore("Cache").put({
            url: this.key,
            data,
            parsed: this.parsed || null,
            last_updated: this.lastUpdated,
            last_modified: this.lastModified || null,
            etag: this.etag || null,
            res_length: this.resLength || null,
            dat_size: this.datSize || null,
            readcgi_ver: this.readcgiVer || null
          });
          await indexedDBRequestToPromise(req);
        } catch (error) {
          e = error;
          app.log("error", "Cache::put: トランザクション中断");
          throw new Error(e);
        }
      }

      /**
      @method delete
      @return {Promise}
      */
      async delete() {
        var db, e, req;
        try {
          db = (await Cache._dbOpen);
          req = db.transaction("Cache", "readwrite").objectStore("Cache").delete(url);
          await indexedDBRequestToPromise(req);
        } catch (error) {
          e = error;
          app.log("error", "Cache::delete: トランザクション中断");
          throw new Error(e);
        }
      }

    }
    /**
    @property _dbOpen
    @type Promise
    @static
    @private
    */
    Cache._dbOpen = new Promise(function(resolve, reject) {
      var req;
      req = indexedDB.open("Cache", 1);
      req.onerror = reject;
      req.onupgradeneeded = function({
          target: {
            result: db,
            transaction: tx
          }
        }) {
        var objStore;
        objStore = db.createObjectStore("Cache", {
          keyPath: "url"
        });
        objStore.createIndex("last_updated", "last_updated", {
          unique: false
        });
        objStore.createIndex("last_modified", "last_modified", {
          unique: false
        });
        tx.oncomplete = function() {
          return resolve(db);
        };
      };
      req.onsuccess = function({
          target: {
            result: db
          }
        }) {
        resolve(db);
      };
    });

    return Cache;

  }).call(window);

  var target = $__("div");

  let serverNet = new Map();
  let serverSc = new Map();
  let serverPink = new Map();
  class URL extends window.URL {
      constructor(url) {
          super(url);
          this.guessedType = { type: "unknown", bbsType: "unknown" };
          this.tsld = null;
          this.archive = false;
          this.rawUrl = url;
          this.rawHash = this.hash;
          this.hash = "";
          this.fix();
      }
      fixPathAndSetType(reg, replace, type) {
          const res = reg.exec(this.pathname);
          if (res) {
              this.pathname = replace(res);
              this.guessedType = type;
          }
          return !!res;
      }
      fix() {
          // 2ch.net -> 5ch.net & jbbs.livedoor.jp -> jbbs.shitaraba.net
          if (this.hostname === "2ch.net" || this.hostname.endsWith(".2ch.net")) {
              this.hostname = this.hostname.replace("2ch.net", "5ch.net");
          }
          else if (this.hostname === "jbbs.livedoor.jp") {
              this.hostname = "jbbs.shitaraba.net";
          }
          // スレ系: 誤爆する事は考えられないので、パラメータ部分をバッサリ切ってしまう
          // 板系: 完全に誤爆を少しでも減らすために、パラメータ形式も限定する
          if (this.hostname === "ula.5ch.net") {
              const res = URL.CH_THREAD_ULA_REG.exec(this.pathname);
              if (res) {
                  this.hostname = res[2];
                  this.pathname = `/test/read.cgi/${res[1]}/${res[3]}/`;
                  this.guessedType = { type: "thread", bbsType: "2ch" };
              }
              return;
          }
          if (this.hostname.includes("machi.to")) {
              const isThread = this.fixPathAndSetType(URL.MACHI_THREAD_REG, (res) => `/bbs/read.cgi/${res[1]}/`, { type: "thread", bbsType: "machi" });
              if (isThread)
                  return;
              this.fixPathAndSetType(URL.MACHI_BOARD_REG, (res) => `/${res[1]}`, { type: "board", bbsType: "machi" });
              return;
          }
          if (this.hostname === "jbbs.shitaraba.net") {
              const isThread = this.fixPathAndSetType(URL.SHITARABA_THREAD_REG, (res) => `/bbs/${res[1]}/`, { type: "thread", bbsType: "jbbs" });
              if (isThread) {
                  if (this.pathname.includes("read_archive")) {
                      this.archive = true;
                  }
                  return;
              }
              const isArchive = this.fixPathAndSetType(URL.SHITARABA_ARCHIVE_REG, (res) => `/bbs/read_archive.cgi/${res[1]}/${res[2]}/`, { type: "thread", bbsType: "jbbs" });
              if (isArchive) {
                  this.archive = true;
                  return;
              }
              this.fixPathAndSetType(URL.SHITARABA_BOARD_REG, (res) => `/${res[1]}`, { type: "board", bbsType: "jbbs" });
              return;
          }
          // 2ch系
          {
              const isThread = this.fixPathAndSetType(URL.CH_THREAD_REG, (res) => `/${res[1]}/`, { type: "thread", bbsType: "2ch" });
              if (isThread)
                  return;
              /*
              const isThread2 = this.fixPathAndSetType(
                URL.CH_THREAD_REG2,
                (res) => `/${res[1]}/`,
                {type: "thread", bbsType: "2ch"}
              );
              if (isThread2) return;
              */
              this.fixPathAndSetType(URL.CH_BOARD_REG, (res) => `/${res[1]}`, { type: "board", bbsType: "2ch" });
          }
      }
      guessType() {
          return this.guessedType;
      }
      isArchive() {
          return this.archive;
      }
      getTsld() {
          if (this.tsld === null) {
              const dotList = this.hostname.split(".");
              const len = dotList.length;
              if (len >= 2) {
                  this.tsld = `${dotList[len - 2]}.${dotList[len - 1]}`;
              }
              else {
                  this.tsld = "";
              }
          }
          return this.tsld;
      }
      isHttps() {
          return (this.protocol === "https:");
      }
      toggleProtocol() {
          this.protocol = this.isHttps() ? "http:" : "https:";
      }
      createProtocolToggled() {
          const toggled = new URL(this.href);
          toggled.toggleProtocol();
          return toggled;
      }
      getResNumber() {
          const { type, bbsType } = this.guessedType;
          if (type !== "thread" || bbsType === "unknown") {
              return null;
          }
          const raw = new window.URL(this.rawUrl);
          if (bbsType === "jbbs") {
              const res = URL.SHITARABA_RESNUM_REG.exec(raw.pathname);
              return res ? res[1] : null;
          }
          if (bbsType === "machi") {
              const res = URL.MACHI_RESNUM_REG.exec(raw.pathname);
              return res ? res[1] : null;
          }
          if (raw.hostname === "ula.5ch.net") {
              const res = URL.CH_RESNUM_REG2.exec(raw.pathname);
              return res ? res[1] : null;
          }
          // 2ch系
          {
              const res = URL.CH_RESNUM_REG.exec(raw.href);
              if (res) {
                  return res[1];
              }
          }
          return null;
      }
      toBoard() {
          const { type, bbsType } = this.guessedType;
          if (type !== "thread") {
              throw new Error("app.URL.URL.toBoard: toBoard()はThreadでのみ呼び出せます");
          }
          if (bbsType === "jbbs") {
              const pathname = this.pathname.replace(URL.SHITARABA_TO_BOARD_REG, "/$1/");
              return new URL(`${this.origin}${pathname}`);
          }
          {
              const pathname = this.pathname.replace(URL.CH_TO_BOARD_REG, "/$1/");
              return new URL(`${this.origin}${pathname}`);
          }
      }
      getHashParams() {
          return this.rawHash ? new URLSearchParams(this.rawHash.slice(1)) : new URLSearchParams();
      }
      setHashParams(data) {
          this.hash = (new URLSearchParams(data)).toString();
      }
      convertFromPhone() {
          let mode = this.getTsld();
          let reg;
          switch (this.hostname) {
              case "itest.5ch.net":
                  reg = URL.ITEST_5CH_REG;
                  break;
              case "c.5ch.net":
                  reg = URL.C_5CH_NET_REG;
                  break;
              case "sp.2ch.sc":
                  reg = URL.SP_2CH_SC_REG;
                  break;
              case "itest.bbspink.com":
                  reg = URL.ITEST_BBSPINK_REG;
                  break;
              default:
                  return;
          }
          const res = reg.exec(this.pathname);
          if (!res)
              return;
          const board = res[1];
          const thread = res[2] ? res[2] : null;
          if (!board)
              return;
          let server = null;
          if (mode === "5ch.net") {
              if (serverNet.has(board)) {
                  server = serverNet.get(board);
                  // 携帯用bbspinkの可能性をチェック
              }
              else if (serverPink.has(board)) {
                  server = serverPink.get(board);
                  mode = "bbspink.com";
              }
          }
          else if (mode === "2ch.sc" && serverSc.has(board)) {
              server = serverSc.get(board);
          }
          else if (mode === "bbspink.com" && serverPink.has(board)) {
              server = serverPink.get(board);
          }
          if (server === null)
              return;
          this.hostname = `${server}.${mode}`;
          this.pathname = `/${board}/` + (thread ? `/${thread}/` : "");
      }
      async exchangeNetSc() {
          const { type } = this.guessedType;
          const splits = this.pathname.split("/");
          const tsld = this.getTsld();
          let boardKey;
          if (type === "thread" && splits.length > 3) {
              boardKey = splits[3];
          }
          else if (type === "board" && splits.length > 1) {
              boardKey = splits[1];
          }
          else {
              return;
          }
          if (tsld === "5ch.net" && serverSc.has(boardKey)) {
              const server = serverSc.get(boardKey);
              this.hostname = `${server}.2ch.sc`;
              return;
          }
          else if (serverNet.has(boardKey)) {
              const server = serverNet.get(boardKey);
              this.hostname = `${server}.5ch.net`;
              return;
          }
          if (tsld !== "5ch.net")
              return;
          {
              const hostname = this.hostname.replace(".5ch.net", ".2ch.sc");
              const req = new Request("HEAD", `http://${hostname}${this.pathname}`);
              const { status, responseURL: resUrlStr } = await req.send();
              if (status >= 400) {
                  throw new Error("移動先情報の取得の通信に失敗しました");
              }
              const resUrl = new URL(resUrlStr);
              const server = resUrl.hostname.split(".")[0];
              const splits = resUrl.pathname.split("/");
              let boardKey;
              if (type === "thread" && splits.length > 3) {
                  boardKey = splits[3];
              }
              else if (type === "board" && splits.length > 1) {
                  boardKey = splits[1];
              }
              else {
                  this.href = resUrlStr;
                  return;
              }
              if (!serverSc.has(boardKey)) {
                  serverSc.set(boardKey, server);
              }
              this.hostname = resUrl.hostname;
          }
      }
      async createNetScConverted() {
          const newUrl = new URL(this.href);
          await newUrl.exchangeNetSc();
          return newUrl;
      }
  }
  URL.CH_THREAD_REG = /^\/((?:\w+\/)?test\/(?:read\.cgi|-)\/\w+\/\d+).*$/;
  //private static readonly CH_THREAD_REG2 = /^\/(\w+)\/?(?!test)$/;
  URL.CH_THREAD_ULA_REG = /^\/2ch\/(\w+)\/([\w\.]+)\/(\d+).*$/;
  URL.CH_BOARD_REG = /^\/((?:subback\/|test\/-\/)?\w+\/)(?:#.*)?$/;
  URL.MACHI_THREAD_REG = /^\/bbs\/read\.cgi\/(\w+\/\d+).*$/;
  URL.MACHI_BOARD_REG = /^\/(\w+\/)(?:#.*)?$/;
  URL.SHITARABA_THREAD_REG = /^\/bbs\/(read(?:_archive)?\.cgi\/\w+\/\d+\/\d+).*$/;
  URL.SHITARABA_ARCHIVE_REG = /^\/(\w+\/\d+)\/storage\/(\d+)\.html$/;
  URL.SHITARABA_BOARD_REG = /^\/(\w+\/\d+\/)(?:#.*)?$/;
  URL.CH_RESNUM_REG = /^https?:\/\/[\w\.]+\/(?:\w+\/)?test\/(?:read\.cgi|-)\/\w+\/\d+\/(?:i|g\?g=)?(\d+).*$/;
  URL.CH_RESNUM_REG2 = /^\/2ch\/\w+\/[\w\.]+\/\d+\/(\d+).*$/;
  URL.MACHI_RESNUM_REG = /^\/bbs\/read\.cgi\/\w+\/\d+\/(\d+).*$/;
  URL.SHITARABA_RESNUM_REG = /^\/bbs\/read(?:_archive)?\.cgi\/\w+\/\d+\/\d+\/(\d+).*$/;
  URL.CH_TO_BOARD_REG = /^\/(?:test|bbs)\/read\.cgi\/(\w+)\/\d+\/$/;
  URL.SHITARABA_TO_BOARD_REG = /^\/bbs\/read(?:_archive)?\.cgi\/(\w+\/\d+)\/\d+\/$/;
  URL.ITEST_5CH_REG = /\/(?:(?:\w+\/)?test\/read\.cgi\/(\w+)\/(\d+)\/|(?:subback\/)?(\w+)(?:\/)?)/;
  URL.C_5CH_NET_REG = /\/test\/-\/(\w+)\/(?:(\d+)\/)?/;
  URL.SP_2CH_SC_REG = /\/(?:(?:\w+\/)?test\/read\.cgi\/(\w+)\/(\d+)\/|(?:subback\/)?(\w+)\/)/;
  URL.ITEST_BBSPINK_REG = /\/(?:(?:\w+\/)?test\/read\.cgi\/(\w+)\/(\d+)\/|(?:subback\/)?(\w+)(?:\/)?)/;
  function parseQuery(urlStr, fromSearch = true) {
      if (fromSearch) {
          return new URLSearchParams(urlStr.slice(1));
      }
      return (new window.URL(urlStr)).searchParams;
  }

  var _FADE_IN_FRAMES, _FADE_OUT_FRAMES, _INVALIDED_EVENT, _TIMING, _animatingMap, _resetAnimatingMap;

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

  var Timer, Write;

  Timer = (function() {
    class Timer {
      constructor(onFinish) {
        this.onFinish = onFinish;
        return;
      }

      wake() {
        if (this._timeout != null) {
          this.kill();
        }
        this._timeout = setTimeout(() => {
          this.onFinish();
        }, this._MSEC);
      }

      kill() {
        clearTimeout(this._timeout);
        this._timeout = null;
      }

    }
    Timer.prototype._timeout = null;

    Timer.prototype._MSEC = 30 * 1000;

    return Timer;

  }).call(window);

  var Write$1 = Write = (function() {
    class Write {
      static setFont() {
        var font, fontface;
        if (navigator.platform.includes("Win")) {
          return;
        }
        font = localStorage.getItem("textar_font");
        if (font == null) {
          return;
        }
        fontface = new FontFace("Textar", `url(${font})`);
        document.fonts.add(fontface);
      }

      constructor() {
        var param, ref, ref1, ref2, ref3;
        this._onTimerFinish = this._onTimerFinish.bind(this);
        param = parseQuery(location.search);
        this.url = new URL(param.get("url"));
        this.title = (ref = param.get("title")) != null ? ref : param.get("url");
        this.name = (ref1 = param.get("name")) != null ? ref1 : app.config.get("default_name");
        this.mail = (ref2 = param.get("mail")) != null ? ref2 : app.config.get("default_mail");
        this.message = (ref3 = param.get("message")) != null ? ref3 : "";
        this.timer = new Timer(this._onTimerFinish);
        this._setHeaderModifier();
        this._setupTheme();
        this._setDOM();
        this._setBeforeUnload();
        this._setTitle();
        this._setupMessage();
        this._setupForm();
        return;
      }

      _beforeSendFunc() {
        var url;
        url = new URL(this.url.href);
        return function({method, requestHeaders}) {
          var i, isSameOrigin, j, len, name, origin, setReferer, setUserAgent, ua, uaExists;
          origin = browser.runtime.getURL("").slice(0, -1);
          isSameOrigin = requestHeaders.some(function({name, value}) {
            return name === "Origin" && (value === origin || value === "null");
          }) || !requestHeaders.includes("Origin");
          if (!(method === "POST" && isSameOrigin)) {
            return;
          }
          if (url.getTsld() === "2ch.sc") {
            url.protocol = "http:";
          }
          ua = app.config.get("useragent").trim();
          uaExists = ua.length > 0;
          setReferer = false;
          setUserAgent = !uaExists;
          for (i = j = 0, len = requestHeaders.length; j < len; i = ++j) {
            ({name} = requestHeaders[i]);
            if (!setReferer && name === "Referer") {
              requestHeaders[i].value = url.href;
              setReferer = true;
            } else if (!setUserAgent && name === "User-Agent") {
              requestHeaders[i].value = ua;
              setUserAgent = true;
            }
            if (setReferer && setUserAgent) {
              break;
            }
          }
          if (!setReferer) {
            requestHeaders.push({
              name: "Referer",
              value: url.href
            });
          }
          if (!setUserAgent && uaExists) {
            requestHeaders.push({
              name: "User-Agent",
              value: ua
            });
          }
          return {requestHeaders};
        };
      }

      _setHeaderModifier() {}

      _setupTheme() {
        // テーマ適用
        this._changeTheme(app.config.get("theme_id"));
        this._insertUserCSS();
        // テーマ更新反映
        app.message.on("config_updated", ({key, val}) => {
          if (key === "theme_id") {
            this._changeTheme(val);
          }
        });
      }

      _changeTheme(themeId) {
        // テーマ適用
        this.$view.removeClass("theme_default", "theme_dark", "theme_none");
        this.$view.addClass(`theme_${themeId}`);
      }

      _insertUserCSS() {
        var style;
        style = $__("style");
        style.id = "user_css";
        style.textContent = app.config.get("user_css");
        document.head.addLast(style);
      }

      _setDOM() {
        this._setSageDOM();
        this._setDefaultInput();
        this.$view.C("preview_button")[0].on("click", (e) => {
          var $button, $div, $pre, text;
          e.preventDefault();
          text = this.$view.T("textarea")[0].value;
          //行頭のスペースは削除される。複数のスペースは一つに纏められる。
          text = text.replace(/^\u0020*/g, "").replace(/\u0020+/g, " ");
          $div = $__("div").addClass("preview");
          $pre = $__("pre");
          $pre.textContent = text;
          $button = $__("button").addClass("close_preview");
          $button.textContent = "戻る";
          $button.on("click", function() {
            this.parent().remove();
          });
          $div.addLast($pre, $button);
          document.body.addLast($div);
        });
        this.$view.C("message")[0].on("keyup", ({target}) => {
          var line;
          line = target.value.split(/\n/).length;
          this.$view.C("notice")[0].textContent = `${target.value.length}文字 ${line}行`;
        });
      }

      _setSageDOM() {
        var $mail, $sage;
        $sage = this.$view.C("sage")[0];
        $mail = this.$view.C("mail")[0];
        if (app.config.isOn("sage_flag")) {
          $sage.checked = true;
          $mail.disabled = true;
        }
        this.$view.C("sage")[0].on("change", function() {
          if (this.checked) {
            app.config.set("sage_flag", "on");
            $mail.disabled = true;
          } else {
            app.config.set("sage_flag", "off");
            $mail.disabled = false;
          }
        });
      }

      _setDefaultInput() {
        this.$view.C("name")[0].value = this.name;
        this.$view.C("mail")[0].value = this.mail;
        this.$view.C("message")[0].value = this.message;
      }

      _setTitle() {
        var $h1;
        $h1 = this.$view.T("h1")[0];
        document.title = this.title;
        $h1.textContent = this.title;
        if (this.url.isHttps()) {
          $h1.addClass("https");
        }
      }

      _setBeforeUnload() {
        window.on("beforeunload", function() {
          browser.runtime.sendMessage({
            type: "write_position",
            x: screenX,
            y: screenY
          });
        });
      }

      _onTimerFinish() {
        this._onError("一定時間経過しても応答が無いため、処理を中断しました");
      }

      _onError(message) {
        var $notice, dom, ref;
        ref = this.$view.$$("form input, form textarea");
        for (dom of ref) {
          if (!(dom.hasClass("mail") && app.config.isOn("sage_flag"))) {
            dom.disabled = false;
          }
        }
        $notice = this.$view.C("notice")[0];
        if (message) {
          $notice.textContent = `書き込み失敗 - ${message}`;
        } else {
          $notice.textContent = "";
          fadeIn(this.$view.C("iframe_container")[0]);
        }
      }

      _onSuccess(key) {}

      _setupMessage() {
        window.on("message", async({
            data: {type, key, message},
            source
          }) => {
          var id;
          switch (type) {
            case "ping":
              source.postMessage(this._PONG_MSG, "*");
              this.timer.wake();
              break;
            case "success":
              this.$view.C("notice")[0].textContent = "書き込み成功";
              this.timer.kill();
              await app.wait(message);
              this._onSuccess(key);
              ({id} = (await browser.tabs.getCurrent()));
              browser.tabs.remove(id);
              break;
            case "confirm":
              fadeIn(this.$view.C("iframe_container")[0]);
              this.timer.kill();
              break;
            case "error":
              this._onError(message);
              this.timer.kill();
          }
        });
      }

      _getIframeArgs() {
        return {
          rcrxName: this.$view.C("name")[0].value,
          rcrxMail: this.$view.C("sage")[0].checked ? "sage" : this.$view.C("mail")[0].value,
          rcrxMessage: this.$view.C("message")[0].value
        };
      }

      _getFormData() {
        var args, bbsType, splittedUrl;
        ({bbsType} = this.url.guessType());
        splittedUrl = this.url.pathname.split("/");
        args = this._getIframeArgs();
        return {bbsType, splittedUrl, args};
      }

      _setupForm() {
        this.$view.C("hide_iframe")[0].on("click", () => {
          var $iframeC, dom, ref;
          this.timer.kill();
          $iframeC = this.$view.C("iframe_container")[0];
          (async function() {
            var ani;
            ani = (await fadeOut($iframeC));
            ani.on("finish", function() {
              $iframeC.T("iframe")[0].remove();
            });
          })();
          ref = this.$view.$$("input, textarea");
          for (dom of ref) {
            if (!(dom.hasClass("mail") && app.config.isOn("sage_flag"))) {
              dom.disabled = false;
            }
          }
          this.$view.C("notice")[0].textContent = "";
        });
        this.$view.T("form")[0].on("submit", (e) => {
          var $iframe, dom, ref;
          e.preventDefault();
          ref = this.$view.$$("input, textarea");
          for (dom of ref) {
            if (!(dom.hasClass("mail") && app.config.isOn("sage_flag"))) {
              dom.disabled = true;
            }
          }
          $iframe = $__("iframe");
          $iframe.src = "/view/empty.html";
          $iframe.on("load", () => {
            var form, formData, iframeDoc, input, key, ref1, ref2, textarea, val;
            formData = this._getFormData();
            iframeDoc = $iframe.contentDocument;
            //フォーム生成
            form = iframeDoc.createElement("form");
            form.acceptCharset = formData.charset;
            form.action = formData.action;
            form.method = "POST";
            ref1 = formData.input;
            for (key in ref1) {
              val = ref1[key];
              input = iframeDoc.createElement("input");
              input.name = key;
              input.value = val;
              form.appendChild(input);
            }
            ref2 = formData.textarea;
            for (key in ref2) {
              val = ref2[key];
              textarea = iframeDoc.createElement("textarea");
              textarea.name = key;
              textarea.textContent = val;
              form.appendChild(textarea);
            }
            iframeDoc.body.appendChild(form);
            Object.getPrototypeOf(form).submit.call(form);
          }, {
            once: true
          });
          $$.C("iframe_container")[0].addLast($iframe);
          this.timer.wake();
          this.$view.C("notice")[0].textContent = "書き込み中";
        });
      }

    }
    Write.prototype.url = null;

    Write.prototype.title = null;

    Write.prototype.name = null;

    Write.prototype.mail = null;

    Write.prototype.message = null;

    Write.prototype.$view = $$.C("view_write")[0];

    Write.prototype.timer = null;

    Write.prototype._PONG_MSG = "write_iframe_pong";

    return Write;

  }).call(window);

  var SubmitThread;

  Write$1.setFont();

  SubmitThread = (function() {
    class SubmitThread extends Write$1 {
      constructor() {
        super();
        return;
      }

      async _setHeaderModifier() {
        var extraInfoSpec, id;
        ({id} = (await browser.tabs.getCurrent()));
        extraInfoSpec = ["requestHeaders", "blocking"];
        if (browser.webRequest.OnBeforeSendHeadersOptions.hasOwnProperty("EXTRA_HEADERS")) {
          extraInfoSpec.push("extraHeaders");
        }
        browser.webRequest.onBeforeSendHeaders.addListener(this._beforeSendFunc(), {
          tabId: id,
          types: ["sub_frame"],
          urls: ["*://*.5ch.net/test/bbs.cgi*", "*://*.bbspink.com/test/bbs.cgi*", "*://*.2ch.sc/test/bbs.cgi*", "*://*.open2ch.net/test/bbs.cgi*", "*://jbbs.shitaraba.net/bbs/write.cgi/*"]
        }, extraInfoSpec);
      }

      _setTitle() {
        var $h1, title;
        title = this.title + "板";
        $h1 = this.$view.T("h1")[0];
        document.title = title;
        $h1.textContent = title;
        if (this.url.isHttps()) {
          $h1.addClass("https");
        }
      }

      _onSuccess(key) {
        var keys, mail, mes, name, ref, server, thread_url, title, url;
        mes = this.$view.C("message")[0].value;
        name = this.$view.C("name")[0].value;
        mail = this.$view.C("mail")[0].value;
        title = this.$view.C("title")[0].value;
        url = this.url;
        if ((ref = url.getTsld()) === "5ch.net" || ref === "2ch.sc" || ref === "bbspink.com" || ref === "open2ch.net") {
          keys = key.match(/.*\/test\/read\.cgi\/(\w+?)\/(\d+)\/l\d+/);
          if (keys == null) {
            $notice.textContent = "書き込み失敗 - 不明な転送場所";
          } else {
            server = url.origin;
            thread_url = `${server}/test/read.cgi/${keys[1]}/${keys[2]}/`;
            browser.runtime.sendMessage({
              type: "written",
              kind: "own",
              url: url.href,
              thread_url,
              mes,
              name,
              mail,
              title
            });
          }
        } else if (url.getTsld() === "shitaraba.net") {
          browser.runtime.sendMessage({
            type: "written",
            kind: "board",
            url: url.href,
            mes,
            name,
            mail,
            title
          });
        }
      }

      _getIframeArgs() {
        var args;
        args = super._getIframeArgs();
        args.rcrxTitle = this.$view.C("title")[0].value;
        return args;
      }

      _getFormData() {
        var args, bbsType, hostname, protocol, splittedUrl;
        ({protocol, hostname} = this.url);
        ({bbsType, splittedUrl, args} = super._getFormData());
        // 2ch
        if (bbsType === "2ch") {
          // open2ch
          if (this.url.getTsld() === "open2ch.net") {
            return {
              action: `${protocol}//${hostname}/test/bbs.cgi`,
              charset: "UTF-8",
              input: {
                submit: "新規スレッド作成",
                bbs: splittedUrl[1],
                subject: args.rcrxTitle,
                FROM: args.rcrxName,
                mail: args.rcrxMail
              },
              textarea: {
                MESSAGE: args.rcrxMessage
              }
            };
          } else {
            return {
              action: `${protocol}//${hostname}/test/bbs.cgi`,
              charset: "Shift_JIS",
              input: {
                submit: "新規スレッド作成",
                time: (Math.floor(Date.now() / 1000)) - 60,
                bbs: splittedUrl[1],
                subject: args.rcrxTitle,
                FROM: args.rcrxName,
                mail: args.rcrxMail
              },
              textarea: {
                MESSAGE: args.rcrxMessage
              }
            };
          }
        // したらば
        } else if (bbsType === "jbbs") {
          return {
            action: `${protocol}//jbbs.shitaraba.net/bbs/write.cgi/${splittedUrl[1]}/${splittedUrl[2]}/new/`,
            charset: "EUC-JP",
            input: {
              submit: "新規スレッド作成",
              TIME: (Math.floor(Date.now() / 1000)) - 60,
              DIR: splittedUrl[1],
              BBS: splittedUrl[2],
              SUBJECT: args.rcrxTitle,
              NAME: args.rcrxName,
              MAIL: args.rcrxMail
            },
            textarea: {
              MESSAGE: args.rcrxMessage
            }
          };
        }
      }

    }
    SubmitThread.prototype._PONG_MSG = "write_iframe_pong:thread";

    return SubmitThread;

  }).call(window);

  app.boot("/write/submit_thread.html", function() {
    new SubmitThread();
  });

}());
