# EmTeGee App

EmTeGee is a Kivy-based application that uses the Scryfall API to fetch Magic: The Gathering card details and generate the mechanical opposites of their Oracle text. Additionally, it includes a speak button that reads out the opposite text output.

## Features

- Fetches card details from the Scryfall API.
- Generates the mechanical opposites of the Oracle text, detailed in opposites.json.
- Speaks out the opposite text output using the speak button.

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment (Optional):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Ensure you have the required image files:** `banner.png` and `bgtexture.png` in the same directory as the script.

2. **Run the application:**

    ```sh
    python EmTeGee.py
    ```

3. **Interact with the App:**

    - Enter the exact name of the Magic: The Gathering card in the text input field and click the "Search Card" button.
    - The app will display the original Oracle text and the opposite Oracle text within the textured box.
    - Use the "Exit" button to close the app.
    - Use the "Speak" button to read the OPPOSITE text aloud.

## Notes and Warnings

- The mechanical opposites is done by finding and replacing text in a card and replacing it word for word. This list is expected to grow in size over time
- The application expects you to give the card name EXACTLY. It ignores punctuation and capitalization, but you cannot make typos or give a partial name.
- The speak button only speaks out the opposite text output.
- The window size is set to 600x450 and is not resizable.


## Roadmap

- Add delay to searches to abide by Scryfall rate limit recomendation. 
- Reminder text removal. Would be helpful since this app is meant for an audience where keywords will be useless, so replacing keywords with mechanical opposites and removing reminder text would be the most efficient use of space
- Adapting to other platforms. Currently a kivy app using python. Might be more robust in React/Flutter
- Partial matches. Maybe listing matches if partials exist for ease of use
- Better error handling. This thing will crash if you blow air at it
  

## Dependencies

- Kivy

