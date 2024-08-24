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

Session = pa.schema(
  [
      pa.field("session_uuid", pa.string()),
      pa.field("account_id", pa.int64()),
      pa.field("name", pa.string()),
      pa.field("session_type", pa.string()),
      pa.field("dataset_name", pa.string()),
      pa.field("created_at", pa.timestamp('s')),
  ])

ChatHistory = pa.schema(
  [
      pa.field("session_uuid", pa.string()),
      pa.field("role", pa.string()),
      pa.field("message", pa.string()),
      pa.field("created_at", pa.timestamp('ms')),
  ])

DataSet = pa.schema(
  [
      pa.field("uuid", pa.string()),
      pa.field("name", pa.string()),
      pa.field("account_id", pa.int64()),
      pa.field("table_name", pa.string()),
      pa.field("created_at", pa.timestamp('s')),
      pa.field("updated_at", pa.timestamp('s')),
  ])
