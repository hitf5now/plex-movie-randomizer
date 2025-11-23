from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Get host from environment or default to 0.0.0.0 for Docker
    host = os.environ.get('HOST', '0.0.0.0')
    # Get debug mode from environment or default to False
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    app.run(host=host, port=port, debug=debug)
