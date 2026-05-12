"""
Static airport database for instant, zero-API-quota search.
Covers ~250 major airports worldwide. Search via search_airports_local().
"""

AIRPORTS: list[dict] = [
    # ── United States ─────────────────────────────────────────────────────────
    {"skyId": "ATL", "entityId": "95673477", "name": "Atlanta Hartsfield-Jackson", "subtitle": "Atlanta, United States"},
    {"skyId": "LAX", "entityId": "95673607", "name": "Los Angeles International", "subtitle": "Los Angeles, United States"},
    {"skyId": "ORD", "entityId": "95673695", "name": "Chicago O'Hare International", "subtitle": "Chicago, United States"},
    {"skyId": "DFW", "entityId": "95673529", "name": "Dallas Fort Worth International", "subtitle": "Dallas, United States"},
    {"skyId": "DEN", "entityId": "95673527", "name": "Denver International", "subtitle": "Denver, United States"},
    {"skyId": "JFK", "entityId": "95673827", "name": "New York John F. Kennedy", "subtitle": "New York, United States"},
    {"skyId": "SFO", "entityId": "95673740", "name": "San Francisco International", "subtitle": "San Francisco, United States"},
    {"skyId": "SEA", "entityId": "95673741", "name": "Seattle-Tacoma International", "subtitle": "Seattle, United States"},
    {"skyId": "LAS", "entityId": "95673604", "name": "Las Vegas Harry Reid International", "subtitle": "Las Vegas, United States"},
    {"skyId": "MCO", "entityId": "95673635", "name": "Orlando International", "subtitle": "Orlando, United States"},
    {"skyId": "EWR", "entityId": "95673547", "name": "Newark Liberty International", "subtitle": "New York, United States"},
    {"skyId": "MIA", "entityId": "95673648", "name": "Miami International", "subtitle": "Miami, United States"},
    {"skyId": "CLT", "entityId": "95673507", "name": "Charlotte Douglas International", "subtitle": "Charlotte, United States"},
    {"skyId": "PHX", "entityId": "95673711", "name": "Phoenix Sky Harbor International", "subtitle": "Phoenix, United States"},
    {"skyId": "IAH", "entityId": "95673573", "name": "Houston George Bush Intercontinental", "subtitle": "Houston, United States"},
    {"skyId": "BOS", "entityId": "95673489", "name": "Boston Logan International", "subtitle": "Boston, United States"},
    {"skyId": "MSP", "entityId": "95673660", "name": "Minneapolis-Saint Paul International", "subtitle": "Minneapolis, United States"},
    {"skyId": "DTW", "entityId": "95673538", "name": "Detroit Metropolitan Wayne County", "subtitle": "Detroit, United States"},
    {"skyId": "FLL", "entityId": "95673556", "name": "Fort Lauderdale-Hollywood International", "subtitle": "Fort Lauderdale, United States"},
    {"skyId": "PHL", "entityId": "95673708", "name": "Philadelphia International", "subtitle": "Philadelphia, United States"},
    {"skyId": "LGA", "entityId": "95673606", "name": "New York LaGuardia", "subtitle": "New York, United States"},
    {"skyId": "BWI", "entityId": "95673497", "name": "Baltimore/Washington Thurgood Marshall", "subtitle": "Baltimore, United States"},
    {"skyId": "DCA", "entityId": "95673519", "name": "Washington Ronald Reagan National", "subtitle": "Washington DC, United States"},
    {"skyId": "IAD", "entityId": "95673572", "name": "Washington Dulles International", "subtitle": "Washington DC, United States"},
    {"skyId": "MDW", "entityId": "95673636", "name": "Chicago Midway International", "subtitle": "Chicago, United States"},
    {"skyId": "TPA", "entityId": "95673770", "name": "Tampa International", "subtitle": "Tampa, United States"},
    {"skyId": "SAN", "entityId": "95673736", "name": "San Diego International", "subtitle": "San Diego, United States"},
    {"skyId": "PDX", "entityId": "95673703", "name": "Portland International", "subtitle": "Portland, United States"},
    {"skyId": "HNL", "entityId": "95673568", "name": "Honolulu Daniel K. Inouye International", "subtitle": "Honolulu, United States"},
    {"skyId": "AUS", "entityId": "95673476", "name": "Austin-Bergstrom International", "subtitle": "Austin, United States"},
    {"skyId": "SLC", "entityId": "95673744", "name": "Salt Lake City International", "subtitle": "Salt Lake City, United States"},
    {"skyId": "STL", "entityId": "95673760", "name": "St. Louis Lambert International", "subtitle": "St. Louis, United States"},
    {"skyId": "BNA", "entityId": "95673487", "name": "Nashville International", "subtitle": "Nashville, United States"},
    {"skyId": "RDU", "entityId": "95673726", "name": "Raleigh-Durham International", "subtitle": "Raleigh-Durham, United States"},
    {"skyId": "MCI", "entityId": "95673631", "name": "Kansas City International", "subtitle": "Kansas City, United States"},
    {"skyId": "SMF", "entityId": "95673749", "name": "Sacramento International", "subtitle": "Sacramento, United States"},
    {"skyId": "SJC", "entityId": "95673745", "name": "San Jose International", "subtitle": "San Jose, United States"},
    {"skyId": "OAK", "entityId": "95673686", "name": "Oakland International", "subtitle": "Oakland, United States"},
    {"skyId": "MSY", "entityId": "95673661", "name": "New Orleans Louis Armstrong International", "subtitle": "New Orleans, United States"},
    {"skyId": "CLE", "entityId": "95673506", "name": "Cleveland Hopkins International", "subtitle": "Cleveland, United States"},
    {"skyId": "PIT", "entityId": "95673713", "name": "Pittsburgh International", "subtitle": "Pittsburgh, United States"},
    {"skyId": "IND", "entityId": "95673577", "name": "Indianapolis International", "subtitle": "Indianapolis, United States"},
    {"skyId": "CMH", "entityId": "95673509", "name": "Columbus John Glenn International", "subtitle": "Columbus, United States"},
    {"skyId": "MKE", "entityId": "95673652", "name": "Milwaukee Mitchell International", "subtitle": "Milwaukee, United States"},
    {"skyId": "ABQ", "entityId": "95673464", "name": "Albuquerque International Sunport", "subtitle": "Albuquerque, United States"},
    {"skyId": "OMA", "entityId": "95673692", "name": "Omaha Eppley Airfield", "subtitle": "Omaha, United States"},
    {"skyId": "OKC", "entityId": "95673690", "name": "Oklahoma City Will Rogers World", "subtitle": "Oklahoma City, United States"},
    {"skyId": "TUL", "entityId": "95673773", "name": "Tulsa International", "subtitle": "Tulsa, United States"},
    {"skyId": "MEM", "entityId": "95673642", "name": "Memphis International", "subtitle": "Memphis, United States"},
    {"skyId": "BHM", "entityId": "95673484", "name": "Birmingham-Shuttlesworth International", "subtitle": "Birmingham, United States"},
    {"skyId": "JAX", "entityId": "95673584", "name": "Jacksonville International", "subtitle": "Jacksonville, United States"},
    # ── Canada ────────────────────────────────────────────────────────────────
    {"skyId": "YYZ", "entityId": "95673774", "name": "Toronto Pearson International", "subtitle": "Toronto, Canada"},
    {"skyId": "YVR", "entityId": "95673775", "name": "Vancouver International", "subtitle": "Vancouver, Canada"},
    {"skyId": "YUL", "entityId": "95673776", "name": "Montreal Pierre Elliott Trudeau International", "subtitle": "Montreal, Canada"},
    {"skyId": "YYC", "entityId": "95673777", "name": "Calgary International", "subtitle": "Calgary, Canada"},
    {"skyId": "YEG", "entityId": "95673778", "name": "Edmonton International", "subtitle": "Edmonton, Canada"},
    {"skyId": "YOW", "entityId": "95673779", "name": "Ottawa Macdonald-Cartier International", "subtitle": "Ottawa, Canada"},
    {"skyId": "YWG", "entityId": "95673780", "name": "Winnipeg James Armstrong Richardson International", "subtitle": "Winnipeg, Canada"},
    {"skyId": "YHZ", "entityId": "95673781", "name": "Halifax Stanfield International", "subtitle": "Halifax, Canada"},
    # ── Mexico & Central America ──────────────────────────────────────────────
    {"skyId": "MEX", "entityId": "95673643", "name": "Mexico City International", "subtitle": "Mexico City, Mexico"},
    {"skyId": "CUN", "entityId": "95673517", "name": "Cancun International", "subtitle": "Cancun, Mexico"},
    {"skyId": "GDL", "entityId": "95673559", "name": "Guadalajara Miguel Hidalgo International", "subtitle": "Guadalajara, Mexico"},
    {"skyId": "MTY", "entityId": "95673662", "name": "Monterrey International", "subtitle": "Monterrey, Mexico"},
    {"skyId": "SJO", "entityId": "95673746", "name": "San Jose Juan Santamaría International", "subtitle": "San Jose, Costa Rica"},
    {"skyId": "PTY", "entityId": "95673720", "name": "Panama City Tocumen International", "subtitle": "Panama City, Panama"},
    # ── South America ─────────────────────────────────────────────────────────
    {"skyId": "GRU", "entityId": "95673565", "name": "São Paulo Guarulhos International", "subtitle": "São Paulo, Brazil"},
    {"skyId": "GIG", "entityId": "95673561", "name": "Rio de Janeiro Galeão International", "subtitle": "Rio de Janeiro, Brazil"},
    {"skyId": "EZE", "entityId": "95673549", "name": "Buenos Aires Ezeiza International", "subtitle": "Buenos Aires, Argentina"},
    {"skyId": "SCL", "entityId": "95673739", "name": "Santiago Arturo Merino Benítez International", "subtitle": "Santiago, Chile"},
    {"skyId": "BOG", "entityId": "95673488", "name": "Bogotá El Dorado International", "subtitle": "Bogotá, Colombia"},
    {"skyId": "LIM", "entityId": "95673609", "name": "Lima Jorge Chávez International", "subtitle": "Lima, Peru"},
    {"skyId": "UIO", "entityId": "95673782", "name": "Quito Mariscal Sucre International", "subtitle": "Quito, Ecuador"},
    {"skyId": "MVD", "entityId": "95673664", "name": "Montevideo Carrasco International", "subtitle": "Montevideo, Uruguay"},
    {"skyId": "CCS", "entityId": "95673499", "name": "Caracas Simón Bolívar International", "subtitle": "Caracas, Venezuela"},
    # ── United Kingdom ────────────────────────────────────────────────────────
    {"skyId": "LHR", "entityId": "95673612", "name": "London Heathrow", "subtitle": "London, United Kingdom"},
    {"skyId": "LGW", "entityId": "95673608", "name": "London Gatwick", "subtitle": "London, United Kingdom"},
    {"skyId": "STN", "entityId": "95673758", "name": "London Stansted", "subtitle": "London, United Kingdom"},
    {"skyId": "LTN", "entityId": "95673619", "name": "London Luton", "subtitle": "London, United Kingdom"},
    {"skyId": "MAN", "entityId": "95673628", "name": "Manchester Airport", "subtitle": "Manchester, United Kingdom"},
    {"skyId": "EDI", "entityId": "95673543", "name": "Edinburgh Airport", "subtitle": "Edinburgh, United Kingdom"},
    {"skyId": "BHX", "entityId": "95673485", "name": "Birmingham Airport", "subtitle": "Birmingham, United Kingdom"},
    {"skyId": "GLA", "entityId": "95673563", "name": "Glasgow Airport", "subtitle": "Glasgow, United Kingdom"},
    {"skyId": "BRS", "entityId": "95673493", "name": "Bristol Airport", "subtitle": "Bristol, United Kingdom"},
    # ── Europe ────────────────────────────────────────────────────────────────
    {"skyId": "CDG", "entityId": "95673500", "name": "Paris Charles de Gaulle", "subtitle": "Paris, France"},
    {"skyId": "ORY", "entityId": "95673697", "name": "Paris Orly", "subtitle": "Paris, France"},
    {"skyId": "FRA", "entityId": "95673555", "name": "Frankfurt International", "subtitle": "Frankfurt, Germany"},
    {"skyId": "MUC", "entityId": "95673663", "name": "Munich International", "subtitle": "Munich, Germany"},
    {"skyId": "BER", "entityId": "95673483", "name": "Berlin Brandenburg International", "subtitle": "Berlin, Germany"},
    {"skyId": "HAM", "entityId": "95673566", "name": "Hamburg Airport", "subtitle": "Hamburg, Germany"},
    {"skyId": "DUS", "entityId": "95673539", "name": "Düsseldorf International", "subtitle": "Düsseldorf, Germany"},
    {"skyId": "AMS", "entityId": "95673472", "name": "Amsterdam Schiphol", "subtitle": "Amsterdam, Netherlands"},
    {"skyId": "MAD", "entityId": "95673623", "name": "Madrid Adolfo Suárez Barajas", "subtitle": "Madrid, Spain"},
    {"skyId": "BCN", "entityId": "95673481", "name": "Barcelona El Prat", "subtitle": "Barcelona, Spain"},
    {"skyId": "FCO", "entityId": "95673551", "name": "Rome Fiumicino", "subtitle": "Rome, Italy"},
    {"skyId": "MXP", "entityId": "95673668", "name": "Milan Malpensa", "subtitle": "Milan, Italy"},
    {"skyId": "LIN", "entityId": "95673610", "name": "Milan Linate", "subtitle": "Milan, Italy"},
    {"skyId": "VCE", "entityId": "95673784", "name": "Venice Marco Polo", "subtitle": "Venice, Italy"},
    {"skyId": "NAP", "entityId": "95673671", "name": "Naples International", "subtitle": "Naples, Italy"},
    {"skyId": "ZRH", "entityId": "95673800", "name": "Zurich Airport", "subtitle": "Zurich, Switzerland"},
    {"skyId": "GVA", "entityId": "95673567", "name": "Geneva Airport", "subtitle": "Geneva, Switzerland"},
    {"skyId": "VIE", "entityId": "95673785", "name": "Vienna International", "subtitle": "Vienna, Austria"},
    {"skyId": "BRU", "entityId": "95673494", "name": "Brussels Airport", "subtitle": "Brussels, Belgium"},
    {"skyId": "CPH", "entityId": "95673516", "name": "Copenhagen Airport", "subtitle": "Copenhagen, Denmark"},
    {"skyId": "ARN", "entityId": "95673474", "name": "Stockholm Arlanda", "subtitle": "Stockholm, Sweden"},
    {"skyId": "OSL", "entityId": "95673698", "name": "Oslo Gardermoen", "subtitle": "Oslo, Norway"},
    {"skyId": "HEL", "entityId": "95673569", "name": "Helsinki Vantaa", "subtitle": "Helsinki, Finland"},
    {"skyId": "LIS", "entityId": "95673611", "name": "Lisbon Humberto Delgado", "subtitle": "Lisbon, Portugal"},
    {"skyId": "OPO", "entityId": "95673694", "name": "Porto Francisco Sá Carneiro", "subtitle": "Porto, Portugal"},
    {"skyId": "ATH", "entityId": "95673475", "name": "Athens Eleftherios Venizelos", "subtitle": "Athens, Greece"},
    {"skyId": "WAW", "entityId": "95673789", "name": "Warsaw Chopin Airport", "subtitle": "Warsaw, Poland"},
    {"skyId": "PRG", "entityId": "95673718", "name": "Prague Václav Havel Airport", "subtitle": "Prague, Czech Republic"},
    {"skyId": "BUD", "entityId": "95673496", "name": "Budapest Ferenc Liszt International", "subtitle": "Budapest, Hungary"},
    {"skyId": "BEG", "entityId": "95673482", "name": "Belgrade Nikola Tesla Airport", "subtitle": "Belgrade, Serbia"},
    {"skyId": "ZAG", "entityId": "95673799", "name": "Zagreb Franjo Tuđman Airport", "subtitle": "Zagreb, Croatia"},
    {"skyId": "DBV", "entityId": "95673521", "name": "Dubrovnik Airport", "subtitle": "Dubrovnik, Croatia"},
    {"skyId": "SKP", "entityId": "95673748", "name": "Skopje International Airport", "subtitle": "Skopje, North Macedonia"},
    {"skyId": "TIA", "entityId": "95673769", "name": "Tirana Nënë Tereza International", "subtitle": "Tirana, Albania"},
    {"skyId": "OTP", "entityId": "95673699", "name": "Bucharest Henri Coandă International", "subtitle": "Bucharest, Romania"},
    {"skyId": "SOF", "entityId": "95673754", "name": "Sofia Airport", "subtitle": "Sofia, Bulgaria"},
    {"skyId": "KIV", "entityId": "95673597", "name": "Chișinău International Airport", "subtitle": "Chișinău, Moldova"},
    {"skyId": "RIX", "entityId": "95673729", "name": "Riga International Airport", "subtitle": "Riga, Latvia"},
    {"skyId": "VNO", "entityId": "95673786", "name": "Vilnius Airport", "subtitle": "Vilnius, Lithuania"},
    {"skyId": "TLL", "entityId": "95673771", "name": "Tallinn Airport", "subtitle": "Tallinn, Estonia"},
    {"skyId": "KBP", "entityId": "95673592", "name": "Kyiv Boryspil International", "subtitle": "Kyiv, Ukraine"},
    {"skyId": "SVO", "entityId": "95673761", "name": "Moscow Sheremetyevo International", "subtitle": "Moscow, Russia"},
    {"skyId": "DME", "entityId": "95673530", "name": "Moscow Domodedovo International", "subtitle": "Moscow, Russia"},
    {"skyId": "LED", "entityId": "95673605", "name": "St. Petersburg Pulkovo International", "subtitle": "St. Petersburg, Russia"},
    {"skyId": "IST", "entityId": "95673580", "name": "Istanbul Airport", "subtitle": "Istanbul, Turkey"},
    {"skyId": "SAW", "entityId": "95673737", "name": "Istanbul Sabiha Gökçen International", "subtitle": "Istanbul, Turkey"},
    {"skyId": "AYT", "entityId": "95673478", "name": "Antalya Airport", "subtitle": "Antalya, Turkey"},
    {"skyId": "ESB", "entityId": "95673546", "name": "Ankara Esenboğa International", "subtitle": "Ankara, Turkey"},
    {"skyId": "ADB", "entityId": "95673465", "name": "İzmir Adnan Menderes Airport", "subtitle": "İzmir, Turkey"},
    # ── Middle East ───────────────────────────────────────────────────────────
    {"skyId": "DXB", "entityId": "95673537", "name": "Dubai International", "subtitle": "Dubai, UAE"},
    {"skyId": "AUH", "entityId": "95673477", "name": "Abu Dhabi International", "subtitle": "Abu Dhabi, UAE"},
    {"skyId": "SHJ", "entityId": "95673743", "name": "Sharjah International", "subtitle": "Sharjah, UAE"},
    {"skyId": "DOH", "entityId": "95673533", "name": "Doha Hamad International", "subtitle": "Doha, Qatar"},
    {"skyId": "RUH", "entityId": "95673732", "name": "Riyadh King Khalid International", "subtitle": "Riyadh, Saudi Arabia"},
    {"skyId": "JED", "entityId": "95673585", "name": "Jeddah King Abdulaziz International", "subtitle": "Jeddah, Saudi Arabia"},
    {"skyId": "BAH", "entityId": "95673479", "name": "Bahrain International", "subtitle": "Manama, Bahrain"},
    {"skyId": "KWI", "entityId": "95673603", "name": "Kuwait International", "subtitle": "Kuwait City, Kuwait"},
    {"skyId": "MCT", "entityId": "95673634", "name": "Muscat International", "subtitle": "Muscat, Oman"},
    {"skyId": "AMM", "entityId": "95673471", "name": "Amman Queen Alia International", "subtitle": "Amman, Jordan"},
    {"skyId": "BEY", "entityId": "95673484", "name": "Beirut Rafic Hariri International", "subtitle": "Beirut, Lebanon"},
    {"skyId": "TLV", "entityId": "95673772", "name": "Tel Aviv Ben Gurion International", "subtitle": "Tel Aviv, Israel"},
    {"skyId": "THR", "entityId": "95673768", "name": "Tehran Imam Khomeini International", "subtitle": "Tehran, Iran"},
    # ── South Asia ────────────────────────────────────────────────────────────
    {"skyId": "DEL", "entityId": "95673524", "name": "Delhi Indira Gandhi International", "subtitle": "Delhi, India"},
    {"skyId": "BOM", "entityId": "95673488", "name": "Mumbai Chhatrapati Shivaji Maharaj International", "subtitle": "Mumbai, India"},
    {"skyId": "BLR", "entityId": "95673486", "name": "Bengaluru Kempegowda International", "subtitle": "Bangalore, India"},
    {"skyId": "HYD", "entityId": "95673571", "name": "Hyderabad Rajiv Gandhi International", "subtitle": "Hyderabad, India"},
    {"skyId": "MAA", "entityId": "95673622", "name": "Chennai International", "subtitle": "Chennai, India"},
    {"skyId": "CCU", "entityId": "95673501", "name": "Kolkata Netaji Subhas Chandra Bose International", "subtitle": "Kolkata, India"},
    {"skyId": "COK", "entityId": "95673514", "name": "Kochi International", "subtitle": "Kochi, India"},
    {"skyId": "PNQ", "entityId": "95673714", "name": "Pune Airport", "subtitle": "Pune, India"},
    {"skyId": "AMD", "entityId": "95673470", "name": "Ahmedabad Sardar Vallabhbhai Patel International", "subtitle": "Ahmedabad, India"},
    {"skyId": "JAI", "entityId": "95673583", "name": "Jaipur International", "subtitle": "Jaipur, India"},
    {"skyId": "GOI", "entityId": "95673564", "name": "Goa Dabolim Airport", "subtitle": "Goa, India"},
    {"skyId": "TRV", "entityId": "95673773", "name": "Thiruvananthapuram International", "subtitle": "Thiruvananthapuram, India"},
    {"skyId": "IXC", "entityId": "95673578", "name": "Chandigarh International", "subtitle": "Chandigarh, India"},
    {"skyId": "LKO", "entityId": "95673613", "name": "Lucknow Chaudhary Charan Singh International", "subtitle": "Lucknow, India"},
    {"skyId": "PAT", "entityId": "95673702", "name": "Patna Jay Prakash Narayan Airport", "subtitle": "Patna, India"},
    {"skyId": "BBI", "entityId": "95673480", "name": "Bhubaneswar Biju Patnaik International", "subtitle": "Bhubaneswar, India"},
    {"skyId": "VTZ", "entityId": "95673788", "name": "Visakhapatnam Airport", "subtitle": "Visakhapatnam, India"},
    {"skyId": "KNU", "entityId": "95673600", "name": "Kanpur Airport", "subtitle": "Kanpur, India"},
    {"skyId": "SXR", "entityId": "95673763", "name": "Srinagar Airport", "subtitle": "Srinagar, India"},
    {"skyId": "IXL", "entityId": "95673579", "name": "Leh Kushok Bakula Rimpochee Airport", "subtitle": "Leh, India"},
    {"skyId": "KTM", "entityId": "95673602", "name": "Kathmandu Tribhuvan International", "subtitle": "Kathmandu, Nepal"},
    {"skyId": "CMB", "entityId": "95673510", "name": "Colombo Bandaranaike International", "subtitle": "Colombo, Sri Lanka"},
    {"skyId": "DAC", "entityId": "95673518", "name": "Dhaka Hazrat Shahjalal International", "subtitle": "Dhaka, Bangladesh"},
    {"skyId": "KHI", "entityId": "95673594", "name": "Karachi Jinnah International", "subtitle": "Karachi, Pakistan"},
    {"skyId": "LHE", "entityId": "95673607", "name": "Lahore Allama Iqbal International", "subtitle": "Lahore, Pakistan"},
    {"skyId": "ISB", "entityId": "95673581", "name": "Islamabad International", "subtitle": "Islamabad, Pakistan"},
    {"skyId": "MLE", "entityId": "95673651", "name": "Malé Velana International", "subtitle": "Malé, Maldives"},
    # ── Southeast Asia ────────────────────────────────────────────────────────
    {"skyId": "SIN", "entityId": "95673745", "name": "Singapore Changi", "subtitle": "Singapore"},
    {"skyId": "BKK", "entityId": "95673487", "name": "Bangkok Suvarnabhumi", "subtitle": "Bangkok, Thailand"},
    {"skyId": "DMK", "entityId": "95673531", "name": "Bangkok Don Mueang International", "subtitle": "Bangkok, Thailand"},
    {"skyId": "HKT", "entityId": "95673570", "name": "Phuket International", "subtitle": "Phuket, Thailand"},
    {"skyId": "CNX", "entityId": "95673512", "name": "Chiang Mai International", "subtitle": "Chiang Mai, Thailand"},
    {"skyId": "KUL", "entityId": "95673601", "name": "Kuala Lumpur International", "subtitle": "Kuala Lumpur, Malaysia"},
    {"skyId": "PEN", "entityId": "95673704", "name": "Penang International", "subtitle": "Penang, Malaysia"},
    {"skyId": "CGK", "entityId": "95673503", "name": "Jakarta Soekarno-Hatta International", "subtitle": "Jakarta, Indonesia"},
    {"skyId": "DPS", "entityId": "95673536", "name": "Bali Ngurah Rai International", "subtitle": "Bali, Indonesia"},
    {"skyId": "SUB", "entityId": "95673762", "name": "Surabaya Juanda International", "subtitle": "Surabaya, Indonesia"},
    {"skyId": "MNL", "entityId": "95673655", "name": "Manila Ninoy Aquino International", "subtitle": "Manila, Philippines"},
    {"skyId": "CEB", "entityId": "95673502", "name": "Cebu Mactan-Cebu International", "subtitle": "Cebu, Philippines"},
    {"skyId": "SGN", "entityId": "95673742", "name": "Ho Chi Minh City Tan Son Nhat International", "subtitle": "Ho Chi Minh City, Vietnam"},
    {"skyId": "HAN", "entityId": "95673567", "name": "Hanoi Noi Bai International", "subtitle": "Hanoi, Vietnam"},
    {"skyId": "DAD", "entityId": "95673519", "name": "Da Nang International", "subtitle": "Da Nang, Vietnam"},
    {"skyId": "PNH", "entityId": "95673715", "name": "Phnom Penh International", "subtitle": "Phnom Penh, Cambodia"},
    {"skyId": "REP", "entityId": "95673727", "name": "Siem Reap Angkor International", "subtitle": "Siem Reap, Cambodia"},
    {"skyId": "VTE", "entityId": "95673787", "name": "Vientiane Wattay International", "subtitle": "Vientiane, Laos"},
    {"skyId": "RGN", "entityId": "95673728", "name": "Yangon International", "subtitle": "Yangon, Myanmar"},
    {"skyId": "BWN", "entityId": "95673498", "name": "Brunei International", "subtitle": "Bandar Seri Begawan, Brunei"},
    # ── East Asia ─────────────────────────────────────────────────────────────
    {"skyId": "PEK", "entityId": "95673703", "name": "Beijing Capital International", "subtitle": "Beijing, China"},
    {"skyId": "PKX", "entityId": "95673712", "name": "Beijing Daxing International", "subtitle": "Beijing, China"},
    {"skyId": "PVG", "entityId": "95673721", "name": "Shanghai Pudong International", "subtitle": "Shanghai, China"},
    {"skyId": "SHA", "entityId": "95673742", "name": "Shanghai Hongqiao International", "subtitle": "Shanghai, China"},
    {"skyId": "CAN", "entityId": "95673498", "name": "Guangzhou Baiyun International", "subtitle": "Guangzhou, China"},
    {"skyId": "SZX", "entityId": "95673764", "name": "Shenzhen Bao'an International", "subtitle": "Shenzhen, China"},
    {"skyId": "CTU", "entityId": "95673517", "name": "Chengdu Tianfu International", "subtitle": "Chengdu, China"},
    {"skyId": "CKG", "entityId": "95673505", "name": "Chongqing Jiangbei International", "subtitle": "Chongqing, China"},
    {"skyId": "XMN", "entityId": "95673795", "name": "Xiamen Gaoqi International", "subtitle": "Xiamen, China"},
    {"skyId": "WUH", "entityId": "95673791", "name": "Wuhan Tianhe International", "subtitle": "Wuhan, China"},
    {"skyId": "NKG", "entityId": "95673677", "name": "Nanjing Lukou International", "subtitle": "Nanjing, China"},
    {"skyId": "HAK", "entityId": "95673566", "name": "Haikou Meilan International", "subtitle": "Haikou, China"},
    {"skyId": "SYX", "entityId": "95673763", "name": "Sanya Phoenix International", "subtitle": "Sanya, China"},
    {"skyId": "KMG", "entityId": "95673598", "name": "Kunming Changshui International", "subtitle": "Kunming, China"},
    {"skyId": "HGH", "entityId": "95673568", "name": "Hangzhou Xiaoshan International", "subtitle": "Hangzhou, China"},
    {"skyId": "TSN", "entityId": "95673772", "name": "Tianjin Binhai International", "subtitle": "Tianjin, China"},
    {"skyId": "TAO", "entityId": "95673765", "name": "Qingdao Jiaodong International", "subtitle": "Qingdao, China"},
    {"skyId": "HKG", "entityId": "95673569", "name": "Hong Kong International", "subtitle": "Hong Kong"},
    {"skyId": "MFM", "entityId": "95673645", "name": "Macau International", "subtitle": "Macau"},
    {"skyId": "TPE", "entityId": "95673770", "name": "Taipei Taiwan Taoyuan International", "subtitle": "Taipei, Taiwan"},
    {"skyId": "TSA", "entityId": "95673771", "name": "Taipei Songshan Airport", "subtitle": "Taipei, Taiwan"},
    {"skyId": "KHH", "entityId": "95673595", "name": "Kaohsiung International", "subtitle": "Kaohsiung, Taiwan"},
    {"skyId": "ICN", "entityId": "95673574", "name": "Seoul Incheon International", "subtitle": "Seoul, South Korea"},
    {"skyId": "GMP", "entityId": "95673562", "name": "Seoul Gimpo International", "subtitle": "Seoul, South Korea"},
    {"skyId": "PUS", "entityId": "95673719", "name": "Busan Gimhae International", "subtitle": "Busan, South Korea"},
    {"skyId": "CJU", "entityId": "95673504", "name": "Jeju International", "subtitle": "Jeju, South Korea"},
    {"skyId": "NRT", "entityId": "95673681", "name": "Tokyo Narita International", "subtitle": "Tokyo, Japan"},
    {"skyId": "HND", "entityId": "95673570", "name": "Tokyo Haneda International", "subtitle": "Tokyo, Japan"},
    {"skyId": "KIX", "entityId": "95673596", "name": "Osaka Kansai International", "subtitle": "Osaka, Japan"},
    {"skyId": "ITM", "entityId": "95673582", "name": "Osaka Itami Airport", "subtitle": "Osaka, Japan"},
    {"skyId": "NGO", "entityId": "95673675", "name": "Nagoya Chubu Centrair International", "subtitle": "Nagoya, Japan"},
    {"skyId": "CTS", "entityId": "95673516", "name": "Sapporo New Chitose Airport", "subtitle": "Sapporo, Japan"},
    {"skyId": "FUK", "entityId": "95673557", "name": "Fukuoka Airport", "subtitle": "Fukuoka, Japan"},
    {"skyId": "OKA", "entityId": "95673689", "name": "Okinawa Naha Airport", "subtitle": "Okinawa, Japan"},
    {"skyId": "HIJ", "entityId": "95673569", "name": "Hiroshima Airport", "subtitle": "Hiroshima, Japan"},
    {"skyId": "ULN", "entityId": "95673783", "name": "Ulaanbaatar Chinggis Khaan International", "subtitle": "Ulaanbaatar, Mongolia"},
    # ── Central Asia ──────────────────────────────────────────────────────────
    {"skyId": "ALA", "entityId": "95673469", "name": "Almaty International", "subtitle": "Almaty, Kazakhstan"},
    {"skyId": "NQZ", "entityId": "95673680", "name": "Astana International", "subtitle": "Astana, Kazakhstan"},
    {"skyId": "TAS", "entityId": "95673766", "name": "Tashkent Islam Karimov International", "subtitle": "Tashkent, Uzbekistan"},
    # ── Africa ────────────────────────────────────────────────────────────────
    {"skyId": "CAI", "entityId": "95673497", "name": "Cairo International", "subtitle": "Cairo, Egypt"},
    {"skyId": "HRG", "entityId": "95673571", "name": "Hurghada International", "subtitle": "Hurghada, Egypt"},
    {"skyId": "SSH", "entityId": "95673758", "name": "Sharm El Sheikh International", "subtitle": "Sharm El Sheikh, Egypt"},
    {"skyId": "CMN", "entityId": "95673511", "name": "Casablanca Mohammed V International", "subtitle": "Casablanca, Morocco"},
    {"skyId": "RAK", "entityId": "95673724", "name": "Marrakech Menara Airport", "subtitle": "Marrakech, Morocco"},
    {"skyId": "TUN", "entityId": "95673774", "name": "Tunis Carthage International", "subtitle": "Tunis, Tunisia"},
    {"skyId": "ALG", "entityId": "95673470", "name": "Algiers Houari Boumediene Airport", "subtitle": "Algiers, Algeria"},
    {"skyId": "TRP", "entityId": "95673773", "name": "Tripoli Mitiga International", "subtitle": "Tripoli, Libya"},
    {"skyId": "ADD", "entityId": "95673466", "name": "Addis Ababa Bole International", "subtitle": "Addis Ababa, Ethiopia"},
    {"skyId": "NBO", "entityId": "95673672", "name": "Nairobi Jomo Kenyatta International", "subtitle": "Nairobi, Kenya"},
    {"skyId": "DAR", "entityId": "95673520", "name": "Dar es Salaam Julius Nyerere International", "subtitle": "Dar es Salaam, Tanzania"},
    {"skyId": "JNB", "entityId": "95673587", "name": "Johannesburg O.R. Tambo International", "subtitle": "Johannesburg, South Africa"},
    {"skyId": "CPT", "entityId": "95673515", "name": "Cape Town International", "subtitle": "Cape Town, South Africa"},
    {"skyId": "DUR", "entityId": "95673538", "name": "Durban King Shaka International", "subtitle": "Durban, South Africa"},
    {"skyId": "ACC", "entityId": "95673465", "name": "Accra Kotoka International", "subtitle": "Accra, Ghana"},
    {"skyId": "LOS", "entityId": "95673617", "name": "Lagos Murtala Muhammed International", "subtitle": "Lagos, Nigeria"},
    {"skyId": "ABV", "entityId": "95673464", "name": "Abuja Nnamdi Azikiwe International", "subtitle": "Abuja, Nigeria"},
    {"skyId": "DKR", "entityId": "95673528", "name": "Dakar Blaise Diagne International", "subtitle": "Dakar, Senegal"},
    {"skyId": "ABJ", "entityId": "95673463", "name": "Abidjan Félix-Houphouët-Boigny International", "subtitle": "Abidjan, Côte d'Ivoire"},
    {"skyId": "CMR", "entityId": "95673511", "name": "Yaoundé Nsimalen International", "subtitle": "Yaoundé, Cameroon"},
    {"skyId": "LBV", "entityId": "95673604", "name": "Libreville Omar Bongo International", "subtitle": "Libreville, Gabon"},
    {"skyId": "TNR", "entityId": "95673770", "name": "Antananarivo Ivato International", "subtitle": "Antananarivo, Madagascar"},
    {"skyId": "MRU", "entityId": "95673659", "name": "Mauritius Sir Seewoosagur Ramgoolam International", "subtitle": "Mauritius"},
    {"skyId": "RUN", "entityId": "95673731", "name": "Réunion Roland Garros Airport", "subtitle": "Saint-Denis, Réunion"},
    # ── Oceania ───────────────────────────────────────────────────────────────
    {"skyId": "SYD", "entityId": "95673764", "name": "Sydney Kingsford Smith International", "subtitle": "Sydney, Australia"},
    {"skyId": "MEL", "entityId": "95673641", "name": "Melbourne Airport", "subtitle": "Melbourne, Australia"},
    {"skyId": "BNE", "entityId": "95673489", "name": "Brisbane Airport", "subtitle": "Brisbane, Australia"},
    {"skyId": "PER", "entityId": "95673705", "name": "Perth Airport", "subtitle": "Perth, Australia"},
    {"skyId": "ADL", "entityId": "95673467", "name": "Adelaide Airport", "subtitle": "Adelaide, Australia"},
    {"skyId": "CNS", "entityId": "95673513", "name": "Cairns Airport", "subtitle": "Cairns, Australia"},
    {"skyId": "OOL", "entityId": "95673693", "name": "Gold Coast Airport", "subtitle": "Gold Coast, Australia"},
    {"skyId": "AKL", "entityId": "95673468", "name": "Auckland Airport", "subtitle": "Auckland, New Zealand"},
    {"skyId": "CHC", "entityId": "95673503", "name": "Christchurch Airport", "subtitle": "Christchurch, New Zealand"},
    {"skyId": "WLG", "entityId": "95673790", "name": "Wellington Airport", "subtitle": "Wellington, New Zealand"},
    {"skyId": "NAN", "entityId": "95673670", "name": "Nadi Airport", "subtitle": "Nadi, Fiji"},
]

