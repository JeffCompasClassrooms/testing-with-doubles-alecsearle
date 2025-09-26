# 2nd test suite in assignment
# Test all 6 handles in squirrel_server.py

import io
import json
import pytest
from squirrel_server import SquirrelServerHandler
from squirrel_db import SquirrelDB

# use @todo to cause pytest to skip that section
# handy for stubbing things out and then coming back later to finish them.
# @todo is heirarchical, and not sequential. Meaning that
# it will not skip 'peers' of other todos, only children.
todo = pytest.mark.skip(reason='TODO: pending spec')

class FakeRequest():
    def __init__(self, mock_wfile, method, path, body=None):
        self._mock_wfile = mock_wfile
        self._method = method
        self._path = path
        self._body = body

    def sendall(self, x):
        return

    #this is not a 'makefile' like in c++ instead it 'makes' a response file
    def makefile(self, *args, **kwargs):
        if args[0] == 'rb':
            if self._body:
                headers = 'Content-Length: {}\r\n'.format(len(self._body))
                body = self._body
            else:
                headers = ''
                body = ''
            request = bytes('{} {} HTTP/1.0\r\n{}\r\n{}'.format(self._method, self._path, headers, body), 'utf-8')
            return io.BytesIO(request)
        elif args[0] == 'wb':
            return self._mock_wfile

#dummy client and dummy server to pass as params
#when creating SquirrelServerHandler
@pytest.fixture
def dummy_client():
    return ('127.0.0.1', 80)

@pytest.fixture
def dummy_server():
    return None

#a patch for mocking the DB initialize 
# function - this gets called a lot.
@pytest.fixture
def mock_db_init(mocker):
    return mocker.patch.object(SquirrelDB, '__init__', return_value=None)

@pytest.fixture
def mock_db_get_squirrels(mocker, mock_db_init):
    return mocker.patch.object(SquirrelDB, 'getSquirrels', return_value=['squirrel'])


@pytest.fixture
def mock_db_get_squirrel(mocker, mock_db_init):
    return mocker.patch.object(SquirrelDB, 'getSquirrel', return_value='squirrel')

# patch SquirrelServerHandler to make our FakeRequest work correctly
@pytest.fixture(autouse=True)
def patch_wbufsize(mocker):
    mocker.patch.object(SquirrelServerHandler, 'wbufsize', 1)
    mocker.patch.object(SquirrelServerHandler, 'end_headers')


# Fake Requests
@pytest.fixture
def fake_get_squirrels_request(mocker):
    return FakeRequest(mocker.Mock(), 'GET', '/squirrels')

@pytest.fixture
def fake_create_squirrel_request(mocker):
    return FakeRequest(mocker.Mock(), 'POST', '/squirrels', body='name=Chippy&size=small')

@pytest.fixture
def fake_bad_request(mocker):
    return FakeRequest(mocker.Mock(), 'POST', '/squirrels', body='name=Josh&')


#send_response, send_header and end_headers are inherited functions
#from the BaseHTTPRequestHandler. Go look at documentation here:
# https://docs.python.org/3/library/http.server.html
# Seriously. Go look at it. Pay close attention to what wfile is. :o)
# this fixture mocks all of the send____ that we use. 
# It is really just for convenience and cleanliness of code.
@pytest.fixture
def mock_response_methods(mocker):
    mock_send_response = mocker.patch.object(SquirrelServerHandler, 'send_response')
    mock_send_header = mocker.patch.object(SquirrelServerHandler, 'send_header')
    mock_end_headers = mocker.patch.object(SquirrelServerHandler, 'end_headers')
    return mock_send_response, mock_send_header, mock_end_headers


#tests begin here. Your tests should look wildly different. 
# you should begin testing where it makes sense to you.
# 2nd test suite in assignment
# Test all 6 handles in squirrel_server.py

import io
import json
import pytest
from squirrel_server import SquirrelServerHandler
from squirrel_db import SquirrelDB

# use @todo to cause pytest to skip that section
# handy for stubbing things out and then coming back later to finish them.
# @todo is heirarchical, and not sequential. Meaning that
# it will not skip 'peers' of other todos, only children.
todo = pytest.mark.skip(reason='TODO: pending spec')

class FakeRequest():
    def __init__(self, mock_wfile, method, path, body=None):
        self._mock_wfile = mock_wfile
        self._method = method
        self._path = path
        self._body = body

    def sendall(self, x):
        return

    #this is not a 'makefile' like in c++ instead it 'makes' a response file
    def makefile(self, *args, **kwargs):
        if args[0] == 'rb':
            if self._body:
                headers = 'Content-Length: {}\r\n'.format(len(self._body))
                body = self._body
            else:
                headers = ''
                body = ''
            request = bytes('{} {} HTTP/1.0\r\n{}\r\n{}'.format(self._method, self._path, headers, body), 'utf-8')
            return io.BytesIO(request)
        elif args[0] == 'wb':
            return self._mock_wfile

