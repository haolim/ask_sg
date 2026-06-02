import time
import logging
from pydantic import ValidationError
from ask_sg.ingestion.clean import clean
from ask_sg.models.schemas.transaction_ingest import HDBResaleTransaction
from ask_sg.core.database import engine
from sqlalchemy import insert
from ask_sg.models.orm import ResaleTransactions
# Flow
# CSV -> pandas load -> pandas clean -> Pydantic -> SQLAlchemy -> DB
#


logger = logging.getLogger(__name__)
start = time.time()
# 1. Data load
df = clean(data_dir="data/raw")

# 2. Data has been cleaned
records = df.to_dict(orient='records')

# 3. Validate each row through Pydantic
validated = []
errors = []

for record in records:
    try:
        record = HDBResaleTransaction(**record)
        validated.append(record.model_dump())
    except ValidationError as e:
        errors.append({'row': record, 'error': str(e)})

# 4. Insert valid data to DB
with engine.begin() as conn:
    result = conn.execute(
        insert(ResaleTransactions), validated
    )

# 5. Summary
logger.info(f'Valid rows: {len(validated)}')
logger.info(f'Invalid rows: {len(errors)}')

# 6. Inspect errors if any
for err in errors:
    #print(f'Row {err['row']}: {err['error']}')
    logger.warning(f"Validation failed: {err['error']}")

logger.info(f"Ingestion completed in {time.time() - start: 2f}s")