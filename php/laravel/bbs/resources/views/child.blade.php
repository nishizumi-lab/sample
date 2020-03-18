@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
@@parent

<p>ここはメインのサイドバーに追加される</p>
@endsection

@section('content')
<p>ここが本文のコンテンツ</p>
@endsection
