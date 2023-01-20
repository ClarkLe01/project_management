<div align="center">
  <h1>Project Management</h1>
</div>
<br>

<div align="center">
  <a href="http://codecov.io/github/saleor/saleor?branch=master">
    <img src="http://codecov.io/github/saleor/saleor/coverage.svg?branch=master" alt="Codecov" />
  </a>
  <a href="https://docs.saleor.io/">
    <img src="https://img.shields.io/badge/docs-docs.saleor.io-brightgreen.svg" alt="Documentation" />
  </a>
  <a href="https://github.com/python/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  </a>
</div>

## Table of Contents

- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Database Diagram](#database-diagram)
- [Installation](#installation)
- [Demo](#demo)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- [Docker](https://www.docker.com/)
- [Python 3.x](https://www.python.org/)

## Repository Structure

    .
    ├── app                      # Source code
    ├── nginx                    # Nginx Configuration
    ├── .dockerignore
    ├── .env.prod.db.sample      # environment variables file for db images
    ├── .env.prod.sample         # environment variables file for other images
    ├── .gitignore
    ├── README.md
    ├── docker-compose.prod.yml  # build image for production
    └── docker-compose.yml       # build image for development

## Database Diagram



## Installation

_Below is an step of how you can deploy and setting up the app._

1. Clone the repo
   ```sh
   git clone https://github.com/ClarkLe01/project_management.git
   ```
2. Open folder repo & Install requirements
   ```sh
   pip install -r .\app\requirements.txt
   ```
4. Create .env.dev file for development based on .env.prod.sample and change DEBUG=1
5. Create .env.prod file for production based on .env.prod.sample and change DEBUG=0
6. Create .env.prod.db file for database environments based on .env.prod.db.sample
7. Open terminal & build image for development (optional)
   ```sh
   docker compose up
   ```
8. Open terminal & build image for production (optional)
   ```sh
   docker-compose -f .\docker-compose.prod.yml up 
   ```
9. Website will run on [localhost:8000](http://localhost:8000)

_For development, we have DB seed files in <repo>/app/fixtures with account samples which have password is 'admin'._

## Demo

Want to see Saleor in action?

* [View Website Here]()

Login credentials: `admin@gmail.com`/`admin`

## Contributing

We love your contributions and do our best to provide you with mentorship and support. If you are looking for an issue to tackle, take a look at issues labeled [`Help Wanted`](https://github.com/ClarkLe01/project_management/issues).

## License

Disclaimer: Everything you see here is open and free to use as long as you comply with the [license](https://github.com/ClarkLe01/project_management/blob/main/LICENSE). There are no hidden charges. We promise to do our best to fix bugs and improve the code.

#### Crafted with ❤️ by [Project Management](https://github.com/ClarkLe01)

clark.le.goldenowl@gmail.com
