# HIT137 – Group Assignment 3

This is our Group Assignment 3 project for HIT137.  
We built a Tkinter app that uses two Hugging Face models and shows how OOP concepts can be used in Python.

## What the app does
- Lets you pick between two models:
  1. **Text Sentiment Analysis** – finds out if text is positive or negative  
  2. **Image Classification** – guesses what’s in an image  
- GUI made with Tkinter:
  - Menus, dropdowns, text box, file chooser
  - Tabs for Output, Model Info, and OOP Explanations
- We explained where we used OOP concepts right inside the app

## OOP stuff we covered
- **Encapsulation** → keeping model pipelines private
- **Polymorphism** → using the same `.run(input_data)` method for both models
- **Overriding** → each model class overrides `run` and `model_info`
- **Multiple inheritance** → mixins for logging and timing
- **Multiple decorators** → stacked `@timing`, `@logged`, and `@validate_nonempty`

## How to run
1. Make a virtual environment (optional but better)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   .venv\Scripts\activate      # Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

## Files in the project
- `main.py` → starts the app
- `gui.py` → Tkinter window + buttons/menus
- `models.py` → base model class + our 2 models
- `utils.py` → decorators and helper stuff
- `oop_demo.py` → extra small demo of overriding/inheritance
- `CONTRIBUTORS.md` → who did what
- `requirements.txt` → what to install

## Notes
- Make sure you have internet when first running so Hugging Face can fetch the models.
- If something fails, check the console for the error, usually it’s missing a library.
