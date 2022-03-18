#include <iostream>
#include "Eigen/Dense"

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

    Eigen::MatrixXd m{{1.2, 2.1}, {3.3, 4.5}};
    std::cout << m << std::endl;
}