#include <iostream>
#define BI_BIT 512
#include "bigint.h"
#include <string>

// Bài 2: Diffie–Hellman
int main(int argc, char* argv[]) {
	if (argc != 3) return 1;
	if (!freopen(argv[1], "r", stdin)) return 1;
	if (!freopen(argv[2], "w", stdout)) return 1;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	bui p = read_bui_le();
	bui g = read_bui_le();
	bui a = read_bui_le();
	bui b = read_bui_le();
	bui A = pow_mod(g, a, p); // g^a mod p
	bui B = pow_mod(g, b, p); // g^b mod p
	bui K = pow_mod(A, b, p); // g^ab mod p = (g^a)^b mod p = A^b mod p
	std::cout << str_reverse(bui_to_hex(A, true)) << '\n';
	std::cout << str_reverse(bui_to_hex(B, true)) << '\n';
	std::cout << str_reverse(bui_to_hex(K, true)) << '\n';
	return 0;
}