<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/
// インデックスページ用のルーティング
Route::get('/', 'PostsController@index')->name('top');

// 投稿表示用のルーティング

Route::resource('posts', 'PostsController', ['only' => ['create', 'store', 'show', 'edit', 'update', 'destroy']]);

// コメント投稿用のルーティング
Route::resource('comments', 'CommentsController', ['only' => ['store']]);
