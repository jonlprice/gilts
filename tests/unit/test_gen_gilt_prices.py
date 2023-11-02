import pytest
from gen_gilt_prices import Gilt

def test_Coupon1():
    g=Gilt("a","b","c","0 1/8% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("0 1/8% Treasury Gilt 2024")
    print (g)
    assert coupon == 0.125

def test_Coupon2():
    g=Gilt("a","b","c","1 1/8% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("1 1/8% Treasury Gilt 2024")
    print (g)
    assert coupon == 1.125

def test_Coupon3():
    g=Gilt("a","b","c","2 1/8% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("2 1/8% Treasury Gilt 2024")
    print (g)
    assert coupon == 2.125


def test_Coupon4():
    g=Gilt("a","b","c","4¼% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("4¼% Treasury Gilt 2024")
    print (g)
    assert coupon == 4.25

def test_Coupon5():
    g=Gilt("a","b","c","5% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("5% Treasury Gilt 2024")
    print (g)
    assert coupon == 5

def test_Coupon6():
    g=Gilt("a","b","c","10¼% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("10¼% Treasury Gilt 2024")
    print (g)
    assert coupon == 10.25

def test_Coupon7():
    g=Gilt("a","b","c","10 1/8% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")
    coupon = g.calculate_coupon("10 1/8% Treasury Gilt 2024")
    print (g)
    assert coupon == 10.125

def test_calculate_yield():
    # g=Gilt("a","b","c","10 1/8% Treasury Gilt 2024","e","2024-01-31T00:00:00","g","h","i","j","k")

    calculated_yield = Gilt.calculate_yield(5,99,3)

    assert calculated_yield == 5.360134003350083

