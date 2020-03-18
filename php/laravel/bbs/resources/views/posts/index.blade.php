@extends('layout')

<!-- 投稿一覧を取得して表示 -->

@section('content')
<div class="container mt-4">
    <!-- 投稿作成画面へのリンク -->
    <div class="mb-4">
        <a href="{{ route('posts.create') }}" class="btn btn-primary">
            投稿の新規作成
        </a>
    </div>
    @foreach ($posts as $post)
    <div class="card mb-4">
        <div class="card-header">
            <a class="card-link" href="{{ route('posts.show', ['post' => $post]) }}">
                {{ $post->title }}
            </a>
        </div>
        <div class="card-body">
            <p class="card-text">
                <!-- 投稿の冒頭（200文字）を取得し改行あり表示 -->
                {!! nl2br(e(Str::limit($post->body, 200))) !!}
            </p>
        </div>
        <div class="card-footer">
            <span class="mr-2">
                投稿日時 {{ $post->created_at->format('Y.m.d') }}
            </span>

            @if ($post->comments->count())
            <span class="badge badge-primary">
                コメント数 {{ $post->comments->count() }}
            </span>
            @endif
        </div>
    </div>
    @endforeach
    <!-- ページネーション(1ページ、2ページ・・・)へのリンク -->
    <div class="d-flex justify-content-center mb-5">
        {{ $posts->links() }}
    </div>
</div>
@endsection