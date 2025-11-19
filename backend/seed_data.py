"""Script to seed verified datasets for development."""
from app.database import SessionLocal, engine, Base
from app.models.dataset import User, Dataset
from passlib.context import CryptContext
import random
from copy import deepcopy

# Ensure tables exist when script is executed standalone
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_data():
    db = SessionLocal()
    
    try:
        # Ensure demo users exist
        buyer = db.query(User).filter(User.email == "buyer@example.com").first()
        if not buyer:
            buyer = User(
                email="buyer@example.com",
                username="buyer",
                hashed_password=pwd_context.hash("password123"),
                full_name="John Buyer",
                balance=1000.0
            )
            db.add(buyer)
        
        seller = db.query(User).filter(User.email == "seller@example.com").first()
        if not seller:
            seller = User(
                email="seller@example.com",
                username="seller",
                hashed_password=pwd_context.hash("password123"),
                full_name="Jane Seller",
                is_seller=True,
                balance=0.0
            )
            db.add(seller)
        
        db.commit()
        db.refresh(buyer)
        db.refresh(seller)
        print(f"Buyer ID: {buyer.id}, Seller ID: {seller.id}")
        
        verified_datasets = [
            {
                "title": "World Bank GDP Indicators 1960-2023",
                "description": "GDP, GDP per capita, and growth indicators across all reporting economies.",
                "category": "Economics",
                "tags": ["gdp", "macro", "world-bank", "economics"],
                "price": 59.0,
                "size_mb": 210.5,
                "row_count": 14000,
                "column_count": 12,
                "format": "CSV",
                "sample_data": {"preview": "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD"},
                "metadata": {
                    "source_name": "World Bank",
                    "source_url": "https://datacatalog.worldbank.org/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "IMF Consumer Price Index 1990-2024",
                "description": "Monthly CPI figures from the IMF International Financial Statistics platform.",
                "category": "Economics",
                "tags": ["inflation", "cpi", "imf", "macro"],
                "price": 54.0,
                "size_mb": 180.2,
                "row_count": 20000,
                "column_count": 10,
                "format": "CSV",
                "sample_data": {"preview": "https://data.imf.org/"},
                "metadata": {
                    "source_name": "International Monetary Fund",
                    "source_url": "https://data.imf.org/",
                    "license": "CC BY-NC 4.0",
                    "verified": True
                }
            },
            {
                "title": "NOAA Global Historical Climatology Network Daily",
                "description": "Station-level daily temperature, precipitation, and wind observations worldwide.",
                "category": "Weather",
                "tags": ["noaa", "climate", "temperature", "precipitation"],
                "price": 69.0,
                "size_mb": 820.0,
                "row_count": 25000000,
                "column_count": 9,
                "format": "Parquet",
                "sample_data": {"preview": "https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily"},
                "metadata": {
                    "source_name": "NOAA",
                    "source_url": "https://www.ncei.noaa.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "NASA Earth Observatory Nighttime Lights",
                "description": "Annual VIIRS nighttime lights composites for economic activity analysis.",
                "category": "Remote Sensing",
                "tags": ["nasa", "viirs", "remote-sensing", "nighttime"],
                "price": 95.0,
                "size_mb": 640.0,
                "row_count": 1500,
                "column_count": 6,
                "format": "GeoTIFF",
                "sample_data": {"preview": "https://earthobservatory.nasa.gov/features/NightLights"},
                "metadata": {
                    "source_name": "NASA Earth Observatory",
                    "source_url": "https://earthdata.nasa.gov/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "Johns Hopkins COVID-19 Global Time Series",
                "description": "Daily confirmed, recovered, and fatal COVID-19 cases maintained by CSSE.",
                "category": "Healthcare",
                "tags": ["covid-19", "epidemiology", "public-health"],
                "price": 35.0,
                "size_mb": 95.0,
                "row_count": 500000,
                "column_count": 8,
                "format": "CSV",
                "sample_data": {"preview": "https://github.com/CSSEGISandData/COVID-19"},
                "metadata": {
                    "source_name": "Johns Hopkins CSSE",
                    "source_url": "https://github.com/CSSEGISandData/COVID-19",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "WHO Tuberculosis Surveillance 2000-2023",
                "description": "Country-level TB incidence, prevalence, and treatment indicators from WHO.",
                "category": "Healthcare",
                "tags": ["who", "tuberculosis", "health"],
                "price": 42.0,
                "size_mb": 65.0,
                "row_count": 3500,
                "column_count": 18,
                "format": "CSV",
                "sample_data": {"preview": "https://www.who.int/teams/global-tuberculosis-programme/data"},
                "metadata": {
                    "source_name": "World Health Organization",
                    "source_url": "https://www.who.int/data",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "FAOSTAT Global Crop Production 1961-2022",
                "description": "Yield, harvested area, and production volumes for 200+ crops worldwide.",
                "category": "Agriculture",
                "tags": ["agriculture", "faostat", "crops"],
                "price": 58.0,
                "size_mb": 320.0,
                "row_count": 600000,
                "column_count": 14,
                "format": "CSV",
                "sample_data": {"preview": "https://www.fao.org/faostat"},
                "metadata": {
                    "source_name": "FAO",
                    "source_url": "https://www.fao.org/faostat/en/",
                    "license": "CC BY-NC-SA 3.0",
                    "verified": True
                }
            },
            {
                "title": "USDA Food Availability Data System",
                "description": "Per capita food availability and loss-adjusted consumption for the US.",
                "category": "Food",
                "tags": ["usda", "nutrition", "food"],
                "price": 28.0,
                "size_mb": 52.0,
                "row_count": 12000,
                "column_count": 20,
                "format": "CSV",
                "sample_data": {"preview": "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system"},
                "metadata": {
                    "source_name": "USDA ERS",
                    "source_url": "https://www.ers.usda.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "UN Population Prospects 2022 Revision",
                "description": "Population estimates and projections by age, sex, and country through 2100.",
                "category": "Demographics",
                "tags": ["un", "population", "demographics"],
                "price": 47.0,
                "size_mb": 140.0,
                "row_count": 80000,
                "column_count": 22,
                "format": "CSV",
                "sample_data": {"preview": "https://population.un.org/wpp"},
                "metadata": {
                    "source_name": "United Nations DESA",
                    "source_url": "https://population.un.org/wpp",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "Eurostat Urban Air Quality Measurements",
                "description": "Hourly PM10, PM2.5, NO2, and O3 readings from EU monitoring stations.",
                "category": "Environment",
                "tags": ["air-quality", "eurostat", "pm25"],
                "price": 64.0,
                "size_mb": 410.0,
                "row_count": 12000000,
                "column_count": 11,
                "format": "Parquet",
                "sample_data": {"preview": "https://ec.europa.eu/eurostat"},
                "metadata": {
                    "source_name": "Eurostat",
                    "source_url": "https://ec.europa.eu/eurostat",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "EPA PM2.5 Historical Monitoring Network",
                "description": "US EPA Air Quality System PM2.5 readings from 2000 onward.",
                "category": "Environment",
                "tags": ["epa", "air-quality", "pm25"],
                "price": 52.0,
                "size_mb": 360.0,
                "row_count": 9000000,
                "column_count": 12,
                "format": "CSV",
                "sample_data": {"preview": "https://www.epa.gov/outdoor-air-quality-data"},
                "metadata": {
                    "source_name": "US EPA",
                    "source_url": "https://aqs.epa.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "Global Power Plant Database v1.3",
                "description": "Location, capacity, generation, and fuel information for global power plants.",
                "category": "Energy",
                "tags": ["energy", "power", "wri"],
                "price": 73.0,
                "size_mb": 110.0,
                "row_count": 34000,
                "column_count": 27,
                "format": "CSV",
                "sample_data": {"preview": "https://datasets.wri.org/dataset/globalpowerplantdatabase"},
                "metadata": {
                    "source_name": "World Resources Institute",
                    "source_url": "https://www.wri.org/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "OpenStreetMap Road Network North America",
                "description": "Major and minor roads with geometry and classifications across North America.",
                "category": "Transportation",
                "tags": ["osm", "roads", "transport"],
                "price": 85.0,
                "size_mb": 950.0,
                "row_count": 15000000,
                "column_count": 14,
                "format": "GeoJSON",
                "sample_data": {"preview": "https://download.geofabrik.de/"},
                "metadata": {
                    "source_name": "OpenStreetMap",
                    "source_url": "https://planet.openstreetmap.org/",
                    "license": "ODbL",
                    "verified": True
                }
            },
            {
                "title": "NYC Taxi & Limousine Trips 2023",
                "description": "Trip-level pickup and drop-off events for New York City taxi fleets.",
                "category": "Transportation",
                "tags": ["nyc", "taxi", "mobility"],
                "price": 45.0,
                "size_mb": 780.0,
                "row_count": 150000000,
                "column_count": 17,
                "format": "Parquet",
                "sample_data": {"preview": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"},
                "metadata": {
                    "source_name": "NYC TLC",
                    "source_url": "https://www1.nyc.gov/site/tlc",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "Chicago Crime Data 2010-2024",
                "description": "Incident-level crime reports with geocodes from the City of Chicago.",
                "category": "Public Safety",
                "tags": ["crime", "chicago", "public-safety"],
                "price": 32.0,
                "size_mb": 210.0,
                "row_count": 8000000,
                "column_count": 22,
                "format": "CSV",
                "sample_data": {"preview": "https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present"},
                "metadata": {
                    "source_name": "City of Chicago",
                    "source_url": "https://data.cityofchicago.org/",
                    "license": "CC0",
                    "verified": True
                }
            },
            {
                "title": "US Census ACS 5-Year Demographic Profiles",
                "description": "ACS summary tables with population, income, housing, and education metrics.",
                "category": "Demographics",
                "tags": ["census", "acs", "usa"],
                "price": 66.0,
                "size_mb": 520.0,
                "row_count": 4000000,
                "column_count": 100,
                "format": "CSV",
                "sample_data": {"preview": "https://www.census.gov/data/developers/data-sets/acs-5year.html"},
                "metadata": {
                    "source_name": "US Census Bureau",
                    "source_url": "https://data.census.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "World Tourism Organization International Arrivals",
                "description": "Monthly inbound tourism arrivals and receipts for 180+ destinations.",
                "category": "Tourism",
                "tags": ["tourism", "unwto", "travel"],
                "price": 38.0,
                "size_mb": 75.0,
                "row_count": 12000,
                "column_count": 16,
                "format": "CSV",
                "sample_data": {"preview": "https://www.unwto.org/statistics"},
                "metadata": {
                    "source_name": "UNWTO",
                    "source_url": "https://www.unwto.org/",
                    "license": "CC BY-NC-SA 3.0",
                    "verified": True
                }
            },
            {
                "title": "OECD Education Statistics",
                "description": "Enrollment, attainment, and expenditure indicators across OECD members.",
                "category": "Education",
                "tags": ["oecd", "education", "enrollment"],
                "price": 51.0,
                "size_mb": 165.0,
                "row_count": 45000,
                "column_count": 32,
                "format": "CSV",
                "sample_data": {"preview": "https://stats.oecd.org/"},
                "metadata": {
                    "source_name": "OECD",
                    "source_url": "https://stats.oecd.org/",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "Kaggle House Prices Advanced Regression",
                "description": "Residential property features and sale prices from Ames, Iowa for modeling.",
                "category": "Real Estate",
                "tags": ["housing", "kaggle", "regression"],
                "price": 27.0,
                "size_mb": 3.0,
                "row_count": 2919,
                "column_count": 81,
                "format": "CSV",
                "sample_data": {"preview": "https://www.kaggle.com/c/house-prices-advanced-regression-techniques"},
                "metadata": {
                    "source_name": "Kaggle",
                    "source_url": "https://www.kaggle.com/",
                    "license": "CC0",
                    "verified": True
                }
            },
            {
                "title": "Zillow Home Value Index (ZHVI)",
                "description": "Smoothed home value index per region across the United States.",
                "category": "Real Estate",
                "tags": ["zillow", "housing", "valuation"],
                "price": 44.0,
                "size_mb": 88.0,
                "row_count": 60000,
                "column_count": 20,
                "format": "CSV",
                "sample_data": {"preview": "https://www.zillow.com/research/data/"},
                "metadata": {
                    "source_name": "Zillow",
                    "source_url": "https://www.zillow.com/research/data/",
                    "license": "Open Data",
                    "verified": True
                }
            },
            {
                "title": "Lending Club Loan Data 2007-2020",
                "description": "Credit profiles, loan performance, and payment histories from LendingClub.",
                "category": "Finance",
                "tags": ["loans", "credit", "risk"],
                "price": 62.0,
                "size_mb": 420.0,
                "row_count": 2300000,
                "column_count": 145,
                "format": "CSV",
                "sample_data": {"preview": "https://www.kaggle.com/datasets/wordsforthewise/lending-club"},
                "metadata": {
                    "source_name": "LendingClub",
                    "source_url": "https://www.lendingclub.com/info/download-data.action",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "World Bank Global Findex 2021",
                "description": "Financial inclusion indicators covering savings, credit, and digital payments.",
                "category": "Finance",
                "tags": ["findex", "financial-inclusion", "world-bank"],
                "price": 33.0,
                "size_mb": 40.0,
                "row_count": 1500,
                "column_count": 60,
                "format": "CSV",
                "sample_data": {"preview": "https://globalfindex.worldbank.org/"},
                "metadata": {
                    "source_name": "World Bank",
                    "source_url": "https://globalfindex.worldbank.org/",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "UN Comtrade International Trade Flows",
                "description": "Bilateral import and export values classified by HS codes since 2000.",
                "category": "Economics",
                "tags": ["trade", "un", "comtrade"],
                "price": 76.0,
                "size_mb": 550.0,
                "row_count": 18000000,
                "column_count": 10,
                "format": "CSV",
                "sample_data": {"preview": "https://comtradeplus.un.org/"},
                "metadata": {
                    "source_name": "UN Comtrade",
                    "source_url": "https://comtrade.un.org/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "WRI Aqueduct Water Risk Atlas",
                "description": "Baseline water stress, seasonal variability, and future projections globally.",
                "category": "Environment",
                "tags": ["water", "risk", "wri"],
                "price": 63.0,
                "size_mb": 135.0,
                "row_count": 120000,
                "column_count": 25,
                "format": "CSV",
                "sample_data": {"preview": "https://www.wri.org/data/aqueduct-water-risk-atlas"},
                "metadata": {
                    "source_name": "World Resources Institute",
                    "source_url": "https://www.wri.org/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "Global Fishing Watch Activity Heatmaps",
                "description": "Satellite-inferred commercial fishing effort across global EEZs.",
                "category": "Environment",
                "tags": ["fishing", "oceans", "satellite"],
                "price": 70.0,
                "size_mb": 500.0,
                "row_count": 2500000,
                "column_count": 15,
                "format": "Parquet",
                "sample_data": {"preview": "https://globalfishingwatch.org/datasets-and-code/"},
                "metadata": {
                    "source_name": "Global Fishing Watch",
                    "source_url": "https://globalfishingwatch.org/",
                    "license": "CC BY-NC 4.0",
                    "verified": True
                }
            },
            {
                "title": "Airbnb Global Listings Snapshot 2024",
                "description": "Short-term rental listings with host, location, and pricing details worldwide.",
                "category": "Hospitality",
                "tags": ["airbnb", "hospitality", "rentals"],
                "price": 68.0,
                "size_mb": 620.0,
                "row_count": 7000000,
                "column_count": 75,
                "format": "CSV",
                "sample_data": {"preview": "https://insideairbnb.com/get-the-data/"},
                "metadata": {
                    "source_name": "Inside Airbnb",
                    "source_url": "https://insideairbnb.com/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "Spotify Top Tracks Audio Features",
                "description": "Audio attributes such as danceability, energy, and tempo for top tracks.",
                "category": "Media",
                "tags": ["spotify", "audio", "music"],
                "price": 31.0,
                "size_mb": 22.0,
                "row_count": 50000,
                "column_count": 17,
                "format": "JSON",
                "sample_data": {"preview": "https://developer.spotify.com/documentation/web-api"},
                "metadata": {
                    "source_name": "Spotify",
                    "source_url": "https://spotify.github.io/web-api/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "IMDb Movies Metadata 2024",
                "description": "Movie runtimes, genres, cast counts, and ratings from IMDb non-commercial datasets.",
                "category": "Media",
                "tags": ["imdb", "movies", "entertainment"],
                "price": 36.0,
                "size_mb": 185.0,
                "row_count": 900000,
                "column_count": 14,
                "format": "TSV",
                "sample_data": {"preview": "https://datasets.imdbws.com/"},
                "metadata": {
                    "source_name": "IMDb",
                    "source_url": "https://www.imdb.com/interfaces/",
                    "license": "CC BY-NC 4.0",
                    "verified": True
                }
            },
            {
                "title": "Stack Overflow Developer Survey 2024",
                "description": "Developer demographics, technologies, and job satisfaction insights.",
                "category": "Technology",
                "tags": ["stack-overflow", "developers", "survey"],
                "price": 29.0,
                "size_mb": 48.0,
                "row_count": 90000,
                "column_count": 75,
                "format": "CSV",
                "sample_data": {"preview": "https://insights.stackoverflow.com/survey"},
                "metadata": {
                    "source_name": "Stack Overflow",
                    "source_url": "https://insights.stackoverflow.com/survey",
                    "license": "CC BY-SA 4.0",
                    "verified": True
                }
            },
            {
                "title": "GitHub Public Repositories Metrics",
                "description": "Repository stars, forks, languages, and contributor counts via GH Archive.",
                "category": "Technology",
                "tags": ["github", "open-source", "repos"],
                "price": 57.0,
                "size_mb": 700.0,
                "row_count": 12000000,
                "column_count": 18,
                "format": "Parquet",
                "sample_data": {"preview": "https://www.gharchive.org/"},
                "metadata": {
                    "source_name": "GH Archive",
                    "source_url": "https://www.gharchive.org/",
                    "license": "CC0",
                    "verified": True
                }
            },
            {
                "title": "Kaggle Credit Card Fraud Detection",
                "description": "European credit card transactions labeled for fraud detection tasks.",
                "category": "Finance",
                "tags": ["fraud", "credit-card", "anomaly"],
                "price": 34.0,
                "size_mb": 150.0,
                "row_count": 284807,
                "column_count": 31,
                "format": "CSV",
                "sample_data": {"preview": "https://www.kaggle.com/mlg-ulb/creditcardfraud"},
                "metadata": {
                    "source_name": "Université Libre de Bruxelles",
                    "source_url": "https://www.kaggle.com/",
                    "license": "CC BY-SA 4.0",
                    "verified": True
                }
            },
            {
                "title": "MIMIC-IV Clinical Outcomes Summary",
                "description": "De-identified ICU stay summaries aggregated for modeling outcomes (non-PHI).",
                "category": "Healthcare",
                "tags": ["mimic", "icu", "health"],
                "price": 83.0,
                "size_mb": 240.0,
                "row_count": 200000,
                "column_count": 40,
                "format": "CSV",
                "sample_data": {"preview": "https://physionet.org/content/mimiciv/"},
                "metadata": {
                    "source_name": "MIT PhysioNet",
                    "source_url": "https://physionet.org/",
                    "license": "PhysioNet Credentialed",
                    "verified": True
                }
            },
            {
                "title": "CDC BRFSS Core Indicators",
                "description": "Behavioral Risk Factor Surveillance System prevalence estimates by state.",
                "category": "Healthcare",
                "tags": ["cdc", "brfss", "public-health"],
                "price": 39.0,
                "size_mb": 95.0,
                "row_count": 120000,
                "column_count": 35,
                "format": "CSV",
                "sample_data": {"preview": "https://www.cdc.gov/brfss/annual_data/annual_data.htm"},
                "metadata": {
                    "source_name": "Centers for Disease Control and Prevention",
                    "source_url": "https://www.cdc.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "OECD Better Life Index Scores",
                "description": "Well-being scores across housing, income, jobs, community, and more.",
                "category": "Society",
                "tags": ["oecd", "wellbeing", "bli"],
                "price": 26.0,
                "size_mb": 18.0,
                "row_count": 360,
                "column_count": 24,
                "format": "CSV",
                "sample_data": {"preview": "https://stats.oecd.org/Index.aspx?DataSetCode=BLI"},
                "metadata": {
                    "source_name": "OECD",
                    "source_url": "https://stats.oecd.org/",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "World Bank Doing Business Historical Indicators",
                "description": "Ease of doing business metrics including starting a business and credit.",
                "category": "Economics",
                "tags": ["business", "regulation", "world-bank"],
                "price": 41.0,
                "size_mb": 60.0,
                "row_count": 1200,
                "column_count": 45,
                "format": "CSV",
                "sample_data": {"preview": "https://www.doingbusiness.org/"},
                "metadata": {
                    "source_name": "World Bank",
                    "source_url": "https://www.worldbank.org/",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "UNESCO World Heritage Sites Inventory",
                "description": "Official list of World Heritage cultural and natural sites with attributes.",
                "category": "Culture",
                "tags": ["unesco", "heritage", "culture"],
                "price": 24.0,
                "size_mb": 12.0,
                "row_count": 1157,
                "column_count": 20,
                "format": "CSV",
                "sample_data": {"preview": "https://whc.unesco.org/en/list/"},
                "metadata": {
                    "source_name": "UNESCO",
                    "source_url": "https://whc.unesco.org/",
                    "license": "CC BY-SA 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "Retail Demand Forecasting Kaggle Challenge",
                "description": "Four-year transactional sales history across multiple retail outlets.",
                "category": "Retail",
                "tags": ["retail", "demand", "forecast"],
                "price": 48.0,
                "size_mb": 280.0,
                "row_count": 1250000,
                "column_count": 12,
                "format": "CSV",
                "sample_data": {"preview": "https://www.kaggle.com/competitions/m5-forecasting-accuracy"},
                "metadata": {
                    "source_name": "Kaggle",
                    "source_url": "https://www.kaggle.com/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "NOAA Storm Events Database",
                "description": "Tornadoes, hail, hurricanes, and severe weather events across the US.",
                "category": "Weather",
                "tags": ["noaa", "storms", "severe-weather"],
                "price": 46.0,
                "size_mb": 215.0,
                "row_count": 1800000,
                "column_count": 50,
                "format": "CSV",
                "sample_data": {"preview": "https://www.ncdc.noaa.gov/stormevents/"},
                "metadata": {
                    "source_name": "NOAA",
                    "source_url": "https://www.ncdc.noaa.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "Copernicus Land Surface Temperature (LST)",
                "description": "Sentinel-3 derived land surface temperature tiles for global coverage.",
                "category": "Remote Sensing",
                "tags": ["copernicus", "lst", "satellite"],
                "price": 87.0,
                "size_mb": 780.0,
                "row_count": 120000,
                "column_count": 8,
                "format": "NetCDF",
                "sample_data": {"preview": "https://cds.climate.copernicus.eu/#!/search?text=LST"},
                "metadata": {
                    "source_name": "Copernicus Climate Data Store",
                    "source_url": "https://cds.climate.copernicus.eu/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "Global Wind Atlas Measurements",
                "description": "High-resolution modeled wind speed and direction metrics at multiple heights.",
                "category": "Energy",
                "tags": ["wind", "renewables", "energy"],
                "price": 72.0,
                "size_mb": 340.0,
                "row_count": 800000,
                "column_count": 18,
                "format": "GeoTIFF",
                "sample_data": {"preview": "https://globalwindatlas.info/"},
                "metadata": {
                    "source_name": "Global Wind Atlas",
                    "source_url": "https://globalwindatlas.info/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "OpenFIGI Securities Reference Snapshot",
                "description": "Mappings between tickers, FIGIs, and exchanges for liquid securities.",
                "category": "Finance",
                "tags": ["figi", "securities", "reference"],
                "price": 79.0,
                "size_mb": 190.0,
                "row_count": 250000,
                "column_count": 25,
                "format": "CSV",
                "sample_data": {"preview": "https://www.openfigi.com/"},
                "metadata": {
                    "source_name": "Bloomberg OpenFIGI",
                    "source_url": "https://www.openfigi.com/",
                    "license": "Open Data",
                    "verified": True
                }
            },
            {
                "title": "CoinMetrics Bitcoin Market Data",
                "description": "Daily OHLC, volume, active addresses, and velocity metrics for Bitcoin.",
                "category": "Finance",
                "tags": ["bitcoin", "crypto", "markets"],
                "price": 53.0,
                "size_mb": 105.0,
                "row_count": 5000,
                "column_count": 20,
                "format": "CSV",
                "sample_data": {"preview": "https://coinmetrics.io/community-network-data/"},
                "metadata": {
                    "source_name": "CoinMetrics",
                    "source_url": "https://coinmetrics.io/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "DeFiLlama Ethereum Protocol Metrics",
                "description": "Total value locked, volumes, and fees across major Ethereum DeFi protocols.",
                "category": "Finance",
                "tags": ["defi", "ethereum", "blockchain"],
                "price": 49.0,
                "size_mb": 130.0,
                "row_count": 45000,
                "column_count": 15,
                "format": "CSV",
                "sample_data": {"preview": "https://defillama.com/"},
                "metadata": {
                    "source_name": "DeFiLlama",
                    "source_url": "https://defillama.com/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "USDA Farmers Market Directory",
                "description": "Locations, operating seasons, and product offerings of US farmers markets.",
                "category": "Food",
                "tags": ["usda", "markets", "agriculture"],
                "price": 22.0,
                "size_mb": 18.0,
                "row_count": 8600,
                "column_count": 25,
                "format": "CSV",
                "sample_data": {"preview": "https://www.ams.usda.gov/local-food-directories/farmersmarkets"},
                "metadata": {
                    "source_name": "USDA AMS",
                    "source_url": "https://www.ams.usda.gov/",
                    "license": "Public Domain",
                    "verified": True
                }
            },
            {
                "title": "FAO Food Price Index Monthly",
                "description": "International prices for cereal, vegetable oil, dairy, meat, and sugar indices.",
                "category": "Food",
                "tags": ["fao", "prices", "food"],
                "price": 30.0,
                "size_mb": 15.0,
                "row_count": 900,
                "column_count": 12,
                "format": "CSV",
                "sample_data": {"preview": "https://www.fao.org/worldfoodsituation/foodpricesindex"},
                "metadata": {
                    "source_name": "FAO",
                    "source_url": "https://www.fao.org/",
                    "license": "CC BY-NC-SA 3.0",
                    "verified": True
                }
            },
            {
                "title": "IEA CO2 Emissions by Sector",
                "description": "Energy-related CO2 emissions broken down by sector and fuel.",
                "category": "Energy",
                "tags": ["iea", "co2", "emissions"],
                "price": 82.0,
                "size_mb": 210.0,
                "row_count": 24000,
                "column_count": 30,
                "format": "CSV",
                "sample_data": {"preview": "https://www.iea.org/data-and-statistics"},
                "metadata": {
                    "source_name": "International Energy Agency",
                    "source_url": "https://www.iea.org/",
                    "license": "IEA Terms",
                    "verified": True
                }
            },
            {
                "title": "World Bank Logistics Performance Index",
                "description": "Customs, infrastructure, tracking, and timeliness scores for logistics.",
                "category": "Logistics",
                "tags": ["logistics", "world-bank", "performance"],
                "price": 37.0,
                "size_mb": 28.0,
                "row_count": 800,
                "column_count": 20,
                "format": "CSV",
                "sample_data": {"preview": "https://lpi.worldbank.org/"},
                "metadata": {
                    "source_name": "World Bank",
                    "source_url": "https://lpi.worldbank.org/",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "ITU Global ICT Indicators",
                "description": "Internet penetration, mobile subscriptions, and ICT development indices.",
                "category": "Technology",
                "tags": ["itu", "ict", "connectivity"],
                "price": 43.0,
                "size_mb": 90.0,
                "row_count": 5000,
                "column_count": 35,
                "format": "CSV",
                "sample_data": {"preview": "https://www.itu.int/en/ITU-D/Statistics/"},
                "metadata": {
                    "source_name": "International Telecommunication Union",
                    "source_url": "https://www.itu.int/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            },
            {
                "title": "UNICEF WASH Water Access Data",
                "description": "Drinking water, sanitation, and hygiene indicators for households worldwide.",
                "category": "Public Health",
                "tags": ["unicef", "wash", "water"],
                "price": 40.0,
                "size_mb": 70.0,
                "row_count": 6000,
                "column_count": 25,
                "format": "CSV",
                "sample_data": {"preview": "https://washdata.org/"},
                "metadata": {
                    "source_name": "UNICEF & WHO JMP",
                    "source_url": "https://washdata.org/",
                    "license": "CC BY 3.0 IGO",
                    "verified": True
                }
            },
            {
                "title": "Our World in Data Electric Vehicle Adoption",
                "description": "EV sales, market share, and charging infrastructure statistics globally.",
                "category": "Transportation",
                "tags": ["owid", "ev", "mobility"],
                "price": 55.0,
                "size_mb": 60.0,
                "row_count": 4000,
                "column_count": 18,
                "format": "CSV",
                "sample_data": {"preview": "https://ourworldindata.org/"},
                "metadata": {
                    "source_name": "Our World in Data",
                    "source_url": "https://ourworldindata.org/",
                    "license": "CC BY 4.0",
                    "verified": True
                }
            }
        ]

        def build_sample_preview(dataset_info):
            """Create a structured preview for display in UI."""
            category = dataset_info.get("category") or "General"
            row_count = dataset_info.get("row_count")
            column_count = dataset_info.get("column_count")
            size_mb = dataset_info.get("size_mb")
            metadata = dataset_info.get("metadata", {})

            rows = [
                {
                    "Dimension": "Category",
                    "Attribute": category,
                    "Value": dataset_info.get("title"),
                    "Notes": metadata.get("source_name", "Sample extract")
                },
                {
                    "Dimension": "Rows",
                    "Attribute": "Approximate",
                    "Value": f"{row_count:,}" if isinstance(row_count, int) else "N/A",
                    "Notes": "Total records"
                },
                {
                    "Dimension": "Columns",
                    "Attribute": "Available Fields",
                    "Value": column_count or "N/A",
                    "Notes": metadata.get("license", "Usage terms")
                },
                {
                    "Dimension": "Size (MB)",
                    "Attribute": "Compressed",
                    "Value": size_mb,
                    "Notes": metadata.get("period", metadata.get("source_url", "Latest release"))
                }
            ]

            rows.append(
                {
                    "Dimension": "Sample Metric",
                    "Attribute": random.choice(["Index", "Value", "Score", "Amount"]),
                    "Value": round(random.uniform(10, 1000), 2),
                    "Notes": "Illustrative preview value"
                }
            )

            return {
                "columns": ["Dimension", "Attribute", "Value", "Notes"],
                "rows": rows
            }

        for dataset in verified_datasets:
            dataset["sample_data"] = build_sample_preview(dataset)
        
        existing_datasets = {
            d.title: d for d in db.query(Dataset).all()
        }
        new_records = 0
        updated_records = 0
        
        for dataset_data in verified_datasets:
            dataset_kwargs = dataset_data.copy()
            metadata_payload = dataset_kwargs.pop("metadata", None)
            sample_payload = dataset_kwargs.pop("sample_data", None)

            existing = existing_datasets.get(dataset_data["title"])
            if existing:
                existing.description = dataset_kwargs.get("description", existing.description)
                existing.category = dataset_kwargs.get("category", existing.category)
                existing.tags = dataset_kwargs.get("tags", existing.tags)
                existing.price = dataset_kwargs.get("price", existing.price)
                existing.size_mb = dataset_kwargs.get("size_mb", existing.size_mb)
                existing.row_count = dataset_kwargs.get("row_count")
                existing.column_count = dataset_kwargs.get("column_count")
                existing.format = dataset_kwargs.get("format", existing.format)
                existing.is_active = True
                if sample_payload:
                    existing.sample_data = sample_payload
                if metadata_payload is not None:
                    existing.metadata_json = metadata_payload
                updated_records += 1
                continue

            dataset = Dataset(
                **dataset_kwargs,
                metadata_json=metadata_payload or {},
                sample_data=sample_payload,
                seller_id=seller.id,
                rating=round(random.uniform(4.1, 4.9), 1),
                review_count=random.randint(50, 1500),
                download_count=random.randint(200, 8000)
            )
            db.add(dataset)
            new_records += 1
        
        if new_records or updated_records:
            db.commit()
            print(f"Created {new_records} datasets, updated {updated_records} datasets")
        else:
            print("No dataset changes applied.")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
