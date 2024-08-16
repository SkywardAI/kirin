import pyarrow as pa

Account = pa.schema(
  [
      pa.field("username", pa.string()),
      pa.field("email", pa.string()),
      pa.field("_hashed_password", pa.string()),
      pa.field("_hash_salt", pa.string()),
      pa.field("is_active", pa.bool_()),
      pa.field("created_at", pa.timestamp('s')),
      pa.field("updated_at", pa.timestamp('s')),
  ])
