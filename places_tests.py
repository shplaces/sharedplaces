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


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
         ), follow_redirects=True)


    def logout(self, username, password):
        self.app.post('/login', data=dict(
            username=username,
            password=password
         ), follow_redirects=True)
        return self.app.get('/logout', follow_redirects=True)


    def add_comment(self, username, password, title, text):
	self.app.post('/login', data=dict(
            username=username,
            password=password
         ), follow_redirects=True)
	return self.app.post('/add', data=dict(
	    title=title, text=text), follow_redirects=True)


    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Inacreditavel' in rv.data


    def test_add_comments(self):
        rv = self.add_comment('admin', 'default', 'testing title', 'testing comment')
        assert 'testing title' in rv.data
        assert 'testing comment' in rv.data


    def test_login(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username or password' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid username or password' in rv.data


    def test_logout(self):
        rv = self.logout('admin', 'default')
        assert 'You were logged out' in rv.data



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
