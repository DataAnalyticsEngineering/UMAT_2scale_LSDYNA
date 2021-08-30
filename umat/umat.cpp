#include <iostream>
#include <array>
#include <cmath>
#include <stdexcept>
// https://github.com/mileschen360/ezh5
#include "ezh5/ezh5.hpp"

extern "C" {
void umat_cpp_thermal_(const double& mat_id,
                       const double& temperature,
                       double& c1,
                       double& c2,
                       double& c3,
                       double& cvl);
}

void umat_cpp_thermal_(const double& mat_id,
                       const double& temperature,
                       double& c1,
                       double& c2,
                       double& c3,
                       double& cvl)
{
    if (int(mat_id) == 0)
    {
        // auto density = [&temperature]() { return 8.93300e-06; };
        auto thermal_conductivity = 4.20749e+05 - 6.84915e+01 * temperature;
        auto heat_capacity = 3.16246e+08 + 3.17858e+05 * temperature
                             - 3.49795e+02 * pow(temperature, 2) + 1.66327e-01 * pow(temperature, 3);
        auto density = 8.93300e-06;
        auto poisson_ratio = 3.40000e-01;
        auto cte = 1.28170e-05 + 8.23091e-09 * temperature;
        auto elastic_modulus = std::max(6.4126e+05,
                                        1.35742e+08 + 5.85757e+03 * temperature
                                            - 8.16134e+01 * pow(temperature, 2));

        c1 = c2 = c3 = thermal_conductivity;
        cvl = heat_capacity;
    }
    else
    {
        auto thermal_conductivity = 2.19308e+05 - 1.87425e+02 * temperature
                                    + 1.05157e-01 * pow(temperature, 2)
                                    - 2.01180e-05 * pow(temperature, 3);
        auto heat_capacity = 1.23958e+08 + 3.44414e+04 * temperature
                             - 1.25514e+01 * pow(temperature, 2) + 2.87070e-03 * pow(temperature, 3);
        auto density = 1.93000e-05;
        auto poisson_ratio = 2.80000e-01;
        auto cte = 5.07893e-06 + 5.67524e-10 * temperature;
        auto elastic_modulus = 4.13295e+08 - 7.83159e+03 * temperature
                               - 3.65909e+01 * pow(temperature, 2)
                               + 5.48782e-03 * pow(temperature, 3);

        c1 = c2 = c3 = thermal_conductivity;
        cvl = heat_capacity;
    }
}

extern "C" {
void umat_cpp_mechanical_(const double& mat_id,
                          const double& temperature,
                          const double& d_temperature,
                          double& strain,
                          double& stress,
                          double& stiffness);
}

void umat_cpp_mechanical_(const double& mat_id,
                          const double& temperature,
                          const double& d_temperature,
                          double& strain,
                          double& stress,
                          double& stiffness)
{
    throw std::runtime_error("umat_cpp_mechanical_ is not implemented yet!");

    if (int(mat_id) == 0)
    {
        auto density = 8.93300e-06;
        auto poisson_ratio = 3.40000e-01;
        auto cte = 1.28170e-05 + 8.23091e-09 * temperature;
        auto elastic_modulus = std::max(6.4126e+05,
                                        1.35742e+08 + 5.85757e+03 * temperature
                                            - 8.16134e+01 * pow(temperature, 2));
    }
    else
    {
        auto density = 1.93000e-05;
        auto poisson_ratio = 2.80000e-01;
        auto cte = 5.07893e-06 + 5.67524e-10 * temperature;
        auto elastic_modulus = 4.13295e+08 - 7.83159e+03 * temperature
                               - 3.65909e+01 * pow(temperature, 2)
                               + 5.48782e-03 * pow(temperature, 3);
    }
}

extern "C" {
void umat_cpp_thermal_rve_(const double& temperature, double& c1, double& c2, double& c3, double& cvl);
void umat_cpp_mechanical_rve_(const double& temperature,
                              const double& d_temperature,
                              double& strain,
                              double& stress,
                              double& stiffness);
}

void umat_cpp_thermal_rve_(const double& temperature, double& c1, double& c2, double& c3, double& cvl)
{
    throw std::runtime_error("umat_cpp_thermal_rve_ is not implemented yet!");

    //     const std::string FILE_NAME = "/home/alameddin/simkom_updates/material/effective_response.h5";
    //
    //     ezh5::File h5file(FILE_NAME, H5F_ACC_RDONLY);
    //     std::vector<double> tempe;
    //     tempe << h5file["temperature"];
    //
    //     for (int i = 0; i < tempe.size(); ++i)
    //     {
    //         std::cout << tempe[i] << std::endl;
    //     }
    //     // std::vector<double> conductivity;
    //     // auto conductivity = h5file["conductivity"];
    //     // std::cout << typeid(conductivity).name() << std::endl;
    //
    //     h5file.~File();
    //
    //     // std::cout << conductivity.size() << std::endl;
    //
    //     // DataSet dataset = file.openDataSet( DATASET_NAME );
}
