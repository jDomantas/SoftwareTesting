// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58063

#include <iostream>

void f(bool x = !(std::cout << "hi\n")) {}

int main() {
	f();
}

