#include <iostream>

extern "C" {
void cppfun_(const double* argument_1, double* argument_2, double& argument_3);
}

void cppfun_(const double* argument_1, double* argument_2, double& argument_3)
{
    std::cout << "cppfunc was called" << std::endl;
    for (int i = 0; i < 6; i++)
    {
        std::cout << *(argument_1 + i) << " ";
        *(argument_2 + i) = *(argument_1 + i) * 2;
    }
    argument_3 = 1.3;
    std::cout << std::endl;
}