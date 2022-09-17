struct Character {
    char name[64];
    int hp;
    void (*action)(struct Character* src, struct Character* dest, int val);
};