<?php

use Faker\Generator as Faker;

$factory->define(App\Comment::class, function (Faker $faker) {
    return [
        'body' => "千早ぶる神代もきかず龍田川からくれなゐに水くくるとは",
    ];
});