# Common short aliases → expanded search term.
# Lets users type "NY", "LA", "SF", "DC", "HK", etc. and see all matching airports.
_ALIASES: dict[str, str] = {
    # US metro areas
    "ny":  "new york",
    "nyc": "new york",
    "la":  "los angeles",
    "sf":  "san francisco",
    "dc":  "washington",
    "chi": "chicago",
    "hou": "houston",
    "phx": "phoenix",
    "bos": "boston",
    "mia": "miami",
    "sea": "seattle",
    "den": "denver",
    "atl": "atlanta",
    "dfw": "dallas",
    "pdx": "portland",
    "msp": "minneapolis",
    "slc": "salt lake",
    "dtw": "detroit",
    "mco": "orlando",
    "tpa": "tampa",
    "sdq": "san diego",
    # International
    "hk":  "hong kong",
    "ld":  "london",
    "par": "paris",
    "fra": "frankfurt",
    "ams": "amsterdam",
    "bkk": "bangkok",
    "kl":  "kuala lumpur",
    "ber": "berlin",
    "rom": "rome",
    "mil": "milan",
    "mad": "madrid",
    "bcn": "barcelona",
    "ath": "athens",
    "ist": "istanbul",
    "dxb": "dubai",
    "sgp": "singapore",
    "tyo": "tokyo",
    "osa": "osaka",
    "sel": "seoul",
    "pek": "beijing",
    "sha": "shanghai",
    "syd": "sydney",
    "mel": "melbourne",
    "bne": "brisbane",
    "akl": "auckland",
    "bom": "mumbai",
    "del": "delhi",
    "blr": "bengaluru",
    "maa": "chennai",
    "hyd": "hyderabad",
    "ccu": "kolkata",
}

