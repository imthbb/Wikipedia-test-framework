import unittest as ut
import wiki_funcs
import time


class TestingVarious(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        wiki_funcs.set_vars()

    def setUp(self):
        test_name = ut.TestCase.id(self)
        test_name = test_name[test_name.index('.', test_name.index('.') + 1) + 6:]
        with open(wiki_funcs.log_file, 'a') as file:
            file.write(test_name + ' --------------------------------------------v\n')

        self.driver = wiki_funcs.open_browser()
        self.driver.get(wiki_funcs.url)

    def tearDown(self):
        self.driver.close()

    def test_login(self):
        assert wiki_funcs.login(self.driver)

    def test_logout(self):
        assert wiki_funcs.login(self.driver)
        assert wiki_funcs.logout(self.driver)
        time.sleep(.5)
        assert wiki_funcs.login(self.driver)

    # Used primarily for fixing issues, instead of testing:
    def test_watchlist_add(self):
        assert wiki_funcs.login(self.driver)
        assert wiki_funcs.watchlist_add_rmv(self.driver)

    # Used primarily for fixing issues, instead of testing:
    def test_watchlist_rmv(self):
        assert wiki_funcs.login(self.driver)
        assert wiki_funcs.watchlist_add_rmv(self.driver, False)

    def test_watchlist_popup(self):
        assert wiki_funcs.login(self.driver)
        assert wiki_funcs.watchlist_add_rmv(self.driver)
        time.sleep(.35)
        assert wiki_funcs.watchlist_popup(self.driver)
        assert wiki_funcs.watchlist_add_rmv(self.driver, False)
        assert wiki_funcs.watchlist_popup(self.driver)

    # Used primarily for fixing issues, instead of testing:
    def test_change_to_psswd1(self):
        assert wiki_funcs.login(self.driver)
        assert wiki_funcs.change_psswd(self.driver, 0, 1)

    # Used primarily for fixing issues, instead of testing:
    def test_change_to_psswd0(self):
        assert wiki_funcs.login(self.driver, 1)
        assert wiki_funcs.change_psswd(self.driver, 1, 0)

    def test_change_psswd(self):
        assert not wiki_funcs.login(self.driver, 1)
        time.sleep(.6)
        assert wiki_funcs.login(self.driver)
        assert wiki_funcs.change_psswd(self.driver, 0, 1)
        assert wiki_funcs.logout(self.driver)
        assert not wiki_funcs.login(self.driver)
        time.sleep(.6)
        assert wiki_funcs.login(self.driver, 1)
        assert wiki_funcs.change_psswd(self.driver, 1, 0)
        assert wiki_funcs.logout(self.driver)
        assert not wiki_funcs.login(self.driver, 1)
        time.sleep(.6)
        assert wiki_funcs.login(self.driver)


if __name__ == "__main__":
    ut.main()
