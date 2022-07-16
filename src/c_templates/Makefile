main.out: main.cpp
	g++ -Wall -pedantic -O2 -Wno-unused-result -g main.cpp -o main.out -std=c++11

asm: main.cpp
	g++ -Wall -pedantic -O0 -Wno-unused-result -g main.cpp -o main.asm -std=c++11 -S

clean:
	rm -r *.o *.asm *.out ./main.out.dSYM
