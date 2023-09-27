# Steganography
Steganography is a technique that involves concealing secret information or data within another file, often referred to as the carrier file. 

The above code conceals any file within various carrier file types [text, audio, image, video]

## Installation
```
git clone https://github.com/dhananjaymenon/Steganography.git
```

## Useage
```
python encoder.py --secret <file-name> --carrier <file-name> --output <file-name>

python decoder.py --encoded <encoded-file-name> --decoded <directory-name>
```

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
Space Width type steganography is used. Only ```.txt``` files can be the text carrier.

## Audio
Least Significant Bit in each frame is used to encode message. Only ```.wav``` files can be the audio carrier.

## Image
Least Significant Bit in each channel in each pixel is used to encode message. Only ```.png``` files can be the image carrier.

## Video
Least Significant Bit encoding is done on each frame (Image Encoding on each frame). only ```.mov``` files can be the video carrier.

## Note
Secret media must have extension length == 3. Extensions of length 4 are not allowed.


