<?php

use Faker\Generator as Faker;

$factory->define(App\Post::class, function (Faker $faker) {
    return [
        'title' => '徒然草',
        'body' => "徒然（つれづれ）なるままに、日ぐらし、硯（すずり）に向かいて、心にうつりゆくよしなし事（ごと）をそこはかとなく書きつくれば怪しうこそ物狂（ものぐる）おしけれ",
    ];
});