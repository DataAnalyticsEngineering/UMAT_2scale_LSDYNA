#include <iostream>
#include "Eigen/Dense"

Eigen::VectorXd I2{{1., 1., 1., 0, 0, 0}};
auto I4 = Eigen::MatrixXd::Identity(6, 6);
auto IxI = I2 * I2.transpose();
auto P1 = IxI / 3.0;
auto P2 = I4 - P1;

enum class material_id { copper, tungsten, rve };

double min_temperature = 293.15;
double max_temperature = 1300;

double limit_temperature_2minmax(const double temperature)
{
    if (temperature < min_temperature)
        return min_temperature;
    else if (temperature > max_temperature)
        return max_temperature;
    return temperature;
}

typedef double (*func)(double);

class material
{
public:
    func elastic_modulus;
    func poisson_ratio;
    func conductivity;
    func heat_capacity;
    func thermal_strain;
    func cte;
    func yield;

    material(material_id mat_id)
    {
        if (mat_id == material_id::copper)
        {
            poisson_ratio = [](double x) { return 3.40000e-01; };
            conductivity = [](double x) { return 4.20749e+05 + -6.84915e+01 * x; };
            heat_capacity = [](double x) { return 2.94929e+03 + 2.30217e+00 * x + -2.95302e-03 * pow(x, 2) + 1.47057e-06 * pow(x, 3); };
            elastic_modulus = [](double x) { return 1.35742e+08 + 5.85757e+03 * x + -8.16134e+01 * pow(x, 2); };
            cte = [](double x) { return 1.28170e-05 + 8.23091e-09 * x; };
            thermal_strain = [](double x) { return (1.28170e-05 * x + 8.23091e-09 * pow(x, 2) / 2) - (1.28170e-05 * min_temperature + 8.23091e-09 * pow(min_temperature, 2) / 2); };
            yield = [](double x) { return (x < 1000) ? 1.12133e+02 * x + 3.49810e+04 + 1.53393e+05 * tanh((x / 1000 + -6.35754e-01) / -2.06958e-01) : 1200.0; };
        }
        else if (mat_id == material_id::tungsten)
        {
            poisson_ratio = [](double x) { return 2.80000e-01; };
            conductivity = [](double x) { return 2.19308e+05 + -1.87425e+02 * x + 1.05157e-01 * pow(x, 2) + -2.01180e-05 * pow(x, 3); };
            heat_capacity = [](double x) { return 2.39247e+03 + 6.62775e-01 * x + -2.80323e-04 * pow(x, 2) + 6.39511e-08 * pow(x, 3); };
            elastic_modulus = [](double x) { return 4.13295e+08 + -7.83159e+03 * x + -3.65909e+01 * pow(x, 2) + 5.48782e-03 * pow(x, 3); };
            cte = [](double x) { return 5.07893e-06 + 5.67524e-10 * x; };
            thermal_strain = [](double x) { return (5.07893e-06 * x + 5.67524e-10 * pow(x, 2) / 2) - (5.07893e-06 * min_temperature + 5.67524e-10 * pow(min_temperature, 2) / 2); };
            yield = [](double x) { return 1e20; };
        }
    }

    auto get_stiffness(double temperature)
    {
        auto shear_modulus = elastic_modulus(temperature) / (2. * (1. + poisson_ratio(temperature)));
        auto bulk_modulus = elastic_modulus(temperature) / (3. * (1. - 2. * poisson_ratio(temperature)));
        return bulk_modulus * IxI + 2. * shear_modulus * P2;
    }
};

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
    // std::cout << m.data()[0] << std::endl;

    Eigen::VectorXd v{{1.2, 2.1, 3.3, 4.5}};
    v(Eigen::seq(1, 2)) = v(Eigen::seq(1, 2)) * 10;
    std::cout << v(Eigen::seq(1, 2)) << std::endl;

    auto mat = material(material_id::copper);
    // std::cout << mat.elastic_modulus(293.15) << std::endl;
    // std::cout << mat.thermal_strain(380) << std::endl;
    std::cout << mat.get_stiffness(293.15) << std::endl;
}