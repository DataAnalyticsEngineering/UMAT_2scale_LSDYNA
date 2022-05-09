#include <iostream>
#include <array>
#include <cmath>
#include <stdexcept>
// https://github.com/mileschen360/ezh5
#include "ezh5/ezh5.hpp"
#include "../mixed_languages/Eigen/Dense"

Eigen::VectorXd I2{{1., 1., 1., 0, 0, 0}};
auto I4 = Eigen::MatrixXd::Identity(6, 6);
auto IxI = I2 * I2.transpose();
auto P1 = IxI / 3.0;
auto P2 = I4 - P1;
auto sqrt2 = sqrt(2);

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
typedef double (*func_2inputs)(double, double);

class material
{
public:
    func elastic_modulus;
    func poisson_ratio;
    func conductivity;
    func heat_capacity;
    func_2inputs thermal_strain;
    func cte;
    func hardening;
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
            thermal_strain = [](double x, double ref_temp) { return (1.28170e-05 * x + 8.23091e-09 * pow(x, 2) / 2) - (1.28170e-05 * ref_temp + 8.23091e-09 * pow(ref_temp, 2) / 2); };
            yield = [](double x) { return (x < 1000) ? 1.12133e+02 * x + 3.49810e+04 + 1.53393e+05 * tanh((x / 1000 + -6.35754e-01) / -2.06958e-01) : 1200.0; };
            hardening = [](double x) { return 20e6; };
        }
        else if (mat_id == material_id::tungsten)
        {
            poisson_ratio = [](double x) { return 2.80000e-01; };
            conductivity = [](double x) { return 2.19308e+05 + -1.87425e+02 * x + 1.05157e-01 * pow(x, 2) + -2.01180e-05 * pow(x, 3); };
            heat_capacity = [](double x) { return 2.39247e+03 + 6.62775e-01 * x + -2.80323e-04 * pow(x, 2) + 6.39511e-08 * pow(x, 3); };
            elastic_modulus = [](double x) { return 4.13295e+08 + -7.83159e+03 * x + -3.65909e+01 * pow(x, 2) + 5.48782e-03 * pow(x, 3); };
            cte = [](double x) { return 5.07893e-06 + 5.67524e-10 * x; };
            thermal_strain = [](double x, double ref_temp) { return (5.07893e-06 * x + 5.67524e-10 * pow(x, 2) / 2) - (5.07893e-06 * ref_temp + 5.67524e-10 * pow(ref_temp, 2) / 2); };
            yield = [](double x) { return 1e20; };
            hardening = [](double x) { return 1e20; };
        }
    }

    auto shear_modulus(double temperature) { return elastic_modulus(temperature) / (2. * (1. + poisson_ratio(temperature))); }
    auto bulk_modulus(double temperature) { return elastic_modulus(temperature) / (3. * (1. - 2. * poisson_ratio(temperature))); }
    auto get_stiffness(double temperature) { return bulk_modulus(temperature) * IxI + 2. * shear_modulus(temperature) * P2; }
};