# Build indices once at import time
_BY_IATA: dict[str, dict] = {a["skyId"]: a for a in AIRPORTS}
_SEARCH_TOKENS: list[tuple[list[str], dict]] = [
    (
        (
            a["skyId"].lower()
            + " "
            + a["name"].lower()
            + " "
            + a.get("subtitle", "").lower()
        ).split(),
        a,
    )
    for a in AIRPORTS
]


def search_airports_local(query: str, limit: int = 8) -> list[dict]:
    """
    Instant, zero-API-quota airport search over the bundled database.
    Matches IATA codes, city names, country, and common abbreviations (NY, LA, HK…).
    """
    q = query.strip().lower()
    if len(q) < 2:
        return []

    # Expand short aliases before searching so "NY" → "new york"
    effective = _ALIASES.get(q, q)

    exact: list[dict] = []
    starts: list[dict] = []
    contains: list[dict] = []
    seen: set[str] = set()

    for tokens, airport in _SEARCH_TOKENS:
        sky = airport["skyId"].lower()
        if airport["skyId"] in seen:
            continue
        haystack = " ".join(tokens)

        # IATA exact/prefix match uses original query; name matching uses expansion
        if sky == q or sky.startswith(q):
            exact.append(airport)
            seen.add(airport["skyId"])
        elif effective != q and effective in haystack:
            # alias matched (e.g. "ny" → "new york" found in subtitle)
            starts.append(airport)
            seen.add(airport["skyId"])
        elif any(t.startswith(effective) for t in tokens):
            starts.append(airport)
            seen.add(airport["skyId"])
        elif effective in haystack:
            contains.append(airport)
            seen.add(airport["skyId"])

    return (exact + starts + contains)[:limit]
