#include <stdio.h>
struct Character {
    char name[64];
    int hp;
    void (*action)(struct Character* src, struct Character* dest, int val);
};
typedef struct Character Ch;
void punch(Ch* src, Ch* dest, int val) {
    printf("%s のパンチ！ %s に %d のダメージ！\n", src->name, dest->name, val);
    dest->hp -= val;
}
void magic(Ch* src, Ch* dest, int val) {
    int damage = (dest->hp * 4) / 10; // 3割ダメージ
    printf("%s の火炎魔法！ %s は %d のダメージ！\n", src->name, dest->name, damage);
    dest->hp -= damage;
}
int main() {
    Ch planc = { "ぷらんく", 17, punch };
    Ch firerat = { "炎のネズミ", 13, magic };
    for (int i = 0; i < 20; i++) {
        printf("=== %d ターン目 ===\n", i);
        planc.action( &planc, &firerat, 5);
        firerat.action( &firerat, &planc, 3);
        printf("%s の体力は %d\n", planc.name, planc.hp);
        printf("%s の体力は %d\n", firerat.name, firerat.hp);
        if (planc.hp <= 0 || firerat.hp <= 0) break; // END
    }
}