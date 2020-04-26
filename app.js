var app = (function (exports) {
  'use strict';

  function deepCopy(src) {
      if (typeof src !== "object" || src === null) {
          return src;
      }
      const copy = Array.isArray(src) ? [] : {};
      for (const key in src) {
          copy[key] = deepCopy(src[key]);
      }
      return copy;
  }
  function replaceAll(str, before, after) {
      let i = str.indexOf(before);
      if (i === -1)
          return str;
      let result = str.slice(0, i) + after;
      let j = str.indexOf(before, i + before.length);
      while (j !== -1) {
          result += str.slice(i + before.length, j) + after;
          i = j;
          j = str.indexOf(before, i + before.length);
      }
      return result + str.slice(i + before.length);
  }
  function escapeHtml(str) {
      return replaceAll(replaceAll(replaceAll(replaceAll(replaceAll(str, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), '"', "&quot;"), "'", "&apos;");
  }
  function safeHref(url) {
      return /^https?:\/\//.test(url) ? url : "/view/empty.html";
  }
  function clipboardWrite(str) {
      const $textarea = $__("textarea");
      $textarea.value = str;
      document.body.addLast($textarea);
      $textarea.select();
      document.execCommand("copy");
      $textarea.remove();
  }

  const logLevels = new Set(["log", "debug", "info", "warn", "error"]);
  async function criticalError(message) {
      new Notification("深刻なエラーが発生したのでread.crxを終了します", { body: `詳細 : ${message}` });
      const { id } = await parent.browser.tabs.getCurrent();
      parent.browser.tabs.remove(id);
  }
  function log(level, ...data) {
      if (!logLevels.has(level)) {
          log("error", "app.log: 引数levelが不正な値です", level);
          return;
      }
      console[level](...data);
  }
  function assertArg(name, rules) {
      let isError = false;
      for (const [val, type, canbeNull] of rules) {
          if (!(canbeNull && (val === null || val === void 0)) &&
              typeof val !== type) {
              log("error", `${name}: 不正な引数(予期していた型: ${type}, 受け取った型: ${typeof val})`, deepCopy(val));
              isError = true;
          }
      }
      return isError;
  }

  class Callbacks {
      constructor(config = {}) {
          this._callbackStore = new Set();
          this._latestCallArg = null;
          this.wasCalled = false;
          this._config = config;
      }
      add(callback) {
          if (!this._config.persistent && this._latestCallArg) {
              callback(...deepCopy(this._latestCallArg));
          }
          else {
              this._callbackStore.add(callback);
          }
      }
      remove(callback) {
          if (this._callbackStore.has(callback)) {
              this._callbackStore.delete(callback);
          }
          else {
              log("error", "app.Callbacks: 存在しないコールバックを削除しようとしました。");
          }
      }
      call(...arg) {
          if (!this._config.persistent && this._latestCallArg) {
              log("error", "app.Callbacks: persistentでないCallbacksが複数回callされました。");
              return;
          }
          this.wasCalled = true;
          this._latestCallArg = deepCopy(arg);
          const tmpCallbackStore = new Set(this._callbackStore);
          for (const callback of tmpCallbackStore) {
              if (this._callbackStore.has(callback)) {
                  callback(...deepCopy(arg));
              }
          }
          if (!this._config.persistent) {
              this._callbackStore.clear();
          }
      }
      destroy() {
          this._callbackStore.clear();
      }
  }

  function defer() {
      return new Promise((resolve) => {
          setTimeout(resolve, 100);
      });
  }
  function wait(ms) {
      return new Promise((resolve) => {
          setTimeout(resolve, ms);
      });
  }
  function wait5s() {
      return new Promise((resolve) => {
          setTimeout(resolve, 5 * 1000);
      });
  }
  function waitAF() {
      return new Promise((resolve) => {
          requestAnimationFrame(resolve);
      });
  }

  class Message {
      constructor() {
          this._listenerStore = new Map();
          this._bc = new BroadcastChannel(Message.CHANNEL_NAME);
          this._bc.on("message", ({ data: { type, message } }) => {
              this._fire(type, message);
          });
      }
      async _fire(type, message) {
          const msg = deepCopy(message);
          await defer();
          if (this._listenerStore.has(type)) {
              this._listenerStore.get(type).call(msg);
          }
      }
      send(type, message = {}) {
          this._fire(type, message);
          this._bc.postMessage({ type, message });
      }
      on(type, listener) {
          if (!this._listenerStore.has(type)) {
              this._listenerStore.set(type, new Callbacks({ persistent: true }));
          }
          this._listenerStore.get(type).add(listener);
      }
      off(type, listener) {
          if (this._listenerStore.has(type)) {
              this._listenerStore.get(type).remove(listener);
          }
      }
  }
  Message.CHANNEL_NAME = "readcrx";
  var message = new Message();

  class LocalStorage {
      static async get(key, isJson = false) {
          const val = await browser.storage.local.get(key);
          if (!val[key])
              return null;
          if (isJson) {
              return JSON.parse(val[key]);
          }
          return val[key];
      }
      static async getAll() {
          return await browser.storage.local.get(null);
      }
      static async set(key, val, isJson = false) {
          const obj = {};
          obj[key] = isJson ? JSON.stringify(val) : val;
          await browser.storage.local.set(obj);
      }
      static async del(key) {
          await browser.storage.local.remove(key);
      }
  }

  class Config {
      constructor() {
          this._cache = new Map();
          const ready = new Callbacks();
          this.ready = ready.add.bind(ready);
          (async () => {
              if (this._cache.size > 0) {
                  return;
              }
              const res = await LocalStorage.getAll();
              for (const [key, val] of Object.entries(res)) {
                  if (key.startsWith("config_") &&
                      (typeof val === "string" || typeof val === "number")) {
                      this._cache.set(key, val.toString());
                  }
              }
              ready.call();
          })();
          this._onChanged = (change, area) => {
              if (area !== "local") {
                  return;
              }
              for (const [key, val] of Object.entries(change)) {
                  if (!key.startsWith("config_"))
                      continue;
                  const { newValue } = val;
                  if (typeof newValue === "string") {
                      this._cache.set(key, newValue);
                      message.send("config_updated", {
                          key: key.slice(7),
                          val: newValue
                      });
                  }
                  else {
                      this._cache.delete(key);
                  }
              }
          };
          browser.storage.onChanged.addListener(this._onChanged);
      }
      get(key) {
          if (this._cache.has(`config_${key}`)) {
              return this._cache.get(`config_${key}`);
          }
          if (Config._default.has(key)) {
              return Config._default.get(key);
          }
          return null;
      }
      getAll() {
          const object = {};
          for (const [key, val] of Config._default) {
              object[`config_${key}`] = val;
          }
          /*
            // ES2019
            Object.assign(object, Object.fromEntries(this._cache))
          */
          for (const [key, val] of this._cache) {
              object[key] = val;
          }
          return object;
      }
      isOn(key) {
          return this.get(key) === "on";
      }
      async set(key, val) {
          if (typeof key !== "string" ||
              !(typeof val === "string" || typeof val === "number")) {
              log("error", "app.Config::setに不適切な値が渡されました", arguments);
              throw new Error("app.Config::setに不適切な値が渡されました");
          }
          await LocalStorage.set(`config_${key}`, val);
      }
      async del(key) {
          if (assertArg("app.Config::del", [[key, "string"]])) {
              throw new Error("app.Config::delにstring以外の値が渡されました");
          }
          await LocalStorage.del(`config_${key}`);
      }
      destroy() {
          this._cache.clear();
          browser.storage.onChanged.removeListener(this._onChanged);
      }
  }
  Config._default = new Map([
      ["layout", "pane-3"],
      ["theme_id", "default"],
      ["default_scrollbar", "off"],
      ["write_window_x", "0"],
      ["write_window_y", "0"],
      ["always_new_tab", "on"],
      ["button_change_netsc_newtab", "off"],
      ["button_change_scheme_newtab", "off"],
      ["open_all_unread_lazy", "on"],
      ["enable_link_with_res_number", "on"],
      ["bookmark_sort_save_type", "none"],
      ["dblclick_reload", "on"],
      ["auto_load_second", "0"],
      ["auto_load_second_board", "0"],
      ["auto_load_second_bookmark", "0"],
      ["auto_load_all", "off"],
      ["auto_load_move", "off"],
      ["auto_bookmark_notify", "on"],
      ["manual_image_load", "off"],
      ["image_blur", "off"],
      ["image_blur_length", "4"],
      ["image_blur_word", ".{0,5}[^ァ-ヺ^ー]グロ(?:[^ァ-ヺ^ー].{0,5}|$)|.{0,5}死ね.{0,5}"],
      ["image_width", "150"],
      ["image_height", "100"],
      ["audio_supported", "off"],
      ["audio_supported_ogg", "off"],
      ["audio_width", "320"],
      ["video_supported", "off"],
      ["video_supported_ogg", "off"],
      ["video_controls", "on"],
      ["video_width", "360"],
      ["video_height", "240"],
      ["hover_zoom_image", "off"],
      ["zoom_ratio_image", "200"],
      ["hover_zoom_video", "off"],
      ["zoom_ratio_video", "200"],
      ["image_height_fix", "on"],
      ["delay_scroll_time", "600"],
      ["expand_short_url", "none"],
      ["expand_short_url_timeout", "3000"],
      ["aa_font", "aa"],
      ["aa_min_ratio", "40"],
      ["popup_trigger", "click"],
      ["popup_delay_time", "0"],
      ["ngwords", "Title: 5ちゃんねるへようこそ\nTitle:【新着情報】5chブラウザがやってきた！"],
      ["ngobj", "[{\"type\":\"Title\",\"word\":\"5ちゃんねるへようこそ\"},{\"type\":\"Title\",\"word\":\"【新着情報】5chぶらうざがやってきた！\"}]"],
      ["chain_ng", "off"],
      ["chain_ng_id", "off"],
      ["chain_ng_id_by_chain", "off"],
      ["chain_ng_slip", "off"],
      ["chain_ng_slip_by_chain", "off"],
      ["display_ng", "off"],
      ["nothing_id_ng", "off"],
      ["nothing_slip_ng", "off"],
      ["how_to_judgment_id", "first_res"],
      ["repeat_message_ng_count", "0"],
      ["forward_link_ng", "off"],
      ["ng_id_expire", "none"],
      ["ng_id_expire_date", "0"],
      ["ng_id_expire_day", "0"],
      ["ng_slip_expire", "none"],
      ["ng_slip_expire_date", "0"],
      ["ng_slip_expire_day", "0"],
      ["reject_ng_rep", "off"],
      ["bookmark_show_dat", "on"],
      ["default_name", ""],
      ["default_mail", ""],
      ["no_history", "off"],
      ["no_writehistory", "off"],
      ["user_css", ""],
      ["bbsmenu", "https://menu.5ch.net/bbsmenu.html\nhttps://menu.2ch.sc/bbsmenu.html\nhttps://menu.open2ch.net/bbsmenu.html\n"],
      ["bbsmenu_update_interval", "7"],
      ["bbsmenu_option", ""],
      ["useragent", ""],
      ["format_2chnet", "html"],
      ["sage_flag", "on"],
      ["mousewheel_change_tab", "on"],
      ["image_replace_dat_obj", ""],
      ["image_replace_dat", "^https?:\\/\\/(?:www\\.youtube\\.com\\/watch\\?(?:.+&)?v=|youtu\\.be\\/)([\\w\\-]+).*\thttps://img.youtube.com/vi/$1/default.jpg\nhttp:\\/\\/(?:www\\.)?nicovideon?\\.jp\\/(?:(?:watch|thumb)(?:_naisho)?(?:\\?v=|\\/)|\\?p=)(?!am|fz)[a-z]{2}(\\d+)\thttp://tn-skr.smilevideo.jp/smile?i=$1\n\\.(png|jpe?g|gif|bmp|webp)([\\?#:].*)?$\t.$1$2"],
      ["replace_str_txt_obj", "[]"],
      ["replace_str_txt", ""]
  ]);

  ///<reference path="global.d.ts" />
  if (!frameElement) {
      exports.config = new Config();
  }
  const manifest = (async () => {
      if (!/^(?:chrome|moz)-extension:$/.test(location.protocol)) {
          throw new Error("manifest.jsonの取得に失敗しました");
      }
      try {
          const response = await fetch("/manifest.json");
          return await response.json();
      }
      catch (_a) { }
  })();
  async function boot(path, requirements, fn) {
      if (!fn) {
          fn = requirements;
          requirements = null;
      }
      // Chromeがiframeのsrcと無関係な内容を読み込むバグへの対応
      if (frameElement &&
          frameElement.src !== location.href) {
          location.href = frameElement.src;
          return;
      }
      if (location.pathname === path) {
          const htmlVersion = document.documentElement.dataset.appVersion;
          if ((await manifest).version !== htmlVersion) {
              location.reload(true);
              return;
          }
          const onload = () => {
              exports.config.ready(() => {
                  if (!requirements) {
                      fn();
                      return;
                  }
                  const modules = [];
                  for (const module of requirements) {
                      modules.push(parent.app[module]);
                  }
                  fn(...modules);
              });
          };
          // async関数のためDOMContentLoadedに間に合わないことがある
          if (document.readyState === "loading") {
              document.on("DOMContentLoaded", onload);
          }
          else {
              onload();
          }
      }
  }

  exports.manifest = manifest;
  exports.boot = boot;
  exports.Callbacks = Callbacks;
  exports.LocalStorage = LocalStorage;
  exports.message = message;
  exports.defer = defer;
  exports.wait = wait;
  exports.wait5s = wait5s;
  exports.waitAF = waitAF;
  exports.criticalError = criticalError;
  exports.log = log;
  exports.assertArg = assertArg;
  exports.deepCopy = deepCopy;
  exports.replaceAll = replaceAll;
  exports.escapeHtml = escapeHtml;
  exports.safeHref = safeHref;
  exports.clipboardWrite = clipboardWrite;

  return exports;

}({}));
