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

![image](https://mermaid.ink/img/pako:eNqNVdtuozAQ_RWL5zQfwFuVi5TNNokadp8ioYk9ELfGztqmVZXm39cGkwKhaXgBe25nzlw4RVQxjOII9ZRDrqHYSeKe1TpZzBeTx2SxXp3qK_9waQlnZLP8utorJYixYEvzdWms5jInBRoDOXbtS4M6dU7mS7KL_IFopMjf0BCpLM84BcuV3EVdM3oAmSNL9x8tS6D2W8Nz_fqznT2T2ykEtFgAF8S7lvxfiW0AQSPj2thUQoFXIgHfSeANLGjvlxeODFJqMeD6CMa8K8062DfP61-zSfID_IodjWAbdq6cD-JiaKjmx4qyi4w5L5YX6CuqbeqPA0KUrC9C6rIThCpjryLtwWDg1RLBX9EVZToif1fT0Xg87tVrvvg9u69eGRdD4Mqj_-zh816OWr0gtXXvdWImj9vlfTH7jX6Jysp-yGBhwbymDK3rLXMDj6NnU58dh9JpS2IPWFn3J8F1Cs8lYmsOmKo0GxHrcerzm6yfnmar5HaWl3RCP93XNN5RlWaTSYUlpGH68K_nvw5mnEVRoLQ98K0xPquHB3VqxiJ2BkLAXumK9-7IfH5Wqr6bYgdeaRyUe2biBmorUhBfIqn3AWl7ScZhQf2kFXbdbsBdq0rxhYtBrTgUutW9wz5CWi0io1FUoHabjrmlXzWDK9cB3X6IYvfJMINSVCU4O1Uordp-SBrFGQiDo6gervCrCLfn_9Mo6AY?type=png)

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
