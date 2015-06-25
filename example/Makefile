mk_dir       := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

executable   := $(mk_dir)/target/test
test_log     := $(mk_dir)/target/test_results.log
cc           := gcc
flags        := -Wall -Wextra -pedantic -std=c99 -DTEST_LOG="$(test_log)"

src_files := \
	$(wildcard $(mk_dir)/src/*.c) \
	$(wildcard $(mk_dir)/tests/src/*.c)

header_files := \
	$(wildcard $(mk_dir)/include/*.h) \
	$(wildcard $(mk_dir)/tests/include/*.h)

includes := \
	-I$(mk_dir)/include \
	-I$(mk_dir)/tests/include

$(executable) : $(src_files) $(header_files)
	@echo "Building $(executable)"
	@mkdir -p $(dir $(executable))
	$(cc) $(flags) $(includes) $(src_files) -o $(executable)

test : $(executable)
	$(executable)
	cat $(test_log)

clean :
	rm -rf $(mk_dir)/target
