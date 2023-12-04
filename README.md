## Payment Analysis System ReadMe

### Overview
Welcome to the Payment Analysis System, a project designed to provide a streamlined approach to tracking and analyzing your expenditures. This system integrates seamlessly with your UPI system, allowing you to make payments through a QR code and simultaneously collect data for expenditure analysis.

### Features
1. Payment through QR Code:
    - Utilize the barcode scanner to scan QR codes.
    - Enter the payment amount and a brief description.
    - Submit the payment details to the backend for tracking.

2. Expenditure Analysis:
    - Access a user-friendly interface to analyze your expenditure.
    - Leverage a fast-text NLP model to categorize payments (e.g., travel, medicine, food).
    - View categorized expenditures and track spending patterns over time.
    - Select date ranges for detailed analysis between specific periods.

3. SQL Backend:
    - A robust SQL backend stores essential payment information.
    - Fields include the date of the payment, category of payment, and amount.
    - Facilitates efficient retrieval and management of payment data.

### Installation

Follow these steps to set up the project locally:
1. Clone the Repository:
    - Extract the zip file from the GitHub repository to your local machine.

2. Activate Virtual Environment:
    On Windows: `env\Scripts\activate`
    On macOS/Linux: `source venv/bin/activate`

3. Run the Server:
    Execute the following command to run the Python server:
    ```bash
    python app.py
    ```
4. Enjoy:
    - A sample qr code is added. Download this on your phone so that you scan it through your laptop. 
    - Open your preferred web browser and navigate to the provided local address.
    - Explore the payment features and analysis capabilities of the system.

### Important Notes

    NLP Model Limitations:
    The NLP model used for categorizing expenditures is pre-trained and might not be optimal due to a limited dataset.
    Future improvements are planned to enhance its performance.

    Frontend and UI Considerations:

    The project's frontend and UI are part of a prototype and may not be fully polished. 
    Future iterations will focus on improving the user interface.

    Scalability:
    Keep in mind that this version is a prototype, and there are plans to scale the project for broader use in subsequent stages.
    
    Feel free to explore, contribute, and provide feedback for the continuous improvement of the Payment Analysis System. 
    
    Happy analyzing!

