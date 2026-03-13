TARGET=main

CC?=gcc

CFLAGS+= -ansi -Werror -Wall -std=c99 -Wextra -Wdeclaration-after-statement -Wbad-function-cast -Wcast-qual -Wstrict-prototypes -Wmissing-declarations -Wmissing-prototypes -Wno-unused-parameter -Werror -pedantic -g

SOURCES=$(shell echo *.c)

VALGRING_FLAGS=--leak-check=full --show-reachable=yes

OBJECTS=$(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $^ -o $@ $(LDFLAGS)

valgrind:
	valgrind $(VALGRING_FLAGS) ./$(TARGET) < examples/debe_dar_512_c

clean:
	rm -f $(TARGET) $(OBJECTS)  *~ examples/*~

.PHONY: clean all
