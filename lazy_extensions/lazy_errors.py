from .lazyenum import LazyEnum

errors = LazyEnum(
    "Client cannot be verified.",
    "Client is not specified.",
    "Invalid auth token."
)
