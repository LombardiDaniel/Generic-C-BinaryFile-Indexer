indexer: main_rendered.cpp utils.cpp
	g++ -Wall -pedantic -O2 -Wno-unused-result main_rendered.cpp -o indexer -std=c++11

# main: main.cpp utils.cpp
# 	g++ -Wall -pedantic -O2 -Wno-unused-result main.cpp -o indexer -std=c++11

utils: utils.cpp
	g++ -Wall -pedantic -O2 -Wno-unused-result utils.cpp -o utils -std=c++11

asm: main.cpp
	g++ -Wall -pedantic -O0 -Wno-unused-result -g main.cpp -o main.asm -std=c++11 -S
