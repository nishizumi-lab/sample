<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Post;

class PostsController extends Controller
{
    // インデックス用：投稿を作成日時の降順で取得し、posts.indexにデータを渡してビューを生成
    public function index()
    {
        // ページネーションを追加（1ページ10件まで投稿表示）
        // 投稿のリストを取得した時に、紐づくコメントを読み込む(取得した投稿数だけコメント数をカウントさせない:n+1問題)
        // Laravelではwithメソッドで解決可能
        $posts = Post::with(['comments'])->orderBy('created_at', 'desc')->paginate(10);

        // コントローラのメソッドでビューを返す
        // 第一引数にビューの名前、第二引数にビューに渡したい値（連想配列）を設定
        return view('posts.index', compact('posts'));
        // compact('posts') は ['posts' => $posts]);と同じ
    }

    // 投稿画面用：投稿を追加した後は、トップページにリダイレクト
    public function create()
    {
        return view('posts.create');
    }

    public function store(Request $request)
    {
        $params = $request->validate([
            'title' => 'required|max:50',
            'body' => 'required|max:2000',
        ]);
    
        Post::create($params);
    
        return redirect()->route('top');
    }

    // 投稿の詳細表示
    public function show($post_id)
    {
        // DBよりURIパラメータと同じIDを持つPostの情報を取得
        $post = Post::findOrFail($post_id);

        return view('posts.show', [
            'post' => $post,
        ]);
    }

    // 編集用
    public function edit($post_id)
    {
        // DBよりURIパラメータと同じIDを持つPostの情報を取得
        $post = Post::findOrFail($post_id);

        return view('posts.edit', [
            'post' => $post,
        ]);
    }

    // 更新用
    public function update($post_id, Request $request)
    {
        $params = $request->validate([
            'title' => 'required|max:50',
            'body' => 'required|max:2000',
        ]);

        // DBよりURIパラメータと同じIDを持つPostの情報を取得
        $post = Post::findOrFail($post_id);
        $post->fill($params)->save();

        return redirect()->route('posts.show', ['post' => $post]);
    }

    // 投稿削除
    public function destroy($post_id)
    {
        // DBよりURIパラメータと同じIDを持つPostの情報を取得
        $post = Post::findOrFail($post_id);

        \DB::transaction(function () use ($post) {
            $post->comments()->delete();
            $post->delete();
        });

        return redirect()->route('top');
    }
}