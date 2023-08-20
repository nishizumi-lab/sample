<?php

/*
Plugin Name: カスタム投稿プラグイン
Plugin URI: https://example.com
Description: カスタム投稿プラグインです。
Version: 1.0
Author: テスト太郎
Author URI: ttps://example.com
*/

function custom_post_type() {
    register_post_type('custom_post_type',
        array(
            'label' => 'カスタム投稿', //表示名
            'public'        => true, //公開状態
            'exclude_from_search' => false, // 検索対象に含めるか
            'show_ui' => true, // 管理画面に表示するか
            'show_in_menu' => true, // 管理画面のメニューに表示するか
            'menu_position' => 5, // 管理メニューの表示位置を指定
            'hierarchical' => true, // 階層構造を持たせるか
            'has_archive'   => true, // この投稿タイプのアーカイブを作成するか
            'supports' => array(
                'title',
                'editor',
                'comments',
                'excerpt',
                'thumbnail',
                'custom-fields',
                'post-formats',
                'page-attributes',
                'trackbacks',
                'revisions',
                'author'
            ), // 編集画面で使用するフィールド
        )
    );
}
add_action('init', 'custom_post_type', 1);