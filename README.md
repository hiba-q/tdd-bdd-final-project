# TDD / BDD Final Project

This project was developed as part of the Coursera course **"Introduction to Test Driven Development (TDD) / Behavior Driven Development (BDD)"** offered by IBM. The goal of the project is to apply TDD and BDD methodologies to implement and test an online product catalog microservice using Python, Flask, and Nose testing tools.

## Project Overview

The microservice is designed to manage a product catalog with full CRUD capabilities and additional search functionality. The project focuses heavily on writing automated tests first (TDD), defining behavior through scenarios (BDD), and then implementing the service logic.

This includes:
- Model-level testing and development
- API route testing and implementation
- Behavior Driven Development with feature files and step definitions
- Running coverage checks and behavior tests to ensure functionality

## Development Tasks Completed

Throughout the project, I contributed to the following components:

- ✅ Updated `tests/factories.py` to generate fake product data using FactoryBoy.
- ✅ Implemented test cases in `tests/test_models.py` to cover:
  - Create
  - Read
  - Update
  - Delete
  - List All
  - Search by Name, Category, and Availability
- ✅ Developed route test cases in `tests/test_routes.py` for all functionalities mentioned above.
- ✅ Implemented API logic in `service/routes.py` to support full CRUD operations and search features.
- ✅ Wrote BDD scenarios in `features/products.feature` for the user stories:
  - Read
  - Update
  - Delete
  - Search by Name
  - Search by Category
  - Search by Availability
- ✅ Updated `features/steps/load_steps.py` to handle loading of test data.
- ✅ Defined the Step Definitions in `features/steps/web_steps.py` to match BDD steps with application behavior.
- ✅ Verified all tests passed using:
  - `nosetests` with 95%+ code coverage
  - `honcho start` to launch and test the app interface
  - `behave` to confirm all 7 BDD scenarios passed

## Setup Instructions

To set up and run the project:

```bash
bash bin/setup.sh
exit  # then re-enter the shell
```

To start the application:

```bash
honcho start
```

To run tests:

```bash
nosetests --with-coverage
behave
```
## License

Licensed under the Apache License. See [LICENSE](/LICENSE)

## Original Author of Template

John Rofrano, Senior Technical Staff Member, DevOps Champion, @ IBM Research

## <h3 align="center"> © IBM Corporation 2023. All rights reserved. <h3/>
