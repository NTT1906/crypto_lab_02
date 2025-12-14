#include <iostream>
#define BI_BIT 576
#include "bigint.h"
#include <string>

// Bài 4: Chữ ký ElGamal
int main(int argc, char* argv[]) {
	if (argc != 3) return 1;
	if (!freopen(argv[1], "r", stdin)) return 1;
	if (!freopen(argv[2], "w", stdout)) return 1;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	bui p = read_bui_le();
	bui g = read_bui_le();
	bui y = read_bui_le(); // public key
	bui m = read_bui_le(); // message
	bui r = read_bui_le();
	bui h = read_bui_le();
	bui gm = mr_pow_mod(g, m, p); // g^m mod p
	bui yr = mr_pow_mod(y, r, p); // y^r mod p
	bui rh = mr_pow_mod(r, h, p); // r^h mod p
	bui yrrh = mod_native(mul(yr, rh), p); // (y^r * r^h) mod p
	std::cout << (cmp(gm, yrrh) == 0 ? "1\n" : "0\n");
	return 0;
}