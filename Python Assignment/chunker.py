import pandas as pd
import numpy as np


class ChunkIterator:
    def __init__(self, file_path: str, chunk_size: int):
        """
        Initialize the ChunkIterator with the file path and chunk size.
        :param file_path: Path to the dataset file.
        :param chunk_size: Number of rows per chunk.
        """
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_number = 0

    def __iter__(self):
        """
        Create an iterator for the chunks.
        """
        return self

    def __next__(self):
        """
        Read the next chunk of data and return basic statistics.
        :return: A tuple with the chunk DataFrame and basic statistics.
        """
        chunk = pd.read_csv(self.file_path, skiprows=self.chunk_number * self.chunk_size, nrows=self.chunk_size)

        if chunk.empty:
            raise StopIteration

        self.chunk_number += 1

        stats = self.calculate_statistics(chunk)

        return chunk, stats

    def calculate_statistics(self, chunk: pd.DataFrame):
        """
        Calculate basic statistics for the given chunk.
        :param chunk: DataFrame chunk.
        :return: Dictionary with basic statistics.
        """
        stats = {
            'mean': chunk.mean(numeric_only=True).to_dict(),
            'std': chunk.std(numeric_only=True).to_dict(),
            'min': chunk.min(numeric_only=True).to_dict(),
            'max': chunk.max(numeric_only=True).to_dict(),
            'count': chunk.count(numeric_only=True).to_dict()
        }
        return stats


if __name__ == "__main__":
    iterator = ChunkIterator('C:/Users/mahes/Downloads/archive (1)/Mall_Customers.csv', chunk_size=100)

    for chunk, stats in iterator:
        print(f"Chunk Statistics:\n{stats}\n")
