from companies.company import MyCompany

TEST_YEAR = 1


def test_MyCompany():

    expected_free_cashflow = 73365000000.0

    AAPL = MyCompany("AAPL")
    
    free_cashflow = AAPL.compute_free_cashflow(TEST_YEAR)
    assert free_cashflow == expected_free_cashflow

    free_cashflow_growth_rate = AAPL.get_free_cashflow_growth_rate()

    print(AAPL.analyze_dcf(TEST_YEAR))
    
    return 