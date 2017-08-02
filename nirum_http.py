from nirum.transport import Transport
from nirum.exc import UnexpectedNirumResponseError
from requests import Session
from six import string_types
from six.moves import urllib

__all__ = 'HttpTransport',
__version__ = '0.1.1'


def url_endswith_slash(url):
    if not isinstance(url, string_types):
        raise TypeError('url must be a string, not {0!r}'.format(url))
    scheme, netloc, path, _, _ = urllib.parse.urlsplit(url)
    if not (scheme and netloc):
        raise ValueError("{} isn't URL.".format(url))
    if not path.endswith('/'):
        path += '/'
    return urllib.parse.urlunsplit((scheme, netloc, path, '', ''))


class HttpTransport(Transport):

    def __init__(self, url, session=None):
        if session is None:
            session = Session()
        elif not isinstance(session, Session):
            raise TypeError('session must be {0.__module__}.{0.__name__}, not '
                            '{1!r}'.format(Session, session))
        self.url = url_endswith_slash(url)
        self.session = session

    def call(self,
             method_name,
             payload,
             service_annotations,
             method_annotations,
             parameter_annotations):
        response = self.session.post(
            self.url,
            params={'method': method_name},
            headers={'Accept': 'application/json'},
            json=payload
        )
        try:
            content = response.json()
        except ValueError:
            raise UnexpectedNirumResponseError(
                response.content if isinstance('', bytes) else response.text
            )
        return response.ok, content
