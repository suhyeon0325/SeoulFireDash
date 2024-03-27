# SeoulFireDash

**Version 0.1.4**:
- **Data Caching for Speed:** Implemented data caching to enhance application performance.
- **Updated Front Page with Latest Data:** Now includes data from 2018 to March 2024, replacing the previous 2021-2022 dataset.
- **2024 Monthly Fire Incident Prediction Graph:** Introduced a new graph predicting monthly fire incidents for 2024 using machine learning techniques.
- **Enhanced Vulnerability Analysis in Fire Accident Prone Areas:** Improved visualization with vertical bar graphs for easier comparison, including a new comparison feature against the Seoul average in the top/bottom 5 districts view.
- **Seoul District Vulnerability Score Map Update:** Enhanced map readability by displaying district names on the map.
- **New Section in Firefighting Infrastructure Analysis Page:** Added 'Fire Service Accessibility Analysis: Building Fires Exceeding Golden Time' section, with seasonal color-coded markers visualizing building fires where fire service arrived past the critical response time in 2021.
- **Enhanced Emergency Hydrant Location Suggestion Page for Songpa District:** Added pie chart visualizations alongside bar graphs for a clearer understanding of housing types distribution by dong.

**Version 0.1.3**:
- **Sidebar Icons & UI Enhancements**: Introduced intuitive icons for sidebar navigation and refreshed the UI theme for a better user experience.
- **Enhanced Suggestions Page**:
  - Added anonymity and file upload features for submitting suggestions, improving user engagement and feedback detail.
- **Emergency Hydrant Location Suggestion Map for Songpa District**: A new interactive map suggesting optimal locations for emergency hydrants, enriched with local firefighting resource insights.
- **Firefighting Infrastructure & Welfare Information**: Updated the firefighting infrastructure page with direct links to policies and welfare information, enhancing public awareness and access to resources.
- **Vulnerability Analysis Enhancement**: Integrated a vulnerability score ranking data frame in the fire accident vulnerability analysis, offering deeper insights into fire-prone areas.

**Version 0.1.2**:
- **Fire Place Type Bar Graph**: A new bar graph visualization for fire incidents by place types, offering a clear and quick data understanding.
- **Seoul Residential Fire Vulnerability Analysis Table**: An in-depth data table detailing fire vulnerability in Seoul's residential areas, complementing our graphical analyses.
- **Emergency Hydrant Location Suggestion Page**: Introducing a map visualization for proposed emergency hydrant locations in Songpa District, along with insights into local firefighting resources, to enhance fire preparedness and infrastructure.

**Version 0.1.1**: 
- **Ward Fire Place Type Treemap**: Visualize fire incidents by place types within wards.
- **Vulnerable Area Analysis**: Explore in-depth or top 5 most fire-prone areas based on critical indicators like emergency hydrant counts, building types, population density, old housing numbers, and more.
- **Fire Vulnerability Mapping in Seoul**: New visual tool to pinpoint and assess fire-susceptible areas.
- **Seoul Firefighting Infrastructure Visualization**: Map out crucial firefighting resources including stations, hydrants, and water supplies.
- **Suggestions Page**: A new avenue for feedback and ideas to enhance app utility and user experience.

**Version 0.1.0** :

- **Dynamic Data Visualization**: Leveraging Streamlit for interactive visualization, allowing users to explore fire incident data, including incidents, casualties, and damages.
- **In-depth Analysis**: Detailed analyses by incident type and region with custom filters and visualization options to uncover trends and patterns.
- **Comparative Insights**: Analysis between 2021 and 2022 to highlight trends and evaluate fire prevention and response efforts.
- **Data Integration**: Utilizing CSV and SHP files for a thorough representation of fire incidents and impacts.
- **Efficiency and User Experience**: Enhanced data loading with `@st.cache_data`, improved data filtering for regional analysis, and optimized visualization for clearer insights.
