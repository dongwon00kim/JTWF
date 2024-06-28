import argparse
from dataclasses import dataclass
import logging
from pathlib import Path
import pandas as pd

DataTypes = {
    "Callsign": str,
    "Balance": int,
    "AA": int,
    "AG": int,
    "CSAR": int,
    "SorT": int,
    "KIA": int,
}


@dataclass
class ScoreData:
    Callsign: str
    Balance: int
    AA: int
    AG: int
    CSAR: int
    SorT: int
    KIA: int


class DataParser:
    def __init__(self, resource_dir = Path('Resources/')):
        files = list(resource_dir.glob('**/*.json'))
        self.files = []
        for file in files:
            if file.is_dir():
                continue
            self.files.append(file)


    def get_data(self):
        datas = []
        for file in self.files:
            with open(file, "r") as f:
                data = f.read()
                data = data.replace('\t', '').split('\n')

                parsed_data = {}
                for d in data:
                    found_key = None
                    for key in DataTypes.keys():
                        if key in d:
                            found_key = key
                            break

                    if found_key is None:
                        continue

                    start = d.find("=") + 1

                    value = d[start:].strip()

                    end = value.rfind(",")
                    if end > 0:
                        value = value[:end]

                    value = value.replace("'", "")
                    value = value.replace('"', "")
                    parsed_data[found_key] = DataTypes[found_key](value)

                if set(parsed_data.keys()) == set(DataTypes.keys()):
                    datas.append(ScoreData(**parsed_data))

        if datas:
            datas.sort(key=lambda x: x.Balance, reverse=True)

        return datas


    def get_dataframe(self):
        data = self.get_data()
        return pd.DataFrame(data)


if __name__ == "__main__":
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
    data = data_parser.get_data()
    print(data)

    df =  data_parser.get_dataframe()
    print(df)

    print("done")
