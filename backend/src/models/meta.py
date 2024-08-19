import pyarrow as pa

Account = pa.schema(
  [
      pa.field("id", pa.int64()),
      pa.field("username", pa.string()),
      pa.field("email", pa.string()),
      pa.field("_hashed_password", pa.string()),
      pa.field("_hash_salt", pa.string()),
      pa.field("is_verified", pa.bool_()),
      pa.field("is_active", pa.bool_()),
      pa.field("is_logged_in", pa.bool_()),
      pa.field("created_at", pa.timestamp('s')),
      pa.field("updated_at", pa.timestamp('s')),
  ])

NextID = pa.schema(
  [
      pa.field("id", pa.int64()),
  ])
