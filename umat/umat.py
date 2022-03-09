import numpy as np
from enum import Enum
from material_parameters import *
from rve_elastic import get_thermal, get_mechanical

class material_id(Enum):
    copper = 0
    tungsten = 1
    rve = 2

def limit_temperature_2minmax(temperature):
    if temperature < min_temperature:
        return min_temperature
    elif temperature > max_temperature:
        return max_temperature
    return temperature

class material():
    def __init__(self, elastic_modulus, poisson_ratio, heat_capacity, thermal_conductivity, thermal_strain):
        self.elastic_modulus = elastic_modulus
        self.poisson_ratio = poisson_ratio
        self.heat_capacity = heat_capacity
        self.thermal_conductivity = thermal_conductivity
        self.thermal_strain = thermal_strain

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
materials[material_id.copper.value] = material(elastic_modulus=elastic_modulus_cu, poisson_ratio=poisson_ratio_cu,
                                               heat_capacity=heat_capacity_cu, thermal_conductivity=conductivity_cu,
                                               thermal_strain=thermal_strain_cu)

materials[material_id.tungsten.value] = material(elastic_modulus=elastic_modulus_wsc, poisson_ratio=poisson_ratio_wsc,
                                                 heat_capacity=heat_capacity_wsc, thermal_conductivity=conductivity_wsc,
                                                 thermal_strain=thermal_strain_wsc)

def rve_solver_factory(*args):
    # print('rve_solver_factory')
    # print(args)
    # print([type(arg) for arg in args])

    sqrt2 = np.sqrt(2)
    if args[0]:
        try:
            # print(f'{"***mechanical*":>50}')
            mat_id = int(args[1])
            temperature = args[2]
            d_temperature = args[3]
            previous_therma_strain = np.asarray(args[4:10])
            macro_strain = np.asarray(args[10:16])
            temperature = limit_temperature_2minmax(temperature)
            if mat_id == material_id.rve.value:
                stiffness, thermal_strain = get_mechanical(temperature)
            else:
                stiffness = materials[mat_id].get_stiffness(temperature)
                thermal_strain = materials[mat_id].thermal_strain(temperature)

            # Voigt -> Mandel notation
            macro_strain[3:] = macro_strain[3:] / sqrt2

            stress = stiffness @ (macro_strain - (thermal_strain - previous_therma_strain))
            # TODO previous_therma_strain should be updated only after convergence
            # stress2 = stiffness @ macro_strain

            # Mandel -> Voigt notation
            # https://sbrisard.github.io/janus/mandel.html
            stress[3:] = stress[3:] / sqrt2
            stiffness_voigt = np.copy(stiffness)
            stiffness_voigt[3:, 3:] = stiffness_voigt[3:, 3:] / 2
            stiffness_voigt[:3, 3:] = stiffness_voigt[:3, 3:] / sqrt2
            stiffness_voigt[3:, :3] = stiffness_voigt[3:, :3] / sqrt2

            return [*stress.flatten(), *stiffness_voigt.flatten(), *thermal_strain.flatten()]
        except Exception as e:
            print(e)
            raise RuntimeError('--- error in the mechanical part of umat.py ---')
    else:
        try:
            # print(f'{"***thermal****":>50}')
            _, mat_id, temperature, = args

            temperature = limit_temperature_2minmax(temperature)

            if int(mat_id) == material_id.rve.value:
                return get_thermal(temperature)

            conductivity = [materials[int(mat_id)].thermal_conductivity(temperature)] * 3
            heat_capacity = [materials[int(mat_id)].heat_capacity(temperature)]
            return conductivity + heat_capacity  # sum of two lists
        except Exception as e:
            print(e)
            raise RuntimeError('--- error in the thermal part of umat.py ---')

if __name__ == '__main__':
    import numpy as np
    np.random.seed(0)

    mat_id = 0

    macro_strain_voigt = np.asarray([1., 2., 3., 2 * 8., 2 * 10., 2 * 12.])
    macro_strain_mandel = macro_strain_voigt / [1, 1, 1, np.sqrt(2), np.sqrt(2), np.sqrt(2)]

    macro_temperature_gradient = np.random.rand(6)
    temperature = min_temperature + 50
    d_temperature = temperature - min_temperature
    previous_therma_strain = thermal_strain_cu(min_temperature) * np.asarray([1., 1., 1., 0, 0, 0])

    out = rve_solver_factory(*(0, mat_id, temperature))
    print(f'\nConductivity and heat capacity')
    print(f'out = {out}')

    out = rve_solver_factory(*(1, mat_id, temperature, d_temperature, *previous_therma_strain, *macro_strain_voigt))
    print(f'\nStress and stiffness')
    print(f'out = {out}')

    mat_id = 1
    previous_therma_strain = thermal_strain_wsc(min_temperature) * np.asarray([1., 1., 1., 0, 0, 0])

    out = rve_solver_factory(*(0, mat_id, temperature))
    print(f'\nConductivity and heat capacity')
    print(f'out = {out}')

    out = rve_solver_factory(*(1, mat_id, temperature, d_temperature, *previous_therma_strain, *macro_strain_voigt))
    print(f'\nStress and stiffness')
    print(f'out = {out}')

    mat_id = 2
    previous_therma_strain = np.random.rand(6)

    out = rve_solver_factory(*(0, mat_id, temperature))
    print(f'\nConductivity and heat capacity')
    print(f'out = {out}')

    out = rve_solver_factory(*(1, mat_id, temperature, d_temperature, *previous_therma_strain, *macro_strain_voigt))
    print(f'\nStress and stiffness')
    print(f'out = {out}')
