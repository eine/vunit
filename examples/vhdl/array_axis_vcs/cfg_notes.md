# add_array_util
# add_com
# add_osvvm
# add_random
# add_verification_components

---

# add_compile_option(name, value, allow_empty=False)
# add_external_library(library_name, path, vhdl_standard=None)
# add_library(library_name, vhdl_standard=None)
# add_source_file(file_name, library_name, preprocessors=None, include_dirs=None, defines=None, vhdl_standard=None, no_parse=False, file_type=None)
# add_source_files(pattern, library_name, preprocessors=None, include_dirs=None, defines=None, allow_empty=False, vhdl_standard=None, no_parse=False, file_type=None)

# enable_check_preprocessing
# enable_location_preprocessing(additional_subprograms=None, exclude_subprograms=None)

# get_compile_order(source_files=None)
# get_implementation_subset(source_files)
# get_source_file(file_name, library_name=None)
# get_source_files(pattern='*', library_name=None, allow_empty=False)

# library(library_name)

# main(post_run=None)

# set_compile_option(name, value, allow_empty=False)
# set_generic(name, value, allow_empty=False)
# set_parameter(name, value, allow_empty=False)
# set_sim_option(name, value, allow_empty=False)

# Library
# add_source_file(file_name, preprocessors=None, include_dirs=None, defines=None,
# add_source_files(pattern, preprocessors=None, include_dirs=None, defines=None, allow_empty=False, vhdl_standard=None, no_parse=False, file_type=None)
# entity(name)
# get_source_file(file_name)
# get_source_files(pattern='*', allow_empty=False)
# get_test_benches(pattern='*', allow_empty=False)
# module(name)
# name
# set_compile_option(name, value, allow_empty=False)
# set_generic(name, value, allow_empty=False)
# set_parameter(name, value, allow_empty=False)
# set_sim_option(name, value, allow_empty=False)
# test_bench(name)

# SourceFileList
# add_compile_option(name, value)
# add_dependency_on(source_file)
# set_compile_option(name, value)

# SourceFile
# add_compile_option(name, value)
# add_dependency_on(source_file)
# get_compile_option(name)
# library
# name
# set_compile_option(name, value)
# vhdl_standard

# TestBench
# add_config(name, generics=None, parameters=None, pre_config=None, post_check=None, sim_options=None)
# get_tests(pattern='*')
# library
# name
# scan_tests_from_file(file_name)
# set_generic(name, value)
# set_parameter(name, value)
# set_post_check(value)
# set_pre_config(value)
# set_sim_option(name, value)
# test(name)

# Test
# add_config(name, generics=None, parameters=None, pre_config=None, post_check=None, sim_options=None)
# name
# set_generic(name, value)
# set_parameter(name, value)
#  set_post_check(value)
# set_pre_config(value)
# set_sim_option(name, value)
