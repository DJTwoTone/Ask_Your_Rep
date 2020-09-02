# Ask_Your_Rep


Ask Your Rep is a simple Flask app design to allow users to find and contact their state legislature representatives. It alao allows users to register and keep a record of their contacts.

## Installation

The a development version of the app may be installed on local machines by:

- Install Postgresql (if you don't have it installed already)
- run 'createdb ask_your_rep_app' to create a database
- run 'python3 -m venv venv' to create a virtual environment (*note your python command may vary)
- run 'source venv/Scripts/activate' to acivate the virtual environment
- run 'pip install -r requirements.txt' to install all dependencies
- run 'export FLASK_ENV=development' to put Flask in development mode
- run 'python3 seed.py' to generate and input data to our new database
- run 'flask run' to start the server

## Technologies

This app uses Flask for the backend, Postgresql (with some SQLAlchemy magic) for the database, and a mixture of Boostrap (helped Themestr.app), HTML, CSS, and Javascript for the frontend.

It also makes use of:

For finding the longitude and latitude of a user, the Mapquest API will be used:

`https://developer.mapquest.com/documentation/`

For all other information regarding state representatives, the OpenStates API will be used:

`https://docs.openstates.org/`

** Note - Because these are open and free, the number of daily users may be limited

## Future addition

    - add a countdown timer until elections / reelection times
    - transition animations? (Could be too annoying)
    - allow users to link to recordings and pictures in their interactions
    - eagle scream on page transition (Well... Not really an eagle scream, but a red hawk scream. You know what I'm talking about. This would be very annoying, but it would be AWESOME)
    - state mottos?
    - state information??
    - state specific pictures??? (These three would need to be webscraped, I think.)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

MIT License

Copyright (c) [2020] [Benjamin W Slater]

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
