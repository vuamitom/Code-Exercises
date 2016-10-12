# The version of the response info used when persisting response info.
RESPONSE_INFO_VERSION = 3

RESPONSE_INFO_MINIMUM_VERSION = 1

# We reserve up to 8 bits for the version number.
RESPONSE_INFO_VERSION_MASK = 0xFF

# This bit is set if the response info has a cert at the end.
# Version 1 serialized only the end-entity certificate while subsequent
# versions include the available certificate chain.
RESPONSE_INFO_HAS_CERT = 1 << 8

# This bit is set if the response info has a security-bits field (security
# strength in bits of the SSL connection) at the end.
RESPONSE_INFO_HAS_SECURITY_BITS = 1 << 9

# This bit is set if the response info has a cert status at the end.
RESPONSE_INFO_HAS_CERT_STATUS = 1 << 10

# This bit is set if the response info has vary header data.
RESPONSE_INFO_HAS_VARY_DATA = 1 << 11

# This bit is set if the request was cancelled before completion.
RESPONSE_INFO_TRUNCATED = 1 << 12

# This bit is set if the response was received via SPDY.
RESPONSE_INFO_WAS_SPDY = 1 << 13

# This bit is set if the request has NPN negotiated.
RESPONSE_INFO_WAS_NPN = 1 << 14

# This bit is set if the request was fetched via an explicit proxy.
RESPONSE_INFO_WAS_PROXY = 1 << 15

# This bit is set if the response info has an SSL connection status field.
# This contains the ciphersuite used to fetch the resource as well as the
# protocol version compression method and whether SSLv3 fallback was used.
RESPONSE_INFO_HAS_SSL_CONNECTION_STATUS = 1 << 16

# This bit is set if the response info has protocol version.
RESPONSE_INFO_HAS_NPN_NEGOTIATED_PROTOCOL = 1 << 17

# This bit is set if the response info has connection info.
RESPONSE_INFO_HAS_CONNECTION_INFO = 1 << 18

# This bit is set if the request has http authentication.
RESPONSE_INFO_USE_HTTP_AUTHENTICATION = 1 << 19

# This bit is set if ssl_info has SCTs.
RESPONSE_INFO_HAS_SIGNED_CERTIFICATE_TIMESTAMPS = 1 << 20

RESPONSE_INFO_UNUSED_SINCE_PREFETCH = 1 << 21

# This bit is set if the response has a key-exchange-info field at the end.
RESPONSE_INFO_HAS_KEY_EXCHANGE_INFO = 1 << 22

# TODO(darin): Add other bits to indicate alternate request methods.
# For now we don't support storing those.
