# Certificator

Certificator is a web application built with Streamlit that allows you to generate bulk certificates. It's perfect for events, courses, competitions, and more.

## Features

- Generate multiple certificates at once
- Customize the name and coordinates on the certificate
- Download all certificates as a ZIP file

## How to Use

Use the [webversion](https://certificator.streamlit.app/)

#### OR

1. Clone this repository.
2. Install the required Python packages: `pip install -r requirements.txt`
3. Run the app: `streamlit run main.py`
4. Upload your certificate template and a list of names.
5. Adjust the coordinates to position the name correctly on the certificate.
6. Click "Generate" to create the certificates.
7. Download the ZIP file containing all certificates.

## Note

The certificates are temporarily stored in a "certificates" folder, which is automatically deleted after 60 seconds. The ZIP file is also deleted after 60 seconds.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.