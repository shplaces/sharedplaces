import os
import places
import unittest
import tempfile
from coverage import coverage

cov = coverage(branch=True, omit=['templates/*', 'static/*', '/usr/local/*'])
cov.start()

class PlacesTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, places.app.config['DATABASE'] = tempfile.mkstemp()
        places.app.config['TESTING'] = True
        self.app = places.app.test_client()
        with places.app.app_context():
            places.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(places.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Inacreditavel' in rv.data


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
         ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)



    def test_comments(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data



    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data







if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    cov.erase()