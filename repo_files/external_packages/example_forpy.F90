program example_forpy
  use forpy_mod
  implicit none

  integer :: ierror
  type(tuple) :: args
  type(dict) :: kwargs
  type(module_py) :: mymodule
  type(object) :: return_value
  type(list) :: paths
  character(len=:), allocatable :: return_string

  ierror = forpy_initialize()

  ! Instead of setting the environment variable PYTHONPATH,
  ! we can add the current directory "." to sys.path
  ierror = get_sys_path(paths)
  ierror = paths%append(".")
  
  ierror = import_py(mymodule, "example_forpy")
  
  ! Python: 
  ! return_value = mymodule.print_args(12, "Hi", True, message="Hello world!")
  ierror = tuple_create(args, 3)
  ierror = args%setitem(0, 12)
  ierror = args%setitem(1, "Hi")
  ierror = args%setitem(2, .true.)
  
  ierror = dict_create(kwargs)
  ierror = kwargs%setitem("message", "Hello world!")
  
  ierror = call_py(return_value, mymodule, "print_args", args, kwargs)
  ! For call_py, args and kwargs are optional
  ! use call_py_noret to ignore the return value, E. g.:
  ! ierror = call_py_noret(mymodule, "print_args")

  ierror = cast(return_string, return_value)
  write(*,*) return_string

  call args%destroy
  call kwargs%destroy
  call mymodule%destroy
  call return_value%destroy
  call paths%destroy
  
  call forpy_finalize

end program