-- ktx-mcp timetable store (TAGO sync → read-only for MCP)

CREATE TABLE IF NOT EXISTS train_departures (
  dep_code     TEXT NOT NULL,
  arr_code     TEXT NOT NULL,
  travel_date  TEXT NOT NULL,
  dep_time     TEXT NOT NULL,
  arr_time     TEXT NOT NULL,
  train_type   TEXT NOT NULL,
  train_no     TEXT NOT NULL DEFAULT '',
  duration_min INTEGER,
  fetched_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (dep_code, arr_code, travel_date, dep_time, train_type, train_no)
);

CREATE INDEX IF NOT EXISTS idx_train_departures_route_date
  ON train_departures (dep_code, arr_code, travel_date);

CREATE TABLE IF NOT EXISTS sync_runs (
  id            BIGSERIAL PRIMARY KEY,
  mode          TEXT NOT NULL,
  started_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at   TIMESTAMPTZ,
  tago_calls    INTEGER NOT NULL DEFAULT 0,
  routes_synced INTEGER NOT NULL DEFAULT 0,
  status        TEXT NOT NULL DEFAULT 'running',
  error_message TEXT
);

CREATE TABLE IF NOT EXISTS sync_routes (
  dep_code   TEXT NOT NULL,
  arr_code   TEXT NOT NULL,
  priority   INTEGER NOT NULL DEFAULT 100,
  label      TEXT,
  PRIMARY KEY (dep_code, arr_code)
);

-- Seed top routes (expand to 30 in app config)
INSERT INTO sync_routes (dep_code, arr_code, priority, label) VALUES
  ('NAT010000', 'NAT014445', 10, 'Seoul-Busan'),
  ('NATH30000', 'NAT014445', 10, 'Suseo-Busan'),
  ('NAT010000', 'NAT013271', 20, 'Seoul-Dongdaegu'),
  ('NAT011668', 'NAT013271', 30, 'Daejeon-Dongdaegu')
ON CONFLICT DO NOTHING;

-- RLS: public read for timetable data (hosted MCP uses service role or anon read)
ALTER TABLE train_departures ENABLE ROW LEVEL SECURITY;

CREATE POLICY "train_departures_public_read"
  ON train_departures FOR SELECT
  TO anon, authenticated
  USING (true);

-- Writes only via service role (sync worker on Fly)
CREATE POLICY "train_departures_service_write"
  ON train_departures FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);
