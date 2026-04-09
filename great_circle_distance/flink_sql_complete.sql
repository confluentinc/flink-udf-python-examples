-- Complete Flink SQL setup for Great Circle Distance UDFs
-- This file contains all necessary statements to:
-- 1. Register both UDF variants
-- 2. Create a source table (Faker table with ride/trip data)
-- 3. Query distances using both functions

-- ============================================================================
-- STEP 1: Register the UDFs
-- ============================================================================
-- Replace <artifact-id> with the actual value from `confluent flink artifact create`.

-- Scalar variant: simple, row-by-row.  Good for low-to-moderate throughput.
CREATE FUNCTION great_circle_km AS 'great_circle_distance.distance.great_circle_km'
LANGUAGE PYTHON
USING JAR 'confluent-artifact://<artifact-id>';

-- Vectorized variant: batches rows into pandas Series and uses NumPy ops.
-- Prefer this for high-throughput pipelines (large event volumes).
CREATE FUNCTION great_circle_km_vec AS 'great_circle_distance.distance.great_circle_km_vec'
LANGUAGE PYTHON
USING JAR 'confluent-artifact://<artifact-id>';

-- ============================================================================
-- STEP 2: Create source table (Faker table with ride event data)
-- ============================================================================
-- Simulates a stream of ride-share or delivery events with pickup and dropoff
-- coordinates.
CREATE TABLE ride_events (
    ride_id     BIGINT,
    pickup_lat  DOUBLE,
    pickup_lon  DOUBLE,
    dropoff_lat DOUBLE,
    dropoff_lon DOUBLE,
    event_time  TIMESTAMP(3)
) WITH (
    'connector' = 'faker',
    'fields.ride_id.expression'     = '#{number.numberBetween ''1'',''1000000''}',
    'fields.pickup_lat.expression'  = '#{number.randomDouble ''4'',''-90'',''90''}',
    'fields.pickup_lon.expression'  = '#{number.randomDouble ''4'',''-180'',''180''}',
    'fields.dropoff_lat.expression' = '#{number.randomDouble ''4'',''-90'',''90''}',
    'fields.dropoff_lon.expression' = '#{number.randomDouble ''4'',''-180'',''180''}',
    'fields.event_time.expression'  = '#{date.past ''60'',''SECONDS''}'
);

-- ============================================================================
-- STEP 3: Test the scalar UDF
-- ============================================================================
SELECT
    ride_id,
    pickup_lat,
    pickup_lon,
    dropoff_lat,
    dropoff_lon,
    great_circle_km(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon) AS distance_km
FROM ride_events
LIMIT 10;

-- ============================================================================
-- STEP 4: Test the vectorized UDF (identical SQL, higher throughput)
-- ============================================================================
SELECT
    ride_id,
    pickup_lat,
    pickup_lon,
    dropoff_lat,
    dropoff_lon,
    great_circle_km_vec(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon) AS distance_km
FROM ride_events
LIMIT 10;

-- ============================================================================
-- STEP 5: Insert enriched events into an output topic
-- ============================================================================
-- Adjust environment, cluster, and topic names as needed.
CREATE TABLE `my-environment`.`my-cluster`.`ride-events-with-distance` (
    ride_id     BIGINT,
    distance_km DOUBLE,
    event_time  TIMESTAMP(3)
);

INSERT INTO `my-environment`.`my-cluster`.`ride-events-with-distance`
SELECT
    ride_id,
    great_circle_km_vec(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon) AS distance_km,
    event_time
FROM ride_events;
