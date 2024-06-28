
import argparse
import gradio as gr
import logging
import webbrowser

from pathlib import Path
from data_parser import DataParser

def main():
    formatter = (
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    )
    logging.basicConfig(format=formatter, level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--resource_dir", type=Path, help="Directory containing the resources", default=Path("Resources/")
    )
    args = parser.parse_args()

    data_parser = DataParser(args.resource_dir)
    df = data_parser.get_dataframe()


    # Applying style to highlight the maximum value in each row
    styler = df.style.highlight_max(color = 'darkgray', axis = 0)


    title="JTWF Dedicated Server Leaderboard"
    css="footer {visibility: hidden}"

    with gr.Blocks(title=title, css=css) as app:
        gr.Markdown(
            """
            # JTWF Dedicated Server Leaderboard
            """)
        gr.DataFrame(styler)

    webbrowser.open("http://127.0.0.1:7860")
    app.launch()


if __name__ == "__main__":
    formatter = (
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    )
    logging.basicConfig(format=formatter, level=logging.INFO)
    main()