#dummy client and dummy server to pass as params
#when creating SquirrelServerHandler
@pytest.fixture
def dummy_client():
    return ('127.0.0.1', 80)

@pytest.fixture
def dummy_server():
    return None

#a patch for mocking the DB initialize 
# function - this gets called a lot.
@pytest.fixture
def mock_db_init(mocker):
    return mocker.patch.object(SquirrelDB, '__init__', return_value=None)

@pytest.fixture
def mock_db_get_squirrels(mocker, mock_db_init):
    return mocker.patch.object(SquirrelDB, 'getSquirrels', return_value=['squirrel'])

@pytest.fixture
def mock_db_get_squirrel(mocker, mock_db_init):
    return mocker.patch.object(SquirrelDB, 'getSquirrel', return_value='squirrel')

@pytest.fixture
def mock_db_get_squirrel_none(mocker, mock_db_init):
    return mocker.patch.object(SquirrelDB, 'getSquirrel', return_value=None)

# patch SquirrelServerHandler to make our FakeRequest work correctly
@pytest.fixture(autouse=True)
def patch_wbufsize(mocker):
    mocker.patch.object(SquirrelServerHandler, 'wbufsize', 1)
    mocker.patch.object(SquirrelServerHandler, 'end_headers')

# Fake Requests
@pytest.fixture
def fake_get_squirrels_request(mocker):
    return FakeRequest(mocker.Mock(), 'GET', '/squirrels')

@pytest.fixture
def fake_get_squirrel_request(mocker):
    return FakeRequest(mocker.Mock(), 'GET', '/squirrels/1')

@pytest.fixture
def fake_create_squirrel_request(mocker):
    return FakeRequest(mocker.Mock(), 'POST', '/squirrels', body='name=Chippy&size=small')

@pytest.fixture
def fake_update_squirrel_request(mocker):
    return FakeRequest(mocker.Mock(), 'PUT', '/squirrels/1', body='name=UpdatedChippy&size=large')

@pytest.fixture
def fake_delete_squirrel_request(mocker):
    return FakeRequest(mocker.Mock(), 'DELETE', '/squirrels/1')

@pytest.fixture
def fake_bad_request(mocker):
    return FakeRequest(mocker.Mock(), 'POST', '/squirrels', body='name=Josh&')

#send_response, send_header and end_headers are inherited functions
#from the BaseHTTPRequestHandler. Go look at documentation here:
# https://docs.python.org/3/library/http.server.html
# Seriously. Go look at it. Pay close attention to what wfile is. :o)
# this fixture mocks all of the send____ that we use. 
# It is really just for convenience and cleanliness of code.
@pytest.fixture
def mock_response_methods(mocker):
    mock_send_response = mocker.patch.object(SquirrelServerHandler, 'send_response')
    mock_send_header = mocker.patch.object(SquirrelServerHandler, 'send_header')
    mock_end_headers = mocker.patch.object(SquirrelServerHandler, 'end_headers')
    return mock_send_response, mock_send_header, mock_end_headers

@pytest.fixture
def mock_handle404(mocker):
    return mocker.patch.object(SquirrelServerHandler, 'handle404')

