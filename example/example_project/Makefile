SRC_FILES  = src/main.c src/example_src_1.c
INCLUDES   = -I./include
EXECUTABLE = target/example_program
FLAGS      = -Wall -Wextra -pedantic -std=c99

all :
	gcc $(FLAGS) $(INCLUDES) $(SRC_FILES) -o $(EXECUTABLE)

clean :
	rm -rf ./target/* $(EXECUTABLE)
