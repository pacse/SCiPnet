## Fixing the Type Errors

The core issue is a conflict between **runtime flexibility** and **static type checking**. Your overloads promise specific TypedDict types, but the implementation uses generic `dict[str, Any]`. Let me walk you through the fixes.

---

## Problem Analysis

### Issue 1: Overload Signatures vs Implementation

The overloads say:
```python
@overload
def gen_msg(
    msg_type: Literal[MessageTypes.AUTH_REQUEST],
    data: MessageDatas.AuthRequestData  # Specific TypedDict
) -> Messages.AuthRequest: ...
```

But implementation says:
```python
def gen_msg(
    msg_type: str | MessageTypes,
    data: dict[str, Any]  # Generic dict - doesn't match!
) -> Message:
```

**TypedDicts are structurally typed** - a `dict[str, Any]` is NOT assignable to a TypedDict because it could contain anything.

### Issue 2: Return Type

```python
return {
    'type': msg_type.value,
    'data': data
}
```

This returns a plain dict literal, which Pylance doesn't recognize as a TypedDict.

---

## Solution: Two Approaches

### Approach A: Remove Overloads (Simpler)

If you don't need precise type inference at call sites, just use the `Message` union:

````python
# ...existing imports...

from .protocol import (
    MessageTypes, format_map, Messages, MessageDatas,
    Message, MessageData  # Add MessageData import
)

# ...existing code...

# Remove all @overload decorators, just keep the implementation:

def gen_msg(
    msg_type: MessageTypes,
    data: MessageData
) -> Message:
    """
    Generates a generic message

    Parameters
    ----------
    msg_type : MessageTypes
        The message type (enum member)
    data : MessageData
        The message data (must match the expected format for msg_type)

    Returns
    -------
    Message
        The generated message

    Raises
    ------
    TypeError
        - If `msg_type` is not a member of MessageTypes
        - If `data` does not match the expected format for `msg_type`
    """
    # Validate enum (also converts string to enum if needed)
    msg_type = validate_enum('msg_type', msg_type, MessageTypes)

    # Validate data matches expected format
    expected_format = format_map.get(msg_type)
    if expected_format:
        validate_dict('data', data, expected_format)

    # Cast to Message to satisfy type checker
    result: Message = {  # type: ignore[assignment]
        'type': msg_type.value,
        'data': data
    }
    return result
````

**Pros**: Simple, no overload complexity
**Cons**: Callers don't get specific return types; `gen_msg(MessageTypes.AUTH_REQUEST, ...)` returns `Message`, not `AuthRequest`

---

### Approach B: Keep Overloads with Proper Implementation (Recommended)

The key insight: **overloads are for the type checker, the implementation handles runtime**. We need to:

1. Make implementation signature compatible with ALL overloads
2. Use `cast()` or `# type: ignore` for the return

````python
"""
Message builders for socket communication

Contains
--------
- gen_msg (with overloads for type safety)
- gen_auth_request, gen_auth_failed, gen_auth_success
- gen_access_request, gen_access_redacted, gen_access_expunged, gen_access_granted
"""
from typing import Any, overload, Literal, cast

from .protocol import (
    MessageTypes, format_map, Messages, MessageDatas, Message, MessageData
)

from ..general.validation import validate_hex, validate_dict, validate_str, \
                                 validate_int, validate_enum
from ..general.exceptions import arg_error
from ..sql.transformers import Models as PyModels, PydanticBase


# === Main Generator Func ===

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.AUTH_REQUEST],
    data: MessageDatas.AuthRequestData
) -> Messages.AuthRequest: ...

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.AUTH_FAILED],
    data: MessageDatas.AuthFailedData
) -> Messages.AuthFailed: ...

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.AUTH_SUCCESS],
    data: MessageDatas.AuthSuccessData
) -> Messages.AuthSuccess: ...

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.ACCESS_REQUEST],
    data: MessageDatas.AccessRequestData
) -> Messages.AccessRequest: ...

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.ACCESS_REDACTED],
    data: MessageDatas.AccessRedactedData
) -> Messages.AccessRedacted: ...

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.ACCESS_EXPUNGED],
    data: MessageDatas.AccessExpungedData
) -> Messages.AccessExpunged: ...

@overload
def gen_msg(
    msg_type: Literal[MessageTypes.ACCESS_GRANTED],
    data: MessageDatas.AccessGrantedData
) -> Messages.AccessGranted: ...

# Catch-all overload for dynamic usage (e.g., transport.py)
@overload
def gen_msg(
    msg_type: MessageTypes,
    data: MessageData
) -> Message: ...

def gen_msg(
    msg_type: MessageTypes | str,
    data: MessageData | dict[str, Any]
) -> Message:
    """
    Generates a protocol message

    Parameters
    ----------
    msg_type : MessageTypes | str
        The message type (enum member or string value)
    data : MessageData | dict[str, Any]
        The message data

    Returns
    -------
    Message
        The generated message (specific TypedDict based on msg_type)

    Raises
    ------
    FieldError
        - If `msg_type` is not a valid MessageTypes member
        - If `data` does not match the expected format for `msg_type`
    """
    # Convert string to enum if needed
    validated_type = validate_enum('msg_type', msg_type, MessageTypes)

    # Validate data format
    expected_format = format_map.get(validated_type)
    if expected_format:
        validate_dict('data', data, expected_format)

    # Build message - cast needed because dict literal isn't recognized as TypedDict
    return cast(Message, {
        'type': validated_type.value,
        'data': data
    })


