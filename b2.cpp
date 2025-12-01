#include <iostream>
#define BI_BIT 512
#include "bigint.h"
#include <string>
using namespace std;

// Bài 2: Diffie–Hellman
int main(int argc, char* argv[]) {
	if (argc != 3) return 1;
	if (!freopen(argv[1], "r", stdin)) return 1;
	if (!freopen(argv[2], "w", stdout)) return 1;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	return 0;
}