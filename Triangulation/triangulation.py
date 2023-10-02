from numpy import sqrt
from numpy import min
from numpy import max
from numpy import round
from scipy.linalg import lstsq
from scipy.optimize import curve_fit
from scipy.optimize import Bounds


def triangulate(p1, p2, p3, p4, d12, d13, d14):
    p0 = linear_lsqr(p1, p2, p3, p4, d12, d13, d14)[0][:2]
    lb = [min([p1[0], p2[0], p3[0], p4[0]]), min([p1[1], p2[1], p3[1], p4[1]])]
    ub = [max([p1[0], p2[0], p3[0], p4[0]]), max([p1[1], p2[1], p3[1], p4[1]])]
    p0 = [max([p0[0], lb[0]]), max([p0[1], lb[1]])]
    p0 = [min([p0[0], ub[0]]), min([p0[1], ub[1]])]
    p = nonlinear_lsqr(p0, p1, p2, p3, p4, d12, d13, d14, lb, ub)
    return p


def linear_lsqr(p1, p2, p3, p4, d12, d13, d14):
    a = [[p1[0] - p2[0], p1[1] - p2[1], d12], [p1[0] - p3[0], p1[1] - p3[1], d13], [p1[0] - p4[0], p1[1] - p4[1], d14]]
    b = [0.5 * (p1[0] ** 2 - p2[0] ** 2 + p1[1] ** 2 - p2[1] ** 2 + d12 ** 2),
         0.5 * (p1[0] ** 2 - p3[0] ** 2 + p1[1] ** 2 - p3[1] ** 2 + d13 ** 2),
         0.5 * (p1[0] ** 2 - p4[0] ** 2 + p1[1] ** 2 - p4[1] ** 2 + d14 ** 2)]
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
    d12 = sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - sqrt((p2[0] - p[0]) ** 2 + (p2[1] - p[1]) ** 2)
    d13 = sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - sqrt((p3[0] - p[0]) ** 2 + (p3[1] - p[1]) ** 2)
    d14 = sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2) - sqrt((p4[0] - p[0]) ** 2 + (p4[1] - p[1]) ** 2)
    ydata = [d12, d13, d14]
    return ydata


def main():
    p = [0.777, 0.25]
    p1 = [0, 0]
    p2 = [0.8, 0]
    p3 = [0, 0.5]
    p4 = [0.8, 0.5]

    d12 = sqrt((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2) - sqrt((p[0] - p2[0]) ** 2 + (p[1] - p2[1]) ** 2)
    d13 = sqrt((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2) - sqrt((p[0] - p3[0]) ** 2 + (p[1] - p3[1]) ** 2)
    d14 = sqrt((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2) - sqrt((p[0] - p4[0]) ** 2 + (p[1] - p4[1]) ** 2)

    est_p = triangulate(p1, p2, p3, p4, d12, d13, d14)
    est_p = round(est_p, 3)

    print("Actual Position:")
    print(p)
    print("Estimated Position:")
    print(est_p)


if __name__ == "__main__":
    main()
