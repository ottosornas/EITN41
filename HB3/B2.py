from scipy import interpolate

def lagrange(k, n, private_polynomial, shares, participants, master_points):
    shares.insert(0, private_polynomial)

    master_polynomial = interpolate.lagrange(participants, [sum(shares)] + master_points)

    print(master_polynomial)
    print(master_polynomial(0)) #(0) means setting x to 0 in the polynomial we get from master_polynomial and calculating the function

k = 4
n = 7
private_polynomial = sum([3, 5, 10, 11])
shares = [45, 39, 41, 55, 45, 41]
participants = [1, 3, 5, 6]
master_points = [3313, 12939, 21430]

lagrange(k, n, private_polynomial, shares, participants, master_points)

