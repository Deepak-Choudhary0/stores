## Restaurant Monitor Backend APIs

This repository contains the implementation of backend APIs that help restaurant owners monitor the online status of their stores. The project aims to provide restaurant owners with a report showing the uptime and downtime of their stores within their business hours, based on periodic polls of store status data.

### Project Status:

The project is still in progress and requires additional work to fully meet the task requirements. The current implementation includes the core functionality of triggering report generation and checking the status of the report. However, there are some areas that need to be addressed to align with the task requirements completely.

### Functionality Summary:

The backend APIs consist of the following two endpoints:

1. `/trigger_report` Endpoint:
   - This endpoint is used to initiate the generation of a report.
   - It generates a unique `report_id` for each report and starts the report generation process.
   - The output of this endpoint is the `report_id`, which the client can use to poll the status of the report completion.

2. `/get_report` Endpoint:
   - This endpoint is used to check the status of the report or retrieve the generated report in CSV format.
   - The input to this endpoint is the `report_id` generated in the `/trigger_report` endpoint.
   - If the report generation is still ongoing, the API returns "Running" as the output.
   - If the report generation is complete, the API returns "Complete" along with the CSV file containing the store uptime and downtime data.

### Issues and Deviations from Task Requirements:

Upon reviewing the code, the following issues and deviations from the task requirements are identified:

1. Timezone Handling: The provided data sources contain information about the store's timezone. However, the current implementation does not consider the timezone information while calculating uptime and downtime. As a result, the report may not accurately reflect the store status in different timezones.

2. Business Hours Data Handling: The project assumes that if business hours data is missing for a store, it is open 24/7. While this is a reasonable assumption, it may not represent the actual business hours for all stores. A more comprehensive approach would be to accurately capture and handle business hours data for all stores.

3. Interpolation Logic for Uptime and Downtime: The current implementation lacks a well-defined interpolation logic to fill the entire business hours interval with uptime and downtime data based on the periodic polls. A robust and logical interpolation strategy is essential for accurate and meaningful results.

4. Database Integration: The project mentions the requirement to store the provided CSV data into a relevant database and use it for API calls. However, the current implementation does not include database integration. Integrating a database will allow for dynamic data storage and retrieval, aligning with the project requirements.

5. Error Handling and Edge Cases: While the current implementation has some error handling, it may not cover all possible edge cases. Comprehensive error handling and edge case management are necessary to ensure the reliability and robustness of the APIs.

### Next Steps and Future Improvements:

To improve the project and bring it closer to meeting the task requirements, the following steps need to be taken:

1. Implement Timezone Handling: Integrate timezone information into the calculations for uptime and downtime to account for stores in different timezones accurately.

2. Accurate Business Hours Data: Ensure accurate business hours data for all stores to avoid any inconsistencies in the report.

3. Develop Interpolation Logic: Design a reliable and logical interpolation logic to fill the entire business hours interval with uptime and downtime data based on the periodic polls.

4. Integrate Database: Store the provided CSV data into a relevant database and use it for API calls to enable dynamic and up-to-date report generation.

5. Enhance Error Handling: Strengthen error handling and edge case management to improve the reliability and resilience of the APIs.

### Conclusion:

The project is well underway, but there are essential aspects that require attention to meet the task requirements fully. With the necessary enhancements and fixes, it can provide more accurate and comprehensive reports, aligning with the task requirements.

Start PostgreSQL : `service postgresql start`
Root USER : `sudo su postgres`
`psql`
`psql -h localhost -U postgres -d reports`
`\d`
`python3 final.py`

