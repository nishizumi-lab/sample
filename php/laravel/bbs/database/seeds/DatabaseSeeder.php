<?php

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // PostsTableSeeder（投稿のテストデータ登録）を呼び出して、シーディングコマンドで実行されるようにする
        $this->call(PostsTableSeeder::class);
    }
}

