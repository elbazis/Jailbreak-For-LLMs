import base64

# Convert string to bytes

message_bytes = message.encode('utf-8')

# Encode bytes to base64
base64_bytes = base64.b64encode(message_bytes)

# Convert base64 bytes back to string
base64_message = base64_bytes.decode('utf-8')

print(base64_message)  # Output: SGVsbG8sIHdvcmxkIQ==


#DECODING
# Convert base64 string to bytes
base64_bytes = base64_message.encode('utf-8')

# Decode base64 to original bytes
message_bytes = base64.b64decode(base64_bytes)

# Convert bytes back to original string
message = message_bytes.decode('utf-8')

print(message)  # Output: Hello, world!
