CC         := gcc
FLAGS      := -Wall -Wextra -pedantic -std=c99

SRC_FILES  := $(wildcard src/*.c)
INCLUDES   := -Iinclude

EXECUTABLE := target/example_program

ifeq ($(MAKECMDGOALS),test)
  EXECUTABLE := target/test

  SRC_FILES  := $(filter-out %main.c,$(SRC_FILES))

  SRC_FILES  += tests/src/tests.c
  INCLUDES   += -Itests/include
endif

all, test :
	@echo "Building $(EXECUTABLE)"
	$(CC) $(FLAGS) $(INCLUDES) $(SRC_FILES) -o $(EXECUTABLE)

clean :
	rm -rf target/*
