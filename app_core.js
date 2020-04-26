(function (exports) {
  'use strict';

  /**
  @method _checkResNum
  @param {Object} ngObj
  @param {Number} resNum
  @private
  */
  /**
  @method _checkWord
  @param {Object} ngObj
  @param {Object} threadObj/resObj
  @private
  */
  /**
  @method parse
  @param {String} string
  @return {Object}
  */
  var _CONFIG_NAME, _CONFIG_STRING_NAME, _attachName, _checkResNum, _checkWord, _config, _expNgWords, _expireDate, _ignoreNgType, _ignoreResRegNumber, _ng, _setupReg, parse;

  /**
  @class NG
  @static
  */
  var TYPE = {
    INVALID: "invalid",
    REG_EXP: "RegExp",
    REG_EXP_TITLE: "RegExpTitle",
    REG_EXP_NAME: "RegExpName",
    REG_EXP_MAIL: "RegExpMail",
    REG_EXP_ID: "RegExpId",
    REG_EXP_SLIP: "RegExpSlip",
    REG_EXP_BODY: "RegExpBody",
    REG_EXP_URL: "RegExpUrl",
    TITLE: "Title",
    NAME: "Name",
    MAIL: "Mail",
    ID: "ID",
    SLIP: "Slip",
    BODY: "Body",
    WORD: "Word",
    URL: "Url",
    RES_COUNT: "ResCount",
    AUTO: "Auto",
    AUTO_CHAIN: "Chain",
    AUTO_CHAIN_ID: "ChainID",
    AUTO_CHAIN_SLIP: "ChainSLIP",
    AUTO_NOTHING_ID: "NothingID",
    AUTO_NOTHING_SLIP: "NothingSLIP",
    AUTO_REPEAT_MESSAGE: "RepeatMessage",
    AUTO_FORWARD_LINK: "ForwardLink"
  };

  _CONFIG_NAME = "ngobj";

  _CONFIG_STRING_NAME = "ngwords";

  _ng = null;

  _ignoreResRegNumber = /^ignoreResNumber:(\d+)(?:-?(\d+))?,(.*)$/;

  _ignoreNgType = /^ignoreNgType:(?:\$\((.*?)\):)?(.*)$/;

  _expireDate = /^expireDate:(\d{4}\/\d{1,2}\/\d{1,2}),(.*)$/;

  _attachName = /^attachName:([^,]*),(.*)$/;

  _expNgWords = /^\$\[(.*?)\]\$:(.*)$/;

  //jsonには正規表現のオブジェクトが含めれないので
  //それを展開
  _setupReg = function(obj) {
    var _convReg, convFlag, j, len, n, ref, subElement;
    _convReg = function({type, word}) {
      var reg;
      reg = null;
      try {
        reg = new RegExp(word);
      } catch (error) {
        app.message.send("notify", {
          message: `NG機能の正規表現(${type}: ${word})を読み込むのに失敗しました\nこの行は無効化されます`,
          background_color: "red"
        });
      }
      return reg;
    };
    for (n of obj) {
      convFlag = true;
      if (n.subElements != null) {
        ref = n.subElements;
        for (j = 0, len = ref.length; j < len; j++) {
          subElement = ref[j];
          if (!subElement.type.startsWith(TYPE.REG_EXP)) {
            continue;
          }
          subElement.reg = _convReg(subElement);
          if (!subElement.reg) {
            subElement.type = TYPE.INVALID;
            convFlag = false;
            break;
          }
        }
      }
      if (convFlag && n.type.startsWith(TYPE.REG_EXP)) {
        n.reg = _convReg(n);
        if (!n.reg) {
          convFlag = false;
        }
      }
      if (!convFlag) {
        n.type = TYPE.INVALID;
      }
    }
  };

  _config = {
    get: function() {
      return JSON.parse(app.config.get(_CONFIG_NAME));
    },
    set: function(str) {
      app.config.set(_CONFIG_NAME, JSON.stringify(str));
    },
    getString: function() {
      return app.config.get(_CONFIG_STRING_NAME);
    },
    setString: function(str) {
      app.config.set(_CONFIG_STRING_NAME, str);
    }
  };

  /**
  @method get
  @return {Object}
  */
  var get = function() {
    if (_ng == null) {
      _ng = new Set(_config.get());
      _setupReg(_ng);
    }
    return _ng;
  };

  parse = function(string) {
    var _getNgElement, ele, expire, i, j, k, len, m, ng, ngElement, ngStrSplit, ngWord, ref, st;
    ng = new Set();
    if (string === "") {
      return ng;
    }
    _getNgElement = function(ngWord) {
      var ele, i, j, m, ngElement, ref, subElement, tmp;
      if (ngWord.startsWith("Comment:") || ngWord === "") {
        return null;
      }
      ngElement = {
        type: "",
        word: "",
        subElements: []
      };
      switch (false) {
        // キーワードごとのNG処理
        case !ngWord.startsWith("RegExp:"):
          ngElement.type = TYPE.REG_EXP;
          ngElement.word = ngWord.substr(7);
          break;
        case !ngWord.startsWith("RegExpTitle:"):
          ngElement.type = TYPE.REG_EXP_TITLE;
          ngElement.word = ngWord.substr(12);
          break;
        case !ngWord.startsWith("RegExpName:"):
          ngElement.type = TYPE.REG_EXP_NAME;
          ngElement.word = ngWord.substr(11);
          break;
        case !ngWord.startsWith("RegExpMail:"):
          ngElement.type = TYPE.REG_EXP_MAIL;
          ngElement.word = ngWord.substr(11);
          break;
        case !ngWord.startsWith("RegExpID:"):
          ngElement.type = TYPE.REG_EXP_ID;
          ngElement.word = ngWord.substr(9);
          break;
        case !ngWord.startsWith("RegExpSlip:"):
          ngElement.type = TYPE.REG_EXP_SLIP;
          ngElement.word = ngWord.substr(11);
          break;
        case !ngWord.startsWith("RegExpBody:"):
          ngElement.type = TYPE.REG_EXP_BODY;
          ngElement.word = ngWord.substr(11);
          break;
        case !ngWord.startsWith("RegExpUrl:"):
          ngElement.type = TYPE.REG_EXP_URL;
          ngElement.word = ngWord.substr(10);
          break;
        case !ngWord.startsWith("Title:"):
          ngElement.type = TYPE.TITLE;
          ngElement.word = normalize(ngWord.substr(6));
          break;
        case !ngWord.startsWith("Name:"):
          ngElement.type = TYPE.NAME;
          ngElement.word = normalize(ngWord.substr(5));
          break;
        case !ngWord.startsWith("Mail:"):
          ngElement.type = TYPE.MAIL;
          ngElement.word = normalize(ngWord.substr(5));
          break;
        case !ngWord.startsWith("ID:"):
          ngElement.type = TYPE.ID;
          ngElement.word = ngWord;
          break;
        case !ngWord.startsWith("Slip:"):
          ngElement.type = TYPE.SLIP;
          ngElement.word = ngWord.substr(5);
          break;
        case !ngWord.startsWith("Body:"):
          ngElement.type = TYPE.BODY;
          ngElement.word = normalize(ngWord.substr(5));
          break;
        case !ngWord.startsWith("Url:"):
          ngElement.type = TYPE.URL;
          ngElement.word = ngWord.substr(4);
          break;
        case !ngWord.startsWith("ResCount:"):
          ngElement.type = TYPE.RES_COUNT;
          ngElement.word = parseInt(ngWord.substr(9));
          break;
        case !ngWord.startsWith("Auto:"):
          ngElement.type = TYPE.AUTO;
          ngElement.word = ngWord.substr(5);
          if (ngElement.word === "") {
            ngElement.word = "*";
          } else if (tmp = /\$\((.*)\):/.exec(ngElement.word)) {
            if (tmp[1] != null) {
              ngElement.subType = tmp[1].split(",");
            }
          }
          break;
        // AND条件用副要素の切り出し
        case !_expNgWords.test(ngWord):
          m = _expNgWords.exec(ngWord);
          for (i = j = 1; j <= 2; i = ++j) {
            ele = _getNgElement(m[i]);
            if (!ele) {
              continue;
            }
            if (ngElement.type !== "") {
              subElement = {
                type: ngElement.type,
                word: ngElement.word
              };
              ngElement.subElements.push(subElement);
            }
            ngElement.type = ele.type;
            ngElement.word = ele.word;
            if (((ref = ele.subElements) != null ? ref.length : void 0) > 0) {
              ngElement.subElements.push(...ele.subElements);
            }
          }
          break;
        default:
          ngElement.type = TYPE.WORD;
          ngElement.word = normalize(ngWord);
      }
      return ngElement;
    };
    ngStrSplit = string.split("\n");
    for (j = 0, len = ngStrSplit.length; j < len; j++) {
      ngWord = ngStrSplit[j];
      if (ngWord.startsWith("Comment:") || ngWord === "") {
        // 関係ないプレフィックスは飛ばす
        continue;
      }
      ngElement = {};
      // 指定したレス番号はNG除外する
      if ((m = ngWord.match(_ignoreResRegNumber)) != null) {
        ngElement = {
          start: m[1],
          finish: m[2]
        };
        ngWord = m[3];
      // 例外NgTypeの指定
      } else if ((m = ngWord.match(_ignoreNgType)) != null) {
        ngElement = {
          exception: true,
          subType: m[1] != null ? m[1].split(",") : void 0
        };
        ngWord = m[2];
      // 有効期限の指定
      } else if ((m = ngWord.match(_expireDate)) != null) {
        expire = stringToDate(`${m[1]} 23:59:59`);
        ngElement = {
          expire: expire.valueOf() + 1000
        };
        ngWord = m[2];
      // 名前の付与
      } else if ((m = ngWord.match(_attachName)) != null) {
        ngElement = {
          name: m[1]
        };
        ngWord = m[2];
      }
      // キーワードごとの取り出し
      ele = _getNgElement(ngWord);
      ngElement.type = ele.type;
      ngElement.word = ele.word;
      if (ele.subType != null) {
        ngElement.subType = ele.subType;
      }
      if (ele.subElements != null) {
        ngElement.subElements = ele.subElements;
      }
      // 拡張項目の設定
      if (ngElement.exception == null) {
        ngElement.exception = false;
      }
      if (ngElement.subType != null) {
        ref = ngElement.subType;
        for (i = k = ref.length - 1; k >= 0; i = k += -1) {
          st = ref[i];
          ngElement.subType[i] = st.trim();
          if (ngElement.subType[i] === "") {
            ngElement.subType.splice(i, 1);
          }
        }
        if (ngElement.subType.length === 0) {
          ngElement.subType = null;
        }
      }
      if (ngElement.word !== "") {
        ng.add(ngElement);
      }
    }
    return ng;
  };

  /**
  @method set
  @param {Object} obj
  */
  var set = function(string) {
    _ng = parse(string);
    _config.set([..._ng]);
    _setupReg(_ng);
  };

  /**
  @method add
  @param {String} string
  */
  var add = function(string) {
    var addNg, ang;
    _config.setString(string + "\n" + _config.getString());
    addNg = parse(string);
    _config.set([..._config.get()].concat([...addNg]));
    _setupReg(addNg);
    for (ang of addNg) {
      _ng.add(ang);
    }
  };

  _checkWord = function({type, reg, word}, {all, name, mail, id, slip, mes, title, url, resCount}) {
    if ((type === TYPE.REG_EXP && reg.test(all)) || (type === TYPE.REG_EXP_NAME && reg.test(name)) || (type === TYPE.REG_EXP_MAIL && reg.test(mail)) || (type === TYPE.REG_EXP_ID && (id != null) && reg.test(id)) || (type === TYPE.REG_EXP_SLIP && (slip != null) && reg.test(slip)) || (type === TYPE.REG_EXP_BODY && reg.test(mes)) || (type === TYPE.REG_EXP_TITLE && reg.test(title)) || (type === TYPE.REG_EXP_URL && reg.test(url)) || (type === TYPE.TITLE && normalize(title).includes(word)) || (type === TYPE.NAME && normalize(name).includes(word)) || (type === TYPE.MAIL && normalize(mail).includes(word)) || (type === TYPE.ID && (id != null ? id.includes(word) : void 0)) || (type === TYPE.SLIP && (slip != null ? slip.includes(word) : void 0)) || (type === TYPE.BODY && normalize(mes).includes(word)) || (type === TYPE.WORD && normalize(all).includes(word)) || (type === TYPE.URL && url.includes(word)) || (type === TYPE.RES_COUNT && word < resCount)) {
      return type;
    }
    return null;
  };

  _checkResNum = function({start, finish}, resNum) {
    return (start != null) && (((finish != null) && (start <= resNum && resNum <= finish)) || (parseInt(start) === resNum));
  };

  /**
  @method isNGBoard
  @param {String} threadTitle
  @param {String} url
  @param {Number} resCount
  @param {Boolean} exceptionFlg
  @param {String} subType
  @return {Object|null}
  */
  var isNGBoard = function(threadTitle, url, resCount, exceptionFlg = false, subType = null) {
    var n, ngType, now, ref, ref1, threadObj;
    threadObj = {
      all: normalize(threadTitle),
      title: threadTitle,
      url,
      resCount
    };
    now = Date.now();
    ref = get();
    for (n of ref) {
      if (n.type === TYPE.INVALID || n.type === "" || n.word === "") {
        continue;
      }
      if ((ref1 = n.type) !== TYPE.REG_EXP && ref1 !== TYPE.REG_EXP_TITLE && ref1 !== TYPE.TITLE && ref1 !== TYPE.WORD && ref1 !== TYPE.REG_EXP_URL && ref1 !== TYPE.URL && ref1 !== TYPE.RES_COUNT) {
        continue;
      }
      if ((n.expire != null) && now > n.expire) {
        // 有効期限のチェック
        continue;
      }
      if (n.exception !== exceptionFlg) {
        // ignoreNgType用例外フラグのチェック
        continue;
      }
      if ((n.subType != null) && subType && !n.subType.includes(subType)) {
        // ng-typeのチエック
        continue;
      }
      // サブ条件のチェック
      if (n.subElements != null) {
        if (!n.subElements.every(function(subElement) {
          return _checkWord(subElement, threadObj);
        })) {
          continue;
        }
      }
      // メイン条件のチェック
      ngType = _checkWord(n, threadObj);
      if (ngType) {
        return {
          type: ngType,
          name: n.name
        };
      }
    }
    return null;
  };

  /**
  @method isNGThread
  @param {Object} res
  @param {String} title
  @param {String} url
  @param {Number} resCount
  @param {Boolean} exceptionFlg
  @param {String} subType
  @return {Object|null}
  */
  var isNGThread = function(res, title, url, exceptionFlg = false, subType = null) {
    var all, mail, mes, n, name, ngType, now, other, ref, ref1, ref2, resObj;
    name = decodeCharReference(res.name);
    mail = decodeCharReference(res.mail);
    other = decodeCharReference(res.other);
    mes = decodeCharReference(res.message);
    all = name + " " + mail + " " + other + " " + mes;
    resObj = {
      all,
      name,
      mail,
      id: (ref = res.id) != null ? ref : null,
      slip: (ref1 = res.slip) != null ? ref1 : null,
      mes,
      title,
      url
    };
    now = Date.now();
    ref2 = get();
    for (n of ref2) {
      if (n.type === TYPE.INVALID || n.type === "" || n.word === "") {
        continue;
      }
      if (_checkResNum(n, res.num)) {
        // ignoreResNumber用レス番号のチェック
        continue;
      }
      if ((n.expire != null) && now > n.expire) {
        // 有効期限のチェック
        continue;
      }
      if (n.exception !== exceptionFlg) {
        // ignoreNgType用例外フラグのチェック
        continue;
      }
      if ((n.subType != null) && subType && !n.subType.includes(subType)) {
        // ng-typeのチエック
        continue;
      }
      // サブ条件のチェック
      if (n.subElements != null) {
        if (!n.subElements.every(function(subElement) {
          return _checkWord(subElement, resObj);
        })) {
          continue;
        }
      }
      // メイン条件のチェック
      ngType = _checkWord(n, resObj);
      if (ngType) {
        return {
          type: ngType,
          name: n.name
        };
      }
    }
    return null;
  };

  /**
  @method isIgnoreResNumForAuto
  @param {Number} resNum
  @param {String} subType
  @return {Boolean}
  */
  var isIgnoreResNumForAuto = function(resNum, subType = "") {
    var n, ref;
    ref = get();
    for (n of ref) {
      if (n.type !== TYPE.AUTO) {
        continue;
      }
      if ((n.subType != null) && !n.subType.includes(subType)) {
        continue;
      }
      if (_checkResNum(n, resNum)) {
        return true;
      }
    }
    return false;
  };

  /**
  @method isThreadIgnoreNgType
  @param {Object} res
  @param {String} threadTitle
  @param {String} url
  @param {String} ngType
  @return {Boolean}
  */
  var isThreadIgnoreNgType = function(res, threadTitle, url, ngType) {
    return isNGThread(res, threadTitle, url, true, ngType);
  };

  /**
  @method execExpire
  */
  var execExpire = function() {
    var configStr, expire, j, len, m, newConfigStr, ngStrSplit, ngWord, now, updateFlag;
    configStr = _config.getString();
    newConfigStr = "";
    updateFlag = false;
    ngStrSplit = configStr.split("\n");
    now = Date.now();
    for (j = 0, len = ngStrSplit.length; j < len; j++) {
      ngWord = ngStrSplit[j];
      // 有効期限の確認
      if (_expireDate.test(ngWord)) {
        m = ngWord.match(_expireDate);
        expire = stringToDate(m[1] + " 23:59:59");
        if (expire.valueOf() + 1000 < now) {
          updateFlag = true;
          continue;
        }
      }
      if (newConfigStr !== "") {
        newConfigStr += "\n";
      }
      newConfigStr += ngWord;
    }
    // 期限切れデータが存在した場合はNG情報を更新する
    if (updateFlag) {
      _config.setString(newConfigStr);
      _ng = parse(newConfigStr);
      _config.set([..._ng]);
      _setupReg(_ng);
    }
  };

  var NG = /*#__PURE__*/Object.freeze({
    TYPE: TYPE,
    get: get,
    set: set,
    add: add,
    isNGBoard: isNGBoard,
    isNGThread: isNGThread,
    isIgnoreResNumForAuto: isIgnoreResNumForAuto,
    isThreadIgnoreNgType: isThreadIgnoreNgType,
    execExpire: execExpire
  });

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

  var HTTP = /*#__PURE__*/Object.freeze({
    Request: Request,
    Response: Response
  });

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
  function fix(urlStr) {
      return (new URL(urlStr)).href;
  }
  function tsld(urlStr) {
      return (new URL(urlStr).getTsld());
  }
  function getDomain(urlStr) {
      return (new URL(urlStr)).hostname;
  }
  function getProtocol(urlStr) {
      return (new URL(urlStr)).protocol;
  }
  function isHttps(urlStr) {
      return (getProtocol(urlStr) === "https:");
  }
  function setProtocol(urlStr, protocol) {
      const url = new URL(urlStr);
      url.protocol = protocol;
      return url.href;
  }
  function getResNumber(urlStr) {
      return (new URL(urlStr)).getResNumber();
  }
  function threadToBoard(urlStr) {
      return (new URL(urlStr)).toBoard().href;
  }
  function parseQuery(urlStr, fromSearch = true) {
      if (fromSearch) {
          return new URLSearchParams(urlStr.slice(1));
      }
      return (new window.URL(urlStr)).searchParams;
  }
  function buildQuery(data) {
      return (new URLSearchParams(data)).toString();
  }
  const SHORT_URL_LIST = new Set([
      "amba.to",
      "amzn.to",
      "bit.ly",
      "buff.ly",
      "cas.st",
      "cos.lv",
      "dlvr.it",
      "ekaz10.xyz",
      "fb.me",
      "g.co",
      "goo.gl",
      "htn.to",
      "ift.tt",
      "is.gd",
      "itun.es",
      "j.mp",
      "jump.cx",
      "kkbox.fm",
      "morimo2.info",
      "ow.ly",
      "p.tl",
      "prt.nu",
      "redd.it",
      "snipurl.com",
      "spoti.fi",
      "t.co",
      "tiny.cc",
      "tinyurl.com",
      "tl.gd",
      "tr.im",
      "trib.al",
      "qq4q.biz",
      "u0u1.net",
      "ur0.biz",
      "ur0.work",
      "url.ie",
      "urx.nu",
      "urx.red",
      "urx2.nu",
      "urx3.nu",
      "ur0.pw",
      "ur2.link",
      "ustre.am",
      "ux.nu",
      "wb2.biz",
      "wk.tk",
      "xrl.us",
      "y2u.be"
  ]);
  async function expandShortURL(shortUrl) {
      let finalUrl = "";
      const cache = new Cache$1(shortUrl);
      const res = await (async () => {
          try {
              await cache.get();
              return { data: cache.data, url: null };
          }
          catch (_a) {
              const req = new Request("HEAD", shortUrl, {
                  timeout: parseInt(app.config.get("expand_short_url_timeout"))
              });
              let { status, responseURL: resUrl } = await req.send();
              if (shortUrl === resUrl && status >= 400) {
                  return { data: null, url: null };
              }
              // 無限ループの防止
              if (resUrl === shortUrl) {
                  return { data: null, url: null };
              }
              // 取得したURLが短縮URLだった場合は再帰呼出しする
              if (SHORT_URL_LIST.has(getDomain(resUrl))) {
                  resUrl = await expandShortURL(resUrl);
                  return { data: null, url: resUrl };
              }
              return { data: null, url: resUrl };
          }
      })();
      if (res.data === null && res.url !== null) {
          cache.lastUpdated = Date.now();
          cache.data = res.url;
          cache.put();
          finalUrl = res.url;
      }
      else if (res.data !== null && res.url === null) {
          finalUrl = res.data;
      }
      return finalUrl;
  }
  const AUDIO_REG = /\.(?:mp3|m4a|wav|oga|spx)(?:[\?#:&].*)?$/;
  const VIDEO_REG = /\.(?:mp4|m4v|webm|ogv)(?:[\?#:&].*)?$/;
  const OGG_REG = /\.(?:ogg|ogx)(?:[\?#:&].*)?$/;
  function getExtType(filename, { audio = true, video = true, oggIsAudio = false, oggIsVideo = true } = {}) {
      if (audio && AUDIO_REG.test(filename)) {
          return "audio";
      }
      if (video && VIDEO_REG.test(filename)) {
          return "video";
      }
      if (video && oggIsVideo && OGG_REG.test(filename)) {
          return "video";
      }
      if (audio && oggIsAudio && OGG_REG.test(filename)) {
          return "audio";
      }
      return null;
  }
  function applyServerInfo(menu) {
      const boardNet = new Map();
      const boardSc = new Map();
      const boardPink = new Map();
      const res = {
          net: (serverNet.size > 0),
          sc: (serverSc.size > 0),
          bbspink: (serverPink.size > 0)
      };
      if (res.net && res.sc && res.bbspink)
          return res;
      for (const category of menu) {
          for (const board of category.board) {
              let tmp;
              if (!res.net && (tmp = /https?:\/\/(\w+)\.5ch\.net\/(\w+)\/.*?/.exec(board.url)) !== null) {
                  boardNet.set(tmp[2], tmp[1]);
              }
              else if (!res.sc && (tmp = /https?:\/\/(\w+)\.2ch\.sc\/(\w+)\/.*?/.exec(board.url)) !== null) {
                  boardSc.set(tmp[2], tmp[1]);
              }
              else if (!res.bbspink && (tmp = /https?:\/\/(\w+)\.bbspink\.com\/(\w+)\/.*?/.exec(board.url)) !== null) {
                  boardPink.set(tmp[2], tmp[1]);
              }
          }
      }
      if (boardNet.size > 0)
          serverNet = boardNet;
      if (boardSc.size > 0)
          serverSc = boardSc;
      if (boardPink.size > 0)
          serverPink = boardPink;
      return {
          net: (serverNet.size > 0),
          sc: (serverSc.size > 0),
          bbspink: (serverPink.size > 0)
      };
  }
  async function pushServerInfo(menu) {
      const res = applyServerInfo(menu);
      if (res.net && res.sc && res.bbspink) {
          return;
      }
      if (!res.net || !res.bbspink) {
          const tmpUrl = `https://menu.5ch.net/bbsmenu.html`;
          const tmpMenu = (await fetch(tmpUrl, false)).menu;
          applyServerInfo(tmpMenu);
      }
      if (!res.sc) {
          const tmpUrl = `https://menu.2ch.sc/bbsmenu.html`;
          const tmpMenu = (await fetch(tmpUrl, false)).menu;
          applyServerInfo(tmpMenu);
      }
  }

  var URL$1 = /*#__PURE__*/Object.freeze({
    URL: URL,
    fix: fix,
    tsld: tsld,
    getDomain: getDomain,
    getProtocol: getProtocol,
    isHttps: isHttps,
    setProtocol: setProtocol,
    getResNumber: getResNumber,
    threadToBoard: threadToBoard,
    parseQuery: parseQuery,
    buildQuery: buildQuery,
    SHORT_URL_LIST: SHORT_URL_LIST,
    expandShortURL: expandShortURL,
    getExtType: getExtType,
    pushServerInfo: pushServerInfo
  });

  var Board;

  /**
  @class Board
  @constructor
  @param {String} url
  */
  var Board$1 = Board = class Board {
    constructor(url) {
      /**
      @property url
      @type String
      */
      this.url = new URL(url);
      /**
      @property thread
      @type Array | null
      */
      this.thread = null;
      /**
      @property message
      @type String | null
      */
      this.message = null;
      return;
    }

    /**
    @method get
    @return {Promise}
    */
    get() {
      var tmp, xhrCharset, xhrPath;
      tmp = Board._getXhrInfo(this.url);
      if (!tmp) {
        return Promise.reject();
      }
      ({
        path: xhrPath,
        charset: xhrCharset
      } = tmp);
      return new Promise(async(resolve, reject) => {
        var bookmark, cache, dict, etag, hasCache, i, j, k, lastModified, len, len1, len2, needFetch, newBoardUrl, ref, request, response, thread, threadList, threadUrl, val;
        hasCache = false;
        // キャッシュ取得
        cache = new Cache$1(xhrPath);
        needFetch = false;
        try {
          await cache.get();
          hasCache = true;
          if (!(Date.now() - cache.lastUpdated < 1000 * 3)) {
            throw new Error("キャッシュの期限が切れているため通信します");
          }
        } catch (error) {
          needFetch = true;
        }
        try {
          if (needFetch) {
            // 通信
            request = new Request("GET", xhrPath, {
              mimeType: `text/plain; charset=${xhrCharset}`,
              preventCache: true
            });
            if (hasCache) {
              if (cache.lastModified != null) {
                request.headers["If-Modified-Since"] = new Date(cache.lastModified).toUTCString();
              }
              if (cache.etag != null) {
                request.headers["If-None-Match"] = cache.etag;
              }
            }
            response = (await request.send());
          }
          // パース
          // 2chで自動移動しているときはサーバー移転
          if ((response != null) && this.url.getTsld() === "5ch.net" && this.url.hostname !== response.responseURL.split("/")[2]) {
            newBoardUrl = response.responseURL.slice(0, -"subject.txt".length);
            throw {response, newBoardUrl};
          }
          if ((response != null ? response.status : void 0) === 200) {
            threadList = Board.parse(this.url, response.body);
          } else if (hasCache) {
            threadList = Board.parse(this.url, cache.data);
          }
          if (threadList == null) {
            throw {response};
          }
          if (!((response != null ? response.status : void 0) === 200 || (response != null ? response.status : void 0) === 304 || ((response == null) && hasCache))) {
            throw {response, threadList};
          }
          //コールバック
          this.thread = threadList;
          resolve();
          //キャッシュ更新部
          if ((response != null ? response.status : void 0) === 200) {
            cache.data = response.body;
            cache.lastUpdated = Date.now();
            lastModified = new Date(response.headers["Last-Modified"] || "dummy").getTime();
            if (Number.isFinite(lastModified)) {
              cache.lastModified = lastModified;
            }
            if (etag = response.headers["ETag"]) {
              cache.etag = etag;
            }
            cache.put();
            for (i = 0, len = threadList.length; i < len; i++) {
              thread = threadList[i];
              app.bookmark.updateResCount(thread.url, thread.resCount);
            }
          } else if (hasCache && (response != null ? response.status : void 0) === 304) {
            cache.lastUpdated = Date.now();
            cache.put();
          }
        } catch (error) {
          ({response, threadList, newBoardUrl} = error);
          //コールバック
          this.message = "板の読み込みに失敗しました。";
          if ((newBoardUrl != null) && this.url.getTsld() === "5ch.net") {
            try {
              newBoardUrl = ((await chServerMoveDetect(this.url))).href;
              this.message += `サーバーが移転しています\n(<a href="${app.escapeHtml(app.safeHref(newBoardUrl))}"\nclass="open_in_rcrx">${app.escapeHtml(newBoardUrl)}\n</a>)`;
            } catch (error) {}
          //2chでrejectされている場合は移転を疑う
          } else if (this.url.getTsld() === "5ch.net" && (response != null)) {
            try {
              newBoardUrl = ((await chServerMoveDetect(this.url))).href;
              //移転検出時
              this.message += `サーバーが移転している可能性が有ります\n(<a href="${app.escapeHtml(app.safeHref(newBoardUrl))}"\nclass="open_in_rcrx">${app.escapeHtml(newBoardUrl)}\n</a>)`;
            } catch (error) {}
            if (hasCache && (threadList != null)) {
              this.message += "キャッシュに残っていたデータを表示します。";
            }
            if (threadList) {
              this.thread = threadList;
            }
          } else {
            if (hasCache && (threadList != null)) {
              this.message += "キャッシュに残っていたデータを表示します。";
            }
            if (threadList != null) {
              this.thread = threadList;
            }
          }
          reject();
        }
        // dat落ちスキャン
        if (!threadList) {
          return;
        }
        dict = {};
        ref = app.bookmark.getByBoard(this.url.href);
        for (j = 0, len1 = ref.length; j < len1; j++) {
          bookmark = ref[j];
          if (bookmark.type === "thread") {
            dict[bookmark.url] = true;
          }
        }
        for (k = 0, len2 = threadList.length; k < len2; k++) {
          thread = threadList[k];
          if (!(dict[thread.url] != null)) {
            continue;
          }
          dict[thread.url] = false;
          app.bookmark.updateExpired(thread.url, false);
        }
        for (threadUrl in dict) {
          val = dict[threadUrl];
          if (val) {
            app.bookmark.updateExpired(threadUrl, true);
          }
        }
      });
    }

    /**
    @method get
    @static
    @param {String} url
    @return {Promise}
    */
    static async get(url) {
      var board, ref, ref1;
      board = new Board(url);
      try {
        await board.get();
        return {
          status: "success",
          data: board.thread
        };
      } catch (error) {
        return {
          status: "error",
          message: (ref = board.message) != null ? ref : null,
          data: (ref1 = board.thread) != null ? ref1 : null
        };
      }
    }

    /**
    @method _getXhrInfo
    @private
    @static
    @param {app.URL.URL} boardUrl
    @return {Object | null} xhrInfo
    */
    static _getXhrInfo(boardUrl) {
      var tmp;
      tmp = /^\/(\w+)(?:\/(\d+)\/|\/?)$/.exec(boardUrl.pathname);
      if (!tmp) {
        return null;
      }
      switch (boardUrl.getTsld()) {
        case "machi.to":
          return {
            path: `${boardUrl.origin}/bbs/offlaw.cgi/${tmp[1]}/`,
            charset: "Shift_JIS"
          };
        case "shitaraba.net":
          return {
            path: `${boardUrl.protocol}//jbbs.shitaraba.net/${tmp[1]}/${tmp[2]}/subject.txt`,
            charset: "EUC-JP"
          };
        default:
          return {
            path: `${boardUrl.origin}/${tmp[1]}/subject.txt`,
            charset: "Shift_JIS"
          };
      }
    }

    /**
    @method parse
    @static
    @param {app.URL.URL} url
    @param {String} text
    @return {Array | null} board
    */
    static parse(url, text) {
      var baseUrl, bbsType, board, reg, regRes, resCount, scFlg, title, tmp;
      tmp = /^\/(\w+)(?:\/(\w+)|\/?)/.exec(url.pathname);
      scFlg = false;
      switch (url.getTsld()) {
        case "machi.to":
          bbsType = "machi";
          reg = /^\d+<>(\d+)<>(.+)\((\d+)\)$/gm;
          baseUrl = `${url.origin}/bbs/read.cgi/${tmp[1]}/`;
          break;
        case "shitaraba.net":
          bbsType = "jbbs";
          reg = /^(\d+)\.cgi,(.+)\((\d+)\)$/gm;
          baseUrl = `${url.protocol}//jbbs.shitaraba.net/bbs/read.cgi/${tmp[1]}/${tmp[2]}/`;
          break;
        default:
          scFlg = url.getTsld() === "2ch.sc";
          bbsType = "2ch";
          reg = /^(\d+)\.dat<>(.+) \((\d+)\)$/gm;
          baseUrl = `${url.origin}/test/read.cgi/${tmp[1]}/`;
      }
      board = [];
      while ((regRes = reg.exec(text))) {
        title = decodeCharReference(regRes[2]);
        title = removeNeedlessFromTitle(title);
        resCount = +regRes[3];
        board.push({
          url: baseUrl + regRes[1] + "/",
          title,
          resCount,
          createdAt: +regRes[1] * 1000,
          ng: isNGBoard(title, url.href, resCount),
          isNet: scFlg ? !title.startsWith("★") : null
        });
      }
      if (bbsType === "jbbs") {
        board.pop();
      }
      if (board.length > 0) {
        return board;
      }
      return null;
    }

    /**
    @method getCachedResCount
    @static
    @param {String} threadUrl
    @return {Promise}
    */
    static async getCachedResCount(threadUrl) {
      var boardUrl, cache, data, i, lastModified, len, ref, ref1, resCount, url, xhrPath;
      boardUrl = threadUrl.toBoard();
      xhrPath = (ref = Board._getXhrInfo(boardUrl)) != null ? ref.path : void 0;
      if (xhrPath == null) {
        throw new Error("その板の取得方法の情報が存在しません");
      }
      cache = new Cache$1(xhrPath);
      try {
        await cache.get();
        ({lastModified, data} = cache);
        ref1 = Board.parse(boardUrl, data);
        for (i = 0, len = ref1.length; i < len; i++) {
          ({url, resCount} = ref1[i]);
          if (url === threadUrl.href) {
            return {
              resCount,
              modified: lastModified
            };
          }
        }
      } catch (error) {}
      throw new Error("板のスレ一覧にそのスレが存在しません");
    }

  };

  function levenshteinDistance(a, b, allowReplace = true) {
      const repCost = allowReplace ? 1 : 2;
      const table = [];
      table[0] = new Uint16Array(b.length + 1);
      for (let bc = 0; bc <= b.length; bc++) {
          table[0][bc] = bc;
      }
      for (let ac = 1; ac <= a.length; ac++) {
          table[ac] = new Uint16Array(b.length + 1);
          table[ac][0] = ac;
      }
      for (let ac = 1; ac <= a.length; ac++) {
          for (let bc = 1; bc <= b.length; bc++) {
              table[ac][bc] = Math.min(table[ac - 1][bc] + 1, table[ac][bc - 1] + 1, table[ac - 1][bc - 1] + (a[ac - 1] === b[bc - 1] ? 0 : repCost));
          }
      }
      return table[a.length][b.length];
  }

  var Util = /*#__PURE__*/Object.freeze({
    levenshteinDistance: levenshteinDistance
  });

  var $span, boardUrlReg, kataHiraReg, openMap, titleReg, wideSlimNormalizeReg;

  /**
  @class Anchor
  スレッドフロートBBSで用いられる「アンカー」形式の文字列を扱う。
  */
  var Anchor = {
    reg: {
      ANCHOR: /(?:&gt;|＞){1,2}[\d\uff10-\uff19]+(?:[\-\u30fc][\d\uff10-\uff19]+)?(?:\s*[,、]\s*[\d\uff10-\uff19]+(?:[\-\u30fc][\d\uff10-\uff19]+)?)*/g,
      _FW_NUMBER: /[\uff10-\uff19]/g
    },
    parseAnchor: function(str) {
      var data, ref, segReg, segment, segrangeEnd, segrangeStart;
      data = {
        targetCount: 0,
        segments: []
      };
      str = app.replaceAll(str, "\u30fc", "-");
      str = str.replace(Anchor.reg._FW_NUMBER, function($0) {
        return String.fromCharCode($0.charCodeAt(0) - 65248);
      });
      if (!/^(?:&gt;|＞){0,2}([\d]+(?:-\d+)?(?:\s*[,、]\s*\d+(?:-\d+)?)*)$/.test(str)) {
        return data;
      }
      segReg = /(\d+)(?:-(\d+))?/g;
      while (segment = segReg.exec(str)) {
        if (segment[1].length > 5 || ((ref = segment[2]) != null ? ref.length : void 0) > 5) {
          // 桁数の大きすぎる値は無視
          continue;
        }
        if (+segment[1] < 1) {
          // 1以下の値は無視
          continue;
        }
        if (segment[2]) {
          if (+segment[1] <= +segment[2]) {
            segrangeStart = +segment[1];
            segrangeEnd = +segment[2];
          } else {
            segrangeStart = +segment[2];
            segrangeEnd = +segment[1];
          }
        } else {
          segrangeStart = segrangeEnd = +segment[1];
        }
        data.targetCount += segrangeEnd - segrangeStart + 1;
        data.segments.push([segrangeStart, segrangeEnd]);
      }
      return data;
    }
  };

  boardUrlReg = /^https?:\/\/\w+\.5ch\.net\/(\w+)\/$/;

  //2chの鯖移転検出関数
  //移転を検出した場合は移転先のURLをresolveに載せる
  //検出出来なかった場合はrejectする
  //htmlを渡す事で通信をスキップする事が出来る
  var chServerMoveDetect = async function(oldBoardUrl, html) {
    var newBoardUrl, newBoardUrlTmp, res, responseURL, status;
    oldBoardUrl.protocol = "http:";
    if (typeof html !== "string") {
      ({
        //htmlが渡されなかった場合は通信する
        status,
        body: html
      } = (await (new Request("GET", oldBoardUrl.href, {
        mimeType: "text/html; charset=Shift_JIS",
        cache: false
      })).send()));
      if (status !== 200) {
        throw new Error("サーバー移転判定のための通信に失敗しました");
      }
    }
    //htmlから移転を判定
    res = /location\.href="(https?:\/\/(\w+\.)?5ch\.net\/\w*\/)"/.exec(html);
    if (res) {
      if (res[2] != null) {
        newBoardUrlTmp = new URL(res[1]);
      } else {
        ({responseURL} = (await (new Request("GET", res[1])).send()));
        newBoardUrlTmp = new URL(responseURL);
      }
      newBoardUrlTmp.protocol = "http";
      if (newBoardUrlTmp.hostname !== oldBoardUrl.hostname) {
        newBoardUrl = newBoardUrlTmp;
      }
    }
    //bbsmenuから検索
    if (newBoardUrl == null) {
      newBoardUrl = (await (async function() {
        var board, boardKey, category, data, i, j, len, len1, m, newUrl, ref, ref1;
        ({
          menu: data
        } = (await get$1()));
        if (data == null) {
          throw new Error("BBSMenuの取得に失敗しました");
        }
        boardKey = (ref = oldBoardUrl.pathname.split("/")) != null ? ref[1] : void 0;
        if (!boardKey) {
          throw new Error("板のURL形式が不明です");
        }
        for (i = 0, len = data.length; i < len; i++) {
          category = data[i];
          ref1 = category.board;
          for (j = 0, len1 = ref1.length; j < len1; j++) {
            board = ref1[j];
            m = board.url.match(boardUrlReg);
            if (m != null) {
              newUrl = new URL(m[0]);
              newUrl.protocol = "http:";
              if (boardKey === m[1] && oldBoardUrl.hostname !== newUrl.hostname) {
                return newUrl;
              }
            }
          }
        }
        throw new Error("BBSMenuにその板のサーバー情報が存在しません");
      })());
    }
    //移転を検出した場合は移転検出メッセージを送出
    app.message.send("detected_ch_server_move", {
      before: oldBoardUrl.href,
      after: newBoardUrl.href
    });
    return newBoardUrl;
  };

  //文字参照をデコード
  $span = $__("span");

  var decodeCharReference = function(str) {
    return str.replace(/\&(?:#(\d+)|#x([\dA-Fa-f]+)|([\da-zA-Z]+));/g, function($0, $1, $2, $3) {
      //数値文字参照 - 10進数
      if ($1 != null) {
        return String.fromCodePoint($1);
      }
      //数値文字参照 - 16進数
      if ($2 != null) {
        return String.fromCodePoint(parseInt($2, 16));
      }
      //文字実体参照
      if ($3 != null) {
        $span.innerHTML = $0;
        return $span.textContent;
      }
      return $0;
    });
  };

  //マウスクリックのイベントオブジェクトから、リンク先をどう開くべきかの情報を導く
  openMap = new Map([
    [
      //button(number), shift(bool), ctrl(bool)の文字列
      "0falsefalse",
      {
        newTab: false,
        newWindow: false,
        background: false
      }
    ],
    [
      "0truefalse",
      {
        newTab: false,
        newWindow: true,
        background: false
      }
    ],
    [
      "0falsetrue",
      {
        newTab: true,
        newWindow: false,
        background: true
      }
    ],
    [
      "0truetrue",
      {
        newTab: true,
        newWindow: false,
        background: false
      }
    ],
    [
      "1falsefalse",
      {
        newTab: true,
        newWindow: false,
        background: true
      }
    ],
    [
      "1truefalse",
      {
        newTab: true,
        newWindow: false,
        background: false
      }
    ],
    [
      "1falsetrue",
      {
        newTab: true,
        newWindow: false,
        background: true
      }
    ],
    [
      "1truetrue",
      {
        newTab: true,
        newWindow: false,
        background: false
      }
    ]
  ]);

  var getHowToOpen = function({type, button, shiftKey, ctrlKey, metaKey}) {
    var def, key;
    ctrlKey || (ctrlKey = metaKey);
    def = {
      newTab: false,
      newWindow: false,
      background: false
    };
    if (type === "mousedown") {
      key = "" + button + shiftKey + ctrlKey;
      if (openMap.has(key)) {
        return openMap.get(key);
      }
    }
    return def;
  };

  var searchNextThread = async function(threadUrlStr, threadTitle, resString) {
    var boardUrl, threadUrl, threads;
    threadUrl = new URL(threadUrlStr);
    boardUrl = threadUrl.toBoard();
    threadTitle = normalize(threadTitle);
    ({
      data: threads
    } = (await Board$1.get(boardUrl)));
    if (threads == null) {
      throw new Error("板の取得に失敗しました");
    }
    threads = threads.filter(function({url, resCount}) {
      return url !== threadUrl.href && resCount < 1001;
    }).map(function({title, url}) {
      var m, ref, ref1, score;
      score = levenshteinDistance(threadTitle, normalize(title), false);
      m = url.match(/(?:https:\/\/)?(?:\w+(\.[25]ch\.net\/.+)|(.+))$/);
      if (resString.includes((ref = (ref1 = m[1]) != null ? ref1 : m[2]) != null ? ref : url)) {
        score -= 3;
      }
      return {score, title, url};
    }).sort(function(a, b) {
      return a.score - b.score;
    });
    return threads.slice(0, 5);
  };

  // 全角記号/英数(０-９,Ａ-Ｚ,ａ-ｚ,その他記号)
  // 半角カタカナ(ｦ-ｯ, ｱ-ﾝ, ｰ)
  wideSlimNormalizeReg = /[\uff01-\uff5d\uff66-\uff9d]+/g; //＼→\も含む
  //\uff70はｰ(半角カタカナ長音符)

  kataHiraReg = /[\u30a1-\u30f3]/g; //ァ-ン

  // 検索用に全角/半角や大文字/小文字を揃える
  var normalize = function(str) {
    // 全角記号/英数を半角記号/英数に、半角カタカナを全角カタカナに変換
    str = str.replace(wideSlimNormalizeReg, function(s) {
      return s.normalize("NFKC");
    // カタカナをひらがなに変換
    }).replace(kataHiraReg, function($0) {
      return String.fromCharCode($0.charCodeAt(0) - 96);
    });
    // 全角スペース/半角スペースを削除
    str = app.replaceAll(app.replaceAll(str, "\u0020", ""), "\u3000", "");
    // 大文字を小文字に変換
    return str.toLowerCase();
  };

  // striptags
  var stripTags = function(str) {
    return str.replace(/<[^>]+>/ig, "");
  };

  titleReg = / ?(?:\[(?:無断)?転載禁止\]|(?:\(c\)|©|�|&copy;|&#169;)(?:2ch\.net|@?bbspink\.com)) ?/g;

  // タイトルから無断転載禁止などを取り除く
  var removeNeedlessFromTitle = function(title) {
    var title2;
    title2 = title.replace(titleReg, "");
    title = title2 === "" ? title : title2;
    return app.replaceAll(app.replaceAll(title, "<mark>", ""), "</mark>", "");
  };

  var promiseWithState = function(promise) {
    var state;
    state = "pending";
    promise.then(function() {
      state = "resolved";
    }, function() {
      state = "rejected";
    });
    return {
      isResolved: function() {
        return state === "resolved";
      },
      isRejected: function() {
        return state === "rejected";
      },
      getState: function() {
        return state;
      },
      promise
    };
  };

  var indexedDBRequestToPromise = function(req) {
    return new Promise(function(resolve, reject) {
      req.onsuccess = resolve;
      req.onerror = reject;
    });
  };

  var stampToDate = function(stamp) {
    return new Date(stamp * 1000);
  };

  var stringToDate = function(string) {
    var date, flg, ref, ref1, ref2, ref3, ref4;
    date = string.match(/(\d{4})\/(\d{1,2})\/(\d{1,2})(?:\(.\))?\s?(\d{1,2}):(\d\d)(?::(\d\d)(?:\.\d+)?)?/);
    flg = false;
    if (date != null) {
      if (date[1] != null) {
        flg = true;
      }
      if (!((date[2] != null) && (1 <= (ref = +date[2]) && ref <= 12))) {
        flg = false;
      }
      if (!((date[3] != null) && (1 <= (ref1 = +date[3]) && ref1 <= 31))) {
        flg = false;
      }
      if (!((date[4] != null) && (0 <= (ref2 = +date[4]) && ref2 <= 23))) {
        flg = false;
      }
      if (!((date[5] != null) && (0 <= (ref3 = +date[5]) && ref3 <= 59))) {
        flg = false;
      }
      if (!((date[6] != null) && (0 <= (ref4 = +date[6]) && ref4 <= 59))) {
        date[6] = 0;
      }
    }
    if (flg) {
      return new Date(date[1], date[2] - 1, date[3], date[4], date[5], date[6]);
    }
    return null;
  };

  var isNewerReadState = function(a, b) {
    if (!b) {
      return false;
    }
    if (!a) {
      return true;
    }
    if (a.received !== b.received) {
      return a.received < b.received;
    }
    if (a.read !== b.read) {
      return a.read < b.read;
    }
    if (a.date && b.date) {
      return a.date < b.date;
    } else if (a.date) {
      return false;
    } else if (b.date) {
      return true;
    }
    if (a.last !== b.last) {
      return true;
    }
    if (a.offset !== b.offset) {
      return true;
    }
    return false;
  };

  var util = /*#__PURE__*/Object.freeze({
    Anchor: Anchor,
    chServerMoveDetect: chServerMoveDetect,
    decodeCharReference: decodeCharReference,
    getHowToOpen: getHowToOpen,
    searchNextThread: searchNextThread,
    normalize: normalize,
    stripTags: stripTags,
    removeNeedlessFromTitle: removeNeedlessFromTitle,
    promiseWithState: promiseWithState,
    indexedDBRequestToPromise: indexedDBRequestToPromise,
    stampToDate: stampToDate,
    stringToDate: stringToDate,
    isNewerReadState: isNewerReadState
  });

  /**
  @class Cache
  @constructor
  @param {String} key
  */
  var Cache;

  var Cache$1 = Cache = (function() {
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

  /**
  @method parse
  @param {String} html
  @return {Array}
  */
  var _update, bbsmenuOption, parse$1;

  bbsmenuOption = null;

  var target = $__("div");

  /**
  @method fetchAll
  @param {Boolean} [forceReload=false]
  */
  var fetchAll = async function(forceReload = false) {
    var bbsmenu, bbsmenuUrl, i, j, len, len1, menu, opt, tmpOpt, url;
    bbsmenu = [];
    if (!bbsmenuOption || forceReload) {
      if (!bbsmenuOption) {
        bbsmenuOption = new Set();
      } else {
        bbsmenuOption.clear();
      }
      tmpOpt = app.config.get("bbsmenu_option").split("\n");
      for (i = 0, len = tmpOpt.length; i < len; i++) {
        opt = tmpOpt[i];
        if (opt === "" || opt.startsWith("//")) {
          continue;
        }
        bbsmenuOption.add(opt);
      }
    }
    bbsmenuUrl = app.config.get("bbsmenu").split("\n");
    for (j = 0, len1 = bbsmenuUrl.length; j < len1; j++) {
      url = bbsmenuUrl[j];
      if (url === "" || url.startsWith("//")) {
        continue;
      }
      try {
        ({menu} = (await fetch(url, forceReload)));
        bbsmenu.push(...menu);
      } catch (error) {
        app.message.send("notify", {
          message: `板一覧の取得に失敗しました。(${url})`,
          background_color: "red"
        });
      }
    }
    return {
      menu: bbsmenu
    };
  };

  /**
  @method fetch
  @param {String} url
  @param {Boolean} [force=false]
  */
  var fetch = async function(url, force) {
    var cache, lastModified, menu, request, response;
    //キャッシュ取得
    cache = new Cache$1(url);
    try {
      await cache.get();
      if (force) {
        throw new Error("最新のものを取得するために通信します");
      }
      if (Date.now() - cache.lastUpdated > +app.config.get("bbsmenu_update_interval") * 1000 * 60 * 60 * 24) {
        throw new Error("キャッシュが期限切れなので通信します");
      }
    } catch (error) {
      //通信
      request = new Request("GET", url, {
        mimeType: "text/plain; charset=Shift_JIS"
      });
      if (cache.lastModified != null) {
        request.headers["If-Modified-Since"] = new Date(cache.lastModified).toUTCString();
      }
      if (cache.etag != null) {
        request.headers["If-None-Match"] = cache.etag;
      }
      response = (await request.send());
    }
    if ((response != null ? response.status : void 0) === 200) {
      menu = parse$1(response.body);
      //キャッシュ更新
      cache.data = response.body;
      cache.lastUpdated = Date.now();
      lastModified = new Date(response.headers["Last-Modified"] || "dummy").getTime();
      if (Number.isFinite(lastModified)) {
        cache.lastModified = lastModified;
      }
      cache.put();
    } else if (cache.data != null) {
      menu = parse$1(cache.data);
      //キャッシュ更新
      if ((response != null ? response.status : void 0) === 304) {
        cache.lastUpdated = Date.now();
        cache.put();
      }
    }
    if (!((menu != null ? menu.length : void 0) > 0)) {
      throw {response};
    }
    if (!((response != null ? response.status : void 0) === 200 || (response != null ? response.status : void 0) === 304 || (!response && (cache.data != null)))) {
      throw {response, menu};
    }
    return {response, menu};
  };

  /**
  @method get
  @param {Function} Callback
  @param {Boolean} [ForceReload=false]
  */
  var get$1 = async function(forceReload = false) {
    var _updatingPromise, obj;
    if (typeof _updatingPromise === "undefined" || _updatingPromise === null) {
      _updatingPromise = _update(forceReload);
    }
    try {
      obj = (await _updatingPromise);
      obj.status = "success";
      if (forceReload) {
        target.emit(new CustomEvent("change", {
          detail: obj
        }));
      }
    } catch (error) {
      obj = error;
      obj.status = "error";
      if (forceReload) {
        target.emit(new CustomEvent("change", {
          detail: obj
        }));
      }
    }
    return obj;
  };

  parse$1 = function(html) {
    var bbspinkException, category, menu, regBoard, regBoardRes, regCategory, regCategoryRes, subName;
    regCategory = /<b>(.+?)<\/b>(?:.*[\r\n]+<a\s.*?>.+?<\/a>)+/gi;
    regBoard = /<a\shref=(https?:\/\/(?!info\.[25]ch\.net\/|headline\.bbspink\.com)(?:\w+\.(?:[25]ch\.net|open2ch\.net|2ch\.sc|bbspink\.com)|(?:\w+\.)?machi\.to)\/\w+\/)(?:\s.*?)?>(.+?)<\/a>/gi;
    menu = [];
    bbspinkException = bbsmenuOption.has("bbspink.com");
    while (regCategoryRes = regCategory.exec(html)) {
      category = {
        title: regCategoryRes[1],
        board: []
      };
      subName = null;
      while (regBoardRes = regBoard.exec(regCategoryRes[0])) {
        if (bbsmenuOption.has(tsld(regBoardRes[1]))) {
          continue;
        }
        if (bbspinkException && regBoardRes[1].includes("5ch.net/bbypink")) {
          continue;
        }
        if (!subName) {
          if (regBoardRes[1].includes("open2ch.net")) {
            subName = "op";
          } else if (regBoardRes[1].includes("2ch.sc")) {
            subName = "sc";
          } else {
            subName = "";
          }
          if (subName !== "" && !(category.title.endsWith(`(${subName})`) || category.title.endsWith(`_${subName}`))) {
            category.title += `(${subName})`;
          }
        }
        if (subName !== "" && !(regBoardRes[2].endsWith(`(${subName})`) || regBoardRes[2].endsWith(`_${subName}`))) {
          regBoardRes[2] += `_${subName}`;
        }
        category.board.push({
          url: fix(regBoardRes[1]),
          title: regBoardRes[2]
        });
      }
      if (category.board.length > 0) {
        menu.push(category);
      }
    }
    return menu;
  };

  _update = async function(forceReload) {
    var menu;
    ({menu} = (await fetchAll(forceReload)));
    return {menu};
  };

  var BBSMenu = /*#__PURE__*/Object.freeze({
    target: target,
    fetchAll: fetchAll,
    fetch: fetch,
    get: get$1
  });

  /**
  @class BoardTitleSolver
  @static
  */
  /**
  @property _bbsmenu
  @private
  @type Map | null
  */
  /**
  @property _bbsmenuPromise
  @private
  @type Promise | null
  */
  /**
  @method _formatBoardTitle
  @param {String} title
  @param {app.URL.URL} url
  @private
  @return {String}
  */
  /**
  @method _generateBBSMenu
  @return {Promise}
  @private
  */
  /**
  @method _getBBSMenu
  @return {Promise}
  @private
  */
  /**
  @method _setBBSMenu
  @return {Promise}
  @private
  */
  /**
  @method searchFromBBSMenu
  @param {app.URL.URL} url
  @return {Promise}
  */
  /**
  @method searchFromBookmark
  @param {app.URL.URL} url
  @return {Promise}
  */
  /**
  @method searchFromJbbsAPI
  @param {String} url
  @return {Promise}
  */
  /**
  @method searchFromSettingTXT
  @param {app.URL.URL} url
  @return {Promise}
  */
  var _bbsmenu, _bbsmenuPromise, _formatBoardTitle, _generateBBSMenu, _getBBSMenu, _setBBSMenu, searchFromBBSMenu, searchFromBookmark, searchFromJbbsAPI, searchFromSettingTXT;

  _bbsmenu = null;

  _bbsmenuPromise = null;

  _generateBBSMenu = function({status, menu, message}) {
    var bbsmenu, board, i, j, len, len1, title, url;
    if (status === "error") {
      (async function() {
        await app.defer();
        app.message.send("notify", {
          message: message,
          background_color: "red"
        });
      })();
    }
    if (menu == null) {
      throw new Error("板一覧が取得できませんでした");
    }
    bbsmenu = new Map();
    for (i = 0, len = menu.length; i < len; i++) {
      ({board} = menu[i]);
      for (j = 0, len1 = board.length; j < len1; j++) {
        ({url, title} = board[j]);
        bbsmenu.set(url, title);
      }
    }
    _bbsmenu = bbsmenu;
  };

  _setBBSMenu = async function() {
    var obj;
    obj = (await get$1());
    _generateBBSMenu(obj);
    target.on("change", ({
        detail: obj
      }) => {
      _generateBBSMenu(obj);
    });
  };

  _getBBSMenu = async function() {
    if (_bbsmenu != null) {
      return _bbsmenu;
    }
    if (_bbsmenuPromise != null) {
      await _bbsmenuPromise;
    } else {
      _bbsmenuPromise = _setBBSMenu();
      await _bbsmenuPromise;
      _bbsmenuPromise = null;
    }
    return _bbsmenu;
  };

  searchFromBBSMenu = async function(url) {
    var bbsmenu, boardName, ref, ref1, url2;
    bbsmenu = (await _getBBSMenu());
    // スキーム違いについても確認をする
    url2 = url.createProtocolToggled();
    boardName = (ref = (ref1 = bbsmenu.get(url.href)) != null ? ref1 : bbsmenu.get(url2.href)) != null ? ref : null;
    return boardName;
  };

  _formatBoardTitle = function(title, url) {
    switch (url.getTsld()) {
      case "5ch.net":
        title = title.replace("＠2ch掲示板", "");
        break;
      case "2ch.sc":
        title += "_sc";
        break;
      case "open2ch.net":
        title += "_op";
    }
    return title;
  };

  searchFromBookmark = function(url) {
    var bookmark, ref, url2;
    // スキーム違いについても確認をする
    url2 = url.createProtocolToggled();
    bookmark = (ref = app.bookmark.get(url.href)) != null ? ref : app.bookmark.get(url2.href);
    if (bookmark) {
      return _formatBoardTitle(bookmark.title, new URL(bookmark.url));
    }
    return null;
  };

  searchFromSettingTXT = async function(url) {
    var body, res, status;
    ({status, body} = (await new Request("GET", `${url.href}SETTING.TXT`, {
      mimeType: "text/plain; charset=Shift_JIS",
      timeout: 1000 * 10
    }).send()));
    if (status !== 200) {
      throw new Error("SETTING.TXTを取得する通信に失敗しました");
    }
    if (res = /^BBS_TITLE_ORIG=(.+)$/m.exec(body)) {
      return _formatBoardTitle(res[1], url);
    }
    if (res = /^BBS_TITLE=(.+)$/m.exec(body)) {
      return _formatBoardTitle(res[1], url);
    }
    throw new Error("SETTING.TXTに名前の情報がありません");
  };

  searchFromJbbsAPI = async function(url) {
    var ajaxPath, body, res, status, tmp;
    tmp = url.pathname.split("/");
    ajaxPath = `${url.protocol}//jbbs.shitaraba.net/bbs/api/setting.cgi/${tmp[1]}/${tmp[2]}/`;
    ({status, body} = (await new Request("GET", ajaxPath, {
      mimeType: "text/plain; charset=EUC-JP",
      timeout: 1000 * 10
    }).send()));
    if (status !== 200) {
      throw new Error("したらばの板のAPIの通信に失敗しました");
    }
    if (res = /^BBS_TITLE=(.+)$/m.exec(body)) {
      return res[1];
    }
    throw new Error("したらばの板のAPIに名前の情報がありません");
  };

  /**
  @method ask
  @param {app.URL.URL} url
  @return Promise
  */
  var ask = async function(url) {
    var e, name;
    // bbsmenu内を検索
    name = (await searchFromBBSMenu(url));
    if (name != null) {
      return name;
    }
    // ブックマーク内を検索
    name = (await searchFromBookmark(url));
    if (name != null) {
      return name;
    }
    try {
      // SETTING.TXTからの取得を試みる
      if (url.guessType().bbsType === "2ch") {
        return (await searchFromSettingTXT(url));
      }
      // したらばのAPIから取得を試みる
      if (url.guessType().bbsType === "jbbs") {
        return (await searchFromJbbsAPI(url));
      }
    } catch (error) {
      e = error;
      throw new Error(`板名の取得に失敗しました: ${e}`);
    }
  };

  var BoardTitleSolver = /*#__PURE__*/Object.freeze({
    ask: ask
  });

  function newerEntry(a, b) {
      if (a.resCount !== null && b.resCount !== null && a.resCount !== b.resCount) {
          return a.resCount > b.resCount ? a : b;
      }
      return app.util.isNewerReadState(a.readState, b.readState) ? b : a;
  }
  class EntryList {
      constructor() {
          this.cache = new Map();
          this.boardURLIndex = new Map();
      }
      async add(entry) {
          if (this.get(entry.url))
              return false;
          entry = app.deepCopy(entry);
          this.cache.set(entry.url, entry);
          if (entry.type === "thread") {
              const boardURL = threadToBoard(entry.url);
              if (!this.boardURLIndex.has(boardURL)) {
                  this.boardURLIndex.set(boardURL, new Set());
              }
              this.boardURLIndex.get(boardURL).add(entry.url);
          }
          return true;
      }
      async update(entry) {
          if (!this.get(entry.url))
              return false;
          this.cache.set(entry.url, app.deepCopy(entry));
          return true;
      }
      async remove(urlStr) {
          const url = new URL(urlStr);
          urlStr = url.href;
          if (!this.cache.has(urlStr))
              return false;
          if (this.cache.get(urlStr).type === "thread") {
              const boardURL = url.toBoard().href;
              if (this.boardURLIndex.has(boardURL)) {
                  const threadList = this.boardURLIndex.get(boardURL);
                  if (threadList.has(urlStr)) {
                      threadList.delete(urlStr);
                  }
              }
          }
          this.cache.delete(urlStr);
          return true;
      }
      import(target) {
          for (const b of target.getAll()) {
              const a = this.get(b.url);
              if (a) {
                  if (a.type === "thread" && b.type === "thread") {
                      if (newerEntry(a, b) === b) {
                          this.update(b);
                      }
                  }
              }
              else {
                  this.add(b);
              }
          }
      }
      serverMove(from, to) {
          // 板ブックマーク移行
          const boardEntry = this.get(from);
          if (boardEntry) {
              this.remove(boardEntry.url);
              boardEntry.url = to;
              this.add(boardEntry);
          }
          const tmp = (new URL(to)).origin;
          const reg = /^https?:\/\/[\w\.]+\//;
          // スレブックマーク移行
          for (const entry of this.getThreadsByBoardURL(from)) {
              this.remove(entry.url);
              entry.url = entry.url.replace(reg, tmp);
              if (entry.readState) {
                  entry.readState.url = entry.url;
              }
              this.add(entry);
          }
      }
      get(url) {
          url = fix(url);
          return this.cache.has(url) ? app.deepCopy(this.cache.get(url)) : null;
      }
      getAll() {
          return Array.from(this.cache.values());
      }
      getAllThreads() {
          return this.getAll().filter(({ type }) => type === "thread");
      }
      getAllBoards() {
          return this.getAll().filter(({ type }) => type === "board");
      }
      getThreadsByBoardURL(url) {
          const res = [];
          url = fix(url);
          if (this.boardURLIndex.has(url)) {
              for (const threadURL of this.boardURLIndex.get(url)) {
                  res.push(this.get(threadURL));
              }
          }
          return res;
      }
  }
  class SyncableEntryList extends EntryList {
      constructor() {
          super();
          this.onChanged = new app.Callbacks({ persistent: true });
          this.observerForSync = (e) => {
              this.manipulateByBookmarkUpdateEvent(e);
          };
      }
      async add(entry) {
          if (!super.add(entry))
              return false;
          this.onChanged.call({
              type: "ADD",
              entry: app.deepCopy(entry)
          });
          return true;
      }
      async update(entry) {
          const before = this.get(entry.url);
          if (!super.update(entry))
              return false;
          if (before.title !== entry.title) {
              this.onChanged.call({
                  type: "TITLE",
                  entry: app.deepCopy(entry)
              });
          }
          if (before.resCount !== entry.resCount) {
              this.onChanged.call({
                  type: "RES_COUNT",
                  entry: app.deepCopy(entry)
              });
          }
          if ((!before.readState && entry.readState) ||
              ((before.readState && entry.readState) && (before.readState.received !== entry.readState.received ||
                  before.readState.read !== entry.readState.read ||
                  before.readState.last !== entry.readState.last ||
                  before.readState.offset !== entry.readState.offset ||
                  before.readState.date !== entry.readState.date))) {
              this.onChanged.call({
                  type: "READ_STATE",
                  entry: app.deepCopy(entry)
              });
          }
          if (before.expired !== entry.expired) {
              this.onChanged.call({
                  type: "EXPIRED",
                  entry: app.deepCopy(entry)
              });
          }
          return true;
      }
      async remove(url) {
          const entry = this.get(url);
          if (!super.remove(url))
              return false;
          this.onChanged.call({
              type: "REMOVE",
              entry: entry
          });
          return true;
      }
      manipulateByBookmarkUpdateEvent({ type, entry }) {
          switch (type) {
              case "ADD":
                  this.add(entry);
                  break;
              case "TITLE":
              case "RES_COUNT":
              case "READ_STATE":
              case "EXPIRED":
                  this.update(entry);
                  break;
              case "REMOVE":
                  this.remove(entry.url);
                  break;
          }
      }
      followDeletion(b) {
          const aEntries = this.getAll();
          const bList = new Set(b.getAll().map(({ url }) => url));
          for (const { url } of aEntries) {
              if (!bList.has(url)) {
                  this.remove(url);
              }
          }
      }
      syncStart(b) {
          b.import(this);
          this.syncResume(b);
      }
      syncResume(b) {
          this.import(b);
          this.followDeletion(b);
          this.onChanged.add(b.observerForSync);
          b.onChanged.add(this.observerForSync);
      }
      syncStop(b) {
          this.onChanged.remove(b.observerForSync);
          b.onChanged.remove(this.observerForSync);
      }
  }

  var BookmarkEntryList = /*#__PURE__*/Object.freeze({
    newerEntry: newerEntry,
    EntryList: EntryList,
    SyncableEntryList: SyncableEntryList
  });

  class BrowserBookmarkEntryList extends SyncableEntryList {
      constructor(rootNodeId) {
          super();
          this.nodeIdStore = new Map();
          this.ready = new app.Callbacks();
          this.needReconfigureRootNodeId = new app.Callbacks({ persistent: true });
          this.setRootNodeId(rootNodeId);
          this.setUpBrowserBookmarkWatcher();
      }
      static entryToURL(entry) {
          const url = new URL(entry.url);
          const param = {};
          if (entry.resCount !== null && Number.isFinite(entry.resCount)) {
              param.res_count = "" + entry.resCount;
          }
          if (entry.readState) {
              param.last = "" + entry.readState.last;
              param.read = "" + entry.readState.read;
              param.received = "" + entry.readState.received;
              if (entry.readState.offset) {
                  param.offset = "" + entry.readState.offset;
              }
              if (entry.readState.date) {
                  param.date = "" + entry.readState.date;
              }
          }
          if (entry.expired) {
              param.expired = "true";
          }
          url.setHashParams(param);
          return url.href;
      }
      static URLToEntry(urlStr) {
          const url = new URL(urlStr);
          urlStr = url.href;
          const { type, bbsType } = url.guessType();
          if (type === "unknown")
              return null;
          const arg = url.getHashParams();
          const entry = {
              type,
              bbsType,
              url: urlStr,
              title: urlStr,
              resCount: null,
              readState: null,
              expired: false
          };
          const reg = /^\d+$/;
          if (reg.test(arg.get("res_count"))) {
              entry.resCount = +arg.get("res_count");
          }
          if (reg.test(arg.get("received")) &&
              reg.test(arg.get("read")) &&
              reg.test(arg.get("last"))) {
              entry.readState = {
                  url: urlStr,
                  received: +arg.get("received"),
                  read: +arg.get("read"),
                  last: +arg.get("last"),
                  offset: arg.get("offset") ? +arg.get("offset") : null,
                  date: arg.get("date") ? +arg.get("date") : null
              };
          }
          if (arg.get("expired") === "true") {
              entry.expired = true;
          }
          return entry;
      }
      applyNodeAddToEntryList(node) {
          if (!node.url || !node.title)
              return;
          const entry = BrowserBookmarkEntryList.URLToEntry(node.url);
          if (entry === null)
              return;
          entry.title = node.title;
          // 既に同一URLのEntryが存在する場合、
          if (this.get(entry.url)) {
              // addによりcreateBrowserBookmarkが呼ばれた場合
              if (!this.nodeIdStore.has(entry.url)) {
                  this.nodeIdStore.set(entry.url, node.id);
              }
              else if (newerEntry(entry, this.get(entry.url)) === entry) {
                  // node側の方が新しいと判定された場合のみupdateを行う。
                  // 重複ブックマークの削除(元のnodeが古いと判定されたため)
                  browser.bookmarks.remove(this.nodeIdStore.get(entry.url));
                  this.nodeIdStore.set(entry.url, node.id);
                  this.update(entry, false);
              }
              else {
                  // 重複ブックマークの削除(node側の方が古いと判定された場合)
                  browser.bookmarks.remove(node.id);
              }
          }
          else {
              this.nodeIdStore.set(entry.url, node.id);
              this.add(entry, false);
          }
      }
      applyNodeUpdateToEntryList(nodeId, changes) {
          const url = this.getURLFromNodeId(nodeId);
          if (!url)
              return;
          const entry = this.get(url);
          if (typeof changes.url === "string") {
              const newEntry = BrowserBookmarkEntryList.URLToEntry(changes.url);
              newEntry.title = (typeof changes.title === "string" ? changes.title : entry.title);
              if (entry.url === newEntry.url) {
                  if ((BrowserBookmarkEntryList.entryToURL(entry) !==
                      BrowserBookmarkEntryList.entryToURL(newEntry)) ||
                      (entry.title !== newEntry.title)) {
                      this.update(newEntry, false);
                  }
              }
              else {
                  // ノードのURLが他の板/スレを示す物に変更された時
                  this.nodeIdStore.delete(url);
                  this.nodeIdStore.set(newEntry.url, nodeId);
                  this.remove(entry.url, false);
                  this.add(newEntry, false);
              }
          }
          else if (typeof changes.title === "string") {
              if (entry.title !== changes.title) {
                  entry.title = changes.title;
                  this.update(entry, false);
              }
          }
      }
      applyNodeRemoveToEntryList(nodeId) {
          const url = this.getURLFromNodeId(nodeId);
          if (url !== null) {
              this.nodeIdStore.delete(url);
              this.remove(url, false);
          }
      }
      getURLFromNodeId(nodeId) {
          for (const [url, id] of this.nodeIdStore) {
              if (id === nodeId) {
                  return url;
              }
          }
          return null;
      }
      setUpBrowserBookmarkWatcher() {
          let watching = true;
          // Firefoxではbookmarks.onImportBegan/Endedは実装されていない
          if (browser.bookmarks.onImportBegan !== void 0) {
              browser.bookmarks.onImportBegan.addListener(() => {
                  watching = false;
              });
              browser.bookmarks.onImportEnded.addListener(() => {
                  watching = true;
                  this.loadFromBrowserBookmark();
              });
          }
          browser.bookmarks.onCreated.addListener((nodeId, node) => {
              if (!watching)
                  return;
              if (node.parentId === this.rootNodeId && typeof node.url === "string") {
                  this.applyNodeAddToEntryList(node);
              }
          });
          browser.bookmarks.onRemoved.addListener((nodeId) => {
              if (!watching)
                  return;
              this.applyNodeRemoveToEntryList(nodeId);
          });
          browser.bookmarks.onChanged.addListener((nodeId, changes) => {
              if (!watching)
                  return;
              this.applyNodeUpdateToEntryList(nodeId, changes);
          });
          browser.bookmarks.onMoved.addListener(async (nodeId, { parentId, oldParentId }) => {
              if (!watching)
                  return;
              if (parentId === this.rootNodeId) {
                  const res = await browser.bookmarks.get(nodeId);
                  if (res.length === 1 && typeof res[0].url === "string") {
                      this.applyNodeAddToEntryList(res[0]);
                  }
              }
              else if (oldParentId === this.rootNodeId) {
                  this.applyNodeRemoveToEntryList(nodeId);
              }
          });
      }
      setRootNodeId(rootNodeId) {
          this.rootNodeId = rootNodeId;
          return this.loadFromBrowserBookmark();
      }
      async validateRootNodeSettings() {
          try {
              await browser.bookmarks.getChildren(this.rootNodeId);
          }
          catch (_a) {
              this.needReconfigureRootNodeId.call();
          }
      }
      async loadFromBrowserBookmark() {
          // EntryListクリア
          for (const entry of this.getAll()) {
              this.remove(entry.url, false);
          }
          // ロード
          try {
              const res = await browser.bookmarks.getChildren(this.rootNodeId);
              for (const node of res) {
                  this.applyNodeAddToEntryList(node);
              }
              if (!this.ready.wasCalled) {
                  this.ready.call();
              }
              return true;
          }
          catch (_a) {
              app.log("warn", "ブラウザのブックマークからの読み込みに失敗しました。");
              this.validateRootNodeSettings();
              return false;
          }
      }
      async createBrowserBookmark(entry) {
          const res = await browser.bookmarks.create({
              parentId: this.rootNodeId,
              url: BrowserBookmarkEntryList.entryToURL(entry),
              title: entry.title
          });
          if (!res) {
              app.log("error", "ブラウザのブックマークへの追加に失敗しました");
              this.validateRootNodeSettings();
          }
          return !!res;
      }
      async updateBrowserBookmark(newEntry) {
          if (!this.nodeIdStore.has(newEntry.url))
              return false;
          const id = this.nodeIdStore.get(newEntry.url);
          const res = await browser.bookmarks.get(id);
          const changes = {};
          const node = res[0];
          const newURL = BrowserBookmarkEntryList.entryToURL(newEntry);
          // const currentEntry = BrowserBookmarkEntryList.URLToEntry(node.url); //used in future
          if (node.title !== newEntry.title) {
              changes.title = newEntry.title;
          }
          if (node.url !== newURL) {
              changes.url = newURL;
          }
          if (Object.keys(changes).length === 0)
              return true;
          const res2 = await browser.bookmarks.update(id, changes);
          if (res2)
              return true;
          app.log("error", "ブラウザのブックマーク更新に失敗しました");
          this.validateRootNodeSettings();
          return false;
      }
      async removeBrowserBookmark(url) {
          if (this.nodeIdStore.has(url)) {
              this.nodeIdStore.delete(url);
          }
          const res = await browser.bookmarks.getChildren(this.rootNodeId);
          const removeIdList = [];
          if (res) {
              for (const node of res) {
                  if (node.url && node.title) {
                      const entry = BrowserBookmarkEntryList.URLToEntry(node.url);
                      if (entry && entry.url === url) {
                          removeIdList.push(node.id);
                      }
                  }
              }
          }
          if (removeIdList.length === 0)
              return false;
          await Promise.all(removeIdList.map((id) => {
              return browser.bookmarks.remove(id).catch(e => { return; });
          }));
          return true;
      }
      async add(entry, createBrowserBookmark = true) {
          entry = app.deepCopy(entry);
          if (!super.add(entry))
              return false;
          if (createBrowserBookmark) {
              return this.createBrowserBookmark(entry);
          }
          return true;
      }
      async update(entry, updateBrowserBookmark = true) {
          entry = app.deepCopy(entry);
          if (!super.update(entry))
              return false;
          if (updateBrowserBookmark) {
              return this.updateBrowserBookmark(entry);
          }
          return true;
      }
      async remove(url, removeBrowserBookmark = true) {
          if (!super.remove(url))
              return false;
          if (removeBrowserBookmark) {
              return this.removeBrowserBookmark(url);
          }
          return true;
      }
  }

  /**
  @class ReadState
  @static
  */
  var DB_VERSION, _openDB, _recoveryOfDate, _urlFilter;

  DB_VERSION = 2;

  _openDB = new Promise(function(resolve, reject) {
    var req;
    req = indexedDB.open("ReadState", DB_VERSION);
    req.onerror = function(e) {
      app.criticalError("既読情報管理システムの起動に失敗しました");
      reject(e);
    };
    req.onupgradeneeded = function({
        target: {
          result: db,
          transaction: tx
        },
        oldVersion: oldVer
      }) {
      var objStore;
      if (oldVer < 1) {
        objStore = db.createObjectStore("ReadState", {
          keyPath: "url"
        });
        objStore.createIndex("board_url", "board_url", {
          unique: false
        });
        tx.oncomplete = function() {
          resolve(db);
        };
      }
      if (oldVer === 1) {
        _recoveryOfDate(db, tx);
        tx.oncomplete = function() {
          resolve(db);
        };
      }
    };
    req.onsuccess = function({
        target: {
          result: db
        }
      }) {
      resolve(db);
    };
  });

  _urlFilter = function(originalUrlStr) {
    var original, replaced;
    original = new URL(originalUrlStr);
    replaced = new URL(originalUrlStr);
    if (original.hostname.endsWith(".5ch.net")) {
      replaced.hostname = "*.5ch.net";
    }
    return {original, replaced};
  };

  var set$1 = async function(readState) {
    var boardUrl, db, e, req, url;
    if ((readState == null) || typeof readState !== "object") {
      app.log("error", "app.ReadState.set: 引数が不正です", arguments);
      throw new Error("既読情報に登録しようとしたデータが不正です");
    }
    if (app.assertArg("app.ReadState.set", [[readState.url, "string"], [readState.last, "number"], [readState.read, "number"], [readState.received, "number"], [readState.offset, "number", true], [readState.date, "number", true]])) {
      throw new Error("既読情報に登録しようとしたデータが不正です");
    }
    readState = app.deepCopy(readState);
    url = _urlFilter(readState.url);
    readState.url = url.replaced.href;
    boardUrl = url.original.toBoard();
    readState.board_url = _urlFilter(boardUrl.href).replaced.href;
    try {
      db = (await _openDB);
      req = db.transaction("ReadState", "readwrite").objectStore("ReadState").put(readState);
      await indexedDBRequestToPromise(req);
      delete readState.board_url;
      readState.url = url.original.href;
      app.message.send("read_state_updated", {
        board_url: boardUrl.href,
        read_state: readState
      });
    } catch (error) {
      e = error;
      app.log("error", "app.ReadState.set: トランザクション失敗");
      throw new Error(e);
    }
  };

  var get$2 = async function(url) {
    var data, db, e, req, result;
    if (app.assertArg("app.read_state.get", [[url, "string"]])) {
      throw new Error("既読情報を取得しようとしたデータが不正です");
    }
    url = _urlFilter(url);
    try {
      db = (await _openDB);
      req = db.transaction("ReadState").objectStore("ReadState").get(url.replaced.href);
      ({
        target: {result}
      } = (await indexedDBRequestToPromise(req)));
      data = app.deepCopy(result);
      if (data != null) {
        data.url = url.original.href;
      }
    } catch (error) {
      e = error;
      app.log("error", "app.ReadState.get: トランザクション中断");
      throw new Error(e);
    }
    return data;
  };

  var getAll = async function() {
    var db, e, req, res;
    try {
      db = (await _openDB);
      req = db.transaction("ReadState").objectStore("ReadState").getAll();
      res = (await indexedDBRequestToPromise(req));
    } catch (error) {
      e = error;
      app.log("error", "app.ReadState.getAll: トランザクション中断");
      throw new Error(e);
    }
    return res.target.result;
  };

  var getByBoard = async function(url) {
    var data, db, e, key, req, val;
    if (app.assertArg("app.ReadState.getByBoard", [[url, "string"]])) {
      throw new Error("既読情報を取得しようとしたデータが不正です");
    }
    url = _urlFilter(url);
    try {
      db = (await _openDB);
      req = db.transaction("ReadState").objectStore("ReadState").index("board_url").getAll(IDBKeyRange.only(url.replaced.href));
      ({
        target: {
          result: data
        }
      } = (await indexedDBRequestToPromise(req)));
      for (key in data) {
        val = data[key];
        data[key].url = val.url.replace(url.replaced.origin, url.original.origin);
      }
    } catch (error) {
      e = error;
      app.log("error", "app.ReadState.getByBoard: トランザクション中断");
      throw new Error(e);
    }
    return data;
  };

  var remove = async function(url) {
    var db, e, req;
    if (app.assertArg("app.ReadState.remove", [[url, "string"]])) {
      throw new Error("既読情報を削除しようとしたデータが不正です");
    }
    url = _urlFilter(url);
    try {
      db = (await _openDB);
      req = db.transaction("ReadState", "readwrite").objectStore("ReadState").delete(url.replaced.href);
      await indexedDBRequestToPromise(req);
      app.message.send("read_state_removed", {
        url: url.original.href
      });
    } catch (error) {
      e = error;
      app.log("error", "app.ReadState.remove: トランザクション中断");
      throw new Error(e);
    }
  };

  var clear = async function() {
    var db, e, req;
    try {
      db = (await _openDB);
      req = db.transaction("ReadState", "readwrite").objectStore("ReadState").clear();
      await indexedDBRequestToPromise(req);
    } catch (error) {
      e = error;
      app.log("error", "app.ReadState.clear: トランザクション中断");
      throw new Error(e);
    }
  };

  _recoveryOfDate = function(db, tx) {
    return new Promise(function(resolve, reject) {
      var req;
      req = tx.objectStore("ReadState").openCursor();
      req.onsuccess = function({
          target: {
            result: cursor
          }
        }) {
        if (cursor) {
          cursor.value.date = null;
          cursor.update(cursor.value);
          cursor.continue();
        } else {
          resolve();
        }
      };
      req.onerror = function(e) {
        app.log("error", "app.ReadState._recoveryOfDate: トランザクション中断");
        reject(e);
      };
    });
  };

  var ReadState = /*#__PURE__*/Object.freeze({
    set: set$1,
    get: get$2,
    getAll: getAll,
    getByBoard: getByBoard,
    remove: remove,
    clear: clear
  });

  class Bookmark {
      constructor(rootIdNode) {
          this.bel = new BrowserBookmarkEntryList(rootIdNode);
          this.promiseFirstScan = new Promise((resolve, reject) => {
              this.bel.ready.add(() => {
                  resolve();
                  this.bel.onChanged.add(({ type: typeName, entry: bookmark }) => {
                      let type = "";
                      switch (typeName) {
                          case "ADD":
                              type = "added";
                              break;
                          case "TITLE":
                              type = "title";
                              break;
                          case "RES_COUNT":
                              type = "res_count";
                              break;
                          case "EXPIRED":
                              type = "expired";
                              break;
                          case "REMOVE":
                              type = "removed";
                              break;
                      }
                      if (type !== "") {
                          app.message.send("bookmark_updated", { type, bookmark });
                          return;
                      }
                      if (typeName === "READ_STATE") {
                          app.message.send("read_state_updated", {
                              "board_url": threadToBoard(bookmark.url),
                              "read_state": bookmark.readState
                          });
                      }
                  });
              });
          });
          // 鯖移転検出時処理
          app.message.on("detected_ch_server_move", ({ before, after }) => {
              this.bel.serverMove(before, after);
          });
      }
      get(url) {
          const entry = this.bel.get(url);
          return entry ? entry : null;
      }
      getByBoard(boardURL) {
          return this.bel.getThreadsByBoardURL(boardURL);
      }
      getAll() {
          return this.bel.getAll();
      }
      getAllThreads() {
          return this.bel.getAllThreads();
      }
      getAllBoards() {
          return this.bel.getAllBoards();
      }
      async add(url, title, resCount) {
          const entry = BrowserBookmarkEntryList.URLToEntry(url);
          entry.title = title;
          const readState = await get$2(entry.url);
          if (readState) {
              entry.readState = readState;
          }
          if (typeof resCount === "number" &&
              (!entry.resCount || entry.resCount < resCount)) {
              entry.resCount = resCount;
          }
          else if (entry.readState) {
              entry.resCount = entry.readState.received;
          }
          return this.bel.add(entry);
      }
      async remove(url) {
          return this.bel.remove(url);
      }
      async removeAll() {
          const bookmarkData = [];
          for (const { url } of this.bel.getAll()) {
              bookmarkData.push(this.bel.remove(url));
          }
          return (await Promise.all(bookmarkData)).every(v => v);
      }
      async removeAllExpired() {
          const bookmarkData = [];
          for (const { url, expired } of this.bel.getAll()) {
              if (expired) {
                  bookmarkData.push(this.bel.remove(url));
              }
          }
          return (await Promise.all(bookmarkData)).every(v => v);
      }
      async updateReadState(readState) {
          // TODO
          const entry = this.bel.get(readState.url);
          if (entry && app.util.isNewerReadState(entry.readState, readState)) {
              entry.readState = readState;
              return this.bel.update(entry);
          }
          return true;
      }
      async updateResCount(url, resCount) {
          const entry = this.bel.get(url);
          if (entry && (!entry.resCount || entry.resCount < resCount)) {
              entry.resCount = resCount;
              return this.bel.update(entry);
          }
          return true;
      }
      async updateExpired(url, expired) {
          const entry = this.bel.get(url);
          if (entry) {
              entry.expired = expired;
              return this.bel.update(entry);
          }
          return true;
      }
      async import(newEntry) {
          let entry = this.bel.get(newEntry.url);
          let updateEntry = false;
          if (!entry) {
              await this.add(newEntry.url, newEntry.title);
              entry = this.bel.get(newEntry.url);
          }
          if (newEntry.readState && app.util.isNewerReadState(entry.readState, newEntry.readState)) {
              entry.readState = newEntry.readState;
              updateEntry = true;
          }
          if (newEntry.resCount && (!entry.resCount || entry.resCount < newEntry.resCount)) {
              entry.resCount = newEntry.resCount;
              updateEntry = true;
          }
          if (entry.expired !== newEntry.expired) {
              entry.expired = newEntry.expired;
              updateEntry = true;
          }
          if (updateEntry) {
              await this.bel.update(entry);
          }
          return true;
      }
  }

  /**
  @class ContextMenus
  @static
  */
  // browser.contextMenusの呼び出しレベルを統一するための代理クラス
  // (Chrome 53 対策)
  /**
  @method createAll
  */
  var createAll = function() {
    var baseUrl, viewThread;
    baseUrl = browser.runtime.getURL("");
    viewThread = [`${baseUrl}view/thread.html*`];
    create({
      id: "add_selection_to_ngwords",
      title: "選択範囲をNG指定",
      contexts: ["selection"],
      documentUrlPatterns: viewThread
    });
    create({
      id: "add_link_to_ngwords",
      title: "リンクアドレスをNG指定",
      contexts: ["link"],
      enabled: false,
      documentUrlPatterns: viewThread
    });
    create({
      id: "add_media_to_ngwords",
      title: "メディアのアドレスをNG指定",
      contexts: ["image", "video", "audio"],
      documentUrlPatterns: viewThread
    });
    create({
      id: "open_link_with_res_number",
      title: "レス番号を指定してリンクを開く",
      contexts: ["link"],
      enabled: false,
      documentUrlPatterns: viewThread
    });
  };

  /**
  @method create
  @parm {Object} obj
  @return {Number|String} id
  */
  var create = function(obj) {
    return browser.contextMenus.create(obj);
  };

  /**
  @method update
  @parm {Number|String} id
  @parm {Object} obj
  */
  var update = function(id, obj) {
    browser.contextMenus.update(id, obj);
  };

  /**
  @method remove
  @parm {Number|String} id
  */
  var remove$1 = function(id) {
    browser.contextMenus.remove(id);
  };

  /**
  @method removeAll
  */
  var removeAll = function() {
    // removeAll()を使うとbackgroundのコンテキストメニューも削除されてしまうので個別に削除する
    remove$1("add_selection_to_ngwords");
    remove$1("add_link_to_ngwords");
    remove$1("add_media_to_ngwords");
    remove$1("open_link_with_res_number");
  };

  var ContextMenus = /*#__PURE__*/Object.freeze({
    createAll: createAll,
    create: create,
    update: update,
    remove: remove$1,
    removeAll: removeAll
  });

  /**
  @class DOMData
  @static
  */
  var _list;

  _list = new WeakMap();

  var set$2 = function(dom, prop, val) {
    if (!_list.has(dom)) {
      _list.set(dom, {});
    }
    _list.get(dom)[prop] = val;
  };

  var get$3 = function(dom, prop) {
    if (_list.has(dom)) {
      return _list.get(dom)[prop];
    }
    return null;
  };

  var DOMData = /*#__PURE__*/Object.freeze({
    set: set$2,
    get: get$3
  });

  /**
  @class History
  @static
  */
  var DB_VERSION$1, openDB;

  DB_VERSION$1 = 2;

  openDB = function() {
    return new Promise((resolve, reject) => {
      var req;
      req = indexedDB.open("History", DB_VERSION$1);
      req.onerror = reject;
      req.onupgradeneeded = ({
          target: {
            result: db,
            transaction: tx
          },
          oldVersion: oldVer
        }) => {
        var objStore;
        if (oldVer < 1) {
          objStore = db.createObjectStore("History", {
            keyPath: "id",
            autoIncrement: true
          });
          objStore.createIndex("url", "url", {
            unique: false
          });
          objStore.createIndex("title", "title", {
            unique: false
          });
          objStore.createIndex("date", "date", {
            unique: false
          });
          tx.oncomplete = function() {
            resolve(db);
          };
        }
        if (oldVer === 1) {
          _recoveryOfBoardTitle(db, tx);
          tx.oncomplete = function() {
            resolve(db);
          };
        }
      };
      req.onsuccess = function({
          target: {
            result: db
          }
        }) {
        resolve(db);
      };
    });
  };

  /**
  @method add
  @param {String} url
  @param {String} title
  @param {Number} date
  @param {String} boardTitle
  @return {Promise}
  */
  var add$1 = async function(url, title, date, boardTitle) {
    var db, e, req;
    if (app.assertArg("History.add", [[url, "string"], [title, "string"], [date, "number"], [boardTitle, "string"]])) {
      throw new Error("履歴に追加しようとしたデータが不正です");
    }
    try {
      db = (await openDB());
      req = db.transaction("History", "readwrite").objectStore("History").add({url, title, date, boardTitle});
      await indexedDBRequestToPromise(req);
    } catch (error) {
      e = error;
      app.log("error", "History.add: データの格納に失敗しました");
      throw new Error(e);
    }
  };

  /**
  @method remove
  @param {String} url
  @param {Number} date
  @return {Promise}
  */
  var remove$2 = async function(url, date = null) {
    var data, db, e, req, store;
    if (app.assertArg("History.remove", [[url, "string"], [date, "number", true]])) {
      return new Error("履歴から削除しようとしたデータが不正です");
    }
    try {
      db = (await openDB());
      store = db.transaction("History", "readwrite").objectStore("History");
      if (date != null) {
        req = store.index("url").getAll(IDBKeyRange.only(url));
      } else {
        req = store.index("url").getAllKeys(IDBKeyRange.only(url));
      }
      ({
        target: {
          result: data
        }
      } = (await indexedDBRequestToPromise(req)));
      if (date != null) {
        await Promise.all(data.map(async function(datum) {
          if (datum.date !== date) {
            return;
          }
          req = store.delete(datum.id);
          await indexedDBRequestToPromise(req);
        }));
      } else {
        await Promise.all(data.map(async function(datum) {
          req = store.delete(datum);
          await indexedDBRequestToPromise(req);
        }));
      }
    } catch (error) {
      e = error;
      app.log("error", "History.remove: トランザクション中断");
      throw new Error(e);
    }
  };

  /**
  @method get
  @param {Number} offset
  @param {Number} limit
  @return {Promise}
  */
  var get$4 = function(offset = -1, limit = -1) {
    if (app.assertArg("History.get", [[offset, "number"], [limit, "number"]])) {
      return Promise.reject();
    }
    return openDB().then(function(db) {
      return new Promise(function(resolve, reject) {
        var advanced, histories, req;
        req = db.transaction("History").objectStore("History").index("date").openCursor(null, "prev");
        advanced = false;
        histories = [];
        req.onsuccess = function({
            target: {
              result: cursor
            }
          }) {
          var value;
          if (cursor && (limit === -1 || histories.length < limit)) {
            if (!advanced) {
              advanced = true;
              if (offset !== -1) {
                cursor.advance(offset);
                return;
              }
            }
            ({value} = cursor);
            value.isHttps = isHttps(value.url);
            histories.push(value);
            cursor.continue();
          } else {
            resolve(histories);
          }
        };
        req.onerror = function(e) {
          app.log("error", "History.get: トランザクション中断");
          reject(e);
        };
      });
    });
  };

  /**
  @method getUnique
  @param {Number} offset
  @param {Number} limit
  @return {Promise}
  */
  var getUnique = function(offset = -1, limit = -1) {
    if (app.assertArg("History.getUnique", [[offset, "number"], [limit, "number"]])) {
      return Promise.reject();
    }
    return openDB().then(function(db) {
      return new Promise(function(resolve, reject) {
        var advanced, histories, inserted, req;
        req = db.transaction("History").objectStore("History").index("date").openCursor(null, "prev");
        advanced = false;
        histories = [];
        inserted = new Set();
        req.onsuccess = function({
            target: {
              result: cursor
            }
          }) {
          var value;
          if (cursor && (limit === -1 || histories.length < limit)) {
            if (!advanced) {
              advanced = true;
              if (offset !== -1) {
                cursor.advance(offset);
                return;
              }
            }
            ({value} = cursor);
            if (!inserted.has(value.url)) {
              value.isHttps = isHttps(value.url);
              histories.push(value);
              inserted.add(value.url);
            }
            cursor.continue();
          } else {
            resolve(histories);
          }
        };
        req.onerror = function(e) {
          app.log("error", "History.getUnique: トランザクション中断");
          reject(e);
        };
      });
    });
  };

  /**
  @method getAll
  @return {Promise}
  */
  var getAll$1 = async function() {
    var db, e, req, res;
    try {
      db = (await openDB());
      req = db.transaction("History").objectStore("History").getAll();
      res = (await indexedDBRequestToPromise(req));
    } catch (error) {
      e = error;
      app.log("error", "History.getAll: トランザクション中断");
      throw new Error(e);
    }
    return res.target.result;
  };

  /**
  @method count
  @return {Promise}
  */
  var count = async function() {
    var db, e, req, res;
    try {
      db = (await openDB());
      req = db.transaction("History").objectStore("History").count();
      res = (await indexedDBRequestToPromise(req));
    } catch (error) {
      e = error;
      app.log("error", "History.count: トランザクション中断");
      throw new Error(e);
    }
    return res.target.result;
  };

  /**
  @method clear
  @param {Number} offset
  @return {Promise}
  */
  var clear$1 = function(offset = -1) {
    if (app.assertArg("History.clear", [[offset, "number"]])) {
      return Promise.reject();
    }
    return openDB().then(function(db) {
      return new Promise(function(resolve, reject) {
        var advanced, req;
        req = db.transaction("History", "readwrite").objectStore("History").openCursor();
        advanced = false;
        req.onsuccess = function({
            target: {
              result: cursor
            }
          }) {
          if (cursor) {
            if (!advanced) {
              advanced = true;
              if (offset !== -1) {
                cursor.advance(offset);
                return;
              }
            }
            cursor.delete();
            cursor.continue();
          } else {
            resolve();
          }
        };
        req.onerror = function(e) {
          app.log("error", "History.clear: トランザクション中断");
          reject(e);
        };
      });
    });
  };

  /**
  @method clearRange
  @param {Number} day
  @return {Promise}
  */
  var clearRange = async function(day) {
    var dayUnix, db, e, keys, req, store;
    if (app.assertArg("History.clearRange", [[day, "number"]])) {
      return Promise.reject();
    }
    dayUnix = Date.now() - day * 24 * 60 * 60 * 1000;
    try {
      db = (await openDB());
      store = db.transaction("History", "readwrite").objectStore("History");
      req = store.index("date").getAllKeys(IDBKeyRange.upperBound(dayUnix, true));
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
      app.log("error", "History.clearRange: トランザクション中断");
      throw new Error(e);
    }
  };

  var History = /*#__PURE__*/Object.freeze({
    add: add$1,
    remove: remove$2,
    get: get$4,
    getUnique: getUnique,
    getAll: getAll$1,
    count: count,
    clear: clear$1,
    clearRange: clearRange
  });

  /**
  @class ImageReplaceDat
  @static
  */
  /**
  @method parse
  @param {String} string
  @return {Object}
  */
  var _CONFIG_NAME$1, _CONFIG_STRING_NAME$1, _INVALID_URL, _config$1, _dat, _setupReg$1, parse$2;

  _dat = null;

  _CONFIG_NAME$1 = "image_replace_dat_obj";

  _CONFIG_STRING_NAME$1 = "image_replace_dat";

  _INVALID_URL = "invalid://invalid";

  //jsonには正規表現のオブジェクトが含めれないので
  //それを展開
  _setupReg$1 = function() {
    var d;
    for (d of _dat) {
      try {
        d.baseUrlReg = new RegExp(d.baseUrl, "i");
      } catch (error) {
        app.message.send("notify", {
          message: `ImageViewURLReplace.datの一致URLの正規表現(${d.baseUrl})を読み込むのに失敗しました\nこの行は無効化されます`,
          background_color: "red"
        });
        d.baseUrl = _INVALID_URL;
      }
    }
  };

  _config$1 = {
    get: function() {
      return JSON.parse(app.config.get(_CONFIG_NAME$1));
    },
    set: function(str) {
      app.config.set(_CONFIG_NAME$1, JSON.stringify(str));
    },
    getString: function() {
      return app.config.get(_CONFIG_STRING_NAME$1);
    },
    setString: function(str) {
      app.config.set(_CONFIG_STRING_NAME$1, str);
    }
  };

  /**
  @method get
  @return {Object}
  */
  var get$5 = function() {
    if (_dat == null) {
      if (app.config.get(_CONFIG_NAME$1) === "") {
        set$3(_config$1.getString());
      }
      _dat = new Set(_config$1.get());
      _setupReg$1();
    }
    return _dat;
  };

  parse$2 = function(string) {
    var d, dat, datStrSplit, i, len, obj, r, ref, ref1, ref2, rurl;
    dat = new Set();
    if (string === "") {
      return dat;
    }
    datStrSplit = string.split("\n");
    for (i = 0, len = datStrSplit.length; i < len; i++) {
      d = datStrSplit[i];
      if (d === "") {
        continue;
      }
      if (["//", ";", "'"].some(function(ele) {
        return d.startsWith(ele);
      })) {
        continue;
      }
      r = d.split("\t");
      if (r[0] == null) {
        continue;
      }
      obj = {
        baseUrl: r[0],
        replaceUrl: (ref = r[1]) != null ? ref : "",
        referrerUrl: (ref1 = r[2]) != null ? ref1 : "",
        userAgent: (ref2 = r[5]) != null ? ref2 : ""
      };
      if (r[3] != null) {
        obj.param = {};
        rurl = r[3].split("=")[1];
        if (r[3].includes("$EXTRACT")) {
          obj.param = {
            type: "extract",
            pattern: r[4],
            referrerUrl: rurl != null ? rurl : ""
          };
        } else if (r[4].includes("$COOKIE")) {
          obj.param = {
            type: "cookie",
            referrerUrl: rurl != null ? rurl : ""
          };
        }
      }
      dat.add(obj);
    }
    return dat;
  };

  /**
  @method set
  @param {String} string
  */
  var set$3 = function(string) {
    _dat = parse$2(string);
    _config$1.set([..._dat]);
    _setupReg$1();
  };

  /*
  @method replace
  @param {String} string
  @return {Object}
  */
  var replace = function(string) {
    var d, dat, res;
    dat = get$5();
    res = {};
    for (d of dat) {
      if (d.baseUrl === _INVALID_URL) {
        continue;
      }
      if (!d.baseUrlReg.test(string)) {
        continue;
      }
      if (d.replaceUrl === "") {
        return {
          res,
          err: "No parsing"
        };
      }
      if ((d.param != null) && d.param.type === "extract") {
        res.type = "extract";
        res.text = string.replace(d.baseUrlReg, d.replaceUrl);
        res.extract = string.replace(d.baseUrlReg, d.referrerUrl);
        res.extractReferrer = d.param.referrerUrl;
        res.pattern = d.param.pattern;
        res.userAgent = d.userAgent;
        return {res};
      } else if ((d.param != null) && d.param.type === "cookie") {
        res.type = "cookie";
        res.text = string.replace(d.baseUrlReg, d.replaceUrl);
        res.cookie = string.replace(d.baseUrlReg, d.referrerUrl);
        res.cookieReferrer = d.param.referrerUrl;
        res.userAgent = d.userAgent;
        return {res};
      } else {
        res.type = "default";
        res.text = string.replace(d.baseUrlReg, d.replaceUrl);
        if (d.referrerUrl !== "" || d.userAgent !== "") {
          res.type = "referrer";
          res.referrer = string.replace(d.baseUrlReg, d.referrerUrl);
          res.userAgent = d.userAgent;
        }
        return {res};
      }
    }
    return {
      res,
      err: "Fail noBaseUrlReg"
    };
  };

  var ImageReplaceDat = /*#__PURE__*/Object.freeze({
    get: get$5,
    set: set$3,
    replace: replace
  });

  var Notification;

  var Notification$1 = Notification = (function() {
    var createNotification;

    class Notification {
      constructor(title1, message1, url, tag1) {
        this.title = title1;
        this.message = message1;
        this.url = url;
        this.tag = tag1;
        this.notify = null;
        if (window.Notification.permission === "granted") {
          this.notify = createNotification(this.title, this.message, this.tag);
        } else {
          window.Notification.requestPermission(function(permission) {
            if (permission === "granted") {
              return this.notify = createNotification(this.title, this.message, this.tag);
            }
          });
        }
        if (this.notify && this.url !== "") {
          this.notify.on("click", async() => {
            var tab;
            tab = (await browser.tabs.getCurrent());
            browser.tabs.update(tab.id, {
              active: true
            });
            app.message.send("open", {
              url: this.url
            });
            this.notify.close();
          });
        }
        return;
      }

    }
    createNotification = function(title, message, tag) {
      return new window.Notification(title, {
        tag: tag,
        body: message,
        icon: "../img/read.crx_128x128.png"
      });
    };

    return Notification;

  }).call(window);

  /**
  @class ReplaceStrTxt
  @static
  */
  /**
  @method parse
  @param {String} string
  @return {Object}
  */
  var _CONFIG_NAME$2, _CONFIG_STRING_NAME$2, _INVALID_BEFORE, _INVALID_URL$1, _PLACE_TABLE, _URL_PATTERN, _config$2, _replaceTable, _setupReg$2, parse$3;

  _replaceTable = null;

  _CONFIG_NAME$2 = "replace_str_txt_obj";

  _CONFIG_STRING_NAME$2 = "replace_str_txt";

  _URL_PATTERN = {
    CONTAIN: 0,
    DONTCONTAIN: 1,
    MATCH: 2,
    DONTMATCH: 3,
    REGEX: 4,
    DONTREGEX: 5
  };

  _PLACE_TABLE = new Map([["name", "name"], ["mail", "mail"], ["date", "other"], ["msg", "message"]]);

  _INVALID_BEFORE = "#^##invalid##^#";

  _INVALID_URL$1 = "invalid://invalid";

  //jsonには正規表現のオブジェクトが含めれないので
  //それを展開
  _setupReg$2 = function() {
    var d, ref;
    for (d of _replaceTable) {
      try {
        d.beforeReg = (function() {
          switch (d.type) {
            case "rx":
              return new RegExp(d.before, "g");
            case "rx2":
              return new RegExp(d.before, "ig");
            case "ex":
              return new RegExp(d.before.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&"), "ig");
          }
        })();
      } catch (error) {
        app.message.send("notify", {
          message: `ReplaceStr.txtの置換対象正規表現(${d.before})を読み込むのに失敗しました\nこの行は無効化されます`,
          background_color: "red"
        });
        d.before = _INVALID_BEFORE;
      }
      try {
        if ((ref = d.urlPattern) === _URL_PATTERN.REGEX || ref === _URL_PATTERN.DONTREGEX) {
          d.urlReg = new RegExp(d.url);
        }
      } catch (error) {
        app.message.send("notify", {
          message: `ReplaceStr.txtの対象URL/タイトル正規表現(${d.url})を読み込むのに失敗しました\nこの行は無効化されます`,
          background_color: "red"
        });
        d.url = _INVALID_URL$1;
      }
    }
  };

  _config$2 = {
    get: function() {
      return JSON.parse(app.config.get(_CONFIG_NAME$2));
    },
    set: function(str) {
      app.config.set(_CONFIG_NAME$2, JSON.stringify(str));
    },
    getString: function() {
      return app.config.get(_CONFIG_STRING_NAME$2);
    },
    setString: function(str) {
      app.config.set(_CONFIG_STRING_NAME$2, str);
    }
  };

  /**
  @method get
  @return {Object}
  */
  var get$6 = function() {
    if (_replaceTable == null) {
      _replaceTable = new Set(_config$2.get());
      _setupReg$2();
    }
    return _replaceTable;
  };

  parse$3 = function(string) {
    var i, len, obj, r, ref, replaceStrSplit, replaceTable, s;
    replaceTable = new Set();
    if (string === "") {
      return replaceTable;
    }
    replaceStrSplit = string.split("\n");
    for (i = 0, len = replaceStrSplit.length; i < len; i++) {
      r = replaceStrSplit[i];
      if (r === "") {
        continue;
      }
      if (["//", ";", "'"].some(function(ele) {
        return r.startsWith(ele);
      })) {
        continue;
      }
      s = /(?:<(\w{2,3})>)?(.*)\t(.+)\t(name|mail|date|msg|all)(?:\t(?:<(\d)>)?(.+))?/.exec(r);
      if (s == null) {
        continue;
      }
      obj = {
        type: (ref = s[1]) != null ? ref : "ex",
        place: s[4],
        before: s[2],
        after: s[3],
        urlPattern: s[5],
        url: s[6]
      };
      if (obj.type === "") {
        obj.type = "rx";
      }
      if (obj.place === "") {
        obj.place = "all";
      }
      if ((s[6] != null) && (s[5] == null)) {
        obj.urlPattern = 0;
      }
      replaceTable.add(obj);
    }
    return replaceTable;
  };

  /**
  @method set
  @param {String} string
  */
  var set$4 = function(string) {
    _replaceTable = parse$3(string);
    _config$2.set([..._replaceTable]);
    _setupReg$2();
  };

  /*
  @method replace
  @param {String} url
  @param {String} title
  @param {Object} res
  */
  var replace$1 = function(url, title, res) {
    var after, before, d, flag, place, ref, ref1, ref2, ref3, ref4;
    ref = get$6();
    for (d of ref) {
      if (d.before === _INVALID_BEFORE) {
        continue;
      }
      if (d.url === _INVALID_URL$1) {
        continue;
      }
      if (d.url != null) {
        if ((ref1 = d.urlPattern) === _URL_PATTERN.CONTAIN || ref1 === _URL_PATTERN.DONTCONTAIN) {
          flag = url.includes(d.url) || title.includes(d.url);
        } else if ((ref2 = d.urlPattern) === _URL_PATTERN.MATCH || ref2 === _URL_PATTERN.DONTMATCH) {
          flag = ((ref3 = d.url) === url || ref3 === title);
        }
        if ((ref4 = d.urlPattern) === _URL_PATTERN.DONTCONTAIN || ref4 === _URL_PATTERN.DONTMATCH) {
          flag = !flag;
        }
        if (!flag) {
          continue;
        }
      }
      if (d.type === "ex2") {
        ({place, before, after} = d);
        if (place === "all") {
          res = {
            name: app.replaceAll(res.name, before, after),
            mail: app.replaceAll(res.mail, before, after),
            other: app.replaceAll(res.other, before, after),
            message: app.replaceAll(res.message, before, after)
          };
        } else {
          place = _PLACE_TABLE.get(place);
          res[place] = app.replaceAll(res[place], before, after);
        }
      } else {
        ({
          place,
          beforeReg: before,
          after
        } = d);
        if (place === "all") {
          res = {
            name: res.name.replace(before, after),
            mail: res.mail.replace(before, after),
            other: res.other.replace(before, after),
            message: res.message.replace(before, after)
          };
        } else {
          place = _PLACE_TABLE.get(place);
          res[place] = res[place].replace(before, after);
        }
      }
    }
    return res;
  };

  var ReplaceStrTxt = /*#__PURE__*/Object.freeze({
    get: get$6,
    set: set$4,
    replace: replace$1
  });

  var Thread;

  /**
  @class Thread
  @constructor
  @param {String} url
  */
  var Thread$1 = Thread = class Thread {
    constructor(url) {
      this.url = new URL(url);
      this.title = null;
      this.res = null;
      this.message = null;
      this.tsld = this.url.getTsld();
      this.expired = false;
      return;
    }

    get(forceUpdate, progress) {
      var getCachedInfo;
      getCachedInfo = (async() => {
        var ref;
        if ((ref = this.tsld) === "shitaraba.net" || ref === "machi.to") {
          try {
            return {
              status: "success",
              cachedInfo: (await Board$1.getCachedResCount(this.url))
            };
          } catch (error1) {
            return {
              status: "none"
            };
          }
        }
        return {
          status: "none"
        };
      })();
      return new Promise(async(resolve, reject) => {
        var bbsType, cache, cachedInfo, deltaFlg, error, etag, hasCache, isHtml, lastModified, needFetch, newBoardURL, newURL, newUrl, noChangeFlg, readcgiPlace, readcgiVer, ref, request, response, status, thread, threadCache, threadResponse, tmp, xhrCharset, xhrInfo, xhrPath;
        xhrInfo = Thread._getXhrInfo(this.url);
        if (!xhrInfo) {
          this.message = "対応していないURLです";
          reject();
          return;
        }
        ({
          path: xhrPath,
          charset: xhrCharset
        } = xhrInfo);
        cache = new Cache$1(xhrPath);
        hasCache = false;
        deltaFlg = false;
        readcgiVer = 5;
        noChangeFlg = false;
        isHtml = (app.config.get("format_2chnet") !== "dat" && this.tsld === "5ch.net") || this.tsld === "bbspink.com";
        // キャッシュ取得
        needFetch = false;
        try {
          await cache.get();
          hasCache = true;
          if (forceUpdate || Date.now() - cache.lastUpdated > 1000 * 3) {
            // 通信が生じる場合のみ、progressでキャッシュを送出する
            await app.defer();
            tmp = (ref = cache.parsed) != null ? ref : Thread.parse(this.url, cache.data);
            if (tmp != null) {
              this.res = tmp.res;
              this.title = tmp.title;
              progress();
            }
            throw new Error("キャッシュの期限が切れているため通信します");
          }
        } catch (error1) {
          needFetch = true;
        }
        try {
          // 通信
          if (needFetch) {
            if ((this.tsld === "shitaraba.net" && !this.url.isArchive()) || this.tsld === "machi.to") {
              if (hasCache) {
                deltaFlg = true;
                xhrPath += (+cache.resLength + 1) + "-";
              }
            // 2ch.netは差分を-nで取得
            } else if (isHtml) {
              if (hasCache) {
                deltaFlg = true;
                ({readcgiVer} = cache);
                if (readcgiVer >= 6) {
                  xhrPath += (+cache.resLength + 1) + "-n";
                } else {
                  xhrPath += (+cache.resLength) + "-n";
                }
              }
            }
            request = new Request("GET", xhrPath, {
              mimeType: `text/plain; charset=${xhrCharset}`,
              preventCache: true
            });
            if (hasCache) {
              if (cache.lastModified != null) {
                request.headers["If-Modified-Since"] = new Date(cache.lastModified).toUTCString();
              }
              if (cache.etag != null) {
                request.headers["If-None-Match"] = cache.etag;
              }
            }
            response = (await request.send());
          }
          // パース
          ({bbsType} = this.url.guessType());
          if ((response != null ? response.status : void 0) === 200 || (readcgiVer >= 6 && (response != null ? response.status : void 0) === 500)) {
            if (deltaFlg) {
              // 2ch.netなら-nを使って前回取得したレスの後のレスからのものを取得する
              if (isHtml) {
                threadCache = cache.parsed;
                // readcgi ver6,7だと変更がないと500が帰ってくる
                if (readcgiVer >= 6 && response.status === 500) {
                  noChangeFlg = true;
                  thread = threadCache;
                } else {
                  threadResponse = Thread.parse(this.url, response.body, +cache.resLength);
                  // 新しいレスがない場合は最後のレスのみ表示されるのでその場合はキャッシュを送る
                  if (readcgiVer < 6 && threadResponse.res.length === 1) {
                    noChangeFlg = true;
                    thread = threadCache;
                  } else {
                    if (readcgiVer < 6) {
                      threadResponse.res.shift();
                    }
                    thread = threadResponse;
                    thread.res = threadCache.res.concat(threadResponse.res);
                  }
                }
              } else {
                thread = Thread.parse(this.url, cache.data + response.body);
              }
            } else {
              thread = Thread.parse(this.url, response.body);
            }
          // 2ch系BBSのdat落ち
          } else if (bbsType === "2ch" && (response != null ? response.status : void 0) === 203) {
            if (hasCache) {
              if (deltaFlg && isHtml) {
                thread = cache.parsed;
              } else {
                thread = Thread.parse(this.url, cache.data);
              }
            } else {
              thread = Thread.parse(this.url, response.body);
            }
          } else if (hasCache) {
            if (isHtml) {
              thread = cache.parsed;
            } else {
              thread = Thread.parse(this.url, cache.data);
            }
          }
          //パース成功
          if (thread) {
            //2ch系BBSのdat落ち
            if (bbsType === "2ch" && (response != null ? response.status : void 0) === 203) {
              throw {response, thread};
            }
            //通信失敗
            //通信成功（更新なし）
            //通信成功（2ch read.cgi ver6,7の差分更新なし）
            //キャッシュが期限内だった場合
            if (!((response != null ? response.status : void 0) === 200 || (response != null ? response.status : void 0) === 304 || (readcgiVer >= 6 && (response != null ? response.status : void 0) === 500) || (!response && hasCache))) {
              throw {response, thread};
            }
          } else {
            //パース失敗
            throw {response};
          }
          //したらば/まちBBS最新レス削除対策
          ({status, cachedInfo} = (await getCachedInfo));
          if (status === "sucess") {
            while (thread.res.length < cachedInfo.resCount) {
              thread.res.push({
                name: "あぼーん",
                mail: "あぼーん",
                message: "あぼーん",
                other: "あぼーん"
              });
            }
          }
          //コールバック
          if (thread) {
            this.title = thread.title;
            this.res = thread.res;
            this.expired = thread.expired != null;
          }
          this.message = "";
          resolve();
          //キャッシュ更新部
          //通信に成功した場合
          if (((response != null ? response.status : void 0) === 200 && thread) || (readcgiVer >= 6 && (response != null ? response.status : void 0) === 500)) {
            cache.lastUpdated = Date.now();
            if (isHtml) {
              readcgiPlace = response.body.indexOf("<div class=\"footer push\">read.cgi ver ");
              if (readcgiPlace !== -1) {
                readcgiVer = parseInt(response.body.substr(readcgiPlace + 38, 2));
              } else {
                readcgiVer = 5;
              }
              // 2ch(html)のみ
              if (thread.expired) {
                app.bookmark.updateExpired(this.url.href, true);
              }
            }
            if (deltaFlg) {
              if (isHtml && !noChangeFlg) {
                cache.parsed = thread;
                cache.readcgiVer = readcgiVer;
              } else if (noChangeFlg === false) {
                cache.data += response.body;
              }
              cache.resLength = thread.res.length;
            } else {
              if (isHtml) {
                cache.parsed = thread;
                cache.readcgiVer = readcgiVer;
              } else {
                cache.data = response.body;
              }
              cache.resLength = thread.res.length;
            }
            lastModified = new Date(response.headers["Last-Modified"] || "dummy").getTime();
            if (Number.isFinite(lastModified)) {
              cache.lastModified = lastModified;
            }
            etag = response.headers["ETag"];
            if (etag) {
              cache.etag = etag;
            }
            cache.put();
          //304だった場合はアップデート時刻のみ更新
          } else if (hasCache && (response != null ? response.status : void 0) === 304) {
            cache.lastUpdated = Date.now();
            cache.put();
          }
        } catch (error1) {
          ({response, thread} = error1);
          if (thread) {
            this.title = thread.title;
            this.res = thread.res;
          }
          this.message = "";
          //2chでrejectされてる場合は移転を疑う
          if (this.tsld === "5ch.net" && response) {
            try {
              newBoardURL = (await chServerMoveDetect(this.url.toBoard()));
              //移転検出時
              newUrl = new URL(this.url);
              newUrl.hostname = newBoardURL.hostname;
              this.message += `スレッドの読み込みに失敗しました。\nサーバーが移転している可能性が有ります\n(<a href="${app.escapeHtml(app.safeHref(newURL.href))}"\n  class="open_in_rcrx">${app.escapeHtml(newURL.href)}</a>)`;
            } catch (error1) {
              //移転検出出来なかった場合
              if ((response != null ? response.status : void 0) === 203) {
                this.message += "dat落ちしたスレッドです。";
                thread.expired = true;
              } else {
                this.message += "スレッドの読み込みに失敗しました。";
              }
            }
            if (hasCache && !thread) {
              this.message += "キャッシュに残っていたデータを表示します。";
            }
            reject();
          } else if (this.tsld === "shitaraba.net" && !this.url.isArchive()) {
            this.message += "スレッドの読み込みに失敗しました。";
            ({error} = (response != null ? response.headers : void 0) != null);
            if (error != null) {
              switch (error) {
                case "BBS NOT FOUND":
                  this.message += "\nURLの掲示板番号が間違っています。";
                  break;
                case "KEY NOT FOUND":
                  this.message += "\nURLのスレッド番号が間違っています。";
                  break;
                case "THREAD NOT FOUND":
                  this.message += "該当するスレッドは存在しません。\nURLが間違っているか過去ログに移動せずに削除されています。";
                  break;
                case "STORAGE IN":
                  newURL = this.url.href.replace("/read.cgi/", "/read_archive.cgi/");
                  this.message += `過去ログが存在します\n(<a href="${app.escapeHtml(app.safeHref(newURL))}"\n  class="open_in_rcrx">${app.escapeHtml(newURL)}</a>)`;
              }
            }
            reject();
          } else {
            this.message += "スレッドの読み込みに失敗しました。";
            if (hasCache && !thread) {
              this.message += "キャッシュに残っていたデータを表示します。";
            }
            reject();
          }
        }
        if (thread != null) {
          //ブックマーク更新部
          app.bookmark.updateResCount(this.url.href, thread.res.length);
        }
        //dat落ち検出
        if ((response != null ? response.status : void 0) === 203) {
          app.bookmark.updateExpired(this.url.href, true);
        }
      });
    }

    /**
    @method _getXhrInfo
    @static
    @param {app.URL.URL} url
    @return {null|Object}
    */
    static _getXhrInfo(url) {
      var tmp;
      tmp = /^\/(?:test|bbs)\/read(?:_archive)?\.cgi\/(\w+)\/(\d+)\/(?:(\d+)\/)?$/.exec(url.pathname);
      if (!tmp) {
        return null;
      }
      switch (url.getTsld()) {
        case "machi.to":
          return {
            path: `${url.origin}/bbs/offlaw.cgi/${tmp[1]}/${tmp[2]}/`,
            charset: "Shift_JIS"
          };
        case "shitaraba.net":
          if (url.isArchive()) {
            return {
              path: url.href,
              charset: "EUC-JP"
            };
          } else {
            return {
              path: `${url.origin}/bbs/rawmode.cgi/${tmp[1]}/${tmp[2]}/${tmp[3]}/`,
              charset: "EUC-JP"
            };
          }
          break;
        case "5ch.net":
          if (app.config.get("format_2chnet") === "dat") {
            return {
              path: `${url.origin}/${tmp[1]}/dat/${tmp[2]}.dat`,
              charset: "Shift_JIS"
            };
          } else {
            return {
              path: url.href,
              charset: "Shift_JIS"
            };
          }
          break;
        case "bbspink.com":
          return {
            path: url.href,
            charset: "Shift_JIS"
          };
        default:
          return {
            path: `${url.origin}/${tmp[1]}/dat/${tmp[2]}.dat`,
            charset: "Shift_JIS"
          };
      }
    }

    /**
    @method parse
    @static
    @param {app.URL.URL} url
    @param {String} text
    @param {Number} resLength
    @return {null|Object}
    */
    static parse(url, text, resLength) {
      switch (url.getTsld()) {
        case "":
          return null;
        case "machi.to":
          return Thread._parseMachi(text);
        case "shitaraba.net":
          if (url.isArchive()) {
            return Thread._parseJbbsArchive(text);
          } else {
            return Thread._parseJbbs(text);
          }
          break;
        case "5ch.net":
          if (app.config.get("format_2chnet") === "dat") {
            return Thread._parseCh(text);
          } else {
            return Thread._parseNet(text);
          }
          break;
        case "bbspink.com":
          return Thread._parsePink(text, resLength);
        default:
          return Thread._parseCh(text);
      }
    }

    /**
    @method _parseNet
    @static
    @private
    @param {String} text
    @return {null|Object}
    */
    static _parseNet(text) {
      var gotTitle, i, len, line, numberOfBroken, ref, reg, regRes, separator, thread, title, titleReg;
      // name, mail, other, message, thread_title
      if (text.includes("<div class=\"footer push\">read.cgi ver 06") && !text.includes("</div></div><br>")) {
        text = text.replace("</h1>", "</h1></div></div>");
        reg = /<div class="post"[^<>]*><div class="number">\d+[^<>]* : <\/div><div class="name"><b>(?:<a href="mailto:([^<>]*)">|<font [^<>]*>)?(.*?)(?:<\/(?:a|font)>)?<\/b><\/div><div class="date">(.*)<\/div><div class="message"> ?(.*)/;
        separator = "</div></div>";
      } else if (text.includes("<div class=\"footer push\">read.cgi ver 07") || text.includes("<div class=\"footer push\">read.cgi ver 06")) {
        text = text.replace("</h1>", "</h1></div></div><br>");
        reg = /<div class="post"[^<>]*><div class="meta"><span class="number">\d+<\/span><span class="name"><b>(?:<a href="mailto:([^<>]*)">|<font [^<>]*>)?(.*?)(?:<\/(?:a|font)>)?<\/b><\/span><span class="date">(.*)<\/span><\/div><div class="message">(?:<span class="escaped">)? ?(.*)(?:<\/span>)/;
        separator = "</div></div><br>";
      } else {
        reg = /^(?:<\/?div.*?(?:<br><br>)?)?<dt>\d+.*：(?:<a href="mailto:([^<>]*)">|<font [^>]*>)?<b>(.*)<\/b>.*：(.*)<dd> ?(.*)<br><br>$/;
        separator = "\n";
      }
      titleReg = /<h1 [^<>]*>(.*)\n?<\/h1>/;
      numberOfBroken = 0;
      thread = {
        res: []
      };
      gotTitle = false;
      ref = text.split(separator);
      for (i = 0, len = ref.length; i < len; i++) {
        line = ref[i];
        title = gotTitle ? false : titleReg.exec(line);
        regRes = reg.exec(line);
        if (title) {
          thread.title = decodeCharReference(title[1]);
          thread.title = removeNeedlessFromTitle(thread.title);
          gotTitle = true;
        } else if (regRes) {
          thread.res.push({
            name: regRes[2],
            mail: regRes[1] || "",
            message: regRes[4],
            other: regRes[3]
          });
        }
      }
      if (text.includes("<div class=\"stoplight stopred stopdone\">")) {
        thread.expired = true;
      }
      if (thread.res.length > 0 && thread.res.length > numberOfBroken) {
        return thread;
      }
      return null;
    }

    /**
    @method _parseCh
    @static
    @private
    @param {String} text
    @return {null|Object}
    */
    static _parseCh(text) {
      var i, key, len, line, numberOfBroken, ref, sp, thread;
      numberOfBroken = 0;
      thread = {
        res: []
      };
      ref = text.split("\n");
      for (key = i = 0, len = ref.length; i < len; key = ++i) {
        line = ref[key];
        if (line === "") {
          continue;
        }
        // name, mail, other, message, thread_title
        sp = line.split("<>");
        if (sp.length >= 4) {
          if (key === 0) {
            thread.title = decodeCharReference(sp[4]);
          }
          thread.res.push({
            name: sp[0],
            mail: sp[1],
            message: sp[3],
            other: sp[2]
          });
        } else {
          if (line === "") {
            continue;
          }
          numberOfBroken++;
          thread.res.push({
            name: "</b>データ破損<b>",
            mail: "",
            message: "データが破損しています",
            other: ""
          });
        }
      }
      if (thread.res.length > 0 && thread.res.length > numberOfBroken) {
        return thread;
      }
      return null;
    }

    /**
    @method _parseMachi
    @static
    @private
    @param {String} text
    @return {null|Object}
    */
    static _parseMachi(text) {
      var i, len, line, numberOfBroken, ref, resCount, sp, thread;
      thread = {
        res: []
      };
      resCount = 0;
      numberOfBroken = 0;
      ref = text.split("\n");
      for (i = 0, len = ref.length; i < len; i++) {
        line = ref[i];
        if (line === "") {
          continue;
        }
        // res_num, name, mail, other, message, thread_title
        sp = line.split("<>");
        if (sp.length >= 5) {
          while (++resCount !== +sp[0]) {
            thread.res.push({
              name: "あぼーん",
              mail: "あぼーん",
              message: "あぼーん",
              other: "あぼーん"
            });
          }
          if (resCount === 1) {
            thread.title = decodeCharReference(sp[5]);
          }
          thread.res.push({
            name: sp[1],
            mail: sp[2],
            message: sp[4],
            other: sp[3]
          });
        } else {
          if (line === "") {
            continue;
          }
          numberOfBroken++;
          thread.res.push({
            name: "</b>データ破損<b>",
            mail: "",
            message: "データが破損しています",
            other: ""
          });
        }
      }
      if (thread.res.length > 0 && thread.res.length > numberOfBroken) {
        return thread;
      }
      return null;
    }

    /**
    @method _parseJbbs
    @static
    @private
    @param {String} text
    @return {null|Object}
    */
    static _parseJbbs(text) {
      var i, len, line, numberOfBroken, ref, resCount, sp, thread;
      thread = {
        res: []
      };
      resCount = 0;
      numberOfBroken = 0;
      ref = text.split("\n");
      for (i = 0, len = ref.length; i < len; i++) {
        line = ref[i];
        if (line === "") {
          continue;
        }
        // res_num, name, mail, date, message, thread_title, id
        sp = line.split("<>");
        if (sp.length >= 6) {
          while (++resCount !== +sp[0]) {
            thread.res.push({
              name: "あぼーん",
              mail: "あぼーん",
              message: "あぼーん",
              other: "あぼーん"
            });
          }
          if (resCount === 1) {
            thread.title = decodeCharReference(sp[5]);
          }
          thread.res.push({
            name: sp[1],
            mail: sp[2],
            message: sp[4],
            other: sp[3] + (sp[6] ? ` ID:${sp[6]}` : "")
          });
        } else {
          if (line === "") {
            continue;
          }
          numberOfBroken++;
          thread.res.push({
            name: "</b>データ破損<b>",
            mail: "",
            message: "データが破損しています",
            other: ""
          });
        }
      }
      if (thread.res.length > 0 && thread.res.length > numberOfBroken) {
        return thread;
      }
      return null;
    }

    /**
    @method _parseJbbsArchive
    @static
    @private
    @param {String} text
    @return {null|Object}
    */
    static _parseJbbsArchive(text) {
      var gotTitle, i, len, line, numberOfBroken, ref, reg, regRes, separator, thread, title, titleReg;
      // name, mail, other, message, thread_title
      text = app.replaceAll(text, "\n", "");
      text = text.replace(/<\/h1>\s*<dl>/, "</h1></dd><br><br>");
      reg = /<dt[^>]*>\s*\d+ ：\s*(?:<a href="mailto:([^<>]*)">)?\s*(?:<font [^>]*>)?\s*<b>(.*)<\/b>.*：(.*)\s*<\/dt>\s*<dd>\s*(.*)\s*<br>/;
      separator = /<\/dd>[\s\n]*<br><br>/;
      titleReg = /<h1>(.*)<\/h1>/;
      numberOfBroken = 0;
      thread = {
        res: []
      };
      gotTitle = false;
      ref = text.split(separator);
      for (i = 0, len = ref.length; i < len; i++) {
        line = ref[i];
        title = gotTitle ? false : titleReg.exec(line);
        regRes = reg.exec(line);
        if (title) {
          thread.title = decodeCharReference(title[1]);
          gotTitle = true;
        } else if (regRes) {
          thread.res.push({
            name: regRes[2],
            mail: regRes[1] || "",
            message: regRes[4],
            other: regRes[3]
          });
        }
      }
      if (thread.res.length > 0 && thread.res.length > numberOfBroken) {
        return thread;
      }
      return null;
    }

    /**
    @method _parsePink
    @static
    @private
    @param {String} text
    @param {Number} resLength
    @return {null|Object}
    */
    static _parsePink(text, resLength) {
      var gotTitle, i, len, line, numberOfBroken, ref, reg, regRes, resCount, separator, thread, title, titleReg;
      // name, mail, other, message, thread_title
      if (text.includes("<div class=\"footer push\">read.cgi ver 06")) {
        text = text.replace(/<\/h1>/, "</h1></dd></dl>");
        reg = /^.*?<dl class="post".*><dt class=\"\"><span class="number">(\d+).* : <\/span><span class="name"><b>(?:<a href="mailto:([^<>]*)">|<font [^>]*>)?(.*?)(?:<\/a>|<\/font>)?<\/b><\/span><span class="date">(.*)<\/span><\/dt><dd class="thread_in"> ?(.*)$/;
        separator = "</dd></dl>";
      } else if (text.includes("<div class=\"footer push\">read.cgi ver 07")) {
        text = text.replace("</h1>", "</h1></div></div><br>");
        reg = /<div class="post"[^<>]*><div class="meta"><span class="number">(\d+).*<\/span><span class="name"><b>(?:<a href="mailto:([^<>]*)">|<font [^<>]*>)?(.*?)(?:<\/(?:a|font)>)?<\/b><\/span><span class="date">(.*)<\/span><\/div><div class="message">(?:<span class="escaped">)? ?(.*)(?:<\/span>)/;
        separator = "</div></div><br>";
      } else {
        reg = /^(?:<\/?div.*?(?:<br><br>)?)?<dt>(\d+).*：(?:<a href="mailto:([^<>]*)">|<font [^>]*>)?<b>(.*)<\/b>.*：(.*)<dd> ?(.*)<br><br>$/;
        separator = "\n";
      }
      titleReg = /<h1 .*?>(.*)\n?<\/h1>/;
      numberOfBroken = 0;
      thread = {
        res: []
      };
      gotTitle = false;
      resCount = resLength != null ? resLength : 0;
      ref = text.split(separator);
      for (i = 0, len = ref.length; i < len; i++) {
        line = ref[i];
        title = gotTitle ? false : titleReg.exec(line);
        regRes = reg.exec(line);
        if (title) {
          thread.title = decodeCharReference(title[1]);
          thread.title = removeNeedlessFromTitle(thread.title);
          gotTitle = true;
        } else if (regRes) {
          while (++resCount < +regRes[1]) {
            thread.res.push({
              name: "あぼーん",
              mail: "あぼーん",
              message: "あぼーん",
              other: "あぼーん"
            });
          }
          thread.res.push({
            name: regRes[3],
            mail: regRes[2] || "",
            message: regRes[5],
            other: regRes[4]
          });
        }
      }
      if (thread.res.length > 0 && thread.res.length > numberOfBroken) {
        return thread;
      }
      return null;
    }

  };

  var ThreadSearch = (function() {
    var _Class, _parse;

    _Class = class {
      constructor(query, protocol1) {
        this.query = query;
        this.protocol = protocol1;
        return;
      }

      /*
      return ({url, key, subject, resno, server, ita}) ->
      urlProtocol = getProtocol(url)
      boardUrl = new URL("#{urlProtocol}//#{server}/#{ita}/")
      try
        boardTitle = await askBoardTitleSolver(boardUrl)
      catch
        boardTitle = ""
      return {
        url: setProtocol(url, protocol)
        createdAt: stampToDate(key)
        title: decodeCharReference(subject)
        resCount: +resno
        boardUrl: boardUrl.href
        boardTitle
        isHttps: (protocol is "https:")
      }
      */
      async _read(count) {
        var body, parser, result, rss, status;
        //{status, body} = await new Request("GET", "https://dig.5ch.net/?keywords=#{encodeURIComponent(@query)}&maxResult=#{count}&json=1",
        ({status, body} = (await new Request("GET", `https://ff5ch.syoboi.jp/?q=${encodeURIComponent(this.query)}&alt=rss`, {
          cache: false
        }).send()));
        if (status !== 200) {
          throw new Error("検索の通信に失敗しました");
        }
        try {
          parser = new DOMParser();
          rss = parser.parseFromString(body, "application/xml");
          result = Array.from(rss.T("item"));
        } catch (error) {
          //{result} = JSON.parse(body)
          throw new Error("検索のJSONのパースに失敗しました");
        }
        return Promise.all(result.map(_parse(this.protocol)));
      }

      read() {
        if (this.loaded === "None") {
          this.loaded = "Big";
          return this._read();
        }
        return [];
      }

    };

    _Class.prototype.loaded = "None";

    _Class.prototype.loaded20 = null;

    _parse = function(protocol) {
      return async function(item) {
        var boardTitle, boardUrl, m, title, url;
        url = item.T("guid")[0].textContent;
        title = decodeCharReference(item.T("title")[0].textContent);
        m = title.match(/\((\d+)\)$/);
        title = title.replace(/\(\d+\)$/, "");
        boardUrl = (new app.URL.URL(url)).toBoard();
        try {
          boardTitle = (await ask(boardUrl));
        } catch (error) {
          boardTitle = "";
        }
        return {
          url: setProtocol(url, protocol),
          createdAt: Date.parse(item.T("pubDate")[0].textContent),
          title,
          resCount: m != null ? m[1] : 0,
          boardUrl: boardUrl.href,
          boardTitle,
          isHttps: protocol === "https:"
        };
      };
    };

    return _Class;

  }).call(window);

  /*
  if @loaded is "None"
    @loaded = "Small"
    @loaded20 = @_read(20)
    return @loaded20
  if @loaded is "Small"
    @loaded = "Big"
    return _getDiff(await @loaded20, await @_read(500))
  return []
  */

  /**
  @class WriteHistory
  @static
  */
  /**
  @method recoveryOfDate
  @param {Object} db
  @param {Object} tx
  @return {Promise}
  @private
  */
  var DB_VERSION$2, _openDB$1, _recoveryOfDate$1;

  DB_VERSION$2 = 2;

  _openDB$1 = function() {
    return new Promise((resolve, reject) => {
      var req;
      req = indexedDB.open("WriteHistory", DB_VERSION$2);
      req.onerror = reject;
      req.onupgradeneeded = ({
          target: {
            result: db,
            transaction: tx
          },
          oldVersion: oldVer
        }) => {
        var objStore;
        if (oldVer < 1) {
          objStore = db.createObjectStore("WriteHistory", {
            keyPath: "id",
            autoIncrement: true
          });
          objStore.createIndex("url", "url", {
            unique: false
          });
          objStore.createIndex("res", "res", {
            unique: false
          });
          objStore.createIndex("title", "title", {
            unique: false
          });
          objStore.createIndex("date", "date", {
            unique: false
          });
          tx.oncomplete = function() {
            resolve(db);
          };
        }
        if (oldVer === 1) {
          _recoveryOfDate$1(db, tx);
          tx.oncomplete = function() {
            resolve(db);
          };
        }
      };
      req.onsuccess = function({
          target: {
            result: db
          }
        }) {
        resolve(db);
      };
    });
  };

  /**
  @method add
  @param {Object}
  @param {String} [url]
  @param {Number} [res]
  @param {String} [title]
  @param {String} [name]
  @param {String} [mail]
  @param {String} [inputName]
  @param {String} [inputMail]
  @param {String} [message]
  @param {Number} [date]
  @return {Promise}
  */
  var add$2 = async function({url, res, title, name, mail, inputName = null, inputMail = null, message, date}) {
    var db, e, req;
    if (app.assertArg("WriteHistory.add", [[url, "string"], [res, "number"], [title, "string"], [name, "string"], [mail, "string"], [inputName, "string", true], [inputMail, "string", true], [message, "string"], [date, "number"]])) {
      throw new Error("書込履歴に追加しようとしたデータが不正です");
    }
    try {
      db = (await _openDB$1());
      req = db.transaction("WriteHistory", "readwrite").objectStore("WriteHistory").add({
        url,
        res,
        title,
        name,
        mail,
        input_name: inputName != null ? inputName : name,
        input_mail: inputMail != null ? inputMail : mail,
        message,
        date
      });
      await indexedDBRequestToPromise(req);
    } catch (error) {
      e = error;
      app.log("error", "WriteHistory.add: データの格納に失敗しました");
      throw new Error(e);
    }
  };

  /**
  @method remove
  @param {String} url
  @param {Number} res
  @return {Promise}
  */
  var remove$3 = async function(url, res) {
    var data, db, e, req, store;
    if (app.assertArg("WriteHistory.remove", [[url, "string"], [res, "number"]])) {
      return Promise.reject();
    }
    try {
      db = (await _openDB$1());
      store = db.transaction("WriteHistory", "readwrite").objectStore("WriteHistory");
      req = store.index("url").getAll(IDBKeyRange.only(url));
      ({
        target: {
          result: data
        }
      } = (await indexedDBRequestToPromise(req)));
      await Promise.all(data.map(async function(datum) {
        if (datum.res === res) {
          req = store.delete(datum.id);
          await indexedDBRequestToPromise(req);
        }
      }));
    } catch (error) {
      e = error;
      app.log("error", "WriteHistory.remove: トランザクション中断");
      throw new Error(e);
    }
  };

  /**
  @method get
  @param {Number} offset
  @param {Number} limit
  @return {Promise}
  */
  var get$7 = function(offset = -1, limit = -1) {
    if (app.assertArg("WriteHistory.get", [[offset, "number"], [limit, "number"]])) {
      return Promise.reject();
    }
    return _openDB$1().then(function(db) {
      return new Promise(function(resolve, reject) {
        var advanced, histories, req;
        req = db.transaction("WriteHistory").objectStore("WriteHistory").index("date").openCursor(null, "prev");
        advanced = false;
        histories = [];
        req.onsuccess = function({
            target: {
              result: cursor
            }
          }) {
          var value;
          if (cursor && (limit === -1 || histories.length < limit)) {
            if (!advanced) {
              advanced = true;
              if (offset !== -1) {
                cursor.advance(offset);
                return;
              }
            }
            value = cursor.value;
            value.isHttps = isHttps(value.url);
            histories.push(value);
            cursor.continue();
          } else {
            resolve(histories);
          }
        };
        req.onerror = function(e) {
          app.log("error", "WriteHistory.get: トランザクション中断");
          reject(e);
        };
      });
    });
  };

  /**
  @method getByUrl
  @param {String} url
  @return {Promise}
  */
  var getByUrl = async function(url) {
    var db, e, req, res;
    if (app.assertArg("WriteHistory.getByUrl", [[url, "string"]])) {
      throw new Error("書込履歴を取得しようとしたデータが不正です");
    }
    try {
      db = (await _openDB$1());
      req = db.transaction("WriteHistory").objectStore("WriteHistory").index("url").getAll(IDBKeyRange.only(url));
      res = (await indexedDBRequestToPromise(req));
    } catch (error) {
      e = error;
      app.log("error", "WriteHistory.remove: トランザクション中断");
      throw new Error(e);
    }
    return res.target.result;
  };

  /**
  @method getAll
  @return {Promise}
  */
  var getAll$2 = async function() {
    var db, e, req, res;
    try {
      db = (await _openDB$1());
      req = db.transaction("WriteHistory").objectStore("WriteHistory").getAll();
      res = (await indexedDBRequestToPromise(req));
    } catch (error) {
      e = error;
      app.log("error", "WriteHistory.getAll: トランザクション中断");
      throw new Error(e);
    }
    return res.target.result;
  };

  /**
  @method count
  @return {Promise}
  */
  var count$1 = async function() {
    var db, e, req, res;
    try {
      db = (await _openDB$1());
      req = db.transaction("WriteHistory").objectStore("WriteHistory").count();
      res = (await indexedDBRequestToPromise(req));
    } catch (error) {
      e = error;
      app.log("error", "WriteHistory.count: トランザクション中断");
      throw new Error(e);
    }
    return res.target.result;
  };

  /**
  @method clear
  @param {Number} offset
  @return {Promise}
  */
  var clear$2 = function(offset = -1) {
    if (app.assertArg("WriteHistory.clear", [[offset, "number"]])) {
      return Promise.reject();
    }
    return _openDB$1().then(function(db) {
      return new Promise(function(resolve, reject) {
        var advanced, req;
        req = db.transaction("WriteHistory", "readwrite").objectStore("WriteHistory").openCursor();
        advanced = false;
        req.onsuccess = function({
            target: {
              result: cursor
            }
          }) {
          if (cursor) {
            if (!advanced) {
              advanced = true;
              if (offset !== -1) {
                cursor.advance(offset);
                return;
              }
            }
            cursor.delete();
            cursor.continue();
          } else {
            resolve();
          }
        };
        req.onerror = function(e) {
          app.log("error", "WriteHistory.clear: トランザクション中断");
          reject(e);
        };
      });
    });
  };

  /**
  @method clearRange
  @param {Number} day
  @return {Promise}
  */
  var clearRange$1 = async function(day) {
    var dayUnix, db, keys, req, store;
    if (app.assertArg("WriteHistory.clearRange", [[day, "number"]])) {
      return Promise.reject();
    }
    dayUnix = Date.now() - day * 24 * 60 * 60 * 1000;
    try {
      db = (await _openDB$1());
      store = db.transaction("WriteHistory", "readwrite").objectStore("WriteHistory");
      req = store.index("date").getAllKeys(IDBKeyRange.upperBound(dayUnix, true));
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
      app.log("error", "WriteHistory.clearRange: トランザクション中断");
      throw new Error(e);
    }
  };

  _recoveryOfDate$1 = function(db, tx) {
    return new Promise(function(resolve, reject) {
      var req, unixTime201710;
      unixTime201710 = 1506783600; // 2017/10/01 0:00:00
      req = tx.objectStore("WriteHistory").index("date").openCursor(IDBKeyRange.lowerBound(unixTime201710, true));
      req.onsuccess = function({
          target: {
            result: cursor
          }
        }) {
        var date;
        if (cursor) {
          if (cursor.value.res > 1) {
            date = new Date(+cursor.value.date);
            date.setMonth(date.getMonth() - 1);
            cursor.value.date = date.valueOf();
            cursor.update(cursor.value);
          }
          cursor.continue();
        } else {
          resolve();
        }
      };
      req.onerror = function(e) {
        app.log("error", "WriteHistory._recoveryOfDate: トランザクション中断");
        reject(e);
      };
    });
  };

  var WriteHistory = /*#__PURE__*/Object.freeze({
    add: add$2,
    remove: remove$3,
    get: get$7,
    getByUrl: getByUrl,
    getAll: getAll$2,
    count: count$1,
    clear: clear$2,
    clearRange: clearRange$1
  });

  exports.BBSMenu = BBSMenu;
  exports.Board = Board$1;
  exports.BoardTitleSolver = BoardTitleSolver;
  exports.Bookmark = Bookmark;
  exports.BookmarkEntryList = BookmarkEntryList;
  exports.BrowserBookmarkEntryList = BrowserBookmarkEntryList;
  exports.Cache = Cache$1;
  exports.ContextMenus = ContextMenus;
  exports.DOMData = DOMData;
  exports.History = History;
  exports.HTTP = HTTP;
  exports.ImageReplaceDat = ImageReplaceDat;
  exports.NG = NG;
  exports.Notification = Notification$1;
  exports.ReadState = ReadState;
  exports.ReplaceStrTxt = ReplaceStrTxt;
  exports.Thread = Thread$1;
  exports.ThreadSearch = ThreadSearch;
  exports.URL = URL$1;
  exports.util = util;
  exports.Util = Util;
  exports.WriteHistory = WriteHistory;

}(this.app = this.app || {}));
