from operator import mul
from functools import reduce
# solving polynomials 
# base on 
# f(x) = sum( yi * sum([(x - xj) / (xi - xj) for xj in points if j not == i]))
def polynomial_interpolate(points):
    coefs = [0] * len(points)
    for i in range(0, len(points)):
        coefs = [a + b for a, b in zip(coefs, single_term(i, points))]
    return coefs

def single_term(i, points):
    coefs = [1.0]
    for j, p in enumerate(points):        
        if not j == i:
            xj, _ = p
            c1 = [-c*xj for c in coefs] + [0]
            c2 = [0] + [c for c in coefs]
            coefs = [a + b for a, b in zip(c1, c2)]
    # print('temp coefs = ', coefs)
    assert len(coefs) == len(points)
    if len(coefs) > 1:
        xi, yi = points[i]
        denom = reduce(mul, [xi - p[0] for j, p in enumerate(points) if j != i])
        # print('denom = ', denom, [xi - p[0] for j, p in enumerate(points) if j != i])
        # print('denominator = ', denom, ' list = ', [p[0] - xj for j, p in enumerate(points) if j != i])
        coefs = [c * yi / denom for c in coefs]
        assert len(coefs) == len(points)
    return coefs

def eval_polynomial(coefs, points):
    res = []
    for p in points:
        x, _ = p        
        y = 0
        for i, c in enumerate(coefs):        
            if i == 0:
                y += c
            else:
                y += c*x 
                x *= x 
        res.append(y)
    return res

# test
points1 = [(1,1)]
points2 = [(1,1), (2,0)]
points3 = [(1,1), (2,4), (7,9)]

assert polynomial_interpolate(points1) == [1.0]
assert polynomial_interpolate(points2) == [2.0, -1.0]
coefs = polynomial_interpolate(points3)

# assert -2.66666666, 3.9999999, -0.3333333
print(eval_polynomial(coefs, points3))