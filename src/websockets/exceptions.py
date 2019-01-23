import http
from typing import TYPE_CHECKING, Any, Optional

from .http import Headers, HeadersLike


if TYPE_CHECKING:  # pragma: no cover
    from .uri import WebSocketURI
else:
    WebSocketURI = Any


__all__ = [
    "AbortHandshake",
    "ConnectionClosed",
    "DuplicateParameter",
    "InvalidHandshake",
    "InvalidHeader",
    "InvalidHeaderFormat",
    "InvalidHeaderValue",
    "InvalidMessage",
    "InvalidOrigin",
    "InvalidParameterName",
    "InvalidParameterValue",
    "InvalidState",
    "InvalidStatusCode",
    "InvalidUpgrade",
    "InvalidURI",
    "NegotiationError",
    "PayloadTooBig",
    "WebSocketProtocolError",
]


class InvalidHandshake(Exception):
    """
    Exception raised when a handshake request or response is invalid.

    """


class AbortHandshake(InvalidHandshake):
    """
    Exception raised to abort a handshake and return a HTTP response.

    """

    def __init__(
        self, status: http.HTTPStatus, headers: HeadersLike, body: bytes = b""
    ) -> None:
        self.status = status
        self.headers = Headers(headers)
        self.body = body
        message = "HTTP {}, {} headers, {} bytes".format(
            self.status, len(self.headers), len(self.body)
        )
        super().__init__(message)


class RedirectHandshake(InvalidHandshake):
    """
    Exception raised when a handshake gets redirected.

    """

    def __init__(self, wsuri: WebSocketURI) -> None:
        self.wsuri = wsuri


class InvalidMessage(InvalidHandshake):
    """
    Exception raised when the HTTP message in a handshake request is malformed.

    """


class InvalidHeader(InvalidHandshake):
    """
    Exception raised when a HTTP header doesn't have a valid format or value.

    """

    def __init__(self, name: str, value: Optional[str] = None) -> None:
        if value is None:
            message = "Missing {} header".format(name)
        elif value == "":
            message = "Empty {} header".format(name)
        else:
            message = "Invalid {} header: {}".format(name, value)
        super().__init__(message)


class InvalidHeaderFormat(InvalidHeader):
    """
    Exception raised when a Sec-WebSocket-* HTTP header cannot be parsed.

    """

    def __init__(self, name: str, error: str, string: str, pos: int) -> None:
        error = "{} at {} in {}".format(error, pos, string)
        super().__init__(name, error)


class InvalidHeaderValue(InvalidHeader):
    """
    Exception raised when a Sec-WebSocket-* HTTP header has a wrong value.

    """


class InvalidUpgrade(InvalidHeader):
    """
    Exception raised when a Upgrade or Connection header isn't correct.

    """


class InvalidOrigin(InvalidHeader):
    """
    Exception raised when the Origin header in a request isn't allowed.

    """

    def __init__(self, origin: Optional[str]) -> None:
        super().__init__("Origin", origin)


class InvalidStatusCode(InvalidHandshake):
    """
    Exception raised when a handshake response status code is invalid.

    Provides the integer status code in its ``status_code`` attribute.

    """

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        message = "Status code not 101: {}".format(status_code)
        super().__init__(message)


class NegotiationError(InvalidHandshake):
    """
    Exception raised when negotiating an extension fails.

    """


class InvalidParameterName(NegotiationError):
    """
    Exception raised when a parameter name in an extension header is invalid.

    """

    def __init__(self, name: str) -> None:
        self.name = name
        message = "Invalid parameter name: {}".format(name)
        super().__init__(message)


class InvalidParameterValue(NegotiationError):
    """
    Exception raised when a parameter value in an extension header is invalid.

    """

    def __init__(self, name: str, value: Optional[str]) -> None:
        self.name = name
        self.value = value
        message = "Invalid value for parameter {}: {}".format(name, value)
        super().__init__(message)


class DuplicateParameter(NegotiationError):
    """
    Exception raised when a parameter name is repeated in an extension header.

    """

    def __init__(self, name: str) -> None:
        self.name = name
        message = "Duplicate parameter: {}".format(name)
        super().__init__(message)


class InvalidState(Exception):
    """
    Exception raised when an operation is forbidden in the current state.

    """


CLOSE_CODES = {
    1000: "OK",
    1001: "going away",
    1002: "protocol error",
    1003: "unsupported type",
    # 1004 is reserved
    1005: "no status code [internal]",
    1006: "connection closed abnormally [internal]",
    1007: "invalid data",
    1008: "policy violation",
    1009: "message too big",
    1010: "extension required",
    1011: "unexpected error",
    1015: "TLS failure [internal]",
}


def format_close(code: int, reason: str) -> str:
    """
    Display a human-readable version of the close code and reason.


    """
    if 3000 <= code < 4000:
        explanation = "registered"
    elif 4000 <= code < 5000:
        explanation = "private use"
    else:
        explanation = CLOSE_CODES.get(code, "unknown")
    result = "code = {} ({}), ".format(code, explanation)

    if reason:
        result += "reason = {}".format(reason)
    else:
        result += "no reason"

    return result


class ConnectionClosed(InvalidState):
    """
    Exception raised when trying to read or write on a closed connection.

    Provides the connection close code and reason in its ``code`` and
    ``reason`` attributes respectively.

    """

    def __init__(self, code: int, reason: str) -> None:
        self.code = code
        self.reason = reason
        message = "WebSocket connection is closed: "
        message += format_close(code, reason)
        super().__init__(message)


class InvalidURI(Exception):
    """
    Exception raised when an URI isn't a valid websocket URI.

    """

    def __init__(self, uri: str) -> None:
        self.uri = uri
        message = "{} isn't a valid URI".format(uri)
        super().__init__(message)


class PayloadTooBig(Exception):
    """
    Exception raised when a frame's payload exceeds the maximum size.

    """


class WebSocketProtocolError(Exception):
    """
    Internal exception raised when the remote side breaks the protocol.

    """
