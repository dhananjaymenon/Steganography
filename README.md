# Steganography
Steganography is a technique that involves concealing secret information or data within another file, often referred to as the carrier file. 

The above code conceals any file within various carrier file types [text, audio, image, video]

## General technique
### Converting the secret file to a binary string and vice-versa
The secret file is converted to its corresponding Base64 format, which is then converted to binary. This binary string is used for encoding

When decoding, the binary string is converted to its base64 format, which is converted to the secret file. Note that for conversion of Base64 format to the secret file, the extension is required. Hence the extension is sent as metadata through the binary string


### Adding metadata to binary string
It is important to add the length of the binary string to be stored at the beginning of the string. This is necessary for decoding the secret file.

it is not possible to determine the file extension from the Base64-encoded data alone. To determine the file extension or type, you need to have metadata associated with the Base64 string. Hence, the extension is also sent as metadata as it is required for the conversion of Base64 to the secret file.  

### Encoder
The input is:
- Binary string of the base64 format secret file with meta data
- Carrier file
The output is:
- The encoded file that looks similar to the encoded file

### Decoder
The input is:
- the encoded file
The output is:
- The decoded secret file




## Text

## Audio

## Image

## Video

## Conclusion
