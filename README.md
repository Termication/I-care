# I CARE

**Tagline:** Empowering students with easy access to mental health support.

## Project Overview

I CARE is a platform dedicated to providing students in Africa with easy access to mental health professionals. Our mission is to combat the stigma surrounding mental health and offer a confidential, user-friendly system where students can book therapy sessions, either virtual or in-person, with verified doctors. The platform also enables doctors to manage appointments, interact with community posts, and communicate with students via a chat feature.

## Table of Contents

* Features
* Technologies Used
* Getting Started
  * Installation
  * Usage
* Screenshots
* Contributing
* License
* Contact

## Features

* User Authentication: Secure login and sign-up functionality.
* Session Booking: Students can book therapy sessions with doctors.
* Communication: Built-in chat feature for student-doctor communication.
* Doctor Management: Doctors can manage sessions and interact with community posts.
* Confidentiality: Strong emphasis on privacy and data security.
* Localization: Tailored for the South African student demographic.

## Technologies Used

* Languages: Python, JavaScript, TypeScript, HTML
* Frameworks: Flask, React
* Libraries: SQLAlchemy, Redux
* Platforms: Docker, AWS
* Testing Tools: pytest, Selenium

## Technology Trade-offs

* **Flask vs. Django:** Flask was chosen for its lightweight nature and flexibility, allowing for faster development and easier customization. Django was considered too heavy for the specific needs of this project.
* **React vs. Angular:** React was selected for its component-based architecture and strong community support, making it easier to create a dynamic and responsive user interface. Angular was not chosen due to its steeper learning curve.

## Getting Started

### Prerequisites

* Python 3.x
* Node.js & npm
* Docker (for containerization)
* AWS Account (for deployment)

### Installation

##### Clone the repository:
```bash
git clone https://github.com/Termication/I-CARE.git
```

##### Backend Setup:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

##### Frontend Setup:
```bash
cd frontend
npm install
npm start
```
##### Docker Setup (Optional):

```bash
    docker-compose up --build
```
## Usage

    Development: Run both frontend and backend servers for development.
    Production: Use Docker and AWS for deployment.

## Screenshots

Here are some screenshots of the platform:
Login Page

Sign Up Page

## Contributing

We welcome contributions to the I CARE project! If you'd like to contribute, please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes and commit them (git commit -m 'Add some feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request.

##### Please ensure your code adheres to our coding standards and passes all tests.
## License

This project is licensed under the [MIT License](https://opensource.org/license/mit) - see the LICENSE file for details.
## Contact

For any inquiries or feedback, please contact:

    Innocent Karabo Mohlala
    Sekinat Oyelami

We are always happy to hear from users and contributors!