#tests begin here
def describe_SquirrelServerHandler():

    def describe_handleSquirrelsIndex():

        def it_calls_db_getSquirrels_method(fake_get_squirrels_request, dummy_client, dummy_server, mock_db_get_squirrels):            
            #do the thing
            SquirrelServerHandler(fake_get_squirrels_request, dummy_client, dummy_server)

            #assert that the thing was done
            mock_db_get_squirrels.assert_called_once()

        def it_sends_200_status_and_json_response(fake_get_squirrels_request, dummy_client, dummy_server, mock_db_get_squirrels, mock_response_methods):
            #setup
            mock_send_response, mock_send_header, mock_end_headers = mock_response_methods
                 
            #do the thing
            SquirrelServerHandler(fake_get_squirrels_request, dummy_client, dummy_server)
            
            #assert methods calls and arguments
            mock_send_response.assert_called_once_with(200)
            mock_send_header.assert_called_once_with("Content-Type", "application/json")

        def it_writes_squirrels_json_to_response(fake_get_squirrels_request, dummy_client, dummy_server, mock_db_get_squirrels):            
            #do the thing
            response = SquirrelServerHandler(fake_get_squirrels_request, dummy_client, dummy_server)
            
            #assert that the write function was called with json data
            response.wfile.write.assert_called_once_with(bytes(json.dumps(['squirrel']), "utf-8"))

    def describe_handleSquirrelsRetrieve():

        def it_calls_db_getSquirrel_with_correct_id(fake_get_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel):
            #do the thing
            SquirrelServerHandler(fake_get_squirrel_request, dummy_client, dummy_server)
            
            #assert that the thing was done
            mock_db_get_squirrel.assert_called_once_with('1')

        def it_sends_200_and_json_when_squirrel_found(fake_get_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel, mock_response_methods):
            #setup
            mock_send_response, mock_send_header, mock_end_headers = mock_response_methods
            
            #do the thing
            SquirrelServerHandler(fake_get_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_send_response.assert_called_once_with(200)
            mock_send_header.assert_called_once_with("Content-Type", "application/json")

        def it_calls_handle404_when_squirrel_not_found(fake_get_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel_none, mock_handle404):
            #do the thing
            SquirrelServerHandler(fake_get_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_handle404.assert_called_once()

    def describe_handleSquirrelsCreate():

        def it_calls_db_createSquirrel_with_request_data(mocker, fake_create_squirrel_request, dummy_client, dummy_server):
            #setup
            mock_db_create_squirrel = mocker.patch.object(SquirrelDB, 'createSquirrel', return_value=None)

            #do the thing
            SquirrelServerHandler(fake_create_squirrel_request, dummy_client, dummy_server)

            #assert the thing was done
            mock_db_create_squirrel.assert_called_once_with('Chippy', 'small')

        def it_sends_201_status_after_creation(mocker, fake_create_squirrel_request, dummy_client, dummy_server, mock_response_methods):
            #setup
            mock_send_response, mock_send_header, mock_end_headers = mock_response_methods
            mocker.patch.object(SquirrelDB, '__init__', return_value=None)
            mocker.patch.object(SquirrelDB, 'createSquirrel', return_value=None)
            
            #do the thing
            SquirrelServerHandler(fake_create_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_send_response.assert_called_once_with(201)

    def describe_handleSquirrelsUpdate():

        def it_calls_db_updateSquirrel_when_squirrel_exists(mocker, fake_update_squirrel_request, dummy_client, dummy_server):
            #setup
            mocker.patch.object(SquirrelDB, '__init__', return_value=None)
            mocker.patch.object(SquirrelDB, 'getSquirrel', return_value={'id': 1, 'name': 'test'})
            mock_db_update_squirrel = mocker.patch.object(SquirrelDB, 'updateSquirrel', return_value=None)
            
            #do the thing
            SquirrelServerHandler(fake_update_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_db_update_squirrel.assert_called_once_with('1', 'UpdatedChippy', 'large')

        def it_sends_204_status_when_update_successful(mocker, fake_update_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel, mock_response_methods):
            #setup
            mock_send_response, mock_send_header, mock_end_headers = mock_response_methods
            mocker.patch.object(SquirrelDB, 'updateSquirrel', return_value=None)
            
            #do the thing
            SquirrelServerHandler(fake_update_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_send_response.assert_called_once_with(204)

        def it_calls_handle404_when_squirrel_not_found_for_update(fake_update_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel_none, mock_handle404):
            #do the thing
            SquirrelServerHandler(fake_update_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_handle404.assert_called_once()

    def describe_handleSquirrelsDelete():

        def it_calls_db_deleteSquirrel_when_squirrel_exists(mocker, fake_delete_squirrel_request, dummy_client, dummy_server):
            #setup
            mocker.patch.object(SquirrelDB, '__init__', return_value=None)
            mocker.patch.object(SquirrelDB, 'getSquirrel', return_value={'id': 1, 'name': 'test'})
            mock_db_delete_squirrel = mocker.patch.object(SquirrelDB, 'deleteSquirrel', return_value=None)
            
            #do the thing
            SquirrelServerHandler(fake_delete_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_db_delete_squirrel.assert_called_once_with('1')

        def it_sends_204_status_when_delete_successful(mocker, fake_delete_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel, mock_response_methods):
            #setup
            mock_send_response, mock_send_header, mock_end_headers = mock_response_methods
            mocker.patch.object(SquirrelDB, 'deleteSquirrel', return_value=None)
            
            #do the thing
            SquirrelServerHandler(fake_delete_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_send_response.assert_called_once_with(204)

        def it_calls_handle404_when_squirrel_not_found_for_delete(fake_delete_squirrel_request, dummy_client, dummy_server, mock_db_get_squirrel_none, mock_handle404):
            #do the thing
            SquirrelServerHandler(fake_delete_squirrel_request, dummy_client, dummy_server)
            
            #assert
            mock_handle404.assert_called_once()

    def describe_handle404():

        def it_sends_404_status_and_text_plain_headers(mocker, dummy_client, dummy_server, mock_response_methods):
            #setup
            mock_send_response, mock_send_header, mock_end_headers = mock_response_methods
            fake_404_request = FakeRequest(mocker.Mock(), 'GET', '/badpath')
            
            #do the thing
            SquirrelServerHandler(fake_404_request, dummy_client, dummy_server)
            
            #assert
            mock_send_response.assert_called_with(404)
            mock_send_header.assert_called_with("Content-Type", "text/plain")

        def it_writes_404_not_found_message_to_response(mocker, dummy_client, dummy_server):
            #setup
            fake_404_request = FakeRequest(mocker.Mock(), 'GET', '/badpath')
            
            #do the thing
            response = SquirrelServerHandler(fake_404_request, dummy_client, dummy_server)
            
            #assert
            response.wfile.write.assert_called_with(bytes("404 Not Found", "utf-8"))