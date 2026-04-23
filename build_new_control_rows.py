"""
Build new control table rows from all TidyTuesday year readmes.
Appends rows (needs_mapping) for any dataset not already in control_table_full.csv.
"""

import csv
import re
import os

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sanitize_function_name(data_name):
    """Convert a dataset display name into a snake_case R function name."""
    name = data_name.lower()
    # strip markdown link syntax if present
    name = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', name)
    # remove non-alphanumeric except spaces
    name = re.sub(r"[^a-z0-9\s]", " ", name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"_+", "_", name).strip("_")
    return name

def normalize_key(data_name):
    """Lowercase, strip punctuation, collapse spaces — used for deduplication."""
    name = data_name.lower()
    name = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', name)
    name = re.sub(r"[^a-z0-9\s]", " ", name)
    return re.sub(r"\s+", " ", name).strip()


# ---------------------------------------------------------------------------
# ALL TidyTuesday datasets from 2018–2026 readmes
# Format: (date_str, display_name)  -- skip BYOD / special weeks
# ---------------------------------------------------------------------------

ALL_DATASETS = [

    # ── 2018 ─────────────────────────────────────────────────────────────
    ("2018-04-02", "US Tuition Costs"),
    ("2018-04-09", "NFL Positional Salaries"),
    ("2018-04-16", "Global Mortality"),
    ("2018-04-23", "Australian Salaries by Gender"),
    ("2018-04-30", "ACS Census Data 2015"),
    ("2018-05-07", "Global Coffee Chains"),
    ("2018-05-14", "Star Wars Survey"),
    ("2018-05-21", "US Honey Production"),
    ("2018-05-29", "Comic Book Characters"),
    ("2018-06-05", "Biketown Bikeshare"),
    ("2018-06-12", "FIFA World Cup Audience"),
    ("2018-06-19", "Hurricanes and Puerto Rico"),
    ("2018-06-26", "Alcohol Consumption"),
    ("2018-07-03", "Global Life Expectancy"),
    ("2018-07-10", "Craft Beer USA"),
    ("2018-07-17", "Exercise USA"),
    # week 17 2018-07-24 is p-hack-athon – skip
    ("2018-07-31", "Dallas Animal Shelter FY2017"),
    ("2018-08-07", "Airline Safety"),
    ("2018-08-14", "Russian Troll Tweets"),
    ("2018-08-21", "California Fires"),
    ("2018-08-28", "NFL Stats"),
    ("2018-09-04", "Fast Food Calories"),
    ("2018-09-11", "Cats vs Dogs USA"),
    ("2018-09-18", "US Flights"),
    ("2018-09-25", "Global Invasive Species"),
    ("2018-10-02", "US Births"),
    ("2018-10-09", "US Voter Turnout"),
    ("2018-10-16", "College Major and Income"),          # covered – will be filtered
    ("2018-10-23", "Horror Movie Profit"),               # covered
    ("2018-10-30", "R and R Package Downloads"),         # covered
    ("2018-11-06", "US Wind Farm Locations"),            # covered
    ("2018-11-13", "Malaria Data"),                      # covered
    ("2018-11-20", "Thanksgiving Dinner"),               # covered
    ("2018-11-27", "Baltimore Bridges"),                 # covered
    ("2018-12-04", "Medium Article Metadata"),           # covered
    ("2018-12-11", "NYC Restaurant Inspections"),        # covered
    ("2018-12-18", "Cetaceans Data"),                    # covered

    # ── 2019 ─────────────────────────────────────────────────────────────
    ("2019-01-01", "Rstats and TidyTuesday Tweets"),     # covered
    ("2019-01-08", "TVs Golden Age"),                    # covered
    ("2019-01-15", "Space Launches"),                    # covered
    ("2019-01-22", "Incarceration Trends"),              # covered
    ("2019-01-29", "Dairy Production and Consumption"),  # covered
    ("2019-02-05", "House Price Index and Mortgage Rates"),
    ("2019-02-12", "Federal RD Spending"),
    ("2019-02-19", "US PhDs Awarded"),                   # covered
    ("2019-02-26", "French Train Delays"),               # covered
    ("2019-03-05", "Women in the Workplace"),            # covered
    ("2019-03-12", "Board Games"),                       # covered
    ("2019-03-19", "Stanford Open Policing Project"),
    ("2019-03-26", "Seattle Pet Names"),                 # covered
    ("2019-04-02", "Seattle Bike Traffic"),              # covered
    ("2019-04-09", "Tennis Grand Slam Champions"),       # covered
    ("2019-04-16", "The Economist Data Viz Mistakes"),
    ("2019-04-23", "Anime Data"),
    ("2019-04-30", "Chicago Bird Collisions"),           # covered
    ("2019-05-07", "Global Student to Teacher Ratios"),
    ("2019-05-14", "Nobel Prize Winners"),               # covered
    ("2019-05-21", "Global Plastic Waste"),              # covered
    ("2019-05-28", "Wine Ratings"),                      # covered
    ("2019-06-04", "Ramen Ratings"),                     # covered
    ("2019-06-11", "Meteorites"),
    ("2019-06-18", "Christmas Bird Counts"),
    ("2019-06-25", "Global UFO Sightings"),
    ("2019-07-02", "Media Franchise Revenues"),          # covered
    ("2019-07-09", "Womens World Cup"),                  # covered
    ("2019-07-16", "R4DS Membership"),
    ("2019-07-23", "Wildlife Strikes"),
    ("2019-07-30", "Video Games Steam"),
    ("2019-08-06", "Bob Ross Paintings"),                # covered
    ("2019-08-13", "Roman Emperors"),
    ("2019-08-20", "Nuclear Explosions"),
    ("2019-08-27", "Simpsons Guest Stars"),              # covered
    ("2019-09-03", "Moores Law"),
    ("2019-09-10", "Amusement Park Injuries"),
    ("2019-09-17", "National Park Visits"),
    ("2019-09-24", "School Diversity"),
    ("2019-10-01", "All the Pizza"),                     # covered (nyc-pizza)
    ("2019-10-08", "Powerlifting"),
    ("2019-10-15", "Car Fuel Economy"),                  # covered
    ("2019-10-22", "Horror Movie Ratings"),              # covered
    ("2019-10-29", "NYC Squirrel Census"),               # covered
    ("2019-11-05", "Bike and Walk Commutes"),
    ("2019-11-12", "CRAN Code"),                         # covered
    ("2019-11-19", "NZ Bird of the Year"),
    ("2019-11-26", "Student Loan Debt"),
    ("2019-12-03", "Philly Parking Tickets"),
    ("2019-12-10", "Replicating Plots in R"),
    ("2019-12-17", "Adoptable Dogs"),
    ("2019-12-24", "Christmas Songs"),

    # ── 2020 ─────────────────────────────────────────────────────────────
    # week 1 2019-12-31 BYOD – skip
    ("2020-01-07", "Australian Fires"),
    ("2020-01-14", "Passwords"),
    ("2020-01-21", "Song Genres"),
    ("2020-01-28", "San Francisco Trees"),
    ("2020-02-04", "NFL Attendance"),
    ("2020-02-11", "Hotel Bookings"),
    ("2020-02-18", "Foods Carbon Footprint"),
    ("2020-02-25", "Measles Vaccination"),
    ("2020-03-03", "NHL Goals"),
    ("2020-03-10", "College Tuition Diversity and Pay"),
    ("2020-03-17", "The Office"),                        # covered
    ("2020-03-24", "Traumatic Brain Injury"),
    ("2020-03-31", "Beer Production"),                   # covered
    ("2020-04-07", "Tour de France"),                    # covered
    ("2020-04-14", "Best Rap Artists"),
    ("2020-04-21", "GDPR Violations"),                   # covered
    ("2020-04-28", "Broadway Musicals"),                 # covered
    ("2020-05-05", "Animal Crossing"),                   # covered
    ("2020-05-12", "Volcano Eruptions"),                 # covered
    ("2020-05-19", "Beach Volleyball"),                  # covered
    ("2020-05-26", "Cocktails"),                         # covered
    ("2020-06-02", "Marble Races"),
    ("2020-06-09", "African American Achievements"),     # covered
    ("2020-06-16", "African American History"),          # covered
    ("2020-06-23", "Caribou Locations"),                 # covered
    ("2020-06-30", "Claremont Run of X-Men"),            # covered
    ("2020-07-07", "Coffee Ratings"),                    # covered
    ("2020-07-14", "Astronaut Database"),
    ("2020-07-21", "Australian Animal Outcomes"),        # covered
    ("2020-07-28", "Palmer Penguins"),                   # covered
    ("2020-08-04", "European Energy"),                   # covered
    ("2020-08-11", "Avatar The Last Airbender"),
    ("2020-08-18", "Extinct Plants"),                    # covered
    ("2020-08-25", "Chopped"),                           # covered
    ("2020-09-01", "Global Crop Yields"),                # covered
    ("2020-09-08", "Friends Transcripts"),               # covered
    ("2020-09-15", "Government Spending on Kids"),       # covered
    ("2020-09-22", "Himalayan Climbers"),                # covered
    ("2020-09-29", "Beyonce and Taylor Swift Lyrics"),   # covered
    ("2020-10-06", "NCAA Womens Basketball"),            # covered
    ("2020-10-13", "DatasauRus Dozen"),
    ("2020-10-20", "Great American Beer Festival"),      # covered
    ("2020-10-27", "Canadian Wind Turbines"),
    ("2020-11-03", "IKEA Furniture"),                    # covered
    ("2020-11-10", "Historical Phones"),                 # covered
    ("2020-11-17", "Black in Data"),
    ("2020-11-24", "Washington Trails"),
    ("2020-12-01", "Toronto Shelters"),
    ("2020-12-08", "Women of 2020"),
    ("2020-12-15", "Ninja Warrior"),                     # covered
    ("2020-12-22", "Big Mac Index"),                     # covered

    # ── 2021 ─────────────────────────────────────────────────────────────
    # week 1 2020-12-29 BYOD – skip
    ("2021-01-05", "Transit Cost Project"),              # covered
    ("2021-01-12", "Art Collections"),                   # covered
    ("2021-01-19", "Kenya Census"),                      # covered
    ("2021-01-26", "Plastic Pollution"),
    ("2021-02-02", "HBCU Enrollment"),                   # covered
    ("2021-02-09", "Wealth and Income"),                 # covered
    ("2021-02-16", "WEB Du Bois Challenge"),
    ("2021-02-23", "Employment and Earnings"),           # covered
    ("2021-03-02", "SuperBowl Ads"),                     # covered
    ("2021-03-09", "Bechdel Test"),                      # covered
    ("2021-03-16", "Video Games Sliced"),                # covered
    ("2021-03-23", "UN Votes"),                          # covered
    ("2021-03-30", "Makeup Shades"),
    ("2021-04-06", "Global Deforestation"),              # covered
    ("2021-04-13", "US Post Offices"),                   # covered
    ("2021-04-20", "Netflix Titles"),                    # covered
    ("2021-04-27", "CEO Departures"),
    ("2021-05-04", "Water Access Points"),               # covered
    ("2021-05-11", "US Broadband"),
    ("2021-05-18", "Ask a Manager Salary Survey"),
    ("2021-05-25", "Mario Kart World Records"),
    ("2021-06-01", "Survivor TV Show"),
    ("2021-06-08", "Great Lakes Fish"),
    ("2021-06-15", "WEB Du Bois and Juneteenth"),
    ("2021-06-22", "Public Park Access"),
    ("2021-06-29", "Animal Rescues"),
    ("2021-07-06", "International Independence Days"),
    ("2021-07-13", "Scooby Doo"),
    ("2021-07-20", "US Droughts"),
    ("2021-07-27", "Olympic Medals"),
    ("2021-08-03", "Paralympic Medals"),
    ("2021-08-10", "BEA Infrastructure Investment"),
    ("2021-08-17", "Star Trek Voice Commands"),
    ("2021-08-24", "Lemurs"),
    ("2021-08-31", "Bird Baths"),
    ("2021-09-07", "Formula 1 Races"),
    ("2021-09-14", "Billboard Top 100"),
    ("2021-09-21", "Emmy Awards"),
    ("2021-09-28", "NBER Papers"),
    ("2021-10-05", "Registered Nurses"),
    ("2021-10-12", "Global Seafood"),
    ("2021-10-19", "Big Pumpkins"),
    ("2021-10-26", "Ultra Trail Running"),
    ("2021-11-02", "Making Maps with R"),
    ("2021-11-09", "Learning with Afrilearndata"),
    ("2021-11-16", "BlackInDataWeek 2021"),
    ("2021-11-23", "Dr Who"),
    ("2021-11-30", "World Cup Cricket"),
    ("2021-12-07", "Spiders"),
    ("2021-12-14", "Spice Girls"),
    ("2021-12-21", "Starbucks Drinks"),

    # ── 2022 ─────────────────────────────────────────────────────────────
    # week 1 2022-01-04 BYOD – skip
    ("2022-01-11", "Bee Colony Losses"),
    ("2022-01-18", "Chocolate Bar Ratings"),
    ("2022-01-25", "Board Games 2022"),
    ("2022-02-01", "Dog Breeds"),
    ("2022-02-08", "Tuskegee Airmen"),
    ("2022-02-15", "DuBois Challenge 2022"),
    ("2022-02-22", "World Freedom Index"),
    ("2022-03-01", "Alternative Fuel Stations"),
    ("2022-03-08", "Erasmus Student Mobility"),
    ("2022-03-15", "CRAN BIOC Vignettes"),
    ("2022-03-22", "Baby Names"),
    ("2022-03-29", "Collegiate Sports Budgets"),
    ("2022-04-05", "Digital Publications"),
    ("2022-04-12", "Indoor Air Pollution"),
    ("2022-04-19", "Crossword Puzzles and Clues"),
    ("2022-04-26", "Kaggle Hidden Gems"),
    ("2022-05-03", "Solar Wind Utilities"),
    ("2022-05-10", "NYTimes Best Sellers"),
    ("2022-05-17", "Eurovision"),
    ("2022-05-24", "Womens Rugby"),
    ("2022-05-31", "Company Reputation Poll"),
    ("2022-06-07", "Pride Corporate Accountability"),
    ("2022-06-14", "US Drought 2022"),
    ("2022-06-21", "Juneteenth 2022"),
    ("2022-06-28", "UK Gender Pay Gap"),
    ("2022-07-05", "San Francisco Rentals"),
    ("2022-07-12", "European Flights"),
    ("2022-07-19", "Technology Adoption"),
    # week 30 2022-07-26 BYOD – skip
    ("2022-08-02", "Oregon Spotted Frog"),
    ("2022-08-09", "Ferris Wheels"),
    ("2022-08-16", "Open Source Psychometrics"),
    ("2022-08-23", "CHIP Dataset"),
    ("2022-08-30", "Pell Grants"),
    ("2022-09-06", "LEGO Database"),
    ("2022-09-13", "Bigfoot Sightings"),
    ("2022-09-20", "Hydro Wastewater Plants"),
    ("2022-09-27", "Artists in the USA"),
    ("2022-10-04", "Product Hunt Products"),
    ("2022-10-11", "Ravelry Data"),
    ("2022-10-18", "Stranger Things Dialogue"),
    ("2022-10-25", "Great British Bakeoff"),
    ("2022-11-01", "Horror Movies 2022"),
    ("2022-11-08", "Radio Stations"),
    ("2022-11-15", "Web Page Metrics"),
    ("2022-11-22", "UK Museums"),
    ("2022-11-29", "FIFA World Cup 2022"),
    ("2022-12-06", "Elevators"),
    ("2022-12-13", "Monthly State Retail Sales"),
    ("2022-12-20", "Weather Forecast Accuracy"),
    ("2022-12-27", "Star Trek Timelines"),

    # ── 2023 ─────────────────────────────────────────────────────────────
    # week 1 2023-01-03 BYOD – skip
    ("2023-01-10", "Bird FeederWatch Data"),
    ("2023-01-17", "Art History Data"),
    ("2023-01-24", "Alone Data"),
    ("2023-01-31", "Pet Cats UK"),
    ("2023-02-07", "Big Tech Stock Prices"),
    ("2023-02-14", "Hollywood Age Gaps"),
    ("2023-02-21", "Bob Ross Paintings 2023"),
    ("2023-02-28", "African Language Sentiment"),
    ("2023-03-07", "Numbats in Australia"),
    ("2023-03-14", "European Drug Development"),
    ("2023-03-21", "Programming Languages"),
    ("2023-03-28", "Time Zones"),
    ("2023-04-04", "Premier League Match Data"),
    ("2023-04-11", "US Egg Production Data"),
    ("2023-04-18", "Neolithic Founder Crops"),
    ("2023-04-25", "London Marathon"),
    ("2023-05-02", "The Portal Project"),
    ("2023-05-09", "Childcare Costs"),
    ("2023-05-16", "Tornados"),
    ("2023-05-23", "Central Park Squirrels 2023"),
    ("2023-05-30", "Verified Oldest People"),
    ("2023-06-06", "Energy 2023"),
    ("2023-06-13", "African Farmer Led Irrigation Survey"),
    ("2023-06-20", "UFO Sightings Redux"),
    ("2023-06-27", "US Populated Places"),
    ("2023-07-04", "Historical Markers"),
    ("2023-07-11", "Global Surface Temperatures"),
    ("2023-07-18", "GPT Detectors"),
    ("2023-07-25", "Scurvy"),
    ("2023-08-01", "US States"),
    ("2023-08-08", "Hot Ones Episodes"),
    ("2023-08-15", "Spam Email"),
    ("2023-08-22", "Refugees"),
    ("2023-08-29", "Fair Use"),
    ("2023-09-05", "Union Membership in the United States"),
    ("2023-09-12", "The Global Human Day"),
    ("2023-09-19", "CRAN Package Authors"),
    ("2023-09-26", "Roy Kent F Count"),
    ("2023-10-03", "US Government Grant Opportunities"),
    ("2023-10-10", "Haunted Places in the United States"),
    ("2023-10-17", "Taylor Swift Data"),
    ("2023-10-24", "Patient Risk Profiles"),
    ("2023-10-31", "Horror Legends"),
    ("2023-11-07", "US House Election Results"),
    ("2023-11-14", "Diwali Sales Data"),
    ("2023-11-21", "R-Ladies Chapter Events"),
    ("2023-11-28", "Doctor Who Episodes"),
    ("2023-12-05", "Life Expectancy"),
    ("2023-12-12", "Holiday Movies"),
    ("2023-12-19", "Holiday Episodes"),
    ("2023-12-26", "R Package Structure"),

    # ── 2024 ─────────────────────────────────────────────────────────────
    # week 1 2024-01-02 BYOD – skip
    ("2024-01-09", "Canadian NHL Player Birth Dates"),
    ("2024-01-16", "US Polling Places 2012 2020"),
    ("2024-01-23", "Educational Attainment of Young People in English Towns"),
    ("2024-01-30", "Groundhog Predictions"),
    ("2024-02-06", "World Heritage Sites"),
    ("2024-02-13", "Valentines Day Consumer Data"),
    ("2024-02-20", "R Consortium ISC Grants"),
    ("2024-02-27", "Leap Day"),
    ("2024-03-05", "Trash Wheel Collection Data"),
    ("2024-03-12", "Fiscal Sponsors"),
    ("2024-03-19", "X-Men Mutant Moneyball"),
    ("2024-03-26", "NCAA Mens March Madness"),
    ("2024-04-02", "Du Bois Visualization Challenge 2024"),
    ("2024-04-09", "US Solar Eclipses 2023 and 2024"),
    ("2024-04-16", "Shiny Packages"),
    ("2024-04-23", "Objects Launched into Space"),
    ("2024-04-30", "Worldwide Bureaucracy Indicators"),
    ("2024-05-07", "Rolling Stone Album Rankings"),
    ("2024-05-14", "The Great American Coffee Taste Test"),
    ("2024-05-21", "Carbon Majors Emissions Data"),
    ("2024-05-28", "Lisas Vegetable Garden Data"),
    ("2024-06-04", "Cheese"),
    ("2024-06-11", "Campus Pride Index"),
    ("2024-06-18", "US Federal Holidays"),
    ("2024-06-25", "tidyRainbow Datasets"),
    ("2024-07-02", "TidyTuesday Datasets Meta"),
    ("2024-07-09", "David Robinsons TidyTuesday Functions"),
    ("2024-07-16", "English Womens Football"),
    ("2024-07-23", "American Idol Data"),
    ("2024-07-30", "Summer Movies"),
    ("2024-08-06", "Olympic Medals 2024"),
    ("2024-08-13", "Worlds Fairs"),
    ("2024-08-20", "English Monarchs and Marriages"),
    ("2024-08-27", "The Power Rangers Franchise"),
    ("2024-09-03", "Stack Overflow Annual Developer Survey 2024"),
    ("2024-09-10", "Economic Diversity and Student Outcomes"),
    ("2024-09-17", "Shakespeare Dialogue"),
    ("2024-09-24", "International Mathematical Olympiad Data"),
    ("2024-10-01", "Chess Game Dataset Lichess"),
    ("2024-10-08", "National Park Species"),
    ("2024-10-15", "Southern Resident Killer Whale Encounters"),
    ("2024-10-22", "The CIA World Factbook"),
    ("2024-10-29", "Monster Movies"),
    ("2024-11-05", "Democracy and Dictatorship"),
    ("2024-11-12", "ISO Country Codes"),
    ("2024-11-19", "Bobs Burgers Episodes"),
    ("2024-11-26", "US Customs and Border Protection Encounter Data"),
    ("2024-12-03", "National Highways Traffic Flow"),
    ("2024-12-10", "Parfumo Fragrance Dataset"),
    ("2024-12-17", "Dungeons and Dragons Spells 2024"),
    ("2024-12-24", "Global Holidays and Travel"),
    ("2024-12-31", "James Beard Awards"),

    # ── 2025 ─────────────────────────────────────────────────────────────
    # week 1 2025-01-07 BYOD – skip
    ("2025-01-14", "Posit Conf Talks"),
    ("2025-01-21", "The History of Himalayan Mountaineering Expeditions"),
    ("2025-01-28", "Water Insecurity"),
    ("2025-02-04", "The Simpsons Deep Dive"),
    ("2025-02-11", "CDC Datasets"),
    ("2025-02-18", "Agencies from the FBI Crime Data API"),
    ("2025-02-25", "Racial and Ethnic Disparities in Reproductive Medicine"),
    ("2025-03-04", "Long Beach Animal Shelter"),
    ("2025-03-11", "Pixar Films"),
    ("2025-03-18", "Palm Trees"),
    ("2025-03-25", "Amazon Annual Reports Text Data"),
    ("2025-04-01", "Pokemon"),
    ("2025-04-08", "Timely and Effective Care by US State"),
    ("2025-04-15", "Base R Penguins"),
    ("2025-04-22", "Fatal Car Crashes on 4 20"),
    ("2025-04-29", "useR 2025 Program"),
    ("2025-05-06", "NSF Grant Terminations under Trump Administration"),
    ("2025-05-13", "Seismic Events at Mount Vesuvius"),
    ("2025-05-20", "Water Quality at Sydney Beaches"),
    ("2025-05-27", "Dungeons and Dragons Monsters 2024"),
    ("2025-06-03", "Project Gutenberg"),
    ("2025-06-10", "US Judges and historydata R Package"),
    ("2025-06-17", "API Specs"),
    ("2025-06-24", "Measles Cases Across the World"),
    ("2025-07-01", "Weekly US Gas Prices"),
    ("2025-07-08", "The xkcd Color Survey Results"),
    ("2025-07-15", "British Library Funding"),
    ("2025-07-22", "MTA Permanent Art Catalog"),
    ("2025-07-29", "What Have We Been Watching on Netflix"),
    ("2025-08-05", "Income Inequality Before and After Taxes"),
    ("2025-08-12", "Extreme Weather Attribution Studies"),
    ("2025-08-19", "Scottish Munros"),
    ("2025-08-26", "Billboard Hot 100 Number Ones"),
    ("2025-09-02", "Australian Frogs"),
    ("2025-09-09", "Henley Passport Index Data"),
    ("2025-09-16", "Allrecipes"),
    ("2025-09-23", "FIDE Chess Player Ratings"),
    ("2025-09-30", "Crane Observations at Lake Hornborgasjon Sweden"),
    ("2025-10-07", "EuroLeague Basketball"),
    ("2025-10-14", "World Food Day"),
    ("2025-10-21", "Historic UK Meteorological and Climate Data"),
    ("2025-10-28", "Selected British Literary Prizes 1990 2022"),
    ("2025-11-04", "Lead Concentration in Flint Water Samples"),
    ("2025-11-11", "WHO TB Burden Data"),
    ("2025-11-18", "The Complete Sherlock Holmes"),
    ("2025-11-25", "Statistical Performance Indicators"),
    ("2025-12-02", "Zurich Sechselaeuten Snowman"),
    ("2025-12-09", "Cars in Qatar"),
    ("2025-12-16", "Roundabouts Across the World"),
    ("2025-12-23", "The Languages of the World"),
    ("2025-12-30", "Christmas Novels"),

    # ── 2026 ─────────────────────────────────────────────────────────────
    # week 1 2026-01-06 BYOD – skip
    ("2026-01-13", "The Languages of Africa"),
    ("2026-01-20", "Astronomy Picture of the Day APOD Archive"),
    ("2026-01-27", "Brazilian Companies"),
    ("2026-02-03", "Edible Plants Database"),
    ("2026-02-10", "The 2026 Winter Olympics"),
    ("2026-02-17", "Agricultural Production Statistics in New Zealand"),
    ("2026-02-24", "Science Foundation Ireland Grants Commitments"),
    ("2026-03-03", "Golem Grad Tortoise Data"),
    ("2026-03-10", "How Likely Is Likely Probability Phrases"),
    ("2026-03-17", "Salmonid Mortality Data"),
    ("2026-03-24", "One Million Digits of Pi"),
    ("2026-03-31", "Coastal Ocean Temperature by Depth"),
    ("2026-04-07", "Repair Cafes Worldwide"),
    ("2026-04-14", "Bird Sightings at Sea"),
    ("2026-04-21", "Global Health Spending"),
]


