#!/bin/bash

function main {
    i=0
    files_number=0
    echo ""
    echo "·~-~·~-~·~-~·~-~·~-~·~-~·  ¡¡¡ MATEMÁTICA DISCRETA II !!!  ·~-~·~-~·~-~·~-~·~-~·~-~·~"
    echo ""
    echo "·~-~·~-~·~-~·~-~·~-~·-~·-~·   ALGORITMO DE EDMONDS-KARP  ·~-~·~-~·~-~·~-~·~-~·~·~-~·~"
    echo ""
    for example in examples/debe_dar*; do
      OUTPUT=$(./main < $example | grep 'maximal')
      FLOWVALUE=$(echo "$example" | cut -d"_" -f3)
      EXPECTED="Valor del flujo maximal: $FLOWVALUE"
      if [ "$OUTPUT" != "$EXPECTED" ]; then
        echo -e "\e[01;31mERROR!\e[0m"
        echo "Maximal flow$(echo $EXPECTED | cut -d":" -f2) was expected but it was$(echo $OUTPUT | cut -d":" -f2)"
      fi
      if [ "$OUTPUT" == "$EXPECTED" ]; then
        echo -e "\e[01;32mPASS!\e[0m"
	let i=i+1
      fi
      let files_number=files_number+1
    done
    echo ""
    p=$((100 / $files_number))
    echo "Tests al $(($i * p))%"
    echo ""
    make clean > /dev/null
}

make > /dev/null
main

exit 0
