# unit5—techdegree-python

## Description

I built this project to demonstrate my knowledge of the full stack employing the Flask web framework with Python and implement basic CRUD (Create Read Update Delete) functionality. This application is a hypothetical blogging website that allows users to create an account and while signed in can create and modify content. Unauthorized users can view content on the home page only. I learned about decorators and view functions, defining database tables, password hashing, Flask Forms, jinja2 templating and unit testing amongst other things.

## Installation

To run the project, clone the repo to your local machine and in the project directory create a virtual env:

```bash
python3 -m venv env
```

After creation start the env:

```bash
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run project:

```bash
python3 app.py
```

  

## Usage

After starting the project you will be brought directly to the home page where, as an anonymous user, you can only see a list of posts. To view other users entries and to create and modify your own, create a new user account by clicking the “Register” button in the top right corner of the page. 

![Homepage](/screenshots/Home.png)

Fill out the registration form and click the register button. 

![Register](/screenshots/Registration.png)

From there you can see a detail view of any post by clicking the title. 

![Detail](/screenshots/Detail.png)

To create a new entry, click on the “New Entry” button in the top right corner. 

![Empty Entry](/screenshots/EmptyEntry.png)

Fill out the entry form and click “Publish Entry”. 

![Publish entry](/screenshots/NewEntry.png)

Great! Now you should see your new entry at the top of the list. To modify or delete your entry,  first click on the title then click either “Edit entry” or “Delete entry”. screenshot

  

## License

MIT License

Copyright (c) [2021][Branden Morgan]


Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:

  

The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.

  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.

---

## Tests

I’ve provided basic functionality testing in the “app_tests.py” file

Run:

```bash
python3 app_tests.py
```