# ---------------------------------------------------------------------------
# Load existing control table and collect already-covered keys
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CT_PATH = os.path.join(SCRIPT_DIR, "control_table.csv")

existing_keys = set()
existing_dates = set()

with open(CT_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing_rows = list(reader)

for row in existing_rows:
    nk = row.get("normalized_key", "").strip()
    if nk:
        existing_keys.add(nk)
    ds = row.get("data_source", "").strip()
    # extract date like "2020-06-09" from data_source field
    m = re.search(r"(\d{4}-\d{2}-\d{2})", ds)
    if m:
        existing_dates.add(m.group(1))

print(f"Existing rows: {len(existing_rows)}")
print(f"Existing normalized keys: {len(existing_keys)}")
print(f"Existing dates in data_source: {len(existing_dates)}")


# ---------------------------------------------------------------------------
# Generate new rows for uncovered datasets
# ---------------------------------------------------------------------------

# Additional manual key overrides – datasets in the existing table that use
# a different normalized_key from what the date-based name would produce.
COVERED_KEYS_EXTRA = {
    normalize_key("College Major and Income"),           # college_major_income
    normalize_key("Horror Movie Profit"),
    normalize_key("R and R Package Downloads"),
    normalize_key("US Wind Farm Locations"),
    normalize_key("Malaria Data"),
    normalize_key("Thanksgiving Dinner"),
    normalize_key("Baltimore Bridges"),
    normalize_key("Medium Article Metadata"),
    normalize_key("NYC Restaurant Inspections"),
    normalize_key("Cetaceans Data"),
    normalize_key("Rstats and TidyTuesday Tweets"),
    normalize_key("TVs Golden Age"),
    normalize_key("Space Launches"),
    normalize_key("Incarceration Trends"),
    normalize_key("Dairy Production and Consumption"),
    normalize_key("US PhDs Awarded"),
    normalize_key("French Train Delays"),
    normalize_key("Women in the Workplace"),
    normalize_key("Board Games"),
    normalize_key("Seattle Pet Names"),
    normalize_key("Seattle Bike Traffic"),
    normalize_key("Tennis Grand Slam Champions"),
    normalize_key("Chicago Bird Collisions"),
    normalize_key("Nobel Prize Winners"),
    normalize_key("Global Plastic Waste"),
    normalize_key("Wine Ratings"),
    normalize_key("Ramen Ratings"),
    normalize_key("Media Franchise Revenues"),
    normalize_key("Womens World Cup"),
    normalize_key("Bob Ross Paintings"),
    normalize_key("Simpsons Guest Stars"),
    normalize_key("All the Pizza"),
    normalize_key("Car Fuel Economy"),
    normalize_key("Horror Movie Ratings"),
    normalize_key("NYC Squirrel Census"),
    normalize_key("CRAN Code"),
    normalize_key("The Office"),
    normalize_key("Beer Production"),
    normalize_key("Tour de France"),
    normalize_key("GDPR Violations"),
    normalize_key("Broadway Musicals"),
    normalize_key("Animal Crossing"),
    normalize_key("Volcano Eruptions"),
    normalize_key("Beach Volleyball"),
    normalize_key("Cocktails"),
    normalize_key("African American Achievements"),
    normalize_key("African American History"),
    normalize_key("Caribou Locations"),
    normalize_key("Claremont Run of X-Men"),
    normalize_key("Coffee Ratings"),
    normalize_key("Australian Animal Outcomes"),
    normalize_key("Palmer Penguins"),
    normalize_key("European Energy"),
    normalize_key("Extinct Plants"),
    normalize_key("Chopped"),
    normalize_key("Global Crop Yields"),
    normalize_key("Friends Transcripts"),
    normalize_key("Government Spending on Kids"),
    normalize_key("Himalayan Climbers"),
    normalize_key("Beyonce and Taylor Swift Lyrics"),
    normalize_key("NCAA Womens Basketball"),
    normalize_key("Great American Beer Festival"),
    normalize_key("IKEA Furniture"),
    normalize_key("Historical Phones"),
    normalize_key("Ninja Warrior"),
    normalize_key("Big Mac Index"),
    normalize_key("Transit Cost Project"),
    normalize_key("Art Collections"),
    normalize_key("Kenya Census"),
    normalize_key("HBCU Enrollment"),
    normalize_key("Wealth and Income"),
    normalize_key("Employment and Earnings"),
    normalize_key("SuperBowl Ads"),
    normalize_key("Bechdel Test"),
    normalize_key("Video Games Sliced"),
    normalize_key("UN Votes"),
    normalize_key("Global Deforestation"),
    normalize_key("US Post Offices"),
    normalize_key("Netflix Titles"),
    normalize_key("Water Access Points"),
}

all_covered = existing_keys | COVERED_KEYS_EXTRA

new_rows = []
seen_new = set()

for date_str, data_name in ALL_DATASETS:
    nk = normalize_key(data_name)
    # skip if already covered by key or by date
    if nk in all_covered:
        continue
    if date_str in existing_dates:
        continue
    if nk in seen_new:
        continue
    seen_new.add(nk)

    fn = sanitize_function_name(data_name)
    title = f"Analyzing {data_name} in R"

    new_rows.append({
        "transcript_title": title,
        "transcript_file": "",
        "code_file": "",
        "function_name": fn,
        "data_source": f"TidyTuesday {date_str}",
        "analysis_intent": "",
        "analysis_type": "",
        "pattern_signature": "",
        "adaptation_hint": "",
        "ker_status": "needs_mapping",
        "notes": "",
        "normalized_key": nk,
    })

print(f"\nNew rows to add: {len(new_rows)}")
for r in new_rows[:5]:
    print(f"  {r['data_source']:20s}  {r['function_name']}")
print("  ...")


# ---------------------------------------------------------------------------
# Write updated CSV
# ---------------------------------------------------------------------------

out_path = CT_PATH
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_rows)
    writer.writerows(new_rows)

print(f"\nWrote {len(existing_rows) + len(new_rows)} rows to {out_path}")
print("Done.")
