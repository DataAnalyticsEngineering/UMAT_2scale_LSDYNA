import numpy as np

young_modulus, poisson_ratio = 128.85e6, 0.34
# young_modulus, poisson_ratio = 408.e6, 0.28

shear_modulus = young_modulus / (2 * (1. + poisson_ratio))
bulk_modulus = young_modulus / (3 * (1. - 2. * poisson_ratio))

print(f'{shear_modulus = :.3e}')
print(f'{bulk_modulus  = :.3e}')

C = np.zeros((6, 6))
C[range(6), range(6)] = poisson_ratio
C = np.diag([1, 1, 1, 0.5, 0.5, 0.5]) - C
for i in range(3):
    for j in range(3):
        if i != j:
            C[i, j] = poisson_ratio

print('\n Structure of the stiffness matrix')
print(C)

stiffness_voigt = C * young_modulus / ((1 + poisson_ratio) * (1 - 2 * poisson_ratio))

print('\n Material stiffness in Voigt notation')
with np.printoptions(precision=4, suppress=True, formatter={'float': '{:>2.8e}'.format}, linewidth=100):
    print(stiffness_voigt)

stiffness_mandel = np.copy(stiffness_voigt)
stiffness_mandel[3:, 3:] = stiffness_mandel[3:, 3:] * 2
stiffness_mandel[:3, 3:] = stiffness_mandel[:3, 3:] * np.sqrt(2)
stiffness_mandel[3:, :3] = stiffness_mandel[3:, :3] * np.sqrt(2)
print('\n Material stiffness in Mandel notation')
with np.printoptions(precision=4, suppress=True, formatter={'float': '{:>2.8e}'.format}, linewidth=100):
    print(stiffness_mandel)
# This matrix is identical to the effective stiffness from FANS with an RVE of two identical materials, i.e. one homogeneous material. Hence, notation should be changed from Mandel to Voigt notation in order to use in LS-DYNA

I2 = np.asarray([1., 1., 1., 0, 0, 0])
I4 = np.eye(6)
IxI = np.outer(I2, I2)
P1 = IxI / 3.0
P2 = I4 - P1

stiffness = bulk_modulus * IxI + 2. * shear_modulus * P2
# stiffness = 3 * bulk_modulus * P1 + 2. * shear_modulus * P2
print('\n Material stiffness in Mandel notation')
with np.printoptions(precision=4, suppress=True, formatter={'float': '{:>2.8e}'.format}, linewidth=100):
    print(stiffness)
