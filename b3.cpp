#include <iostream>
#define BI_BIT 512
#include "bigint.h"
#include <string>

// Bài 3: ElGamal mã hóa/giải mã
int main(int argc, char* argv[]) {
	if (argc != 3) return 1;
	if (!freopen(argv[1], "r", stdin)) return 1;
	if (!freopen(argv[2], "w", stdout)) return 1;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	bui p = read_bui_le();
	bui g = read_bui_le();
	bui x = read_bui_le(); 
	bui c1 = read_bui_le();
	bui c2 = read_bui_le();
	bui s_inv;
	bui h = mr_pow_mod(g, x, p); // h = g^x mod p
	std::cout << str_reverse(bui_to_hex(h, true)) << '\n';
	bui s = pow_mod(c1, x, p); // s = c1^x mod p
	mod_inverse(s, p, s_inv); // s_inv = s^(-1) mod p
	bui m = mod_native(mul(c2, s_inv), p); // m - c2 * s_inv mod p
	std::cout << str_reverse(bui_to_hex(m, true)) << '\n';
	return 0;
}