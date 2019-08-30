# Ugly import of routes has been moved from __init__.py file to here
from dictionary import app, application

# To run the server using python command rather than flask command
if __name__ == '__main__':
    # Debug True is set to make sure whenever there is change
    # then we don't need to stop and restart the server
    app.run(debug=True, port=7550)