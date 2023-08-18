<?php

/*
Plugin Name: テスト用プラグイン
Plugin URI: https://example.com
Description: テスト用プラグインです。
Version: 1.0
Author: テスト太郎
Author URI: ttps://example.com
*/

add_action('admin_notices', function() {

  echo <<<EOF

<div class="notice notice-info is-dismissible">
	<p>これはテスト用プラグインです。</p>
</div>

EOF;
	
});