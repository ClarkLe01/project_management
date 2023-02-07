<div align="center">
  <h1>Project Management</h1>
</div>
<br>
<p align='center'>
<img src="https://img.shields.io/badge/Django-239120?logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/Python-239120?logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/html5-E34F26?logo=html5&logoColor=white" />
<img src="https://img.shields.io/badge/css3-1572B6?logo=css3&logoColor=white" />
<img src="https://img.shields.io/badge/bootstrap-563D7C?logo=bootstrap&logoColor=white" />
<img src="https://img.shields.io/badge/Github-181717?logo=github&logoColor=white" />
</p>

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

[![image](https://mermaid.ink/img/pako:eNqNVNFu6jAM_ZUoz9sP9G3igsRlAzR635Aq07glW5twk3TTxPj3JWkKaenY-gBtbB-fYzs-0lwypAlF9YdDqaDeCmKf5Sqdz-aTh3S-Wh7bI_dwYQhnZL24HO2krIg2YBp9OdRGcVGSGrWGEvvxjUaVWZDZgmyp-yAKc-RvqImQhhc8B8Ol2NJ-WL4HUSLLdh9RJOTm28BT-_dvM30mtyUEtlgDr4iDFvx_gzGB4FFwpU0moMYrUwXfWeANDCiHy2tbDNKoagT6AFq_S8V63NfPq7_TSfoDfV8dhWC66lyBX3gF4Nn8cfq7ohS8iiQxm8Tw2oo4uNfM_fRRDkq-YG7aBvdypg-bxe9yDqfpnJU1w5QhwoB-zRga20B9g4_twbr9JrkU1lsQs0cfPRw32w5eCsRo2Jj0np2JDQbN6Zusnp6my_S2yrOc0LQrNQx1rvjBD3MPyMvslHguQYYe0r--ZG0ybSPqGoUZkI_uykne38tjN3uJDagq2Enl696fy89P7-qmKbHkpcJRu6tM0lGNMgXzOZN8H7HGmygJW-Anr7BQtiNwUZeScy1GvZLQ6Gh6xzGCrKiQ9I7WqOw6YXaz-mGw7dqjvYQ0sa8MC2gq34KTdYXGyM2HyGlSQKXxjraXK-zjcHr6AkdguM8?type=png)]

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

Want to see the demo?

* [View Website Here](http://smalldemoclark.live/)

Login credentials: `admin@gmail.com`/`admin`

## Contributing

We love your contributions and do our best to provide you with mentorship and support. If you are looking for an issue to tackle, take a look at issues labeled [`Help Wanted`](https://github.com/ClarkLe01/project_management/issues).

## License

Disclaimer: Everything you see here is open and free to use as long as you comply with the [license](https://github.com/ClarkLe01/project_management/blob/main/LICENSE). There are no hidden charges. We promise to do our best to fix bugs and improve the code.

#### Crafted with ❤️ by [Project Management](https://github.com/ClarkLe01)

clark.le.goldenowl@gmail.com
