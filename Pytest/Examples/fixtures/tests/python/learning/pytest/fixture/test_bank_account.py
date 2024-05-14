import pytest

from Pytest.Examples.fixtures.src.python.learning.pytest.fixture.bank_account import BankAccount


@pytest.fixture
def bank_account():
    return BankAccount(123, 500)


def test_deposit(bank_account):
    bank_account.deposit(400)
    assert bank_account.get_balance() == 900


def test_deposit_zero(bank_account):
    with pytest.raises(ValueError):
        bank_account.deposit(0)


def test_deposit_negative(bank_account):
    with pytest.raises(ValueError):
        bank_account.deposit(-100)


def test_deposit_str(bank_account):
    with pytest.raises(TypeError):
        bank_account.deposit("invalidinput")


def test_withdrawl(bank_account):
    bank_account.withdrawl(200)
    assert bank_account.get_balance() == 300


def test_withdrawl_zero(bank_account):
    with pytest.raises(ValueError):
        bank_account.withdrawl(0)


def test_withdrawl_negative(bank_account):
    with pytest.raises(ValueError):
        bank_account.withdrawl(-100)


def test_withdrawl_str(bank_account):
    with pytest.raises(TypeError):
        bank_account.withdrawl("invalidinput")
