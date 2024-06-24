#!/bin/bash
rm -f output.bin
rm -f memray-flamegraph-output.html
python -m memray run -o output.bin --aggregate mem_updates.py 
python -m memray flamegraph output.bin
firefox memray-flamegraph-output.html
