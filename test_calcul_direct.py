import numpy as np
from res_direct import res_direct

def nu(z):
    return (1 - z)**2

def nu_prime(z):
    return - 2 * (1 - z)

def test_premiere_func(dt, h_max):
    """renvoie l'erreur entre la vraie solution et la solution
        par différences finies avec la premiere fonction"""
    def u(z, t):
        return 1000 * (np.sin(np.pi*z) - np.sin(2*np.pi*z)) * np.sin(t)
    def cst_u(z, t):
        return 1/(t+0.01) +z-z
    def u_t_independant(z,t):
        return np.cos(np.pi*z)

    def cst_f(z, t):
        """should be du/dt - nu'(z) * du/dz - nu(z) d²u/dz²"""
        return -1/((t+0.01)**2) + z - z # +z - z pour np.array

    def f_t_independant(z, t):
        return np.pi*(nu(z) * np.pi * np.cos(z) + nu_prime(z)*np.sin(z))

    def cst_b(t):
        return cst_u(0, t)

    def b_t_independant(t):
        return cst_u(0, t)

    def f(z, t):
        return 1000 * ((np.sin(np.pi*z) - np.sin(2*np.pi*z)) \
                * np.cos(t) - \
                np.sin(t) * ( nu_prime(z) * np.pi * \
                (np.cos(np.pi*z) - 2*np.cos(2*np.pi*z)) \
                + nu(z) * np.pi * np.pi * \
                (np.sin(np.pi*z) - 4 * np.sin(2*np.pi*z))))

    def a(t): # du/dz (0)
        return 0

    def b(t): # u(H, t)
        return 0

    t_f = 1
    return test_calcul_direct(u_t_independant, f_t_independant, a, b_t_independant, t_f, dt, h_max)

def test_calcul_direct(u, f, a, b, t_f, dt, h_max):
    discretisation_h = np.array([h for h in np.linspace(0, 1, 1/h_max)])
    # ici on a h = h_max, la discretisation est uniforme

    u0 = u(discretisation_h, 0)
    n_max = t_f
    hat_u = res_direct(u0, f, discretisation_h, 
                    dt, t_f, 
                    nu(discretisation_h),
                    nu_prime(discretisation_h),
                    a, b)

    # calcul d'erreur quadratique:
    uf = u(discretisation_h, t_f)
    return max(abs(uf - hat_u))

dt = 0.1
h = 0.1
for i in range(5):
    print(test_premiere_func(dt, 10**(-1-i)), "  :  10^(-", i+1, ")")