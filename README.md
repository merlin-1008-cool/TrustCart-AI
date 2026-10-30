🛒 TrustCart AI – Smart Shopping Price Comparison & Seller Trust Analysis

Compare Prices. Verify Deals. Shop with Confidence.

TrustCart AI is an intelligent shopping price comparison and seller trust analysis application designed to help consumers make smarter online purchasing decisions.

Online shopping platforms frequently advertise discounts and special offers, but customers often struggle to determine whether a deal genuinely offers value for money.

TrustCart AI addresses this challenge by bringing price comparison, historical price analysis, and seller trust evaluation together in one platform.

🚀 Live Demo

Try the application here:

https://trustcart-ai-dultszgqktk3pvg4k7385k.streamlit.app/

🎯 Project Objectives

* Compare product prices across multiple online shopping platforms.
* Help customers identify the best available prices.
* Analyse historical price movements to evaluate advertised discounts.
* Assess seller credibility using trust indicators.
* Help users identify potentially misleading offers.
* Allow customers to monitor products against their target prices.

✨ Key Features

1. Multi-Platform Price Comparison

Compare product prices across 12 selected online retailers:

1. Amazon India
2. Flipkart
3. Croma
4. Reliance Digital
5. Vijay Sales
6. Tata CLiQ
7. Tata Neu
8. JioMart
9. Snapdeal
10. Meesho
11. Samsung India
12. Myntra

2. Historical Price Analysis

Analyse product price movements over time to help customers understand whether an advertised discount represents a genuine saving.

3. Seller Trust Score

Evaluate seller reliability using available indicators such as:

* Seller verification status
* Customer complaints
* Seller reliability indicators
* Price-related risk signals

4. Smart Deal Evaluation

Help customers distinguish attractive offers from potentially misleading discounts by combining price and seller-related information.

5. Target Price Monitoring

Allow users to specify their desired purchase price and monitor products against their target.

The application is designed to provide notifications when monitored products reach the target price.

🧠 Technology Stack

Technology	Purpose
Python	Core application development
Streamlit	Interactive web application
Pandas	Data processing and analysis
Plotly	Interactive data visualisation
Hashlib	Hashing and supporting application functionality
Git & GitHub	Version control and project hosting
Streamlit Community Cloud	Application deployment

🏗️ Project Architecture

TrustCart-AI/
│
├── app.py
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── price_analysis.py
│   ├── trust_score.py
│   ├── seller_analysis.py
│   │
│   └── connectors/
│
├── tests/
│   └── test_trust_score.py
│
├── data/
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
│
└── README.md

⚙️ Installation and Setup

Clone the repository:

git clone https://github.com/merlin-1008-cool/TrustCart-AI.git

Navigate to the project directory:

cd TrustCart-AI

Create a virtual environment:

python -m venv .venv

Activate the environment:

Mac/Linux:

source .venv/bin/activate

Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

🧪 Testing

Run the automated tests using:

python -m pytest

The project includes seller trust scoring tests and connector registration validation.

🔮 Future Enhancements

* Real-time product price collection through authorised retailer APIs and affiliate integrations.
* Automated six-month historical price tracking.
* Advanced deal authenticity detection.
* Expanded seller reputation analysis.
* Automated target-price notifications.
* AI-powered shopping recommendations.
* Additional retailer integrations.

⚠️ Data Availability

Retailer integrations depend on the availability of authorised APIs, affiliate feeds, and permitted data-access methods.

The 12-retailer connector framework provides the foundation for future integrations. Not all retailers currently provide live product data through the application.

👨‍💻 Developer

Merlin Martina I

Developed as a practical AI-powered shopping intelligence project focused on price transparency, seller reliability, and smarter purchasing decisions.

⸻

⭐ If you find this project interesting, feel free to explore the live application and GitHub repository!
