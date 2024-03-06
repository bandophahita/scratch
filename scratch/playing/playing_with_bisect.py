import bisect


bmi_ranges = [
(0, 15.99),
(16.00, 16.99),
(17.00, 18.49),
(18.50, 24.99),
(25.00, 29.99),
(30.00, 34.99),
(35.00, 39.99),
(40.00, 1000.00),
]

def limit(t):
    return t[0]


limitValues = [line[0] for line in bmi_ranges][1:]

bmi_range = bmi_ranges[bisect.bisect(limitValues, 1001)]

bmi_range2 = bisect.bisect(bmi_ranges, 1001, key=limit)

print()
