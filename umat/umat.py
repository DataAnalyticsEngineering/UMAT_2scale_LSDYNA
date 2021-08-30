import numpy as np
from enum import Enum
import scipy.integrate as integrate
from material_parameters import *
from rve_elastic import get_thermal, get_mechanical

class material_id(Enum):
    copper = 0
    tungsten = 1
    rve = 2

class material():
    def __init__(self, density, elastic_modulus, poisson_ratio, heat_capacity, thermal_conductivity, thermal_exp):
        self.density = density
        self.elastic_modulus = elastic_modulus
        self.poisson_ratio = poisson_ratio
        self.heat_capacity = heat_capacity
        self.thermal_conductivity = thermal_conductivity
        self.thermal_exp = thermal_exp

    def get_stiffness(self, temper):
        I2 = np.asarray([1., 1., 1., 0, 0, 0])
        I4 = np.eye(6)
        IxI = np.outer(I2, I2)
        P1 = IxI / 3.0
        P2 = I4 - P1
        shear_modulus = self.elastic_modulus(temper) / (2. * (1. + self.poisson_ratio(temper)))
        bulk_modulus = self.elastic_modulus(temper) / (3. * (1. - 2. * self.poisson_ratio(temper)))
        return bulk_modulus * IxI + 2. * shear_modulus * P2

materials = {}
materials[material_id.copper.value] = material(density=density_cu, elastic_modulus=elastic_modulus_cu,
                                               poisson_ratio=poisson_ratio_cu, heat_capacity=heat_capacity_cu,
                                               thermal_conductivity=conductivity_cu, thermal_exp=cte_cu)

materials[material_id.tungsten.value] = material(density=density_wsc, elastic_modulus=elastic_modulus_wsc,
                                                 poisson_ratio=poisson_ratio_wsc, heat_capacity=heat_capacity_wsc,
                                                 thermal_conductivity=conductivity_wsc, thermal_exp=cte_wsc)

def rve_solver_factory(*args):

    # print('rve_solver_factory')
    # print(args)
    # print([type(arg) for arg in args])

    sqrt2 = np.sqrt(2)
    if args[0]:
        # print(f'{"***mechanical*":>50}')
        _, mat_id, temperature, delta_temperature, *macro_strain = args

        if temperature < 293:
            temperature = 293

        if int(mat_id) == material_id.rve.value:
            stiffness, cte = get_mechanical(temperature)
        else:
            stiffness = materials[int(mat_id)].get_stiffness(temperature)
            cte = materials[int(mat_id)].thermal_exp(temperature)

        # Voigt -> Mandel notation
        macro_strain[3:] = macro_strain[3:] / sqrt2

        if delta_temperature > 0 and delta_temperature < 670: # TODO: don't run at initialisation
            if mat_id == material_id.rve.value:
                stress = stiffness @ (macro_strain - cte * delta_temperature * np.asarray([1., 1., 1., 0, 0, 0]))
            else:
                stress = stiffness @ (macro_strain - integrate.quad(lambda x: materials[int(mat_id)].thermal_exp(x), 0, delta_temperature)[0] * np.asarray([1., 1., 1., 0, 0, 0])) 
                # TODO: change to work with RVE (cte should be given as a function handle)
        else:
            stress = stiffness @ macro_strain

        # Mandel -> Voigt notation
        # https://sbrisard.github.io/janus/mandel.html
        stress[3:] = stress[3:] / sqrt2
        stiffness_voigt = np.copy(stiffness)
        stiffness_voigt[3:, 3:] = stiffness_voigt[3:, 3:] / 2
        stiffness_voigt[:3, 3:] = stiffness_voigt[:3, 3:] / sqrt2
        stiffness_voigt[3:, :3] = stiffness_voigt[3:, :3] / sqrt2

        return [*stress.flatten(), *stiffness_voigt.flatten()]

    else:
        # print(f'{"***thermal****":>50}')
        _, mat_id, temperature, = args
        if int(mat_id) == 2:
            return get_thermal(temperature)
        else:
            conductivity = [materials[int(mat_id)].thermal_conductivity(temperature)] * 3
            heat_capacity = [materials[int(mat_id)].heat_capacity(temperature)]
            return conductivity + heat_capacity  # sum of two lists

if __name__ == '__main__':
    import numpy as np

    mat_id = 1

    macro_strain_voigt = np.asarray([1., 2., 3., 2 * 8., 2 * 10., 2 * 12.])
    macro_strain_mandel = macro_strain_voigt / [1, 1, 1, np.sqrt(2), np.sqrt(2), np.sqrt(2)]

    macro_temperature_gradient = np.random.rand(6)
    temperature = 293
    delta_temperature = np.random.rand()

    out = rve_solver_factory(*(0, mat_id, temperature))
    print(f'\nConductivity and heat capacity')
    print(f'out = {out}')

    out = rve_solver_factory(*(1, mat_id, temperature, delta_temperature, *macro_strain_voigt))
    print(f'\nStress and stiffness')
    print(f'out = {out}')

    mat_id = 2

    out = rve_solver_factory(*(0, mat_id, temperature))
    print(f'\nConductivity and heat capacity')
    print(f'out = {out}')

    out = rve_solver_factory(*(1, mat_id, temperature, delta_temperature, *macro_strain_voigt))
    print(f'\nStress and stiffness')
    print(f'out = {out}')
# debug
# print('***1***')
# try:
#     pass
# except Exception as e:
#     print(e)
# print('***2***')