# ...existing generator implementations (gen_auth_request, etc.)...
````

**Key changes:**

1. **Added catch-all overload**: `def gen_msg(msg_type: MessageTypes, data: MessageData) -> Message`
   - This allows transport.py to call with dynamic `MessageTypes` values

2. **Implementation signature accepts union**: `MessageTypes | str` and `MessageData | dict[str, Any]`
   - This is compatible with all overloads

3. **Used `cast()`**: Tells type checker "trust me, this dict is a Message"
   - Runtime: no effect
   - Type checking: satisfies return type

---

## Fix for transport.py

With the catch-all overload added, transport.py should work. But the current code has a subtle issue:

````python
# ...existing code...

def send(conn: socket.socket, msg_type: MessageTypes, msg_data: MessageData) -> None:
    """
    Builds a Message from `msg_type` and `msg_data` and sends it over `conn`

    Parameters
    ----------
    conn : socket.socket
        The socket connection to send data over
    msg_type : MessageTypes
        The message type
    msg_data : MessageData
        The message data (must match expected format for msg_type)

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    ValueError
        If `data` is None or empty
    ConnectionError
        If there is an error transmitting data
    """
    # build data - gen_msg handles validation
    data = encode(gen_msg(msg_type, msg_data))

    with socket_context_manager(
        'Error sending data', conn,
    ):
        conn.sendall(data)

# ...existing code...
````

**Change**: `msg_data: dict[str, Any]` → `msg_data: MessageData`

This matches the catch-all overload signature.

---

## Fix for `validate_enum`

Your current implementation looks correct! Let me verify:

````python
# ...existing code...

E = TypeVar('E', bound=Enum)

def validate_enum(
                  field: str,
                  field_val: Any,
                  enum_type: type[E]
                 ) -> E:
    """
    Validates `field_val` is a member of `enum_type`

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : Any
        The value to validate (can be enum member or its value)
    enum_type : type[E]
        The enum class to check against

    Returns
    -------
    E
        The validated enum member

    Raises
    ------
    FieldError
        If `field_val` is not a valid member/value of `enum_type`
    """
    # If already an enum member, return it
    if isinstance(field_val, enum_type):
        return field_val

    # Try to convert from value (e.g., 'auth_request' -> MessageTypes.AUTH_REQUEST)
    try:
        return enum_type(field_val)
    except ValueError as e:
        valid_vals = [m.value for m in enum_type]
        raise field_error(
            field, field_val,
            f'member of {enum_type.__name__} (valid values: {valid_vals})'
        ) from e

# ...existing code...
````

**Added**: Check if already an enum member first, then try conversion.

---

## Fix for `validate_msg`

There's a bug - you're validating `msg` against `expected_format` but `expected_format` is the **data** format, not the **message** format:

````python
# ...existing code...

def validate_msg(
                 msg: dict[str, Any]
                ) -> dict[str, Any]:
    """
    Validates a message has the correct structure and data format

    Parameters
    ----------
    msg : dict[str, Any]
        The message to validate

    Returns
    -------
    dict[str, Any]
        The validated message

    Raises
    ------
    TypeError
        If `msg` is not a dict with str keys
    FieldError
        - If `msg` keys don't match {'type', 'data'}
        - If `msg['type']` is not a valid MessageTypes member
        - If `msg['data']` does not match the expected format
    """
    validate_dict('message', msg)

    if set(msg.keys()) != MESSAGE_KEYS:
        raise field_error(
            'message keys', list(msg.keys()),
            f'keys to match {list(MESSAGE_KEYS)}'
        )

    # Validate type is valid enum member
    msg_type = validate_enum("msg['type']", msg['type'], MessageTypes)

    # Get expected data format for this message type
    expected_format = format_map.get(msg_type)
    if not expected_format:
        raise field_error(
            "msg['type']", msg['type'],
            'valid MessageTypes member with defined format'
        )

    # Validate data matches expected format (not the whole message!)
    validate_dict("msg['data']", msg['data'], expected_format)

    return msg

# ...existing code...
````

**Fix**: Changed `validate_dict('msg', msg, expected_format)` to `validate_dict("msg['data']", msg['data'], expected_format)`

---

## Summary of Changes

| File | Change |
|------|--------|
| builders.py | Add catch-all overload, use `cast()` for return, add `MessageData` import |
| transport.py | Change `msg_data: dict[str, Any]` to `msg_data: MessageData` |
| validation.py | Add enum member check in `validate_enum`, fix `validate_msg` to validate `msg['data']` not `msg` |

---

## Quick Reference: The Fixed Overload Pattern

```python
# Specific overloads for static type checking
@overload
def gen_msg(msg_type: Literal[MessageTypes.AUTH_REQUEST], data: AuthRequestData) -> AuthRequest: ...

# Catch-all for dynamic usage
@overload
def gen_msg(msg_type: MessageTypes, data: MessageData) -> Message: ...

# Implementation accepts everything, validates at runtime
def gen_msg(msg_type: MessageTypes | str, data: MessageData | dict[str, Any]) -> Message:
    # ... validation ...
    return cast(Message, {'type': ..., 'data': ...})
```

This pattern gives you:
- ✅ Precise types when calling with literals: `gen_msg(MessageTypes.AUTH_REQUEST, {...})` → `AuthRequest`
- ✅ Flexibility when calling with variables: `gen_msg(some_type, some_data)` → `Message`
- ✅ Runtime validation regardless of how it's called


Also TODO: get server-client stuff working 😭
