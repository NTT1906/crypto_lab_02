#include <iostream>
#define BI_BIT 512
#include "bigint.h"
#include <string>
using namespace std;

int main(int argc, char* argv[]) {
	if (argc != 3) return 1;
	if (!freopen(argv[1], "r", stdin)) return 1;
	if (!freopen(argv[2], "w", stdout)) return 1;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	bui p = read_bui_le();
	bui n = read_bui_le();
	string line;
	vector<bui> U;
	U.reserve(n[BI_N - 1]);
	getline(cin, line);
	stringstream ss(line);
	string tok;
	while (ss >> tok) {
		U.push_back(bui_from_hex(normalize_hex_le_to_be(tok)));
	}
	bui g = read_bui_le();

	bui one = bui1();
	bui pm1 = p;
	sub_ip(pm1, one);

	MontgomeryReducer mr(p);

	for (auto &q : U) {
		bui e, r;
		divmod(pm1, q, e, r); // e = (p-1)/q
		// tính t = g^e mod p
		bui t = mr.pow(g, e);
		// bui t = pow_mod(g, e, p);
		if (cmp(t, mr.convertedOne) == 0) {
			cout << "0\n";
			return 0;
		}
	}
	cout << "1\n";
	return 0;
}