import numpy as np
from scipy.linalg import lstsq
from scipy.optimize import curve_fit, Bounds


# Triangulates a 2D position using Least Squares Estimation (LSE) of Time Difference of Arrival values (TDoA)
def triangulate(p1, p2, p3, p4, tdoa12, tdoa13, tdoa14, c):
    p1, p2, p3, p4 = np.asarray([p1, p2, p3, p4])

    # Calculates distances
    d12, d13, d14 = c * np.asarray([tdoa12, tdoa13, tdoa14])

    # Performs initial position estimate using linear LSE
    p0 = linear_lse(p1, p2, p3, p4, d12, d13, d14)[:2]

    # Sets the bounds of the non-linear LSE solution
    lb = np.asarray([np.min([p1[0], p2[0], p3[0], p4[0]]), np.min([p1[1], p2[1], p3[1], p4[1]])]) - 0.001
    ub = np.asarray([np.max([p1[0], p2[0], p3[0], p4[0]]), np.max([p1[1], p2[1], p3[1], p4[1]])]) + 0.001

    # Ensures initial position estimate is within the bounds
    p0 = np.asarray([np.max([p0[0], lb[0]]), np.max([p0[1], lb[1]])])
    p0 = np.asarray([np.min([p0[0], ub[0]]), np.min([p0[1], ub[1]])])

    # Estimates position using non-linear LSE
    try:
        p = nonlinear_lse(p0, p1, p2, p3, p4, d12, d13, d14, lb, ub)
    except:
        p = p0

    return p, p0


def linear_lse(p1, p2, p3, p4, d12, d13, d14):
    # Creates LSE matrix
    a = np.asarray([[p1[0] - p2[0], p1[1] - p2[1], d12],
                    [p1[0] - p3[0], p1[1] - p3[1], d13],
                    [p1[0] - p4[0], p1[1] - p4[1], d14]])

    # Creates LSE vector
    b = 0.5 * np.asarray([(p1[0] ** 2 - p2[0] ** 2 + p1[1] ** 2 - p2[1] ** 2 + d12 ** 2),
                          (p1[0] ** 2 - p3[0] ** 2 + p1[1] ** 2 - p3[1] ** 2 + d13 ** 2),
                          (p1[0] ** 2 - p4[0] ** 2 + p1[1] ** 2 - p4[1] ** 2 + d14 ** 2)])

    # Performs linear LSE
    p = lstsq(a, b)[0]
    return p


def nonlinear_lse(p0, p1, p2, p3, p4, d12, d13, d14, lb, ub):
    # Sets non-linear LSE inputs
    xdata = np.array([p1, p2, p3, p4])
    ydata = np.array([d12, d13, d14])
    bounds = Bounds(lb, ub)

    # Performs non-linear LSE
    p = curve_fit(objective_func, xdata, ydata, p0, bounds=bounds, method='trf')[0]
    return p


# Objective function for non-linear LSE
def objective_func(xdata, *p):
    p1, p2, p3, p4 = xdata
    d12 = np.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - np.sqrt((p2[0] - p[0]) ** 2 + (p2[1] - p[1]) ** 2)
    d13 = np.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - np.sqrt((p3[0] - p[0]) ** 2 + (p3[1] - p[1]) ** 2)
    d14 = np.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - np.sqrt((p4[0] - p[0]) ** 2 + (p4[1] - p[1]) ** 2)
    ydata = [d12, d13, d14]
    return ydata
