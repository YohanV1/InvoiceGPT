# InvoiceGPT

InvoiceGPT is an intelligent invoice processing solution that leverages GPT-4 Vision for advanced OCR capabilities, allowing automated extraction and interpretation of invoice data. Built with Streamlit, it offers a user-friendly interface for managing financial documents with AI-powered insights.

## Features

- **Advanced OCR Processing**: Utilizes GPT-4 Vision to accurately extract data from any invoice format
- **Secure Storage**: Automated storage of processed data in Amazon S3 and AWS RDS (MySQL)
- **Data Security**: Implements Google Authentication and robust data isolation
- **Natural Language Querying**: AI-powered chatbot interface using LangChain and GPT-4
- **Smart Auto-Splitting**: Intelligent categorization of invoice items across PDF and image formats
- **Analytics Dashboard**: Advanced tools for financial data analysis and insights

## Technology Stack

- Frontend: Streamlit
- AI/ML: GPT-4 Vision, GPT-4o-mini, LangChain
- Storage: Amazon S3, AWS RDS (MySQL)
- Authentication: Google Auth
- OCR: GPT-4 Vision

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/invoicegpt.git
cd invoicegpt
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google OAuth 2.0:

* Go to the Google Cloud Console
* Create a new project or select an existing one
* Enable the Google OAuth2 API
* Go to Credentials > Create Credentials > OAuth Client ID
* Configure the OAuth consent screen
* Create OAuth 2.0 Client ID (Web application type)
* Download the client configuration JSON file
* Rename it to google_creds.json and place it in the root directory

3. Set up environment variables:
```bash
# Create a .env file with the following variables
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Access the application through your web browser at `http://localhost:8501`

3. Log in using your Google account

4. Upload invoices through the user interface

5. Use the chatbot interface to query your invoice data using natural language

## Project Structure

```
invoicegpt/
├── .streamlit/           # Streamlit configuration files
├── database_files/       # Database related files and schemas
├── images/              # Application icons and images
├── navigation_pages/    # Streamlit page navigation files
├── utilities/           # Utility functions and helpers
├── .gitignore          # Git ignore configuration
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
└── main.py             # Main application entry point
```

## Key Features Explained

### Store Invoices
- Centralized document storage
- Secure cloud backup
- Easy access and organization

### Smart Processing
- Advanced OCR technology
- Automated data extraction
- Intelligent interpretation

### Auto-Splitting
- Automatic item categorization
- Support for multiple formats
- Precise allocation of items

### User-Friendly Interface
- Intuitive design
- Accessible to all skill levels
- Streamlined workflow

### AI Querying
- Natural language processing
- Instant response generation
- Detailed financial insights

### Data Insights
- Advanced analytics tools
- Custom reporting
- Business intelligence features

## Security

InvoiceGPT prioritizes data security through:
- Secure Google Authentication
- Data isolation
- AWS S3 encrypted storage
- Secure database connections

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the [MIT License](https://github.com/YohanV1/InvoiceGPT/blob/main/LICENSE)

## Support

For support, please open an issue in the GitHub repository.