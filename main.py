from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from pysus import SINAN
import pandas as pd
import io

app = FastAPI()

@app.get("/download_csv")
def download_csv(
    dis_code: str = Query(..., description="Código da doença, ex: MENT"),
    year_init: int = Query(..., description="Ano inicial, ex: 2005"),
    year_end: int = Query(..., description="Ano final, ex: 2025")
):
    sinan = SINAN().load()
    years = list(range(year_init, year_end + 1))
    files = sinan.get_files(dis_code=dis_code, year=years)

    df_list = []
    for file in files:
        tmp = file.download()
        df_list.append(tmp.to_dataframe())

    final_df = pd.concat(df_list, ignore_index=True)
    
    buffer = io.StringIO()
    final_df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={dis_code}_{year_init}_{year_end}.csv"})
