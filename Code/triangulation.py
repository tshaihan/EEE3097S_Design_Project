import numpy as np
from scipy.linalg import lstsq
from scipy.optimize import curve_fit, Bounds


def triangulate(p1, p2, p3, p4, d12, d13, d14):
    p0 = linear_lsqr(p1, p2, p3, p4, d12, d13, d14)[0][:2]
    lb = np.array([np.min([p1[0], p2[0], p3[0], p4[0]]), np.min([p1[1], p2[1], p3[1], p4[1]])]) - 1
    ub = np.array([np.max([p1[0], p2[0], p3[0], p4[0]]), np.max([p1[1], p2[1], p3[1], p4[1]])]) + 1
    p0 = np.array([np.max([p0[0], lb[0]]), np.max([p0[1], lb[1]])])
    p0 = np.array([np.min([p0[0], ub[0]]), np.min([p0[1], ub[1]])])
    p = nonlinear_lsqr(p0, p1, p2, p3, p4, d12, d13, d14, lb, ub)
    return p


def linear_lsqr(p1, p2, p3, p4, d12, d13, d14):
    a = np.array([[p1[0] - p2[0], p1[1] - p2[1], d12],
                  [p1[0] - p3[0], p1[1] - p3[1], d13],
                  [p1[0] - p4[0], p1[1] - p4[1], d14]])
    b = np.array([0.5 * (p1[0] ** 2 - p2[0] ** 2 + p1[1] ** 2 - p2[1] ** 2 + d12 ** 2),
                  0.5 * (p1[0] ** 2 - p3[0] ** 2 + p1[1] ** 2 - p3[1] ** 2 + d13 ** 2),
                  0.5 * (p1[0] ** 2 - p4[0] ** 2 + p1[1] ** 2 - p4[1] ** 2 + d14 ** 2)])
    p = lstsq(a, b)
    return p


def nonlinear_lsqr(p0, p1, p2, p3, p4, d12, d13, d14, lb, ub):
    xdata = [p1, p2, p3, p4]
    ydata = [d12, d13, d14]
    bounds = Bounds(lb, ub)
    p = curve_fit(objective_func, xdata, ydata, p0, bounds=bounds, method='trf')[0]
    return p


def objective_func(xdata, *p):
    p1, p2, p3, p4 = xdata
    d12 = np.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - np.sqrt((p2[0] - p[0]) ** 2 + (p2[1] - p[1]) ** 2)
    d13 = np.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - np.sqrt((p3[0] - p[0]) ** 2 + (p3[1] - p[1]) ** 2)
    d14 = np.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - np.sqrt((p4[0] - p[0]) ** 2 + (p4[1] - p[1]) ** 2)
    ydata = [d12, d13, d14]
    return ydata
