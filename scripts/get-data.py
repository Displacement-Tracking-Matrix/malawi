import polars as pl
from azure.identity import InteractiveBrowserCredential
from azure.storage.filedatalake import DataLakeFileClient

# ABFS path details
filesystem_name = "5a67e7d9-d47a-4b06-a89f-fecf731b5d43"
account_name = "onelake"
file_path = "edc2267b-dc94-4ff8-be27-a9fa7a91c6d8/Files/mwi.parquet"

# Build the full URL
url = f"https://{account_name}.dfs.fabric.microsoft.com/{filesystem_name}/{file_path}"

# Authenticate with browser
credential = InteractiveBrowserCredential()

# Create file client
file_client = DataLakeFileClient(account_url=f"https://{account_name}.dfs.fabric.microsoft.com",
                                 file_system_name=filesystem_name,
                                 file_path=file_path,
                                 credential=credential)

# Download the file content into memory
download = file_client.download_file()
file_bytes = download.readall()

# Read it into Polars
df = pl.read_parquet(file_bytes)
df.write_csv("../data/mwi.csv")