extern "C" void umat_cpp_mechanical_(const double& mat_id,
                                     const double& temper,
                                     const double& d_temperature,
                                     const double* strain_in,
                                     double* stress,
                                     double* tangent_stiffness,
                                     const double& elastic_flag,
                                     double* plastic_strain,
                                     double& hardening_q,
                                     double* thermal_strain_hsv,
                                     const double& ref_temp)
{
    double temperature = limit_temperature_2minmax(temper);

    auto mat = material(material_id(int(mat_id))); // TODO pass mat_id as integer?
    Eigen::MatrixXd stiffness = mat.get_stiffness(temperature);
    auto thermal_strain = mat.thermal_strain(temperature, ref_temp) * I2;

    using Eigen::seq;

    Eigen::Map<const Eigen::VectorXd> strain(strain_in, 6);
    Eigen::VectorXd strain_mandel = strain;
    Eigen::Map<Eigen::VectorXd> plastic_strain_mandel(plastic_strain, 6);
    strain_mandel(seq(3, 5)) /= sqrt2;

    Eigen::VectorXd stress_mandel = stiffness * (strain_mandel - plastic_strain_mandel - thermal_strain);

    // if (int(elastic_flag) == 0) // elastic material model
    if (int(elastic_flag) == 1) // plastic material model with linear isotropic hardening and no viscous effects
    {
        auto dev_stress = P2 * stress_mandel;
        auto norm_dev = dev_stress.norm();
        if (norm_dev > 0)
        {
            auto dev_normal = dev_stress / norm_dev;
            auto yield_stress = [mat, temperature](double hardening_q) { return mat.yield(temperature) + mat.hardening(temperature) * hardening_q; };
            auto evaluate_yield_function = [mat, temperature, yield_stress](double x, double hardening_q) { return x - sqrt(2.0 / 3.0) * yield_stress(hardening_q); };
            auto trial_yield_func = evaluate_yield_function(norm_dev, hardening_q);
            if (trial_yield_func > 0)
            {
                // std::cout << "plastic" << '\n';
                // std::cout << trial_yield_func << '\n';
                double d_lambda = trial_yield_func / (2 * mat.shear_modulus(temperature) + 2. / 3. * mat.hardening(temperature));
                plastic_strain_mandel += d_lambda * dev_normal;
                hardening_q += sqrt(2.0 / 3.0) * d_lambda;
                stress_mandel = stiffness * (strain_mandel - plastic_strain_mandel - thermal_strain);
                stiffness = stiffness - (4 * pow(mat.shear_modulus(temperature), 2) * (dev_normal * dev_normal.transpose()) / (2 * mat.shear_modulus(temperature) + 2. / 3. * yield_stress(hardening_q)))
                            - (4 * pow(mat.shear_modulus(temperature), 2) * d_lambda / norm_dev * (P2 - dev_normal * dev_normal.transpose()));
            }
            if (trial_yield_func == 0)
            {
                double d_lambda = trial_yield_func / (2 * mat.shear_modulus(temperature));
                plastic_strain_mandel += d_lambda * dev_normal;
                hardening_q += sqrt(2.0 / 3.0) * d_lambda;
                stress_mandel = stiffness * (strain_mandel - plastic_strain_mandel - thermal_strain);
                stiffness = stiffness - (4 * pow(mat.shear_modulus(temperature), 2) * (dev_normal * dev_normal.transpose()) / (2 * mat.shear_modulus(temperature) + 2. / 3. * yield_stress(hardening_q)))
                            - (4 * pow(mat.shear_modulus(temperature), 2) * d_lambda / norm_dev * (P2 - dev_normal * dev_normal.transpose()));
            }
        }
    }

    // Mandel -> Voigt notation
    stress_mandel(seq(3, 5)) /= sqrt2;
    stiffness(seq(3, 5), seq(3, 5)) /= 2;
    stiffness(seq(0, 2), seq(3, 5)) /= sqrt2;
    stiffness(seq(3, 5), seq(0, 2)) /= sqrt2;

    Eigen::Map<Eigen::VectorXd>(thermal_strain_hsv, thermal_strain.size()) = thermal_strain;
    Eigen::Map<Eigen::VectorXd>(plastic_strain, plastic_strain_mandel.size()) = plastic_strain_mandel;
    Eigen::Map<Eigen::VectorXd>(stress, stress_mandel.size()) = stress_mandel;
    Eigen::Map<Eigen::MatrixXd>(tangent_stiffness, stiffness.rows(), stiffness.cols()) = stiffness;
}

extern "C" void umat_cpp_thermal_(const double& mat_id, const double& temperature, double& c1, double& c2, double& c3, double& cvl)
{
    auto mat = material(material_id(int(mat_id))); // TODO pass mat_id as integer?
    // Note: if iortho=0 in the material card in mat_44.k, the material is considered isotropic and only c1 is used
    c1 = c2 = c3 = mat.conductivity(temperature);
    cvl = mat.heat_capacity(temperature);
}

extern "C" {
void umat_cpp_mechanical_rve_(const double& temperature, const double& d_temperature, double& strain, double& stress, double& stiffness);
}

extern "C" void umat_cpp_thermal_rve_(const double& temperature, double& c1, double& c2, double& c3, double& cvl)
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
