# Edmonds-Karp en Rust. Produce el binario 'main' para el test runner.
.PHONY: build clean

build:
	cargo build --release
	cp target/release/main main

clean:
	cargo clean
	rm -f main
