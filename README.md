# VEJA News Scraper

This program was developed as part of an extension program at the Laboratory of Neologism at UFES, with non-commercial goals. Its main objective is to create a corpus for identifying neologisms in the Brazilian Portuguese language.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/veja-news-scraper.git
   ```

2. Change into the project directory:
   ```bash
   cd veja-news-scraper
   ```

3. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `src` directory with the following environment variables:
   - `VEJA_EMAIL`: Your VEJA account email.
   - `VEJA_PASSWORD`: Your VEJA account password.

## Usage

### Step 1: Collect Links

Run the `get_links.py` script to collect links to VEJA news articles.

```bash
python get_links.py --headless --sector <sector> --time-range <start_year,end_year> --data-path <data_directory>
```

- `--headless`: If this flag is set, the program will run without a GUI.
- `--sector`: Specify the sector to be listed. The default is to collect links from all sectors on the site.
- `--time-range`: Define the time range for collecting links. The default is from 2008 to 2023.
- `--data-path`: Set the root directory path where the links will be stored. The default is the current working directory (./data).

### Step 2: Generate News

After collecting the links, run the `generate_news.py` script to download the news articles.

```bash
python generate_news.py --sector <sector> --time-range <start_year:end_year> --data-path <data_directory>
```

- `--sector`: Specify the sector to be listed. The default is to collect news from all sectors on the site.
- `--time-range`: Define the time range for collecting news articles. The default is from 2008 to 2023.
- `--data-path`: Set the root directory path where the links are stored and where the news files will be saved. The default is the current working directory (./data).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.