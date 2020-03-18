<?php

use Illuminate\Database\Seeder;
use App\Post;
use App\Comment;

class PostsTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // Factoryのテストデータを登録（投稿は23件、コメントは各投稿あたり4件）登録
        factory(Post::class, 23)
            ->create()
            ->each(function ($post) {
                $comments = factory(App\Comment::class, 4)->make();
                $post->comments()->saveMany($comments);
            });
    }
}